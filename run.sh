#!/bin/bash
echo "cd"
cd "${0%/*}"

echo "Activate venv"
source venv/bin/activate

echo "Updating G-Frame repo"
git pull --rebase --autostash

echo "Starting Flask..."
export FLASK_APP=gframe.app && python -m flask run
