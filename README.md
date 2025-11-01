[![Python version: 3.14](https://img.shields.io/badge/python%20version-3.14-1464b4.svg)](https://www.python.org)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[![qa manual:main](https://github.com/raj-open/example-rabbit-mq/actions/workflows/manual.yaml/badge.svg?branch=main)](https://github.com/raj-open/example-rabbit-mq/actions/workflows/manual.yaml)
[![qa manual:staging](https://github.com/raj-open/example-rabbit-mq/actions/workflows/manual.yaml/badge.svg?branch=staging)](https://github.com/raj-open/example-rabbit-mq/actions/workflows/manual.yaml)

[![qa auto:staging](https://github.com/raj-open/example-rabbit-mq/actions/workflows/auto.yaml/badge.svg?branch=staging)](https://github.com/raj-open/example-rabbit-mq/actions/workflows/auto.yaml)
[![qa auto:current](https://github.com/raj-open/example-rabbit-mq/actions/workflows/auto.yaml/badge.svg)](https://github.com/raj-open/example-rabbit-mq/actions/workflows/auto.yaml)

# Example Rabbit MQ #

This repository provides an example implementation of a tool with a single feature `SEARCH-FS`,
which upon performs the following:

- given a request payload;
- accesses a _path_ to a directory within a _file system_;
- iterates recursively through all file objects within the given diectory;
- notifies an instance of Rabbit MQ for each file found.

## System requirements ##

- [bash](https://gitforwindows.org)

- [python 3.11--3.14](https://www.python.org/downloads) (currently tested with v3.14)

- [justfile tool](https://github.com/casey/just/releases) version `^1.4.*`

- [docker + CLI tools](https://docs.docker.com/engine/install)

NOTE: We primarily use Docker for local testing, in particular to spin up a Rabbit MQ server.

## Basic setup ##

Call

```bash
just setup
```

and modify if so desired the values in

- .env
- .env.docker-vars
- .env.docker-secrets

For demonstration purposes all values should be fine.
One may merely need or wish to modify

```bash
PATH_LOGS
PYTHON_PATH
```

as well as the HTTP/RABBIT-settings

## Usage of main application ##

The main code base can be run in three modes:

- via the cli
- via the API
- via the API within docker

The cli-usage is limited

### Docker-free usage ###

For all sakes and purposes, so that local docker-less execution is possible,
call

```bash
just build
```

which assumes that the .env file has been correctly set up.

### Usage with docker ###

For full integration (or at least mocking), activate the docker engine and carry out

```bash
just docker-build # builds the application
# optional
just docker-qa # performs qa on the docker image of the main code base
```

To start the ap

## Usage of Rabbit Message Queue ##

Activate the docker engine and carry out

```bash
just docker-build-queue # builds the container for RabbitMQ
```

### Activation/Deactivation of Queue ###

The following commands start/stop the queue:

```bash
just docker-start-queue
just docker-stop-queue
```

### Set up users ###

Either as a background process or in a separate terminal start the queue (see [above](#activationdeactivation-of-queue)).
Now call

```bash
just docker-register-users
```

which creates an admin and guest user.

### Admin user ###

Open the browers to the following address (see values in your .env file):

```text
http://${HTTP_IP}:${HTTP_PORT_RABBIT_WEB}
```

log in using

```text
Username: ${HTTP_ADMIN_USER_RABBIT}
Password: ${HTTP_ADMIN_PASSWORD_RABBIT}
```

### Guest user ###

In the code base we use

```text
Username: ${HTTP_GUEST_USER_RABBIT}
Password: ${HTTP_GUEST_PASSWORD_RABBIT}
```

## Execution ##

Start the queue (see [above](#activationdeactivation-of-queue)).
Start the server
