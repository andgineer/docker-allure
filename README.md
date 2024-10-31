[![Docker Automated build](https://img.shields.io/docker/image-size/andgineer/allure)](https://hub.docker.com/r/andgineer/allure)

[Docker container](https://hub.docker.com/r/andgineer/allure) for generating Yandex Allure test report

## About

[Yandex Allure](https://github.com/allure-framework/allure2/releases) generates visually appealing and easily navigable test reports.

For usage examples, see this [my blog](https://sorokin.engineer/posts/en/pytest_allure_selenium_auto_screenshot.html)

## Usage

### Generate Test Results
Save test results to `./allure-results`:

    pip install allure-pytest
    pytest --alluredir=./allure-results

### Generate and View Reports

Generate report in ./allure-report from results in ./allure-results:

    docker run --rm -it \
        -v ${PWD}/allure-results:/allure-results \
        -v ${PWD}/allure-report:/allure-report \
        andgineer/allure \
        allure generate /allure-results -o /allure-report --clean

Serve report on `localhost:8800`:

    docker run --rm -it \
        -v ${PWD}/allure-results:/allure-results \
        -v ${PWD}/allure-report:/allu-report \
        -p 8800:80 \
        andgineer/allure \
        allure serve -p 80 /allure-results

> Docker requires absolute paths, hence ${PWD} is used to reference the current working directory.

Sample test results are included in the ./allure-results folder. Use the command above to view the report at localhost:8800.

## Allure Framework Releases

[allure-framework](https://github.com/allure-framework/allure2/releases)


