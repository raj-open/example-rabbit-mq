# Demo #

Each folder in this directory contains an example filesystem with requests config.

The README file in each folder explains how to run tool against the case
and the expected outcome.

## General usage ##

For ease of use one can also run the demos as follows:

1. Open 2 terminals

2. In terminal 1 start the queue

    ```bash
    just docker-start-queue
    ```

3. In terminal 2 run the command

    ```bash
    just demo {name}
    ```

    where `{name}` is the name of the subfolder, e.g. `"example-case-1"`.

## Results ##

The current demos should result in the following:

![Results](img/results-demo.png)
