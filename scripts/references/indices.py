import sys
import argparse
from PyInquirer import prompt

from os import listdir
from os.path import isfile, join

import json

import re

def getReferences() -> dict:
  file = "./data/references.json"
  try:
    with open(file, "r") as f:
      references = json.load(f)
    return references
  except IOError:
    print(f"Could not open {file}.")
    return

def getTranscript(epCode: str) -> str:
  try:
    file = "./transcripts/" + epCode + ".txt"
    with open(file, "r") as f:
      transcript = f.read()
    return transcript
  except IOError:
    print(f"Could not read {file}.")
    return

def getEpMismatches(references: dict, transcript: str, epCode: str = None) -> dict:
  epMismatches = []
  for refType in references[epCode]:
    for instance in references[epCode][refType]:
      reference = instance["reference"]
      expected = reference["entity"]
      sentence = reference["sentence"]
      startInDoc = reference["startInDoc"]
      endInDoc = reference["endInDoc"]
      # actual = transcripts[epCode][startInDoc:endInDoc]
      actual = transcript[startInDoc:endInDoc]
      if actual != expected:
        errorLog = {
          "expected": expected,
          "sentence": sentence,
          "startInDoc": startInDoc,
          "endInDoc": endInDoc,
          "actual": actual
        }
        epMismatches.append(errorLog)
  return epMismatches

def getMatches(transcript: str, search: str) -> dict:
  results = re.finditer(search, transcript)
  matches = []
  for result in results:
    match = {
      "startInDoc": result.start(),
      "endInDoc": result.end(),
      "context": "…" + transcript[result.start() - 20 : result.end() + 20] + "…"
    }
    matches.append(match)
  if len(matches) == 0:
    print("No results found.")
    return
  return matches

def getNewIndices(ref, matches):
  matchesList = [
    str(match["startInDoc"]) + "-" + str(match["endInDoc"]) + " in \"" +
    match["context"].replace("\n", "\\n") + "\""
    for match in matches]
  diffs = []
  for match in matches:
    diffs.append(abs(ref["startInDoc"] - match["startInDoc"]))
  leastDiff = min(diffs)
  closestMatch = matches[diffs.index(leastDiff)]
  print()
  print("Closest match:")
  print(
    str(closestMatch["startInDoc"]) + "-" + str(closestMatch["endInDoc"]) + " in \"" +
        closestMatch["context"].replace("\n", "\\n") + "\"")
  confirm = prompt({"type": "confirm", "name": "confirm", "message": "Shift to closest match?"})
  if confirm["confirm"]:
    return (closestMatch["startInDoc"], closestMatch["endInDoc"])
  else:
    matchChoice = prompt({
      "type": "list",
      "name": "matchChoice",
      "message": "Shift to:",
      "choices": matchesList
      })
    index = matchesList.index(matchChoice["matchChoice"])
    return (matches[index]["startInDoc"], matches[index]["endInDoc"])

def strAtIndices(transcript: str, indices: tuple) -> str:
  return transcript[indices[0]:indices[1]]

def shift(references: dict, transcript: str, epCode: str, orig: tuple, shift: tuple):
  posDiff = shift[0] - orig[0]
  lenDiff = abs((shift[1] - shift[0]) - (orig[1] - orig[0]))
  epRefs = references[epCode]
  if lenDiff == 0:
    print("Difference in position.")
    print(f"Shifting {epCode} references {posDiff} characters if occurring at index {orig[0]} or after...")
    for refType in epRefs:
      for ref in epRefs[refType]:
        reference = ref["reference"]
        startInDoc = reference["startInDoc"]
        endInDoc = reference["endInDoc"]
        if startInDoc >= orig[0]:
          origStr = transcript[startInDoc:endInDoc].replace("\n", "\\n")
          shiftStart = startInDoc + posDiff
          reference["startInDoc"] = shiftStart
          shiftEnd = endInDoc + posDiff
          reference["endInDoc"] = shiftEnd
          shiftStr = transcript[shiftStart:shiftEnd].replace("\n", "\\n")
          log = origStr + " -> " + shiftStr
          if reference["entity"] == shiftStr:
            log += "\033[92m ✓\033[0m"
          print(log)
  else:
    print("Difference in length.")
    print(f"Resetting {epCode} indices {orig} to {shift}...")
    for refType in epRefs:
      for ref in epRefs[refType]:
        if ref["reference"]["startInDoc"] == orig[0]:
          ref["reference"]["startInDoc"] = shift[0]
          ref["reference"]["endInDoc"] = shift[1]
          pass
  writeReferences(references)

def writeReferences(references: dict):
  fileName = "./data/references.json"
  try:
    j = json.dumps(references, indent=2)
    with open(fileName, "w") as f:
      print(j, file=f)
      print()
      print(f"Successfully saved to file {fileName}!")
  except IOError:
    print(f"Could not write to {fileName}.")

def epCodeType(argStr):
  if not re.match(r"s\d{2}e\d{2}", argStr):
    raise argparse.ArgumentTypeError("Couldn't parse episode code. For example, for season 1 episode 1, the episode code should be s01e01.")
  return argStr

def audit(args):
  epCodes = []
  if len(args.epCode) > 0:
    epCodes = args.epCode
  else:
    epCodes = sorted([f[:-4] for f in listdir("./transcripts") if isfile(join("./transcripts", f))])[1:]

  references = getReferences()
  transcripts = {}
  mismatches = {}
  for epCode in epCodes:
    transcript = getTranscript(epCode)
    epMismatches = getEpMismatches(references, transcript, epCode)
    if len(epMismatches) > 0:
      mismatches[epCode] = epMismatches
      transcripts[epCode] = transcript

  if not mismatches:
    print("All indices match up!")
    return

  print()
  print("Mismatches:")
  for ep in mismatches:
    print(ep)
    for error in mismatches[ep]:
      print(error)
    print()

def fix(args):
  epCodes = []
  if len(args.epCode) > 0:
    epCodes = args.epCode
  else:
    epCodes = sorted([f[:-4] for f in listdir("./transcripts") if isfile(join("./transcripts", f))])[1:]

  references = getReferences()
  transcripts = {}
  mismatches = {}
  for epCode in epCodes:
    transcript = getTranscript(epCode)
    epMismatches = getEpMismatches(references, transcript, epCode)
    if len(epMismatches) > 0:
      mismatches[epCode] = epMismatches
      transcripts[epCode] = transcript

  if not mismatches:
    print("All indices match up!")
    return

  firstEp = list(mismatches.keys())[0]
  firstError = mismatches[firstEp][0]
  print()
  print(f"First error in {firstEp}:")
  print("Expected \"" +
    firstError["expected"] + "\" in \"" +
    firstError["sentence"] + "\" at indices " +
    str(firstError["startInDoc"]) + "-" + str(firstError["endInDoc"]) + ", but found \"" +
    firstError["actual"].encode("unicode_escape").decode("utf-8") + "\" instead.")
  results = getMatches(transcripts[firstEp], firstError["expected"])
  shifted = getNewIndices(firstError, results)
  original = (firstError["startInDoc"], firstError["endInDoc"])
  print(original, shifted)
  print()

  shift(references, transcripts[firstEp], firstEp, original, shifted)

def find(args):
  transcript = getTranscript(args.epCode).encode("unicode_escape").decode("utf-8")
  results = re.finditer(args.search, transcript)
  counter = 0
  for result in results:
    counter += 1
    print(result.start(), result.end())
    print(transcript[result.start() - 20 : result.end() + 20])
  if type == "p":
    if search in all_people:
      person_info = all_people[search].copy()
      person_info.insert(0, search)
      print(person_info)
  elif type == "t":
    if search in all_titles:
      title_info = all_titles[search].copy()
      title_info.insert(0, search)
      print(title_info)
  if counter is 0:
    print("No results found.")

def main(argv):
  parser = argparse.ArgumentParser(
    description="Checks references file for mismatches with transcripts, identifies correct indices, and shifts indices.")
  subparsers = parser.add_subparsers(
    description="command", required=True)
  parser_audit = subparsers.add_parser("audit",
    help="list all mismatches",
    description="List mismatches between references and transcripts for given episodes. If no epCode is given, all episodes will be checked.")
  parser_audit.add_argument("epCode",
    help="episode code, e.g. s01e01 for season 1 episode 1",
    type=epCodeType,
    nargs="*")
  parser_audit.set_defaults(func=audit)
  parser_fix = subparsers.add_parser("fix",
    help="fix first mismatch",
    description="Fix first mismatch found. Interactive interface to confirm indices shifts.")
  parser_fix.add_argument("epCode",
    help="episode code, e.g. s01e01 for season 1 episode 1",
    type=epCodeType,
    nargs="*")
  parser_fix.set_defaults(func=fix)
  parser_find = subparsers.add_parser("find",
    help="find indices of search string",
    description="Get list of indices for all matches of a search string in an episode. Helpful for a manual indices fix.")
  parser_find.add_argument("epCode",
    help="episode code, e.g. s01e01 for season 1 episode 1",
    type=epCodeType)
  parser_find.add_argument("search",
    help="search string in quotes")
  parser_find.set_defaults(func=find)
  args = parser.parse_args(argv[1:]) if len(argv) > 1 else parser.parse_args(argv)
  args.func(args)

if __name__ == "__main__":
  main(sys.argv)