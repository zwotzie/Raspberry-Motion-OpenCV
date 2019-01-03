#!/usr/bin/env bash

# https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_locally.md

# From the tensorflow/models/research/ directory

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#
# pipline config contains label_map
PIPELINE_CONFIG_PATH=${BASEDIR}/training_data/ssd_inception_v2_coco.config
# {path to model directory}
MODEL_DIR=${BASEDIR}/model
# NUM_TRAIN_STEPS=50000
NUM_TRAIN_STEPS=50
SAMPLE_1_OF_N_EVAL_EXAMPLES=1

python object_detection/model_main.py \
    --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
    --model_dir=${MODEL_DIR} \
    --num_train_steps=${NUM_TRAIN_STEPS} \
    --sample_1_of_n_eval_examples=$SAMPLE_1_OF_N_EVAL_EXAMPLES \
    --alsologtostderr