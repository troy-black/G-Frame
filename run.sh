#!/bin/bash
echo "cd"
cd "${0%/*}"

echo "Activate venv"
source venv/bin/activate

echo "Updating G-Frame repo"
git pull --rebase --autostash

echo "Checking for updates to requirements.txt"
pip install -r requirements.txt

echo "Starting Flask..."
export FLASK_APP=gframe.app && python -m flask run &
