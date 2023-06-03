"""
Usage: 
  evaluate_object_recognition.py <jsonDetections>
  
Description:
  Script to evaluate object recognition. Additionally, this needs as standard input file of Charades annotations with format "VIDEO,OBJECTS"
"""
from docopt import docopt
import sys
import json
import gensim.downloader as api


# Initialization
args=docopt(__doc__)
wv = api.load('word2vec-google-news-300')

# Get data
videos = []
with open(args['<jsonDetections>'], 'r') as f:
  data = json.load(f)
  for item in data:
    videos.append({
      "video": item['video'],
      "objects": item['objects']
    })

print("VIDEO,GT_OBJECTS,DETECTED_OBJECTS,RECALL")
line_number = 0
for line in sys.stdin:
  # Split info
  tokens = line.split(',')
  # Init utilized vars
  counter = 0
  video = tokens[0]
  list_gt_objects = tokens[1]
  gt_objects = list_gt_objects.replace('\n','').split(';')
  # Iterate
  video_objects = videos[line_number]['objects']
  for j in gt_objects:
    found = False
    for i in video_objects:
      if j.find('/') != -1:
        j_objects = j.split('/')
        for k in j_objects:
          try:
            if wv.similarity(i,k.replace(' ', '')) > 0.62:
              #print(i + " " + k)
              found = True
              counter += 1
              break
          except KeyError:
            continue
        if found == True:
          break
      else:
        try:
          if wv.similarity(i,j.replace(' ','')) > 0.62:
            #print(i + " " + j)
            #found = True
            counter += 1
            break
        except KeyError:
          continue
    #if found == True:
      #break
  line_number += 1
  recall = float(counter / len(gt_objects))
  print(video + "," + list_gt_objects.replace('\n','') + "," + ';'.join(video_objects) + "," + str(recall))
    