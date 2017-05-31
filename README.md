Generates Yandex Allure 2 report and serve it.

To generate report (test results should be in ./allure-results, result will be in ./allure-report)

    docker run --rm -it -v ${PWD}/allure-results:/allure-results -v ${PWD}/allure-report:/allure-report docker masterandrey/docker-allure ./allure generate /allure-results -o /allure-report --clean

to serve report on port 8800:

    docker run --rm -it -v ${PWD}/allure-results:/allure-results -v ${PWD}/allure-report:/allu-report -p 8800:80 docker masterandrey/docker-allure ./allure serve -p 80 /allure-results



