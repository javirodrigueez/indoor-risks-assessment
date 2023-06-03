"""
Usage: 
  get_objects.py <testName>
"""
from docopt import docopt
import os
import yaml
import json

args=docopt(__doc__)

# Filtering functions
def filter_videos(v):
  return '.mp4' in v
def filter_name(name):
  def condition(v):
    return name in v
  return condition


# Initialization
file_list = os.listdir('/videocap/runs/detect/' + args['<testName>'])
videos_list = list(filter(filter_videos, file_list))
objects = []
with open('/videocap/yolo/data/coco.yaml', 'r') as f:
  data = yaml.safe_load(f)
  objects = data['names']

# Iterate over each video
print('[')
for v in range(len(videos_list)):
  pathdir = '/videocap/runs/detect/' + args['<testName>'] + '/labels/'
  object_files = os.listdir(pathdir)
  video_object_files = list(filter(filter_name(videos_list[v].replace('.mp4', '')), object_files))
  # Iterate over files of a video
  detections = set()
  for i in video_object_files:
    with open(pathdir + i, 'r') as f:
      for line in f:
        tokens = line.split(' ')
        detections.add(objects[int(tokens[0])])
  data = {
    "video": videos_list[v],
    "objects": list(detections)
  }
  if v == len(videos_list)-1:
    print(json.dumps(data, indent=2))
  else:
    print(json.dumps(data, indent=2) + ',')
print(']')
