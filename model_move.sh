#!/usr/bin/env bash
#
# if you want to clean up the models and start from scratch again
#

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${BASEDIR}/train_configuration.rc


# make backup of existing trained model and create fresh model directory
mv ${MODEL_DIR} ${MODEL_DIR}.${MODEL_NAME}.${NUM_TRAIN_STEPS}.$(date --iso-8601)
mkdir ${MODEL_DIR}

# cp ${PRETRAINED_MODEL_DIR}/* ${MODEL_DIR}/
