"""
This script is used to obtain objects from swinbert captions.

Usage: 
  get_objects_from_captions.py <jsonObjects> <captionFile>
"""
from docopt import docopt

import sys
from transform_class import CustomTransform
import json
import gensim.downloader as api


# Initialization
args=docopt(__doc__)
wv = api.load('word2vec-google-news-300')
t = CustomTransform()

# Obtain coco classes
objects = []
with open(args['<jsonObjects>'], 'r') as f:
  data = json.load(f)
  for item in data:
    objects.append(item['object'])

# Obtain objects
pred_objects = []
video_id = ''
f = open(args['<captionFile>'], 'r')
lines = f.readlines()
f.close()

# Iterate
print("[")
for i, line in enumerate(lines):
  pred_objects = []
  tokens = line.split(',')
  caption = tokens[2]
  caption_transformed = t.transform(caption, True, False, False)
  video_id = tokens[0]
  words = caption_transformed.split(' ')
  for w in words:
    for o in objects:
      try:
        if wv.similarity(w, o) > 0.62:
          pred_objects.append(o)
          break
      except KeyError:
        continue
  data = {
    "video": video_id + '.mp4',
    "objects": pred_objects
  }
  # Print results
  if (i == len(lines)-1):
    print(json.dumps(data, indent=2))
  else:
    print(json.dumps(data, indent=2) + ',')

print("]")