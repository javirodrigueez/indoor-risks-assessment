# ARGUMENTS
# ------------------------
# 1st --> number of videos in the input list
# 2nd --> name of dataset (should be equal to name of the directory associated)
# 3rd --> absolute path to directory where the videos are (begins and ends in '/')
# 4th --> output file
# ------------------------
# INPUT
# ------------------------
# An input with the video list must be provided
# -------------------------

# preparation of given environment
EVAL_DIR="./models/table1/$2/best-checkpoint/"
CHECKPOINT="./models/table1/$2/best-checkpoint/model.bin"
# execution of tests
echo "VIDEO,GROUND-THRUTH,INFERENCE" > $4
while read i
do
	echo -n $i, >> $4
	# obtain data for annotation to compare with each output. If in th gt description appears the character ',' we replace it to '|' to ease the blue extraction then
	NAME=$(echo $i | awk -F. '{print $1}')
        cat -n /videocap/annotations/Charades_v1_train.csv | grep $NAME | sed ':a;s/^\(\([^"]*"[^"]*"[^"]*\)*[^"]*"[^",]*\),/\1|/;ta' | awk -F, '{ printf $9 }' >> $4
        cat -n /videocap/annotations/Charades_v1_test.csv | grep $NAME | sed ':a;s/^\(\([^"]*"[^"]*"[^"]*\)*[^"]*"[^",]*\),/\1|/;ta' | awk -F, '{ printf $9 }' >> $4
        echo -n , >> $4
        # inference
	VIDEO=$3/$i
	CUDA_VISIBLE_DEVICES="0" python src/tasks/run_caption_VidSwinBert_inference.py \
       --resume_checkpoint $CHECKPOINT  \
       --eval_model_dir $EVAL_DIR \
       --test_video_fname $VIDEO \
       --do_lower_case \
       --do_test \
       | tail -n3 | head -n1 | awk -F: '{print $2}' >> $4
done