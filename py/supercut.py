from videogrep import videogrep
import sys
import re
import json
from os import listdir
from os.path import isfile, join

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
  for ref in references[code]:
    entity = re.escape(ref["reference"]["entity"])
    search.add(entity)
  return search

def compileRefs(code):
  references = getReferences()
  search = set()
  if re.match(r"s\d{2}e\d{2}", code):
    search = search | compileRefsSet(references, code)
  elif re.match(r"s\d{2}", code):
    epCodes = sorted([f[:-4] for f in listdir("transcripts/community/") if isfile(join("transcripts/community/", f)) and code in f])[1:]
    for epCode in epCodes:
      search = search | compileRefsSet(references, epCode)
  else:
    return ""
  searchStr = "(" + "|".join(search) + ")"
  print(searchStr)
  return searchStr

def create_supercut(code):
  # inFiles
  inFiles = []
  path_temp = "video/community/{}/{}.mkv"
  if re.match(r"s\d{2}e\d{2}", code):
    path = path_temp.format(code[:3], code)
    if isfile(path):
      inFiles.append(path)
  elif re.match(r"s\d{2}", code):
    epCodes = sorted([f[:-4] for f in listdir("video/community/" + code) if isfile(join("video/community/" + code, f)) and code in f])[1:]
    for epCode in epCodes:
      path = path_temp.format(epCode[:3], epCode)
      if isfile(path):
        inFiles.append(path)
  if len(inFiles) == 0:
    return
  # outFile
  outFile = "video/supercuts/supercut-" + code + ".mp4"
  # search
  search = compileRefs(code)
  if not search:
    return
  # go!
  videogrep(inFiles, outFile, search, "re")

def main():
  if len(sys.argv) == 2:
    create_supercut(sys.argv[1])
  else:
    print("usage: \n\
  epCode: s01e01 for season 1 episode 1\n\
  season: s01 for all episodes in season 1")
    # print("usage: \n\
  # epCode: s01e01 for season 1 episode 1")

if __name__ == "__main__":
  main()