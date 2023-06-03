# ARGUMENTS
# ------------------------------
# 1st --> where the videos are
# 2nd --> number of videos
# 3rd --> name of the test
# 4th -> output file
# ------------------------------

# get videos
rm results/input_videos/*
rm results/output_videos/*
VIDEOS=$(ls $1 | shuf -n $2)
for i in $VIDEOS
do
  cp $1/$i results/input_videos/
done
python3 detect.py --weights yolov7.pt --conf 0.7 --img-size 640 --source results/input_videos/ --name $3 --save-txt | head -n -1 | tail -n +10 > $4
for i in $VIDEOS
do
  cp runs/detect/$i results/output_videos
done