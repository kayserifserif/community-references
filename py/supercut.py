import sys
import re
import json
from videogrep import videogrep

def getReferences():
  file = "./data/community/references.json"
  try:
    with open(file) as f:
      references = json.load(f)
    return references
  except IOError:
    print(f"Could not read {file}.")
    return

def compileRefsSet(references, code):
  search = set()
  for refType in references[code]:
    for ref in references[code][refType]:
      entity = re.escape(ref["reference"]["entity"])
      search.add(entity)
  return search

def compileRefs(code):
  references = getReferences()
  search = set()
  if re.match(r"s\d{2}e\d{2}", code):
    search = search | compileRefsSet(references, code)
  elif re.match(r"s\d{2}", code):
    epCodes = sorted([f[:-4] for f in listdir("./transcripts") if isfile(join("./transcripts", f)) and code in f])[1:]
    for epCode in epCodes:
      search = search | compileRefsSet(references, epCode)
  searchStr = "(" + "|".join(search) + ")"
  print(searchStr)
  return searchStr

def create_supercut(epCode):
  epCode = epCode
  inFile = ["video/community/" + epCode[:3] + "/" + epCode + ".mkv"]
  search = compileRefs(epCode.lower())
  outFile = "video/supercuts/supercut-" + epCode + ".mp4"
  videogrep(inFile, outFile, search, "re")

def main():
  if len(sys.argv) == 2 and re.match(r"s\d{2}e\d{2}", sys.argv[1]):
    create_supercut(sys.argv[1])
  else:
    print("usage: \n\
  epCode: s01e01 for season 1 episode 1")

if __name__ == "__main__":
  main()