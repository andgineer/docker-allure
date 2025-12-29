# Docker Allure Tests

Pytest test suite for verifying the Docker Allure image functionality.

## Running Tests Locally

### Prerequisites
- Docker running locally
- Python 3.9+
- uv package manager

### Build the Docker image

```bash
# Build with specific version
docker build --build-arg ALLURE_VERSION=2.36.0 -t allure-test:latest .

# Or extract version from workflow
ALLURE_VERSION=$(grep -A 1 'version: "2\.' ../.github/workflows/dockerhub.yml | head -1 | cut -d'"' -f2)
docker build --build-arg ALLURE_VERSION=$ALLURE_VERSION -t allure-test:latest .
```

### Run tests

Run all tests:
```bash
uv run pytest tests/ -v
```

Run specific test:
```bash
uv run pytest tests/test_docker_allure.py::test_allure_generate -v
```

### Test a different image

Override the image name with an environment variable:
```bash
ALLURE_IMAGE=andgineer/allure:latest uv run pytest tests/ -v
```

## Tests Included

1. **test_allure_generate** - Verifies that `allure generate` command creates HTML reports from test results
2. **test_allure_serve** - Verifies that `allure serve` starts a web server and serves the UI
3. **test_allure_version** - Checks that Allure CLI is installed and accessible
4. **test_java_available** - Verifies Java runtime is available (required for Allure)

## CI/CD Integration

These tests are automatically run in GitHub Actions before publishing the Docker image to ensure quality.
