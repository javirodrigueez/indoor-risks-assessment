# ARGS
# --------------------
# 1st arg --> directory where the videos to test are
# 2nd arg --> directory where the annotations of the video are
# --------------------

export REPO_DIR=$PWD
DATASETS=$REPO_DIR'/datasets/'
MODELS=$REPO_DIR'/models/'
OUTPUT_DIR=$REPO_DIR'/output/'
VIDEO_DIR=$1
ANNOT_DIR=$2
source launch_container.sh $DATASETS $MODELS $OUTPUT_DIR $VIDEO_DIR $ANNOT_DIR --prepro