#!/usr/bin/env bash

for file in test_files/*; do
    echo "==========> TESTING ${file} <=========="
    expect "test.exp" "${file}"
done
