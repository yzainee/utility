#!/usr/bin/env bash

#make necessary changes in config.py
gunicorn --pythonpath ver_utils/ -w 2 --threads 2 -b 0.0.0.0:5000 rest_api:app
