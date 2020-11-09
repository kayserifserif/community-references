from PyInquirer import prompt

from os import listdir
from os.path import isfile, join

import json

import re

def getReferences() -> dict:
  file = "./data/community/references.json"
  try:
    with open(file, "r") as f:
      references = json.load(f)
    return references
  except IOError:
    print(f"Could not open {file}.")
    return

def getTranscript(epCode: str) -> str:
  try:
    file = "./transcripts/community/" + epCode + ".txt"
    with open(file, "r") as f:
      transcript = f.read()
    return transcript
  except IOError:
    print(f"Could not read {file}.")
    return

def getEpMismatches(references: dict, transcript: str, epCode: str = None) -> list:
  epMismatches = []
  for instance in references[epCode]:
    reference = instance["reference"]
    actual = transcript[reference["startInDoc"]:reference["endInDoc"]]
    if actual != reference["entity"]:
      reference["actual"] = actual
      epMismatches.append(reference)
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

def getNewIndices(ref, matches, run=False):
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
  if not run:
    confirm = prompt({"type": "confirm", "name": "confirm", "message": "Shift to closest match?"})
  else:
    confirm = {"confirm": True}  
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

def shift(references: dict, transcript: str, epCode: str, orig: dict, shift: tuple):
  origPos = (orig["startInDoc"], orig["endInDoc"])
  posDiff = shift[0] - origPos[0]
  lenDiff = abs((shift[1] - shift[0]) - (origPos[1] - origPos[0]))
  epRefs = references[epCode]
  if lenDiff == 0:
    print("Difference in position.")
    print(f"Shifting {epCode} references {posDiff} characters if occurring at index {origPos[0]} or after...")
    for ref in epRefs:
      reference = ref["reference"]
      startInDoc = reference["startInDoc"]
      endInDoc = reference["endInDoc"]
      if startInDoc >= origPos[0]:
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
        reference.pop("actual", None)
  else:
    print("Difference in length.")
    print(f"Resetting {epCode} indices {origPos} to {shift}...")
    found = False
    if not found:
      for ref in epRefs:
        reference = ref["reference"]
        if reference["startInDoc"] == origPos[0] and reference["entity"] == orig["entity"]:
          reference["startInDoc"] = shift[0]
          reference["endInDoc"] = shift[1]
          reference.pop("actual", None)
  writeReferences(references)

def writeReferences(references: dict):
  fileName = "./data/community/references.json"
  try:
    j = json.dumps(references, indent=2)
    with open(fileName, "w") as f:
      print(j, file=f)
      print()
      print(f"Successfully saved to file {fileName}!")
      print()
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
    epCodes = sorted([f[:-4] for f in listdir("./transcripts/community/") if isfile(join("./transcripts/community/", f))])[1:]

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

  if args.all:
    print()
    print("Mismatches:")
    for ep in mismatches:
      print(ep)
      for error in mismatches[ep]:
        print(error)
      print()
  else:
    print()
    print("First mismatch:")
    ep = list(mismatches.keys())[0]
    print(ep)
    print(mismatches[ep][0])
    print()

# def fixFirstError():
  # return

def fix(args):
  epCodes = []
  if len(args.epCode) > 0:
    epCodes = args.epCode
  else:
    epCodes = sorted([f[:-4] for f in listdir("./transcripts/community/") if isfile(join("./transcripts/community/", f))])[1:]

  if not args.run:

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
    sentence = firstError["sentence"][:firstError["startInSent"]] + "[" + firstError["entity"] + "]" + firstError["sentence"][firstError["endInSent"]:]
    print("Expected \"" +
      firstError["entity"] + "\" in \"" +
      sentence + "\" at indices " +
      str(firstError["startInDoc"]) + "-" + str(firstError["endInDoc"]) + ", but found \"" +
      firstError["actual"].encode("unicode_escape").decode("utf-8") + "\" instead.")
    results = getMatches(transcripts[firstEp], firstError["entity"])
    shifted = getNewIndices(firstError, results, run=False)
    original = (firstError["startInDoc"], firstError["endInDoc"])
    print(original, shifted)
    print()
    shift(references, transcripts[firstEp], firstEp, firstError, shifted)
  
  else:

    references = getReferences()
    for epCode in epCodes:
      transcripts = {epCode: getTranscript(epCode)}
      epMismatches = getEpMismatches(references, transcripts[epCode], epCode)

      while epMismatches:
        firstError = epMismatches[0]
        print()
        sentence = firstError["sentence"][:firstError["startInSent"]] + "[" + firstError["entity"] + "]" + firstError["sentence"][firstError["endInSent"]:]
        print("Expected \"" +
          firstError["entity"] + "\" in \"" +
          sentence + "\" at indices " +
          str(firstError["startInDoc"]) + "-" + str(firstError["endInDoc"]) + ", but found \"" +
          firstError["actual"].encode("unicode_escape").decode("utf-8") + "\" instead.")
        results = getMatches(transcripts[epCode], firstError["entity"])
        shifted = getNewIndices(firstError, results, run=True)
        original = (firstError["startInDoc"], firstError["endInDoc"])
        print(original, shifted)
        print()
        shift(references, transcripts[epCode], epCode, firstError, shifted)
        references = getReferences()
        epMismatches = getEpMismatches(references, transcripts[epCode], epCode)
      
      if not epMismatches:
        print(f"All indices match up for {epCode}!")

def find(args):
  transcript = getTranscript(args.epCode)
  results = re.finditer(args.search, transcript)
  counter = 0
  for result in results:
    counter += 1
    context = transcript[result.start() - 20 : result.end() + 20].encode("unicode_escape").decode("utf-8")
    print(result.start(), result.end(), context)
  if counter is 0:
    print("No results found.")
