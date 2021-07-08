#!/bin/bash
if [ $(date "+%Y") != 2021 ]; then
    exit
fi

script_path=$(readlink -f "$0")
script_dir=$(dirname "$script_path")
echo "Running in directory \`$script_dir'" >> recent_cron.log

cd "$script_dir"
mkdir -p log

dt="$(date '+%Y%d%m-%H%M%S')"
echo "Starting on $dt" >> recent_cron.log
sh fetch_and_update.sh $1 > "log/$dt.log" 2> "log/$dt-err.log"
echo "Finished on $(date '+%Y%d%m-%H%M%S')" >> recent_cron.log
