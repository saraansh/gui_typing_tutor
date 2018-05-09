# -*- coding: utf-8 -*-
import numpy
import sys
import os
import glob

from utils import getDataset, defineModel, getText, getInputOutput

def predict(filename):
  raw_text = getText(filename)
  data = getDataset(raw_text)
  model = defineModel(data)

  loadWeights(model)
  generateText(model, raw_text)

def loadWeights(model):
  #filepath = sys.argv[3]
  files = glob.glob(os.getcwd() + "\\*")
  filepath = max(files, key=os.path.getctime) 
  model.load_weights(filepath)
  model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

def generateText(model, raw_text):
  chars = sorted(list(set(raw_text)))
  char_to_int = dict((char, number) for number, char in enumerate(chars))
  int_to_char = dict((i, c) for i, c in enumerate(chars))

  n_chars = len(raw_text)
  n_vocab = len(chars)

  # Prepare the dataset of input to output pairs encoded as integers
  sequence_length = 100

  input, output = getInputOutput(raw_text, n_chars, char_to_int, sequence_length)

  start = numpy.random.randint(0, len(input)-1)
  pattern = input[start]

  iterations = int(sys.argv[2])
  words = ""
  counter = 0
  while (counter!=iterations):
    x = numpy.reshape(pattern, (1, len(pattern), 1))
    x = x / float(n_vocab)
    prediction = model.predict(x, verbose=0)
    index = numpy.argmax(prediction)
    result = int_to_char[index]
    seq_in = [int_to_char[value] for value in pattern]
    sys.stdout.write(result)
    pattern.append(index)
    pattern = pattern[1:len(pattern)]
    words = words + result
    if (result==' '):
      counter = counter + 1
  #print(words, "\nDone.")
  output = "C:/Users/Hopeless/ML Projects/TypeAI/metrics_gui/predicted.txt"
  with open(output, w) as f:
    f.write(words)

if __name__ == "__main__":
    #filepath = sys.argv[0]
    filepath = "C:/Users/Hopeless/ML Projects/TypeAI/metrics_gui/curated_v1.txt"
    predict(filepath)
