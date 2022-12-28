#!/bin/bash
source venv/bin/activate
flask db upgrade
exec gunicorn -c gunicorn.conf.py --access-logfile - --error-logfile - scales:app --worker-tmp-dir /dev/shm
