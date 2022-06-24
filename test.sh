#!/usr/bin/env bash
echo "######################### Unittesting #########################"
python3 test_encounters.py
echo "####################### END Unittesting #######################"

for file in test_files/*.txt; do
    echo "==========> TESTING ${file} <=========="
    python3 "./encounters.py" -f "${file}"
done
