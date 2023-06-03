"""
Usage: 
  get_objects.py <testName>
"""
from docopt import docopt
import os
import yaml
import json
import subprocess
import re
import spacy

args=docopt(__doc__)

# Utils
def filter_videos(v):
  return '.mp4' in v
def filter_name(name):
  def condition(v):
    return name in v
  return condition
""" def apply_lemma(i):
  if i == "tvs":
    return "tv"
  else:
    return nlp(i)[0].lemma_ """

# Initialization
file_list = os.listdir('/videocap/runs/detect/' + args['<testName>'])
#nlp = spacy.load('en_core_web_sm')
videos_list = list(filter(filter_videos, file_list))
objects = []

# Get data
with open('/videocap/yolo/data/coco.yaml', 'r') as f:
  data = yaml.safe_load(f)
  objects = data['names']

# Iterate over each video
print('[')
for v in range(len(videos_list)):
  # Get only lines related to actual video
  command = 'cat /videocap/risks_results/' +  args['<testName>'] + '.txt | grep "video ' + str(v+1) + '/"'
  output = subprocess.check_output(command, shell=True)
  output = output.decode('utf-8')
  lines = output.split('\n')
  video_name = lines[0][lines[0].find(args['<testName>'] + '/')+len(args['<testName>'])+1 : lines[0].find(':')]
  detections = set()
  for l in lines:
    start = l.find('.mp4')
    end = l.find(' Done.')
    line_objects = l[start+6:end]
    if len(line_objects) == 0:
      continue
    clean_line = re.sub(r'[\d\s]+', '', line_objects)
    list_objects = clean_line.split(',')
    list_objects.pop()
    #list_objects = map(apply_lemma, list_objects)

    detections.update(list_objects)
  data = {
    "video": video_name,
    "objects": list(detections)
  }
  if v == len(videos_list)-1:
    print(json.dumps(data, indent=2))
  else:
    print(json.dumps(data, indent=2) + ',')
print(']')