# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Docker container project for generating Yandex Allure test reports. The container packages Allure commandline tools with Java runtime to create and serve visual test reports from test results.

## Architecture

- **Base Image**: Amazon Corretto 24 Alpine JDK - provides Java runtime for Allure
- **Core Tool**: Allure Framework commandline (version 2.34.1) installed from Maven repository
- **Additional Tools**: 
  - Python 3 and uv package manager for Python dependencies
  - github-custom-actions Python package installed in virtual environment
- **Volumes**: 
  - `/allure-results` - input directory for test result files
  - `/allure-report` - output directory for generated HTML reports

## Common Commands

### Building the Docker Image
```bash
docker build --build-arg ALLURE_VERSION=2.36.0 -t andgineer/allure .
```
Note: ALLURE_VERSION must be specified via build-arg (versions are defined in .github/workflows/dockerhub.yml)

### Generating Reports from Test Results
Generate HTML report from allure-results to allure-report:
```bash
docker run --rm -it \
    -v ${PWD}/allure-results:/allure-results \
    -v ${PWD}/allure-report:/allure-report \
    andgineer/allure \
    allure generate /allure-results -o /allure-report --clean
```

### Serving Reports
Serve report on localhost:8800:
```bash
docker run --rm -it \
    -v ${PWD}/allure-results:/allure-results \
    -v ${PWD}/allure-report:/allure-report \
    -p 8800:80 \
    andgineer/allure \
    allure serve -h 0.0.0.0 -p 80 /allure-results
```

### Development Workflow
The project includes sample test results in `./allure-results/` for testing the container functionality.

## Key Environment Variables
- `ALLURE_VERSION=2.34.1` - Version of Allure framework to install
- `ALLURE_HOME=/opt/allure-$ALLURE_VERSION/` - Installation directory for Allure
- `PATH` - Extended to include Allure binaries and uv Python environment

## Dependencies
- Java runtime (Amazon Corretto 24)
- Allure commandline tools (downloaded from Maven repository)
- Python 3 with uv package manager
- github-custom-actions Python package