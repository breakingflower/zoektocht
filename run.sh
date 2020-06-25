#!/bin/bash

source "/mnt/c/Users/Zaphod Beeblebrox/Documents/flask-website/venv/bin/activate"
export FLASK_APP=application.py
export FLASK_ENV=development
flask run
