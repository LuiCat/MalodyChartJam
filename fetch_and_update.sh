#!/bin/bash
cd "$(dirname "$0")"

if [ $(date "+%Y") != 2021 ]; then
    exit
fi

file = update_$1.py
if [ ! -f "$file" ]; then
    echo "Script $file does not exist."
    exit
fi

echo "Fetching updates from GitHub..."

git fetch --all
git checkout -f origin/deployment

echo "Updating Submissions..."

python3 "$file" $1
