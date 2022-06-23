#!/usr/bin/env bash
echo "######################### Unittesting #########################"
python3 test_encounters.py
echo "####################### END Unittesting #######################"

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
