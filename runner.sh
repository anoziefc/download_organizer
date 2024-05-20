#!/usr/bin/bash
##bash script to check if my script is running and runs it if it isn't

SCRIPT_NAME="dir_organizer.py"
SCRIPT_PATH="/home/bobo/Desktop/download_organizer/dir_organizer.py"
VENV_PATH="/home/bobo/Desktop/download_organizer/venv"

if ps aux | grep -v grep | grep "$SCRIPT_NAME" > /dev/null
then
    :
else
    export WATCH_PATH="/home/bobo/Downloads"
    export USE_PATH="/home/bobo/Desktop/download_organizer/"
    "$SCRIPT_PATH"
    deactivate
fi
