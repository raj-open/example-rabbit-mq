#  Demo #

Each folder in this directory contains an example file system with requests config.

The README file in each folder explains how to run tool against the case
and the expected outcome.

For ease of use one can also run the demos as follows:

Run as follows

1. Open 2 terminals

2. In terminal 1 start the queue

    ```bash
    just docker-start-queue
    ``

3. In terminal 2 run the command

    ```bash
    just demo {name}
    ````

    where `{name}` is the name of the subfolder, e.g. `"example-case-1"`.
