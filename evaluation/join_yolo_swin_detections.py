"""
Usage: 
  join_yolo_swin_detections.py <jsonYolo> <jsonSwin>
"""
from docopt import docopt
import json

# Utils
def search_name(name):
  def condition(v):
    return name == v['video']
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

# Join objects
for yolo in yoloDetections:
  swin = list(filter(search_name(yolo['video']), swinDetections))[0]
  allDetections = yolo['objects']
  allDetections.extend(swin['objects'])
  objects = list(dict.fromkeys(allDetections))
  data = {
    "video": yolo['video'],
    "objects": objects
  }
  detections.append(data)

# Print results
print(json.dumps(detections, indent=2))