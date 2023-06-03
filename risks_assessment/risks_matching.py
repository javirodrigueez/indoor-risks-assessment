"""
Usage: 
  risks_matching.py <jsonVideos> <jsonRisksObjects> <jsonRisksProps>
"""
from docopt import docopt
import json

# Init
args=docopt(__doc__)
objects = []
risks = []
properties = []

# Utils
def search_name(name):
  def condition(i):
    return name == i['object']
  return condition
def search_prop(name):
  def condition(i):
    return name == i['name']
  return condition

# Get data
with open(args['<jsonVideos>'], 'r') as f:
  videos = json.load(f)
with open(args['<jsonRisksObjects>'], 'r') as f:
  risks = json.load(f)
with open(args['<jsonRisksProps>'], 'r') as f:
  properties = json.load(f)

# Compute matching
all_risks = []
for v in videos:
  detections = v['objects']
  all_risks_video = []
  for obj in detections:
    object_risks = []
    risk = list(filter(search_name(obj['name']), risks))
    if len(risk) > 0:
      risk = risk[0]
      # Add specific risks
      if len(risk['specific_risks']) > 0:
        for r in risk['specific_risks']:
          object_risks.append({
            "name": r['name'],
            "en": r['en'] # TODO: Add spanish
          })
      # Add properties risks
      if len(risk['properties']) > 0:
        for p in risk['properties']:
          p_risks = list(filter(search_prop(p), properties))
          if len(p_risks) > 0:
            p_risks = p_risks[0]
            for pr in p_risks['risks']:
              object_risks.append({
                "name": pr['name'],
                "en": pr['en'] # TODO: Add spanish
              })  
          else:
            print('ERROR: Property not found in properties corpus')
      # Add all risks to object
      all_risks_video.append({
        "object": obj['name'],
        "level": obj['level'],
        "risks": object_risks
      })
    else:
      print('ERROR: Object not found in risks corpus')
  all_risks.append({
    "video": v['video'],
    "risks": all_risks_video
  })    
print(json.dumps(all_risks, indent=2))