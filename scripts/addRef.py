import sys
import json
import re

def getReferences():
  references = {}
  with open("./output/references.json", "r") as f:
    references = json.load(f)
  return references

def getReferents():
  referents = {}
  with open("./output/referents.json", "r") as f:
    referents = json.load(f)
  return referents

def addRef(epCode, entity, start, end, const):
  references = getReferences()
  referents = getReferents()
  details = None
  if len(const) == 9:
    for refType in referents:
      for refName in referents[refType]:
        ref = referents[refType][refName]
        if refType == "people":
          typeConst = "nconst"
        else:
          typeConst = "tconst"
        if (ref["details"][typeConst] == const):
          details = ref["details"]
  newRef = {}
  newRef["reference"] = {
    "entity": entity,
    "sentence": "",
    "startInDoc": start,
    "endInDoc": end,
    "startInSent": "\\N",
    "endInSent": "\\N"
  }
  if details:
    newRef["referent"] = details
  else:
    print("Referent not given or not found.")
    if const == "p":
      newRef["referent"] = {
        "name": "",
        "nconst": "",
        "birthYear": "\\N",
        "deathYear": "\\N",
        "professions": [],
        "knownFor": []
      }
    else:
      newRef["referent"] = {
        "title": "",
        "tconst": "",
        "titleType": "",
        "startYear": "\\N",
        "endYear": "\\N",
        "genres": []
      }
  print(newRef)
  if const == "p" or (details and "nconst" in details):
    references[epCode]["people"].append(newRef)
    references[epCode]["people"] = sorted(references[epCode]["people"], key=lambda x: x["reference"]["startInDoc"])
  else:
    references[epCode]["titles"].append(newRef)
    references[epCode]["titles"] = sorted(references[epCode]["titles"], key=lambda x: x["reference"]["startInDoc"])

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
  if len(sys.argv) is 6 and re.match(r"s\d\de\d\d", sys.argv[1]) and sys.argv[3].isdigit() and sys.argv[4].isdigit():
    addRef(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])

  else:

    print("usage:\n\
  commands:\n\
    [episodeCode] [entity] [start] [end] [const | entityType]\n\
  arguments:\n\
    [episodeCode]: code of episode to analyse, in the form of s01e01\n\
    [entity]: reference entity, in quotes\n\
    [start]: starting index in transcript\n\
    [end]: ending index in transcript\n\
    [const | entityType]: IMDb nconst for person or tconst for title OR p for person or t for title")

if __name__ == "__main__":
  main()