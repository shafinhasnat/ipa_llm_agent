#!/bin/bash

# Run 10 concurrent loops making requests
for i in {1..10}; do
    (
        while true; do
            curl http://localhost:8001/1000003
        done
    ) &
done

# Wait for all background processes
wait
