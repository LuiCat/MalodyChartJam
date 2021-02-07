#!/bin/bash
cd "$(dirname "$0")"

if [ $(date "+%Y") != 2021 ]; then
    exit
fi

file="update_$1.py"
if [ ! -f "$file" ]; then
    echo "Script $file does not exist."
    exit
fi

echo "Deploying..."
sh git_fetch_deployment.sh

echo "Updating Python modules..."
pip install pygtrie
pip install getmac
pip install html2text

echo "Updating Submissions..."

python3 "$file" $1
