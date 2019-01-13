#!/usr/bin/env bash

#
# hmm in model/ there is already an frozen_inference_graph.pb
#

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${BASEDIR}/train_configuration.rc

# make backup of exported trained model and create a fresh directory
if find ${EXPORT_MODEL_DIR} -mindepth 1 | read; then
    # just to be sure when removing, that the variable is set!
    [ -n "${EXPORT_MODEL_DIR}" ] && rm -rf ${EXPORT_MODEL_DIR}
    mkdir ${EXPORT_MODEL_DIR}
fi

# export the graph
python object_detection/export_inference_graph.py \
    --input_type=${INPUT_TYPE} \
    --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
    --trained_checkpoint_prefix=${TRAINED_CKPT_PREFIX} \
    --output_directory=${EXPORT_MODEL_DIR}

# make a backup for later use
echo "Make backup from ${EXPORT_MODEL_DIR} to ${EXPORT_MODEL_DIR}.${MODEL_NAME}.${NUM_TRAIN_STEPS}.$(date --iso-8601)"
cp -a ${EXPORT_MODEL_DIR} ${EXPORT_MODEL_DIR}.${MODEL_NAME}.${NUM_TRAIN_STEPS}.$(date --iso-8601)