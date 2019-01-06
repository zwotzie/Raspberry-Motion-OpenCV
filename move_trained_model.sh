#!/usr/bin/env bash

#
# if you want to clean up the models and start from scratch again
#

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${BASEDIR}/train_configuration.rc


# make backup of existing trained model and create fresh model directory
mv ${MODEL_DIR} ${MODEL_DIR}-$(date --iso-8601)
mkdir ${MODEL_DIR}

cp ${PRETRAINED_MODEL_DIR}/* ${MODEL_DIR}/


# make backup of exported trained model and create a fresh directory
if find ${EXPORT_MODEL_DIR} -mindepth 1 | read; then
    mv ${EXPORT_MODEL_DIR} ${EXPORT_MODEL_DIR}-$(date --iso-8601)
    mkdir ${EXPORT_MODEL_DIR}
fi
