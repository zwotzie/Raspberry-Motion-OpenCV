#!/usr/bin/env bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${BASEDIR}/train_configuration.rc



mv ${MODEL_DIR} ${MODEL_DIR}-$(date --iso-8601)

mkdir ${MODEL_DIR}

cp ${PRETRAINED_MODEL_DIR}/* ${MODEL_DIR}