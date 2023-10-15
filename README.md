[Docker container](https://hub.docker.com/r/andgineer/allure) that generates Yandex Allure test report

## About

[Yandex Allure](https://github.com/allure-framework/allure2/releases) creates beautiful and 
easy to navigate test reports.

Example of Allure usage see in [my blog](https://sorokin.engineer/posts/en/pytest_allure_selenium_auto_screenshot.html)

## Usage

If test results are in `./allure-results` you can generate report in `./allure-report` like this:

    docker run --rm -it \
        -v ${PWD}/allure-results:/allure-results \
        -v ${PWD}/allure-report:/allure-report \
        andgineer/allure \
        ./allure generate /allure-results -o /allure-report --clean

to serve report on port `8800`:

    docker run --rm -it \
        -v ${PWD}/allure-results:/allure-results \
        -v ${PWD}/allure-report:/allu-report \
        -p 8800:80 \
        andgineer/allure \
        ./allure serve -p 80 /allure-results

There are test results in `./allure-results` folder in this repo, so you can serv report
with the command above on `localhost:8800`.

## Allure Releases

[allure-framework](https://github.com/allure-framework/allure2/releases)


