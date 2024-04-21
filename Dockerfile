FROM amazoncorretto:11-alpine-jdk

ARG ALLURE_VERSION=2.28.0
ARG ALLURE_REPO=https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline
ARG ALLURE_HOME=/opt/allure-$ALLURE_VERSION/

RUN apk update && \
    apk add --no-cache bash curl python3 && \
    rm -rf /var/cache/apk/* && \
    curl -L -o /tmp/allure.tgz \
         $ALLURE_REPO/$ALLURE_VERSION/allure-commandline-$ALLURE_VERSION.tgz && \
    mkdir -p $ALLURE_HOME && \
    tar -xzf /tmp/allure.tgz -C $(dirname $ALLURE_HOME) && \
    python3 -m pip freeze && \
    rm -rf /tmp/* && \
    chmod -R +x $ALLURE_HOME/bin

ENV PATH=$PATH:$ALLURE_HOME/bin

VOLUME ["/allure-results"]
VOLUME ["/allure-report"]

# Create virtual environment in the /.venv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    uv venv .venv
ENV PATH="/.venv/bin:$PATH"

RUN allure --version && \
    python --version && \
    uv --version && \
    python -c "import github_custom_actions; print('github_custom_actions', github_custom_actions.__version__)"

# Create a virtual environment in the container
#RUN python3 -m venv /opt/venv

# Activate the virtual environment
#ENV PATH="/opt/venv/bin:$PATH"

# Install requirements using pip from the virtual environment
#RUN pip install --no-cache-dir github-custom-actions