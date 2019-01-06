#!/usr/bin/env bash

event_id=$1

source ~/py3/bin/activate

export PYTHONPATH=${PYTHONPATH}:/home/pi/models/research/:/home/pi/models/research/slim

# run in background and with low niceness:
nice -10 python on_event_end_tf.py ${event_id} &
