# DESCRIPTION
# -------------------------------------------------------
# This script is used to obtain risks from a given video
# -------------------------------------------------------
# ARGUMENTS
# -------------------------------------------------------
# 1 -> video
# 2 -> directory where swinbert model is located
# -------------------------------------------------------

# Initialization
echo "Video $1 prepared to be analysed...."
VIDEO=$1
EVAL_DIR="$2"
CHECKPOINT="$2/model.bin"

# Remove previous execution
rm risks_results/*
rm runs -rf

# Prepare new execution
cp $1 risks_results/
mv risks_results/$(ls risks_results | grep mp4) risks_results/input.mp4

# Obtain SwinBERT description
echo "Obtaining SwinBERT description..."
NAME=$(echo $1 | awk -F/ '{print $NF}' | awk -F. '{print $1}')
echo -n $NAME, >> risks_results/swinbert_caption.txt
cat -n /videocap/annotations/Charades_v1_train.csv | grep $NAME | sed ':a;s/^\(\([^"]*"[^"]*"[^"]*\)*[^"]*"[^",]*\),/\1|/;ta' | awk -F, '{ printf $9 }' >> risks_results/swinbert_caption.txt
echo -n , >> risks_results/swinbert_caption.txt
CUDA_VISIBLE_DEVICES="0" python src/tasks/run_caption_VidSwinBert_inference.py \
--resume_checkpoint $CHECKPOINT  \
--eval_model_dir $EVAL_DIR \
--test_video_fname $VIDEO \
--do_lower_case \
--do_test \
| tail -n3 | head -n1 | awk -F: '{print $2}' | awk '{gsub(/\,/, "|")} 1' >> risks_results/swinbert_caption.txt

# Obtain objects from SwinBERT
echo "Extracting objects from SwinBERT description..."
python3 evaluation/get_objects_from_caption.py risks_data/risks_objects.json risks_results/swinbert_caption.txt > risks_results/swinbert_objects.json

# Obtain objects from YOLOv7
echo "Extracting objects from YOLOv7...."
python3 /videocap/yolo/detect.py --weights /videocap/yolo/yolov7.pt --conf 0.7 --img-size 640 --source $VIDEO --name test --save-txt > risks_results/test.txt
python3 /videocap/yolo/evaluation/get_objects.py test > risks_results/yolo_objects.json # TODO: Change this
cp runs/detect/test/$(ls runs/detect/test/ | grep mp4) risks_results/output.mp4

# Join objects by levels
python3 risks_assessment/join_yolo_swin_detections_by_levels.py risks_results/yolo_objects.json risks_results/swinbert_objects.json > risks_results/all_objects.json

# Risks assessment
python3 risks_assessment/risks_matching.py risks_results/all_objects.json risks_data/risks_objects.json risks_data/risks_properties.json > risks_results/output_risks.json

# Estandarization of file format
sed -i '1i\VIDEO,GROUND-TRUTH,INFERENCE' risks_results/swinbert_caption.txt