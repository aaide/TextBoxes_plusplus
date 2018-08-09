#!/bin/bash

# Start docker container
#
# Usage:
#     sudo ./runRos.sh

nvidia-docker run -it \
                  --rm \
                  -v ${PWD}/models:/opt/caffe/models \
                  -v ${PWD}/crnn/model:/opt/caffe/crnn/model \
                  -v ${PWD}/demo_images:/opt/caffe/demo_images \
                  tbpp_crnn:gpu bash
