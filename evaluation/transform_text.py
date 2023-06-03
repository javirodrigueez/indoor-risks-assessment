"""
Usage: 
  test.py [--punct] [--lemma] [--pos]
"""
from docopt import docopt
from transform_class import CustomTransform
import sys

args=docopt(__doc__)
t = CustomTransform()

for line in sys.stdin:
    tokens = line.split(',')
    tokens[1] = t.transform(tokens[1].replace(';',' ;'), args['--punct'], args['--lemma'], args['--pos']).strip('"').lower().strip()
    tokens[2] = t.transform(tokens[2], args['--punct'], args['--lemma'], args['--pos']).strip()
    print(','.join(tokens))