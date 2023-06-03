DATA_DIR=$1
MODEL_DIR=$2
OUTPUT=$3
VIDEO_DIR=$4
ANNOT_DIR=$5

if [ -z $CUDA_VISIBLE_DEVICES ]; then
    CUDA_VISIBLE_DEVICES='0'
fi

if [ "$4" = "--prepro" ]; then
    RO=""
else
    RO=",readonly"
fi

docker run --memory="16g" --gpus '"'device=$CUDA_VISIBLE_DEVICES'"' --ipc=host --rm -it \
    --mount src=$(pwd),dst=/videocap,type=bind \
    --mount src=$DATA_DIR,dst=/videocap/datasets,type=bind \
    --mount src=$MODEL_DIR,dst=/videocap/models,type=bind \
    --mount src=$OUTPUT,dst=/videocap/output,type=bind \
    --mount src=$VIDEO_DIR,dst=/videocap/videos,type=bind \
    --mount src=$ANNOT_DIR,dst=/videocap/annotations,type=bind \
    --name risks_swinbert_yolo_jrodriguez \
    -e NVIDIA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
    -w /videocap javiro01/risks-assessment:latest \
    bash -c "source /videocap/setup.sh && bash" 
