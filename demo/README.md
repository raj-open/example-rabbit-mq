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

    > [!TIP]
    > Call one of
    >
    > ```bash
    > just demo "example-all"
    > just demos # equivalent command
    > ```
    >
    > to run all the examples.

## Alternative via FastApi ##

In step 2 one can alternatively start the FastApi server
(via `just start-server` or `just docker-start-server`)
and send a POST-request to the endpoing `/feature/search-fs`
with JSON-body e.g.

```json
{
    "ref": {
      "location": "OS",
      "path": "demo/example-case-1/requests.yaml"
    }
}
```

to run `SEARCH-FS` against `example-case-1` or

```json
{
    "ref": {
      "location": "OS",
      "path": "demo/example-all/requests.yaml"
    }
}
```

to run `SEARCH-FS` against all cases.

## Results ##

The current demos should result in the following:

![Results](img/results-demo.png)
