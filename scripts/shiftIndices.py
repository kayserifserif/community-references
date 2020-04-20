import sys
from os import listdir
from os.path import isfile, join
import re
import json

def getReferences():
  references = {}
  with open("./output/references.json", "r") as f:
    references = json.load(f)
  return references

def shiftIndices(epCode, origi, shifti):
  references = getReferences()
  epRefs = references[epCode]
  diff = shifti - origi
  print(f"Shifting references {diff} characters if occurring at index {origi} or after...")
  for refType in epRefs:
    for ref in epRefs[refType]:
      reference = ref["reference"]
      startInDoc = reference["startInDoc"]
      if startInDoc >= origi:
        reference["startInDoc"] += diff
        reference["endInDoc"] += diff
  writeReferences(references)

def resetIndices(epCode, origStart, origEnd, shiftStart, shiftEnd):
  references = getReferences()
  epRefs = references[epCode]
  found = False
  for refType in epRefs:
    for ref in epRefs[refType]:
      reference = ref["reference"]
      startInDoc = reference["startInDoc"]
      endInDoc = reference["endInDoc"]
      if startInDoc == origStart and endInDoc == origEnd:
        found = True
        entity = reference["entity"]
        print(f"Resetting indices for {entity} from {origStart} {origEnd} to {shiftStart} {shiftEnd}...")
        reference["startInDoc"] = shiftStart
        reference["endInDoc"] = shiftEnd
      elif (startInDoc == origStart and endInDoc != origEnd) or (startInDoc != origStart and endInDoc == origEnd):
        print(f"Oops. Original indices don't match. Given: {origStart} {origEnd}; actual: {startInDoc} {endInDoc}.")
  if not found:
    print("Indices not found.")
    return
  writeReferences(references)

def writeReferences(references):
  try:
    j = json.dumps(references, indent=2)
    fileName = "./output/references.json"
    with open(fileName, "w") as f:
      print(j, file=f)
      print(f"Successfully saved to file {fileName}!")
  except IOError:
    print("Could not write to file.")

def main():
  if len(sys.argv) is 4 and re.match(r"s\d\de\d\d", sys.argv[1]) and sys.argv[2].isdigit() and sys.argv[3].isdigit():
    shiftIndices(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))

  elif len(sys.argv) is 6 and re.match(r"s\d\de\d\d", sys.argv[1]) and sys.argv[2].isdigit() and sys.argv[3].isdigit() and sys.argv[4].isdigit() and sys.argv[5].isdigit():
    resetIndices(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))

  else:

    print("usage:\n\
  commands:\n\
    [episodeCode] [originalStart] [shiftedStart]\n\
    [episodeCode] [originalStart] [originalEnd] [shiftedStart] [shiftedEnd]\n\
  arguments:\n\
    [episodeCode]: code of episode to analyse, in the form of s01e01\n\
    [originalStart]: original startInDoc index to shift, affecting both the exact reference and those after it\n\
    [originalEnd]: original endInDoc index to shift\n\
    [shiftedStart]: new startInDoc index\n\
    [shiftedEnd]: new endInDoc index")

if __name__ == "__main__":
  main()