#!/usr/bin/env bash
#
# if you want to clean up the models and start from scratch again
#

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${BASEDIR}/train_configuration.rc


# make backup of exported trained model and create a fresh directory
if find ${EXPORT_MODEL_DIR} -mindepth 1 | read; then
    mv ${EXPORT_MODEL_DIR} ${EXPORT_MODEL_DIR}.${MODEL_NAME}.${NUM_TRAIN_STEPS}.$(date --iso-8601)
    mkdir ${EXPORT_MODEL_DIR}
fi
