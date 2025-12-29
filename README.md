[![Docker Automated build](https://img.shields.io/docker/image-size/andgineer/allure)](https://hub.docker.com/r/andgineer/allure)

# Docker Allure

[Docker container](https://hub.docker.com/r/andgineer/allure) for generating Allure test reports.

## About

[Allure Framework](https://github.com/allure-framework/allure2/releases) generates visually appealing and easily navigable test reports from your test results.

This Docker image packages:
- **Allure Framework** - Test report generation
- **Amazon Corretto** - Java runtime for Allure
- **Python 3 + uv** - For Python dependencies
- **github-custom-actions** - Python package for CI/CD integration

For usage examples, see [my blog](https://sorokin.engineer/posts/en/pytest_allure_selenium_auto_screenshot.html).

## Quick Start

### 1. Generate Test Results
Save test results to `./allure-results`:

```bash
pip install allure-pytest
pytest --alluredir=./allure-results
```

### 2. Generate Report
Generate HTML report from `./allure-results` to `./allure-report`:

```bash
docker run --rm -it \
    -v ${PWD}/allure-results:/allure-results \
    -v ${PWD}/allure-report:/allure-report \
    andgineer/allure \
    allure generate /allure-results -o /allure-report --clean
```

### 3. Serve Report
View the report at `localhost:8800`:

```bash
docker run --rm -it \
    -v ${PWD}/allure-results:/allure-results \
    -v ${PWD}/allure-report:/allure-report \
    -p 8800:80 \
    andgineer/allure \
    allure serve -h 0.0.0.0 -p 80 /allure-results
```

> **Note:** Docker requires absolute paths - `${PWD}` references your current working directory.

### Try It Out
Sample test results are included in `./allure-results/`. Run the serve command above to view the report at `localhost:8800`.

## Building Locally

Build the Docker image:

```bash
docker build -t andgineer/allure .
```

## Volume Mounts

- `/allure-results` - Input directory for test result files
- `/allure-report` - Output directory for generated HTML reports

## Publishing New Versions

To publish a new Allure version:

1. Update `ALLURE_VERSION` in `Dockerfile` to the [latest Allure release](https://github.com/allure-framework/allure2/releases)
2. Commit and push to master: `git commit -am "upgrade to Allure X.XX.X" && git push`
3. GitHub Actions automatically builds, tests, and publishes to Docker Hub

The workflow only publishes if no GitHub release exists for that version.

## Resources

- [Allure Framework Releases](https://github.com/allure-framework/allure2/releases)
- [Docker Hub](https://hub.docker.com/r/andgineer/allure)
- [Allure Documentation](https://docs.qameta.io/allure/)


