# Example - Case 3 #

Run as follows

1. Open 2 terminals

2. In terminal 1 start the queue

    ```bash
    just docker-start-queue
    ```

3. In terminal 2 run the command

    ```bash
    just run SEARCH-FS --requests 'demo/example-case-3/requests.yaml'
    ````

This should yield 6 messages in the queue - the empty logs should _not_ be skipped.
