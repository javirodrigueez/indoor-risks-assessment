"""
Usage: 
  filter_annotations.py <jsonObjects>

Description:
  Needs as standard input file of Charades annotations. Script used to filter videos from Charades dataset (filter by the ones which have objects belonging to our COCO2017 subset classes)
"""
from docopt import docopt
import sys
import json
import gensim.downloader as api


# Initialization
args=docopt(__doc__)
wv = api.load('word2vec-google-news-300')

objects = []
with open(args['<jsonObjects>'], 'r') as f:
  data = json.load(f)
  for item in data:
    objects.append(item['object'])

print("VIDEO,OBJECTS")
for line in sys.stdin:
  tokens = line.split(',')
  video = tokens[0]
  gt_objects = tokens[7].split(';')
  matches = []
  for j in gt_objects:
    #found = False
    for i in objects:
      if j.find('/') != -1:
        j_objects = j.split('/')
        found = False
        for k in j_objects:
          try:
            if wv.similarity(i,k.replace(' ', '')) > 0.6:
              found = True
              #print(line.replace('\n', ''))
              matches.append(k)
              break
          except KeyError:
            continue
        if found == True:
          break
      else:
        try:
          if wv.similarity(i,j.replace(' ','')) > 0.6:
            #found = True
            #print(line.replace('\n', ''))
            matches.append(j)
            break
        except KeyError:
          continue
    #if found == True:
      #break
  print(video + ',' + ';'.join(matches))