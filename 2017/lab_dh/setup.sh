#!/bin/bash

echo "Hosting alice from bob_alice.py on port 10001"
socat TCP-LISTEN:10001,reuseaddr,fork EXEC:"python ./bob_alice.py --check_parameters alice" & 
echo "Hosting bob from bob_alice.py on port 10002"
socat TCP-LISTEN:10002,reuseaddr,fork EXEC:"python ./bob_alice.py --check_parameters bob" & 

echo "Hosting task1_sniffing on 10003"
socat TCP-LISTEN:10003,reuseaddr,fork EXEC:"python ./task1_sniffing.py" & 

echo "Hosting check_keys alice from bob_alice on 30001"
socat TCP-LISTEN:30001,reuseaddr,fork EXEC:"python ./bob_alice.py --check_keys alice" & 
echo "Hosting check_keys bob from bob_alice on 30002"
socat TCP-LISTEN:30002,reuseaddr,fork EXEC:"python ./bob_alice.py --check_keys bob" & 

echo "Hosting subgroups_confinement from bob_alice on 40001"
socat TCP-LISTEN:40001,reuseaddr,fork EXEC:"python ./bob_alice.py subgroups_confinement" & 
