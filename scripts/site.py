from references import *

import sys

def main():
  if len(sys.argv) is 2 and sys.argv[1] == "annotate":
    annotate.main()
  elif len(sys.argv) is 2 and sys.argv[1] == "top":
    top.main()
  else:
    print("usage: analyse | annotate | top\n\
  annotate: generate annotated transcripts\n\
  top: generate charts for episodes with the most references")

if __name__ == "__main__":
  main()