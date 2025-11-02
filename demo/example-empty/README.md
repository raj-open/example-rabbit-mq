# Example - Empty #

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

This should yield 0 messages in the queue.
