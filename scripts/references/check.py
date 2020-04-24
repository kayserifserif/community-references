import sys
from os import listdir
from os.path import isfile, join
import json
import re

def check():
  transcripts = {};
  epCodes = sorted([f[:-4] for f in listdir("./transcripts") if isfile(join("./transcripts", f))])[1:]
  for epCode in epCodes:
    with open("./transcripts/" + epCode + ".txt", "r") as f:
      transcripts[epCode] = f.read()

  with open("./output/references.json", "r") as f:
    references = json.load(f)
    for epCode in references:

      people = references[epCode]["people"]
      titles = references[epCode]["titles"]

      for instance in people:
        reference = instance["reference"]
        entity = reference["entity"]
        sentence = reference["sentence"]
        startInDoc = reference["startInDoc"]
        endInDoc = reference["endInDoc"]
        actual = transcripts[epCode][startInDoc:endInDoc]
        if actual != entity:
          if len(actual) != len(entity):
            problem = "length"
          else:
            problem = "pos"
          print(epCode + " / " + sentence + " / " + entity + " " + str(startInDoc) + " " + str(endInDoc) + " / " + actual + " / " + problem)

def main():
  check()

if __name__ == "__main__":
  main()