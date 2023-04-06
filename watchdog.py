#!/bin/bash
watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command='echo "--------------------------------------------------------------" && python3 watcher.py' \
    --wait \
    --drop 
