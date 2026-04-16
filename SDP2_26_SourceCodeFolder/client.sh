#!/bin/bash

# Number of clients to run
num_clients=100000

# Loop through a range of clients
for ((i=1; i<=$num_clients; i++)); do
    # Execute Python script with client ID as argument
    python3 legitimate_client.py $i
done