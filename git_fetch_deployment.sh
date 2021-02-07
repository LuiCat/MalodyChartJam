#!/bin/bash

echo "Starting SSH Agent..."
eval `ssh-agent -s`
ssh-add ~/.ssh/cd

echo "Fetching updates from GitHub..."
git fetch --all
git checkout -f origin/deployment
