"""
Tests for the Docker Allure image functionality.

These tests verify that the Docker image can:
1. Generate Allure reports from test results
2. Serve the Allure UI on a web server

Tests can be run locally or in CI:
    pytest tests/test_docker_allure.py -v
"""

import time
from pathlib import Path

import docker
import pytest
import requests


@pytest.fixture(scope="session")
def docker_client():
    """Create a Docker client for the test session."""
    return docker.from_env()


@pytest.fixture(scope="session")
def image_name():
    """Get the image name to test (can be overridden via env var)."""
    import os
    return os.getenv("ALLURE_IMAGE", "allure-test:latest")


@pytest.fixture(scope="session")
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


def test_allure_generate(docker_client, image_name, project_root, tmp_path):
    """Test that Allure can generate reports from test results."""
    allure_results = project_root / "allure-results"
    allure_report = tmp_path / "allure-report"
    allure_report.mkdir()

    # Verify test results exist
    assert allure_results.exists(), f"Test results directory not found: {allure_results}"
    assert list(allure_results.glob("*.json")), "No test result files found"

    # Run allure generate
    container = docker_client.containers.run(
        image_name,
        command=["allure", "generate", "/allure-results", "-o", "/allure-report", "--clean"],
        volumes={
            str(allure_results): {"bind": "/allure-results", "mode": "ro"},
            str(allure_report): {"bind": "/allure-report", "mode": "rw"},
        },
        remove=True,
        detach=False,
    )

    # Verify report was generated
    index_file = allure_report / "index.html"
    assert index_file.exists(), "Allure report index.html not generated"

    # Verify essential report files exist
    assert (allure_report / "app.js").exists(), "Allure app.js not found"
    assert (allure_report / "styles.css").exists(), "Allure styles.css not found"

    print(f"✓ Allure generate successful - report created at {allure_report}")


def test_allure_serve(docker_client, image_name, project_root):
    """Test that Allure serve can start and serve the UI."""
    allure_results = project_root / "allure-results"

    # Verify test results exist
    assert allure_results.exists(), f"Test results directory not found: {allure_results}"

    # Start Allure serve in detached mode
    container = docker_client.containers.run(
        image_name,
        command=["allure", "serve", "-h", "0.0.0.0", "-p", "80", "/allure-results"],
        volumes={
            str(allure_results): {"bind": "/allure-results", "mode": "ro"},
        },
        ports={"80/tcp": 8800},
        detach=True,
        remove=True,
    )

    try:
        # Wait for server to start (max 30 seconds)
        max_wait = 30
        for i in range(max_wait):
            try:
                response = requests.get("http://localhost:8800", timeout=2)
                if response.status_code == 200:
                    print(f"✓ Allure serve UI is running (responded in {i+1}s)")

                    # Verify we got HTML content
                    assert "<!DOCTYPE html>" in response.text or "<html" in response.text.lower()
                    assert "allure" in response.text.lower()

                    # Verify the behaviors page shows the expected test structure:
                    # End-to-end test suit -> Selenium -> Test selenium grid is alive -> 3 tests
                    behaviors_response = requests.get("http://localhost:8800/data/behaviors.json", timeout=2)
                    if behaviors_response.status_code == 200:
                        behaviors_data = behaviors_response.json()
                        assert len(behaviors_data["children"]) > 0, "No behaviors found in report"

                        # Navigate: Feature -> Story -> Suite -> Tests
                        feature = behaviors_data["children"][0]
                        assert feature["name"] == "End-to-end test suit", \
                            f"Expected 'End-to-end test suit' feature, got '{feature['name']}'"

                        story = feature["children"][0]
                        assert story["name"] == "Selenium", \
                            f"Expected 'Selenium' story, got '{story['name']}'"

                        suite = story["children"][0]
                        assert suite["name"] == "Test selenium grid is alive", \
                            f"Expected 'Test selenium grid is alive' suite, got '{suite['name']}'"

                        # Verify we have 3 tests (Chrome, Edge, Firefox)
                        test_count = len(suite["children"])
                        assert test_count == 3, \
                            f"Expected 3 tests in suite, got {test_count}"

                        # Verify all tests passed
                        test_names = [test["name"] for test in suite["children"]]
                        assert all("test_selenium[Browser:" in name for name in test_names), \
                            f"Unexpected test names: {test_names}"

                        print(f"✓ Allure report shows 'End-to-end test suit' with 3 selenium tests (Chrome, Edge, Firefox)")

                    return  # Test passed
            except (requests.ConnectionError, requests.Timeout):
                time.sleep(1)
                continue

        # If we got here, server didn't start in time
        logs = container.logs().decode("utf-8")
        pytest.fail(f"Allure serve failed to start within {max_wait}s. Logs:\n{logs}")

    finally:
        # Cleanup: stop and remove container
        try:
            container.stop(timeout=5)
        except Exception as e:
            print(f"Warning: Error stopping container: {e}")


def test_allure_version(docker_client, image_name):
    """Test that Allure is installed and can report its version."""
    result = docker_client.containers.run(
        image_name,
        command=["allure", "--version"],
        remove=True,
        detach=False,
    )

    output = result.decode("utf-8").strip()
    # Allure --version returns just the version number like "2.35.1"
    assert len(output) > 0 and output[0].isdigit(), f"Unexpected version output: {output}"
    print(f"✓ Allure version: {output}")


def test_java_available(docker_client, image_name):
    """Test that Java is available in the container (required for Allure)."""
    result = docker_client.containers.run(
        image_name,
        command=["java", "-version"],
        remove=True,
        detach=False,
        stderr=True,
    )

    output = result.decode("utf-8").strip()
    assert "java" in output.lower() or "openjdk" in output.lower(), \
        f"Java not found or unexpected version output: {output}"
    print(f"✓ Java is available: {output.split(chr(10))[0]}")
