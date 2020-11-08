import sys
import re
from videogrep import videogrep

def create_supercut(epCode):
  epCode = epCode.upper()
  inFile = ["video/community/Community-" + epCode[:3] + "/Community-" + epCode + ".mkv"]
  search = "(Marty\\ McFly|Edward\\ Scissorhands|Ricardo\\ Montalban|Dolly\\ Parton|E\\.T\\.)"
  outFile = "video/supercuts/supercut-" + epCode + ".mp4"
  videogrep(inFile, outFile, search, "re")

def main():
  if len(sys.argv) == 2 and re.match(r"s\d{2}", sys.argv[1]):
    create_supercut(sys.argv[1])
  else:
    print("usage: \n\
  epCode: s01e01 for season 1 episode 1")

if __name__ == "__main__":
  main()