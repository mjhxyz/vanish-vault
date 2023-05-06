#!/bin/bash
PROJECT_SRC="/home/mao/git/vv"
PROJECT_PATH="/home/mao/project/vv"

cd $PROJECT_SRC
git stash
git pull origin master
git stash pop

source $PROJECT_PATH/venv/bin/activate
pip install .
