#!/usr/bin/env bash
#
# if you want to clean up the models and start from scratch again
#

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${BASEDIR}/train_configuration.rc


if find ${MODEL_DIR} -mindepth 1 | read; then
   echo "${MODEL_DIR} not empty..."
else
    if [ ! -d ${MODEL_DIR} ]; then
        mkdir ${MODEL_DIR}
    fi
   cp -a ${PRETRAINED_MODEL_DIR}/* ${MODEL_DIR}/
fi

