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

Build the Docker image (specify Allure version via build-arg):

```bash
# Build with specific Allure version
docker build --build-arg ALLURE_VERSION=2.36.0 -t andgineer/allure .

# Or use latest 2.x from workflow
ALLURE_VERSION=$(grep -A 1 'version: "2\.' .github/workflows/dockerhub.yml | head -1 | cut -d'"' -f2)
docker build --build-arg ALLURE_VERSION=$ALLURE_VERSION -t andgineer/allure .
```

## Volume Mounts

- `/allure-results` - Input directory for test result files
- `/allure-report` - Output directory for generated HTML reports

## Publishing New Versions

To publish a new Allure version:

### Automatic Update (Recommended)
Run the version update script to fetch latest versions from GitHub:
```bash
# Check for updates (dry-run)
uv run update_allure_versions.py --dry-run

# Apply updates
uv run update_allure_versions.py
```

This automatically updates `.github/workflows/dockerhub.yml` with the latest Allure 2.x and 3.x versions.

### Manual Update
Alternatively, edit `.github/workflows/dockerhub.yml` matrix directly to set versions.

### Deploy
GitHub Actions automatically builds, tests, and publishes both 2.x and 3.x versions to Docker Hub.

**Available tags:**
- `2.x.x`, `2`, `latest` - Allure 2.x
- `3.x.x`, `3` - Allure 3.x

The workflow only publishes if no GitHub release exists for that version.

## Resources
- [Allure Framework Releases](https://github.com/allure-framework/allure2/releases)
- [Docker Hub](https://hub.docker.com/r/andgineer/allure)
- [Allure Documentation](https://docs.qameta.io/allure/)


