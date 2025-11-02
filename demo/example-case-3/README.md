# Example - Case 3 #

## Description ##

- A nested filesystem with some empty files
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
    just run SEARCH-FS --requests 'demo/example-case-3/requests.yaml'
    ```

## Expected results ##

- Should yield 14 messages in the queue.
- All files at all levels should be covered.
- The nested subfolder containing empty logs should be skipped.
