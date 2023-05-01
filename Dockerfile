FROM openjdk:8-jre

ENV ALLURE="allure-2.21.0"
COPY "${ALLURE}.tgz" /

RUN apt-get update \
    && apt-get install tar \
    && tar -xvf "${ALLURE}.tgz" \
    && chmod -R +x /${ALLURE}/bin

VOLUME ["/allure-results"]
VOLUME ["/allure-report"]

WORKDIR /${ALLURE}/bin
