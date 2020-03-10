import sys
from os import listdir
from os.path import isfile, join
import json
import re
import html

def makeAnnotations(epCode):
  # get transcript for this episode
  with open("./transcripts/community-" + epCode + ".txt", "r") as f:
    transcript = f.read()
  # get all references
  with open("./output/references.json", "r") as f:
    references = json.load(f)
    epRefs = references[epCode]
  # set up lines
  lines = ""
  # collect all indices
  indices = []
  for refType in epRefs:
    for instance in epRefs[refType]:
      reference = instance["reference"]
      indices.append([
        reference["startIndex"], reference["endIndex"], reference["entity"]
      ])
  indices = sorted(indices)
  # if there are any references
  if len(indices) > 0:
    # add the transcript up until the first reference
    lines += transcript[:indices[0][0]]
    # wrap the reference and add it
    for i, indexSet in enumerate(indices):
      lines += "<span class=\"reference\">" + indexSet[2] + "</span>"
      # continue adding the transcript up until the next reference
      end = indexSet[1]
      if (i is not (len(indices) - 1)):
        newStart = indices[i+1][0]
        lines += transcript[end:newStart]
      else:
        lines += transcript[end:]
  # if there are no references
  else:
    lines += transcript
  # wrap lines in p tags
  lines = re.sub(r'^', "<p>", lines, flags=re.MULTILINE)
  lines = re.sub(r'$', "</p>", lines, flags=re.MULTILINE)
  # set up html
  html = "<!DOCTYPE html>\n<html lang=\"en\">\n"
  head = "<head>\n" \
       + "<meta charset=\"UTF-8\">\n"\
       + "<style>\n" \
       + "body {{ line-height: 1.5; font-family: sans-serif }}\n" \
       + ".nav {{ display: flex; justify-content: center; text-align: center; width: 200px; margin: auto; }}\n" \
       + ".nav a:first-of-type {{ margin-right: 1em }}\n" \
       + "#title {{ text-align: center }}\n" \
       + "#transcript {{ width: 60%; margin: 100px auto; }}\n" \
       + ".reference {{ display: inline-block; padding: 0.2em 0.5em; background-color: #c0eeee }}\n" \
       + "</style>\n" \
       + "</head>\n"
  html += head
  body = "<body>\n"
  nav = "<nav class=\"nav\">"
  # print(epCodes.index(epCode))
  index = epCodes.index(epCode)
  if index > 0:
    prevCode = epCodes[index - 1]
    nav += "<a href=\"community-" + prevCode + ".html\">← " + prevCode.upper() + "</a>"
  if index < len(epCodes) - 1:
    nextCode = epCodes[index + 1]
    nav += "<a href=\"community-" + nextCode + ".html\">" + nextCode.upper() + " →</a>"
  nav += "</nav>\n"
  body += nav
  title = "<h1 id=\"title\">" + epCode.upper() + "</h1>\n"
  body += title
  body += "<div id=\"transcript\">\n"
  body += lines
  body += "\n</div>\n"
  body += nav
  body += "</body>\n"
  html += body
  html += "</html>"
  # output html file
  with open("./annotated/community-" + epCode + ".html", "w") as f:
    f.write(html.format(htmlText=html))

def main():
  global epCodes
  epCodes = sorted([f[10:16] for f in listdir("./transcripts") if isfile(join("./transcripts", f))])[1:]
  if len(sys.argv) is 2 and re.match(r"s\d\de\d\d", sys.argv[1]):
    makeAnnotations(sys.argv[1])
  elif len(sys.argv) is 2 and re.match("all", sys.argv[1]):
    for epCode in epCodes:
      makeAnnotations(epCode)
  else:
    print("usage: \n\
          \t [searchString]: string to search for, in quotes")

if __name__ == "__main__":
  main()