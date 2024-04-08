FROM openjdk:8-jdk-alpine

ARG ALLURE_VERSION=2.27.0
ARG ALLURE_REPO=https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline
ARG ALLURE_HOME=/opt/allure-$ALLURE_VERSION/

RUN apk update && \
    apk add --no-cache bash curl && \
    rm -rf /var/cache/apk/*

RUN set -e && curl --insecure -L -o /tmp/allure.tgz \
         $ALLURE_REPO/$ALLURE_VERSION/allure-commandline-$ALLURE_VERSION.tgz && \
    mkdir -p $ALLURE_HOME
RUN set -e && tar -xzf /tmp/allure.tgz -C $(dirname $ALLURE_HOME) && \
    rm -rf /tmp/* && \
    chmod -R +x $ALLURE_HOME/bin

ENV PATH=$PATH:$ALLURE_HOME/bin

VOLUME ["/allure-results"]
VOLUME ["/allure-report"]

