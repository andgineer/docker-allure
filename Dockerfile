FROM amazoncorretto:24-alpine-jdk

ARG ALLURE_VERSION=2.34.1
ARG ALLURE_REPO=https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline
ARG ALLURE_HOME=/opt/allure-$ALLURE_VERSION/

RUN apk update && \
    apk add --no-cache bash curl python3 && \
    rm -rf /var/cache/apk/* && \
    curl -L -o /tmp/allure.tgz \
         $ALLURE_REPO/$ALLURE_VERSION/allure-commandline-$ALLURE_VERSION.tgz && \
    mkdir -p $ALLURE_HOME && \
    tar -xzf /tmp/allure.tgz -C $(dirname $ALLURE_HOME) && \
    rm -rf /tmp/* && \
    chmod -R +x $ALLURE_HOME/bin && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    $HOME/.local/bin/uv --version

ENV PATH=$PATH:$ALLURE_HOME/bin
ENV PATH="/root/.local/bin:$PATH"

VOLUME ["/allure-results"]
VOLUME ["/allure-report"]

# Create and activate virtual environment in the /.venv
RUN uv venv .venv
ENV PATH="/.venv/bin:$PATH"

# install github-custom-actions
RUN uv pip install --upgrade github-custom-actions && \
    uv pip list && \
    allure --version && \
    python -c "import github_custom_actions; print('github_custom_actions', github_custom_actions.__version__)" && \
    python --version && \
    uv --version

# Create a virtual environment in the container
#RUN python3 -m venv /opt/venv

# Activate the virtual environment
#ENV PATH="/opt/venv/bin:$PATH"

# Install requirements using pip from the virtual environment
#RUN pip install --no-cache-dir github-custom-actions