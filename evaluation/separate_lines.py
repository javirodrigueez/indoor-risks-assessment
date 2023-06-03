"""
Usage: 
  separate_lines.py <predictionFile> <annotationFile> [--punct]
"""
from docopt import docopt

import sys

args=docopt(__doc__)
annot_file = open(args['<annotationFile>'], 'w')
preds_file = open(args['<predictionFile>'], 'w')

for line in sys.stdin:
	tokens = line.split(',')
	annotations = tokens[1].split(';')
	prediction = tokens[2].strip('\n').strip(' ')
	for i in annotations:
		if args['--punct']:
			annot_file.write(i.replace('|','').strip(' ')+'\n')
			preds_file.write(prediction.replace('|', '')+'\n')
		else:
			annot_file.write(i.replace('|',',').strip(' ')+'\n')
			preds_file.write(prediction.replace('|', ',')+'\n')



annot_file.close()
preds_file.close()
