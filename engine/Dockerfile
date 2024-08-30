FROM debian:12

LABEL maintainer="Ataf Fazledin Ahamed (github.com/fazledyn)"

ARG CODEQL_VERSION="2.15.5"

ARG VENV_HOME="/workspace/env"

ARG CODEQL_HOME="/workspace/tools/"

ARG SEMGREP_HOME="/workspace/tools/semgrep"

RUN apt-get update && apt-get install -y git wget jq python3 python3-pip python3-virtualenv

RUN python3 -m virtualenv ${VENV_HOME}

RUN "${VENV_HOME}/bin/pip" install semgrep

RUN mkdir -p ${CODEQL_HOME} && \
    cd /tmp && \
    wget https://github.com/github/codeql-action/releases/download/codeql-bundle-v${CODEQL_VERSION}/codeql-bundle-linux64.tar.gz && \
    tar -xvf /tmp/codeql-bundle-linux64.tar.gz --directory ${CODEQL_HOME} && \
    rm /tmp/codeql-bundle-linux64.tar.gz

ENV PATH="${PATH}:/${CODEQL_HOME}/codeql"

ENV PATH="${PATH}:/${VENV_HOME}/bin"

RUN codeql pack download trailofbits/cpp-queries trailofbits/go-queries

RUN mkdir -p "${SEMGREP_HOME}/rules" && \
    cd "${SEMGREP_HOME}/rules" && \
    # wget -O auto.yml https://semgrep.dev/c/p/auto && \
    # wget -O brakeman.yml https://semgrep.dev/c/p/brakeman && \
    # wget -O ci.yml https://semgrep.dev/c/p/ci && \
    # wget -O clientside-js.yml https://semgrep.dev/c/p/clientside-js && \
    # wget -O command-injection.yml https://semgrep.dev/c/p/command-injection && \
    wget -O default.yml https://semgrep.dev/c/p/default && \
    # wget -O django.yml https://semgrep.dev/c/p/django && \
    # wget -O docker-compose.yml https://semgrep.dev/c/p/docker-compose && \
    # wget -O docker.yml https://semgrep.dev/c/p/docker && \
    # wget -O dockerfile.yml https://semgrep.dev/c/p/dockerfile && \
    # wget -O electron-desktop-app.yml https://semgrep.dev/c/p/electron-desktop-app && \
    # wget -O eslint-plugin-security.yml https://semgrep.dev/c/p/eslint-plugin-security && \
    # wget -O expressjs.yml https://semgrep.dev/c/p/expressjs && \
    # wget -O flask.yml https://semgrep.dev/c/p/flask && \
    # wget -O github-actions.yml https://semgrep.dev/c/p/github-actions && \
    # wget -O gitlab-bandit.yml https://semgrep.dev/c/p/gitlab-bandit && \
    # wget -O gitlab-eslint.yml https://semgrep.dev/c/p/gitlab-eslint && \
    # wget -O golang.yml https://semgrep.dev/c/p/golang && \
    # wget -O insecure-transport.yml https://semgrep.dev/c/p/insecure-transport && \
    # wget -O java.yml https://semgrep.dev/c/p/java && \
    # wget -O javascript.yml https://semgrep.dev/c/p/javascript && \
    # wget -O jwt.yml https://semgrep.dev/c/p/jwt && \
    # wget -O kubernetes.yml https://semgrep.dev/c/p/kubernetes && \
    # wget -O mobsfscan.yml https://semgrep.dev/c/p/mobsfscan && \
    # wget -O nginx.yml https://semgrep.dev/c/p/nginx && \
    # wget -O nodejs.yml https://semgrep.dev/c/p/nodejs && \
    # wget -O nodejsscan.yml https://semgrep.dev/c/p/nodejsscan && \
    # wget -O ocaml.yml https://semgrep.dev/c/p/ocaml && \
    # wget -O owasp-top-ten.yml https://semgrep.dev/c/p/owasp-top-ten && \
    # wget -O phpcs-security-audit.yml https://semgrep.dev/c/p/phpcs-security-audit && \
    wget -O python.yml https://semgrep.dev/c/p/python && \
    # wget -O r2c-best-practices.yml https://semgrep.dev/c/p/r2c-best-practices && \
    # wget -O r2c-bug-scan.yml https://semgrep.dev/c/p/r2c-bug-scan && \
    # wget -O r2c-ci.yml https://semgrep.dev/c/p/r2c-ci && \
    # wget -O r2c-security-audit.yml https://semgrep.dev/c/p/r2c-security-audit && \
    # wget -O r2c.yml https://semgrep.dev/c/p/r2c && \
    # wget -O react.yml https://semgrep.dev/c/p/react && \
    # wget -O ruby.yml https://semgrep.dev/c/p/ruby && \
    # wget -O secrets.yml https://semgrep.dev/c/p/secrets && \
    # wget -O semgrep-misconfigurations.yml https://semgrep.dev/c/p/semgrep-misconfigurations && \
    # wget -O semgrep-rule-lints.yml https://semgrep.dev/c/p/semgrep-rule-lints && \
    # wget -O sql-injection.yml https://semgrep.dev/c/p/sql-injection && \
    # wget -O supply-chain.yml https://semgrep.dev/c/p/supply-chain && \
    # wget -O terraform.yml https://semgrep.dev/c/p/terraform && \
    # wget -O test.yml https://semgrep.dev/c/p/test && \
    wget -O trailofbits.yml https://semgrep.dev/c/p/trailofbits && \
    # wget -O typescript.yml https://semgrep.dev/c/p/typescript && \
    # wget -O xss.yml https://semgrep.dev/c/p/xss && \
    # wget -O gitlab-gosec.yml https://semgrep.dev/c/r/gitlab.gosec && \
    # wget -O hazanasec.weak_crypto.yml https://semgrep.dev/c/p/hazanasec.weak_crypto && \
    # wget -O hazanasec.non-prepared-sql-statements.yml https://semgrep.dev/c/p/hazanasec.non-prepared-sql-statements && \
    # wget -O hazanasec.nodejs_nosql_injection.yml https://semgrep.dev/c/p/hazanasec.nodejs_nosql_injection && \
    # wget -O hazanasec.jwt-security-audit.yml https://semgrep.dev/c/p/hazanasec.jwt-security-audit && \
    # wget -O hazanasec.generic_possible_xss.yml https://semgrep.dev/c/p/hazanasec.generic_possible_xss && \
    # wget -O hazanasec.possible_path_traversal.yml https://semgrep.dev/c/p/hazanasec.possible_path_traversal && \
    # wget -O findsecbugs.yml https://semgrep.dev/c/p/findsecbugs && \
    # wget -O webappsecurityz.3zrr-rules.yml https://semgrep.dev/c/p/webappsecurityz.3zrr-rules && \
    # wget -O traw.c.yml https://semgrep.dev/c/p/traw.c && \
    # wget -O tkisason.javascript-kitchensink.yml https://semgrep.dev/c/p/tkisason.javascript-kitchensink && \
    sed -i 's/0.0.0.0, ::/0.0.0.0, (colon)(colon)/' ${SEMGREP_HOME}/rules/*.yml && \
    semgrep -f ${SEMGREP_HOME}/rules --validate --metrics off

WORKDIR /workspace

COPY ./entrypoint.py /workspace/

ENTRYPOINT [ "python3", "/workspace/entrypoint.py" ]

CMD [ "" ]
