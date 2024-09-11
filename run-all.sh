#!/bin/bash

cd CreateKB
python3 main.py
cd ../ProveML
make prover
