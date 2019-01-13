#!/usr/bin/env bash

event_id=$1

source ~/py3/bin/activate



BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export PYTHONPATH=${PYTHONPATH}:/home/pi/models/research/:/home/pi/models/research/slim

# run in background and with low niceness:
nice -10 python ${BASEDIR}/on_event_end_tf.py ${event_id} &
