# Example - Case 2 #

## Description ##

- An nearly flat file system with a nested folder containing empty files.
- `skip-empty` set to `false`

## Execution ##

Run as follows

1. Open 2 terminals

2. In terminal 1 start the queue

    ```bash
    just docker-start-queue
    ```

3. In terminal 2 run the command

    ```bash
    just run SEARCH-FS --requests 'demo/example-case-2/requests.yaml'
    ````

## Expected results ##

- Should yield 6 messages in the queue.
- The folders at lowest level should be logged.
- The nested subfolder containing empty logs should _not_ be skipped.
