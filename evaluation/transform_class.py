# ARGS
# ---------------
# Input -> Lines to be transformed

import spacy
import sys

class CustomTransform:

  def __init__(self):
    self.nlp = spacy.load('en_core_web_sm')
    
  def pos_filtering(self, doc):
    tokens = []
    for token in doc:
      if token.pos_ in ['ADJ', 'NOUN', 'VERB', 'PUNCT', 'PROPN']:
        tokens.append(token)
    return tokens
  
  def punct_filtering(self, tokens):
    filtered = []
    for i in range(len(tokens)):
      if tokens[i].pos_ != 'PUNCT' or tokens[i].text == ';': # We keep ';' as we need it to separate annotations
        filtered.append(tokens[i])
    return filtered
         
  def transform(self, line, punct, lemma, pos):
    tokens = self.nlp(line)
    
    if punct:
      tokens = self.punct_filtering(tokens)
    if pos:
      tokens = self.pos_filtering(tokens)
    
    sentence = ''
    for i in tokens:
      if i.pos_ == 'PUNCT':
        if lemma:
          sentence = sentence + str(i.lemma_)
        else:
          sentence = sentence + str(i)
      else:
        if lemma:
          sentence = sentence + ' ' + str(i.lemma_)
        else:
          sentence = sentence + ' ' + str(i)
    return sentence.strip()
