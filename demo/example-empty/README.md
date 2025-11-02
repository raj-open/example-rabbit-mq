# Example - Empty #

## Description ##

- An "empty" folder
- `skip-empty` set to `true`

## Execution ##

Run as follows

1. Open 2 terminals

2. In terminal 1 start the queue

    ```bash
    just docker-start-queue
    ```

3. In terminal 2 run the command

    ```bash
    just run SEARCH-FS --requests 'demo/example-empty/requests.yaml'
    ````

## Expected results ##

- Should yield 0 messages in the queue.
