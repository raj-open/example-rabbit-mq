# ----------------------------------------------------------------
# NOTE: Setting shell does not work!
# For GitHub-actions we need "bash", but
# for Windows we need "sh".
# The solution is to ensure tasks are written with bash-shebang
# if they involve bash-syntax, e.g. 'if [[ ... ]] then else fi'.
# ----------------------------------------------------------------
# set shell := [ "bash", "-c" ]

_default:
    @- just --unsorted --list

menu:
    @- just --unsorted --choose

# ----------------------------------------------------------------
# Justfile
# Recipes for various workflows.
# ----------------------------------------------------------------

set dotenv-load := true
# set dotenv-path := [".env", ".env.docker-vars"]
set positional-arguments := true

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATH_ROOT := justfile_directory()
CURRENT_DIR := invocation_directory()
OS := if os_family() == "windows" { "windows" } else { "linux" }
PYVENV_ON := if os_family() == "windows" { ". .venv/Scripts/activate" } else { ". .venv/bin/activate" }
PYVENV := if os_family() == "windows" { "python" } else { "python3" }
LINTING := "ruff"
GEN_MODELS := "datamodel_code_generator"
GEN_MODELS_DOCUMENTATION := "openapi-generator-cli"
TOOL_TEST_BDD := "behave"

# --------------------------------
# Macros
# --------------------------------

_clean-all-files path pattern:
    #!/usr/bin/env bash
    find {{path}} -type f -name "{{pattern}}" -exec basename {} \; 2> /dev/null
    find {{path}} -type f -name "{{pattern}}" -exec rm {} \; 2> /dev/null
    exit 0;

_clean-all-folders path pattern:
    #!/usr/bin/env bash
    find {{path}} -type d -name "{{pattern}}" -exec basename {} \; 2> /dev/null
    find {{path}} -type d -name "{{pattern}}" -exec rm -rf {} \; 2> /dev/null
    exit 0;

_generate-documentation path_schema target_path name:
    @{{PYVENV_ON}} && {{GEN_MODELS_DOCUMENTATION}} generate \
        --skip-validate-spec \
        --input-spec {{path_schema}}/schema-{{name}}.yaml \
        --generator-name markdown \
        --output "{{target_path}}/{{name}}"

_build-documentation-recursively path_schema target_path:
    #!/usr/bin/env bash
    while read path; do
        if [[ "${path}" == "" ]]; then continue; fi
        path="${path##*/}";
        name="$( echo """${path}""" | sed -E """s/^schema-(.*)\.yaml$/\1/g""")";
        echo "- generate documentation for ${name}."
        just _generate-documentation "{{path_schema}}" "{{target_path}}" "${name}";
    done <<< "$( ls -f {{path_schema}}/schema-*.yaml )";
    exit 0;

_generate-models path_schema target_path name:
    @ # cf. https://github.com/koxudaxi/datamodel-code-generator?tab=readme-ov-file#all-command-options
    @{{PYVENV_ON}} && {{PYVENV}} -m {{GEN_MODELS}} \
        --input-file-type openapi \
        --output-model-type pydantic_v2.BaseModel \
        --encoding "UTF-8" \
        --disable-timestamp \
        --use-schema-description \
        --use-standard-collections \
        --use-union-operator \
        --use-default-kwarg \
        --field-constraints \
        --output-datetime-class AwareDatetime \
        --capitalise-enum-members \
        --enum-field-as-literal one \
        --set-default-enum-member \
        --use-subclass-enum \
        --allow-population-by-field-name \
        --strict-nullable \
        --use-double-quotes \
        --target-python-version 3.11 \
        --input "{{path_schema}}/schema-{{name}}.yaml" \
        --output "{{target_path}}/{{name}}.py"

_generate-models-recursively path_schema target_path:
    #!/usr/bin/env bash
    while read path; do
        if [[ "${path}" == "" ]]; then continue; fi
        path="${path##*/}";
        name="$( echo """${path}""" | sed -E """s/^schema-(.*)\.yaml$/\1/g""")";
        echo "- generate models for ${name}."
        just _generate-models "{{path_schema}}" "{{target_path}}" "${name}";
    done <<< "$( ls -f {{path_schema}}/schema-*.yaml )";
    exit 0;

_dco project="local" file="docker-compose.yaml" *args:
    #!/usr/bin/env bash
    # ensure environment is overridden by docker variables
    source <(cat .env .env.docker-vars)
    # export COMPOSE_BAKE=true
    docker compose \
        --project-name "{{project}}" \
        --file "{{file}}" \
        --env-file ".env" \
        --env-file ".env.docker-vars" \
        {{args}}

_docker-stop service project="${DOCKER_PROJECT}" file="docker-compose.yaml":
    @just _dco "{{project}}" "{{file}}" stop "{{service}}"

_docker-build service progress="tty" project="${DOCKER_PROJECT}" file="docker-compose.yaml":
    @echo "BUILD DOCKER +LOG {{service}}"
    @- just clean-docker "{{service}}" "{{project}}" "{{file}}" 2> /dev/null
    @just _dco "{{project}}" "{{file}}" logs --tail=0 {{service}} \
        && just _dco "{{project}}" "{{file}}" --progress={{progress}} build {{service}}

_docker-up service progress="tty" project="${DOCKER_PROJECT}" file="docker-compose.yaml":
    @echo "RUN DOCKER +LOG {{service}}"
    @- just clean-docker "{{service}}" "{{project}}" "{{file}}" 2> /dev/null
    @just _dco "{{project}}" "{{file}}" logs --tail=0 {{service}} \
        && just _dco "{{project}}" "{{file}}" --progress={{progress}} up {{service}}

_docker-run service project="${DOCKER_PROJECT}" file="docker-compose.yaml" cmd="bash --login -i" *args:
    @echo "EXEC DOCKER CMD (it) {{service}}"
    @- just clean-docker "{{service}}" "{{project}}" "{{file}}" 2> /dev/null
    @just _dco "{{project}}" "{{file}}" run --rm --interactive --service-ports {{service}} {{cmd}} {{args}}

# ----------------------------------------------------------------
# TARGETS
# ----------------------------------------------------------------

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: build
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

setup:
    @echo "TASK: SETUP"
    @mkdir -p "setup"
    @# For general setup
    - cp -n "templates/template.env"  ".env"
    @# For local execution
    - cp -n "templates/template-config.yaml"    "setup/config.yaml"
    - cp -n "templates/template-requests.yaml"  "setup/requests.yaml"
    @# For docker development
    - cp -n "templates/template.env.docker-vars"              ".env.docker-vars"
    - cp -n "templates/template.env.docker-secrets"           ".env.docker-secrets"

build:
    @echo "TASK: BUILD"
    @- just build-venv
    @just check-system
    @just build-requirements
    @just build-models

build-venv:
    @echo "SUBTASK: create venv if not exists"
    @${PYTHON_PATH} -m venv .venv

build-requirements:
    @echo "SUBTASK: build requirements"
    @just build-requirements-basic
    @just build-requirements-dependencies
    @just build-requirements-export

build-requirements-basic:
    @- {{PYVENV_ON}} && {{PYVENV}} -m pip install --upgrade pip 2> /dev/null
    @{{PYVENV_ON}} && pip install ruff uv

build-requirements-dependencies:
    @{{PYVENV_ON}} && uv pip install \
        --exact \
        --strict \
        --compile-bytecode \
        --no-python-downloads \
        --requirements pyproject.toml
    @{{PYVENV_ON}} && uv sync

build-requirements-export:
    @- rm -f requirements.txt 2> /dev/null
    @{{PYVENV_ON}} && uv pip freeze \
        --exclude-editable \
        --no-python-downloads \
        --project "." \
        --strict \
        --verbose \
        > requirements.txt

build-models:
    @echo "SUBTASK: build data models from schemata."
    @rm -rf "src/models/generated" 2> /dev/null
    @mkdir -p "src/models/generated"
    @touch "src/models/generated/__init__.py"
    @just _generate-models-recursively "models" "src/models/generated"

build-docs:
    @echo "SUBTASK: build documentation for data models from schemata."
    @rm -rf "docs/models" 2> /dev/null
    @mkdir -p "docs/models"
    @- just _build-documentation-recursively "models" "docs/models"
    @- just _clean-all-files "." ".openapi-generator*"
    @- just _clean-all-folders "." ".openapi-generator*"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: execution
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# run in cli mode
run *args:
    @{{PYVENV_ON}} && {{PYVENV}} -m src.cli {{args}}

# run via fast api
start-server env_path=".env" log_path="${PATH_LOGS}":
    @{{PYVENV_ON}} && {{PYVENV}} -m src.api \
        --env "{{env_path}}" \
        --log "{{log_path}}"

# --------------------------------
# TARGETS: docker
# --------------------------------

docker-explore service="build":
    @just _docker-run "{{service}}"

docker-clean progress="tty":
    @- docker compose rm -sf "base" 2> /dev/null
    @- docker compose rm -sf "build" 2> /dev/null
    @- docker image prune -a 2> /dev/null

# NOTE: only for debugging purposes - not needed for build
docker-setup progress="tty":
    @just _docker-build "base" "{{progress}}"

docker-build progress="tty":
    @just create-logs "${PATH_LOGS}"
    @just _docker-build "build" "{{progress}}"

docker-qa progress="tty":
    @just _docker-up "qa" "{{progress}}"

docker-start-server progress="tty":
    @just create-logs "${PATH_LOGS}"
    @just _docker-up "server" "{{progress}}"

docker-stop-server:
    @just _docker-stop "server"

docker-build-queue progress="tty":
    @just _docker-up "queue-build" "{{progress}}"

docker-start-queue progress="tty":
    @mkdir -p "${PATH_LOGS_QUEUE}"
    @mkdir -p "${PATH_LOGS_QUEUE_STATE}"
    @just _docker-up "queue-server" "{{progress}}"

docker-stop-queue progress="tty":
    @just _docker-stop "queue-server"

docker-register-users progress="tty":
    @mkdir -p "${PATH_LOGS_QUEUE}"
    @mkdir -p "${PATH_LOGS_QUEUE_STATE}"
    @just _docker-up "queue-admin" "{{progress}}"

# --------------------------------
# TARGETS: development + tools
# --------------------------------

# Recipe only works if local file dev exists
dev *args:
    @{{PYVENV_ON}} && {{PYVENV}} -m dev {{args}}

docker-dev:
    @just _docker-run "example" "${DOCKER_PROJECT}_sandbox" "docker-compose.sandbox.yaml"
    @just _docker-stop "example" "${DOCKER_PROJECT}_sandbox" "docker-compose.sandbox.yaml" 2> /dev/null

ping:
    @echo "$(date '+%Y-%m-%d %H:%M:%S') \$dev [DEBUG] ping success"

greet name:
    @echo "$(date '+%Y-%m-%d %H:%M:%S') \$dev [DEBUG] Hello, {{name}}!" >> ${PATH_LOGS}/debug.log

check-time-matches-cron cron_expr time="*":
    @{{PYVENV_ON}} && {{PYVENV}} -m scripts.cron "{{cron_expr}}" --time "{{time}}"

# Recipe only works if local file scripts/mocks.py exists
create-mocks *args:
    @{{PYVENV_ON}} && {{PYVENV}} -m scripts.mocks {{args}}

demo name:
    @just run SEARCH-FS --requests "demo/{{name}}/requests.yaml"

# --------------------------------
# TARGETS: terminate execution
# --------------------------------

# finds pid based on port
get-pid PORT:
    @- lsof -ti ":{{PORT}}" 2> /dev/null

# kills process based on process ID
kill-pid PID:
    @echo "Killing {{PID}}"
    @kill -9 {{PID}} 2> /dev/null

kill-port PORT:
    #!/usr/bin/env bash
    PID="$( just get-pid "{{PORT}}" )";
    if [[ "${PID}" == "" ]]; then
        echo "No process running on PORT {{PORT}}";
    else
        echo "Process ${PID} running on PORT {{PORT}}";
        just kill-pid "${PID}";
    fi
    exit 0;

# --------------------------------
# TARGETS: tests
# --------------------------------

test-unit path *args:
    @{{PYVENV_ON}} && pytest "{{path}}" {{args}}

test-unit-one path method:
    @just test-unit "{{path}}" -k "{{method}}"

tests-unit:
    @just test-unit "tests/unit" --cov-reset --cov="."

# --------------------------------
# TARGETS: qa
# NOTE: use for development only.
# --------------------------------

qa:
    @{{PYVENV_ON}} && coverage report -m

coverage source_path tests_path:
    @{{PYVENV_ON}} && pytest {{tests_path}} \
        --ignore=tests/integration \
        --cov-reset \
        --cov={{source_path}} \
        --capture=tee-sys \
        2> /dev/null

# --------------------------------
# TARGETS: prettify
# --------------------------------

lint path:
    @{{PYVENV_ON}} && {{PYVENV}} -m {{LINTING}} check \
        --respect-gitignore \
        --show-fixes \
        --no-unsafe-fixes \
        --exit-zero \
        --fix \
        "{{path}}"
    @{{PYVENV_ON}} && {{PYVENV}} -m {{LINTING}} format \
        --respect-gitignore \
        "{{path}}"

lint-dry path:
    @{{PYVENV_ON}} && {{PYVENV}} -m {{LINTING}} check \
        --respect-gitignore \
        --no-unsafe-fixes \
        --exit-zero \
        --diff \
        "{{path}}"

lint-check path:
    @{{PYVENV_ON}} && {{PYVENV}} -m {{LINTING}} check \
        --respect-gitignore \
        --no-unsafe-fixes \
        --exit-zero \
        --verbose \
        "{{path}}"

prettify:
    @just lint "src"
    @just lint "tests"

prettify-dry:
    @just lint-dry "src"
    @just lint-dry "tests"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: clean
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

clean log_path="${PATH_LOGS}":
    @just clean-venv
    @just clean-basic "{{log_path}}"

clean-basic log_path="${PATH_LOGS}":
    @echo "All system artefacts will be force removed."
    @- just _clean-all-files "." ".DS_Store" 2> /dev/null
    @echo "All test artefacts will be force removed."
    @- rm -rf ".pytest_cache" 2> /dev/null
    @- rm -f ".coverage" 2> /dev/null
    @echo "All build artefacts will be force removed."
    @- rm -rf ".venv" 2> /dev/null
    @- rm -rf "build" 2> /dev/null
    @- rm -rf "bindings/rust/target" 2> /dev/null
    @- just _clean-all-folders "." ".idea" 2> /dev/null
    @- just _clean-all-folders "." "__pycache__" 2> /dev/null

clean-venv:
    @echo "VENV will be removed."
    @- just _delete-if-folder-exists ".venv" 2> /dev/null

# removes containers
clean-docker service project="${DOCKER_PROJECT}" file="docker-compose.yaml":
    @just _dco "{{project}}" "{{file}}" rm -f "{{service}}"

# removes containers and images
clean-docker-full service project="${DOCKER_PROJECT}" file="docker-compose.yaml":
    @just _dco "{{project}}" "{{file}}" rm -f "{{service}}"
    @just _dco "{{project}}" "{{file}}" down --remove-orphans
    @just _dco "{{project}}" "{{file}}" down --rmi local
    @docker volume prune -f

# --------------------------------
# TARGETS: logging, session
# --------------------------------

clear-logs log_path="${PATH_LOGS}":
    @rm -rf "{{log_path}}" 2> /dev/null

create-logs log_path="${PATH_LOGS}":
    @just _create-logs-part "debug" "{{log_path}}"
    @just _create-logs-part "out"   "{{log_path}}"
    @just _create-logs-part "err"   "{{log_path}}"

_create-logs-part part log_path="${PATH_LOGS}":
    @mkdir -p "{{log_path}}"
    @touch "{{log_path}}/{{part}}.log"

watch-logs n="10":
    @tail -f -n {{n}} ${PATH_LOGS}/out.log

watch-logs-err n="10":
    @tail -f -n {{n}} ${PATH_LOGS}/err.log

watch-logs-debug n="10":
    @tail -f -n {{n}} ${PATH_LOGS}/debug.log

watch-logs-all n="10":
    @just watch-logs {{n}} &
    @just watch-logs-err {{n}} &
    @just watch-logs-debug {{n}} &

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: requirements
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

check-system:
    @echo "Operating System detected:  {{os_family()}}"
    @echo "Python command used:        ${PYTHON_PATH}"
    @echo "Python command for venv:    {{PYVENV}}"
    @echo "Python path for venv:       $( {{PYVENV_ON}} && which {{PYVENV}} )"
