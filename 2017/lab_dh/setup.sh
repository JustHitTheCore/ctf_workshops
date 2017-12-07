#!/bin/bash

socat TCP-LISTEN:10001,reuseaddr,fork EXEC:"python ./bob_alice.py --check_parameters alice" & 
socat TCP-LISTEN:10002,reuseaddr,fork EXEC:"python ./bob_alice.py --check_parameters bob" & 

socat TCP-LISTEN:10003,reuseaddr,fork EXEC:"python ./task1_sniffing.py" & 

socat TCP-LISTEN:30001,reuseaddr,fork EXEC:"python ./bob_alice.py --check_keys alice" & 
socat TCP-LISTEN:30002,reuseaddr,fork EXEC:"python ./bob_alice.py --check_keys bob" & 

socat TCP-LISTEN:40001,reuseaddr,fork EXEC:"python ./bob_alice.py subgroups_confinement" & 