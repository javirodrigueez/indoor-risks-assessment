# DESCRIPTION
# ------------------------------
# Script that receive names of videos and outputs detections in JSON
# ARGUMENTS
# ------------------------------
# 1st --> file of videos
# 2nd --> where the videos are
# 3rd --> name of the test
# 4th -> output file
# ------------------------------

VIDEOS=$(cat $1)
for i in $VIDEOS
do
  cp $2/$i results/$3/
done
python3 detect.py --weights yolov7.pt --conf 0.7 --img-size 640 --source results/$3/ --name $3 --save-txt | head -n -1 | tail -n +10 > $4
python3 evaluation/get_objects_txt.py $3 > results/objects_$3.json