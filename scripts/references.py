from references import *

import sys

def main():
  if len(sys.argv) >= 2 and sys.argv[1] == "add":
    add.main()
  elif len(sys.argv) >= 2 and sys.argv[1] == "analyse":
    analyse.main(sys.argv[1:])
  elif len(sys.argv) >= 2 and sys.argv[1] == "check":
    check.main(sys.argv[1:])
  elif len(sys.argv) >= 2 and sys.argv[1] == "extract":
    extract.main(sys.argv[1:])
  elif len(sys.argv) >= 2 and sys.argv[1] == "updateReferents":
    updateReferents.main()
  elif len(sys.argv) >= 2 and sys.argv[1] == "shift":
    shift.main(sys.argv[1:])
  else:
    print("usage: add | analyse | check | extract | updateReferents | shift\n\
  add: add reference through interactive interface\n\
  analyse: generate summary statistics\n\
  check: check indices of references for mismatches\n\
  extract: extract references from transcripts\n\
  updateReferents: generate referents file from references file\n\
  shift: shift indices to correct")

if __name__ == "__main__":
  main()