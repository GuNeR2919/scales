#!/bin/bash
source venv/bin/activate
flask db upgrade
exec gunicorn -c gunicorn.conf.py scales:app
