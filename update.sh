#!/bin/bash
PROJECT_SRC="/home/mao/git/vv"
PROJECT_PATH="/home/mao/project/vv"

source $PROJECT_PATH/venv/bin/activate
cd $PROJECT_SRC
pip install .
