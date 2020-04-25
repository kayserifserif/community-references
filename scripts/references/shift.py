import sys
import argparse

from os import listdir
from os.path import isfile, join

import json

import re

def getReferences():
  references = {}
  with open("./data/references.json", "r") as f:
    references = json.load(f)
  return references

def shiftIndices(epCode, orig, shift):
  references = getReferences()
  epRefs = references[epCode]
  diff = shift - orig
  print(f"Shifting references {diff} characters if occurring at index {orig} or after...")
  for refType in epRefs:
    for ref in epRefs[refType]:
      reference = ref["reference"]
      startInDoc = reference["startInDoc"]
      if startInDoc >= orig:
        reference["startInDoc"] += diff
        reference["endInDoc"] += diff
  writeReferences(references)

def resetIndices(epCode, origStart, origEnd, shiftStart):
  shiftEnd = shiftStart + (origEnd - origStart)
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
    fileName = "./data/references.json"
    with open(fileName, "w") as f:
      print(j, file=f)
      print(f"Successfully saved to file {fileName}!")
  except IOError:
    print("Could not write to file.")

def epCode(argStr):
  if not re.match(r"s\d{2}e\d{2}", argStr):
    raise argparse.ArgumentTypeError("Couldn't parse episode code. For example, for season 1 episode 1, the episode code should be s01e01.")
  return argStr

def main(argv):
  parser = argparse.ArgumentParser(
    description="Shift indices in references file to correct mismatches with transcripts.")
  parser.add_argument(
    "epCode",
    help="Episode code, e.g. s01e01 for season 1 episode 1.",
    type=epCode)
  parser.add_argument(
    "origStart",
    help="Original start index.",
    type=int)
  parser.add_argument(
    "origEnd",
    help="Original end index.",
    type=int)
  parser.add_argument(
    "-s", "--shiftTo",
    help="New start index to shift to.",
    type=int)
  
  args = parser.parse_args()

  if args.shiftTo:
    resetIndices(args.epCode, args.origStart, args.origEnd, args.shiftTo)
  else:
    shiftIndices(args.epCode, args.origStart, args.origEnd)

if __name__ == "__main__":
  main(sys.argv)