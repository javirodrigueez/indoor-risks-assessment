"""
Usage: 
  join_yolo_swin_detections_by_levels.py <jsonYolo> <jsonSwin>
"""
from docopt import docopt
import json

# Utils
def search_name(name):
  def condition(v):
    return name == v['video']
  return condition
def search_object(name):
  def condition(v):
    return name == v
  return condition

# Init
args=docopt(__doc__)
yoloDetections = []
swinDetections = []
detections = []

# Get data
with open(args['<jsonYolo>'], 'r') as f:
  yoloDetections = json.load(f)
with open(args['<jsonSwin>'], 'r') as f:
  swinDetections = json.load(f)

# Join objects by levels
for yolo in yoloDetections:
  swin = list(filter(search_name(yolo['video']), swinDetections))[0]
  objects = []
  # Get risks level 2 and 3
  for obj in swin['objects']:
    obj_y = list(filter(search_object(obj), yolo['objects']))
    if len(obj_y) > 0:
      level = 3
    else:
      level = 2
    objects.append({
      "name": obj,
      "level": level
    })
  # Get risks of level 1
  yolo_difference = [item for item in yolo['objects'] if item not in swin['objects']]
  for obj in yolo_difference:
    objects.append({
      "name": obj,
      "level": 1
    })
  # Add detections to general list
  data = {
    "video": yolo['video'],
    "objects": objects
  }
  detections.append(data)

# Print results
print(json.dumps(detections, indent=2))