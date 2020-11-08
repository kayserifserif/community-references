import sys
from os import listdir
from os.path import isfile, join
import json
import re
# from videogrep import videogrep
import pyperclip

videos_dir = "./video"
season_dir = "Community.S{}.Season.{}.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed"
episode_file = "Community.S{}E{}.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed.mkv"

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

def makeVideo(inputPath, searchStr, outputPath):
  videogrep(inputPath, outputPath, searchStr, "re")

def main(argv):
  if len(argv) > 1:
    searchStr = compileRefs(argv[1])
    pyperclip.copy(searchStr)
    print("Copied to clipboard!")
    # season = argv[1][1:3]
    # if re.match(r"s\d{2}e\d{2}", argv[1]):
    #   episode = argv[1][4:6]
    #   inputPath = videos_dir + "/" + season_dir.format(season, season[1]) + "/" + episode_file.format(season, episode)
    # elif re.match(r"s\d{2}", argv[1]):
    #   inputPath = videos_dir + "/" + season_dir.format(season, season[1])
    # print(inputPath)
    # inputPath = f"{argv[1]}.srt"
    # outputPath = argv[1] + ".mp4"
    # print(inputPath)
    # makeVideo(inputPath, searchStr, outputPath)
  else:
    print("usage: [season|episode]\n\
  season: s01 for season 1\n\
  episode: s01e01 for season 1 episode 1")
  # videogrep('path/to/your/files','output_file_name.mp4', 'search_term', 'search_type')

if __name__ == "__main__":
  main(sys.argv)