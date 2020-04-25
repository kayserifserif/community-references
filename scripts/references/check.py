import sys
import argparse

from os import listdir
from os.path import isfile, join

import json

import re

def getTranscript(epCode: str) -> str:
  try:
    file = "./transcripts/" + epCode + ".txt"
    with open(file, "r") as f:
      transcript = f.read()
    return transcript
  except IOError:
    print(f"Cannot read {file}.")
    return

def getReferences() -> dict:
  try:
    file = "./data/references.json"
    with open(file, "r") as f:
      references = json.load(f)
    return references
  except IOError:
    print(f"Cannot read {file}.")
    return

def checkReferences(references: dict, transcripts: dict, epCode: str = None) -> list:
  epErrors = []
  for refType in references[epCode]:
    for instance in references[epCode][refType]:
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
        # errorLog = epCode + " / " + sentence + " / " + entity + " " + str(startInDoc) + " " + str(endInDoc) + " / " + actual + " / " + problem
        errorLog = sentence + " / " + entity + " " + str(startInDoc) + " " + str(endInDoc) + " / " + actual + " / " + problem
        epErrors.append(errorLog)
  return epErrors

def findErrors(epCodes: list = None) -> list:
  if len(epCodes) is 0:
    epCodes = sorted([f[:-4] for f in listdir("./transcripts") if isfile(join("./transcripts", f))])[1:]

  # get transcript(s)
  transcripts = {}
  for epCode in epCodes:
    transcript = getTranscript(epCode)
    transcripts[epCode] = transcript

  # get references
  references = getReferences()
  
  # check references
  errors = {}
  for epCode in epCodes:
    epErrors = checkReferences(references, transcripts, epCode)
    if len(epErrors) > 0:
      errors[epCode] = epErrors
  return errors

def epCodeType(argStr):
  if not re.match(r"s\d{2}e\d{2}", argStr):
    raise argparse.ArgumentTypeError("Couldn't parse episode code. For example, for season 1 episode 1, the episode code should be s01e01.")
  return argStr

def main(argv):
  parser = argparse.ArgumentParser(
    description="Check mismatches between references file and transcripts.")
  parser.add_argument(
    "epCode",
    help="Episode code, e.g. s01e01 for season 1 episode 1. If omitted, checks all episodes.",
    type=epCodeType,
    nargs="*")

  args = parser.parse_args()

  errors = findErrors(args.epCode)
  print()
  for epCode in errors:
    print(epCode)
    for error in errors[epCode]:
      print(error)
    print()

if __name__ == "__main__":
  main(sys.argv)