# ARGUMENTS
# 1 -> input file
# 2 -> output file

import sys
import torch
from torchmetrics import SacreBLEUScore

args = sys.argv[1:]
sacrebleu = SacreBLEUScore(n_gram=1)
output = open(args[1], 'w')
with open(args[0], 'r') as f:
  for line in f:
    tokens = line.split(',')
    reference = tokens[1].replace('|', ',')
    reference = reference.split(';')
    bleu = sacrebleu([tokens[2]], [[i.strip() for i in reference]])
    output.write(str(bleu.item()) + '\n')

output.close()
    

