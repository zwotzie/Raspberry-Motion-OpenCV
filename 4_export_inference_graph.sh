#!/usr/bin/env bash


BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#
# pipline config contains label_map
PIPELINE_CONFIG_PATH=${BASEDIR}/training_data/ssd_inception_v2_coco.config

INPUT_TYPE=image_tensor

TRAINED_CKPT_PREFIX=${BASEDIR}/model
EXPORT_DIR=${BASEDIR}/exported_model


python object_detection/export_inference_graph.py \
    --input_type=${INPUT_TYPE} \
    --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
    --trained_checkpoint_prefix=${TRAINED_CKPT_PREFIX} \
    --output_directory=${EXPORT_DIR}