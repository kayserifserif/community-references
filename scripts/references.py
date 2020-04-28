from references import *

import sys

def main():
  if len(sys.argv) >= 2 and sys.argv[1] == "add":
    add.main()
  elif len(sys.argv) >= 2 and sys.argv[1] == "explore":
    explore.main(sys.argv[1:])
  elif len(sys.argv) >= 2 and sys.argv[1] == "indices":
    indices.main(sys.argv[1:])
  elif len(sys.argv) >= 2 and sys.argv[1] == "updateReferents":
    updateReferents.main()
  else:
    print("usage: add | explore | indices | updateReferents\n\
  add: add reference through interactive interface\n\
  explore: generate summary statistics\n\
  indices: manage indices\n\
  updateReferents: generate referents file from references file")

if __name__ == "__main__":
  main()