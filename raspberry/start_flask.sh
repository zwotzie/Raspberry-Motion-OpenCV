#!/usr/bin/env bash
# set -x

source /home/pi/py3/bin/activate

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python app.py