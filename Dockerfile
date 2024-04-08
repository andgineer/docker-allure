FROM openjdk:8-jre-alpine

ARG ALLURE_VERSION=2.27.0
ARG ALLURE_REPO=https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline
ARG ALLURE_HOME=/opt/allure-$ALLURE_VERSION/

RUN apk update && \
    apk add --no-cache bash wget && \
    rm -rf /var/cache/apk/*

RUN set -e && wget \
#      --no-check-certificate \
      --no-verbose \
      -O /tmp/allure.tgz \
      $ALLURE_REPO/$ALLURE_VERSION/allure-commandline-$ALLURE_VERSION.tgz && \
    mkdir -p $ALLURE_HOME
RUN set -e && tar -vxzf /tmp/allure.tgz -C $(dirname $ALLURE_HOME) && \
    rm -rf /tmp/* && \
    chmod -R +x $ALLURE_HOME/bin

ENV PATH=$PATH:$ALLURE_HOME/bin

VOLUME ["/allure-results"]
VOLUME ["/allure-report"]

