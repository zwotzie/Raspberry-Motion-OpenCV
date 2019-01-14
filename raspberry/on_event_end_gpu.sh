#!/usr/bin/env bash
# set -x

event_id=$1

source ~/py3/bin/activate


export BASEPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"


source ${BASEPATH}/train_configuration.rc


python ${BASEPATH}/raspberry/on_event_end_tf.py ${event_id}
