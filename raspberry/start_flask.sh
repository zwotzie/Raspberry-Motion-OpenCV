#!/usr/bin/env bash
# set -x

source /home/pi/py3/bin/activate

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ${BASEDIR}

exec gunicorn -b 0.0.0.0:5000 --workers=1 --access-logfile=${BASEDIR}/logs/access.log --error-logfile=${BASEDIR}/logs/error.log app:app
# python app.py