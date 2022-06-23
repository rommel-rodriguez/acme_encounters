#!/usr/bin/env bash

if ! which expect; then
    echo "expect package not installed!"
    echo "On Ubuntu based systems run:"
    echo "> apt install expect"
    exit 1
fi

for file in test_files/*; do
    echo "==========> TESTING ${file} <=========="
    expect "test.exp" "${file}"
done
