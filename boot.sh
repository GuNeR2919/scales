#!/bin/bash
source venv/bin/activate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - scales:app --worker-tmp-dir /dev/shm --workers=2 --threads=4 --worker-class=gthread 
