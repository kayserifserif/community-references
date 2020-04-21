import sys
from os import listdir, makedirs
from os import path
import json
import re
import html
from bs4 import BeautifulSoup

def makeAnnotations(epCode, epCodes):
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
  for instance in epRefs["people"]:
    reference = instance["reference"]
    referent = instance["referent"]
    indices.append([
      reference["startInDoc"],
      reference["endInDoc"],
      reference["entity"],
      "people",
      referent["name"],
      referent["nconst"],
      referent["birthYear"],
      referent["deathYear"],
      referent["professions"],
      referent["knownFor"]
    ])
  for instance in epRefs["titles"]:
    reference = instance["reference"]
    referent = instance["referent"]
    indices.append([
      reference["startInDoc"],
      reference["endInDoc"],
      reference["entity"],
      "titles",
      referent["title"],
      referent["tconst"],
      referent["titleType"],
      referent["startYear"],
      referent["endYear"],
      referent["genres"]
    ])
  indices = sorted(indices)
  # if there are any references
  if len(indices) > 0:
    # add the transcript up until the first reference
    lines += transcript[:indices[0][0]]
    # wrap the reference and add it
    for i, indexSet in enumerate(indices):
      ref = "<span class='ref'>"
      reference = f"<span class='reference {indexSet[3]}'>{indexSet[2]}</span>";
      ref += reference
      popup = "<span class='popup'>"
      label = "<span class='label'>"
      if indexSet[3] == "people":
        label += f"<a href='https://www.imdb.com/name/{indexSet[5]}'>{indexSet[4]}</a></span>"
      else:
        label += f"<a href='https://www.imdb.com/title/{indexSet[5]}'>{indexSet[4]}</a></span>"
      popup += label
      if indexSet[3] == "titles":
        popup += f"<span class='titleType'>{indexSet[6]}</span>"
      years = "<span class='years'>"
      if indexSet[3] == "people":
        if indexSet[6] != "\\N":
          years += str(indexSet[6])
        years += "&ndash;"
        if indexSet[7] != "\\N":
          years += str(indexSet[7])
      else:
        if indexSet[7] != "\\N":
          years += str(indexSet[7])
        years += "&ndash;"
        if indexSet[8] != "\\N":
          years += str(indexSet[8])
      years += "</span>"
      popup += years
      if indexSet[3] == "people":
        professions = "<span class='profs list'>"
        for p in indexSet[8]:
          professions += f"<span class='tag prof'>{p}</span>"
        professions += "</span>"
        popup += professions
        knownFor = "<span class='knownFor list'>"
        for k in indexSet[9]:
          knownFor += f"<span class='tag knownFor'><a href='https://www.imdb.com/title/{k}'>{k}</a></span>"
        knownFor += "</span>"
        popup += knownFor
      if indexSet[3] == "titles":
        genres = "<span class='genres list'>"
        for g in indexSet[9]:
          genres += f"<span class='tag genre'>{g}</span>"
        genres += "</span>"
        popup += genres
      popup += "</span>"
      ref += popup
      ref += "</span>"
      lines += ref
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
  html = "<!DOCTYPE html>\n<html lang='en'>\n"
  head = "<head>\n" \
       + "<meta charset='UTF-8'>\n" \
       + "<link rel='stylesheet' href='../../assets/styles.css'>\n" \
       + "</head>\n"
  html += head
  body = "<body>\n"
  nav = "<nav class='nav'>"
  # print(epCodes.index(epCode))
  index = epCodes.index(epCode)
  if index > 0:
    # previous
    prevCode = epCodes[index - 1]
    nav += f"<a href='{prevCode}.html'>← {prevCode.upper()}</a>"
  if index < len(epCodes) - 1:
    # next
    nextCode = epCodes[index + 1]
    nav += f"<a href='{nextCode}.html'>{nextCode.upper()} →</a>"
  nav += "</nav>\n"
  body += nav
  title = f"<h1 id='title'>{epCode.upper()}</h1>\n"
  body += title
  body += "<div id='transcript'>\n"
  body += lines
  body += "\n</div>\n"
  body += nav
  body += "<script src='../../assets/scripts.js'></script>"
  body += "</body>\n"
  html += body
  html += "</html>"
  # output html file
  newDir = "./site/byEpisode/ep/" + epCode
  if not path.exists(newDir):
    makedirs(newDir)
  newFile = newDir + "/index.html"
  with open(newFile, "w") as f:
    f.write(html.format(htmlText=html))
    print(f"Successfully saved {epCode} to file {newFile}!")

def updateIndex(epCodes):
  indexFile = "./site/byEpisode/index.html"
  with open(indexFile, "r") as f:
    soup = BeautifulSoup(f, "html.parser")
  for epCode in epCodes:
    season = epCode[:3]
    seasonList = soup.find(id=season).ul
    epItem = soup.new_tag("li")
    epLink = soup.new_tag("a", href="ep/" + epCode)
    epLink.string = epCode
    epItem.append(epLink)
    seasonList.append(epItem)
  soup.prettify()
  with open(indexFile, "w") as f:
    f.write(str(soup))
    print(f"Successfully updated index {indexFile}!")

def main():
  epCodes = sorted([f[10:16] for f in listdir("./transcripts") if path.isfile(path.join("./transcripts", f))])[1:]
  if len(sys.argv) is 2 and re.match(r"s\d\de\d\d", sys.argv[1]):
    makeAnnotations(sys.argv[1], epCodes)
    updateIndex(epCodes)
  elif len(sys.argv) is 2 and sys.argv[1] == "all":
    for epCode in epCodes:
      makeAnnotations(epCode, epCodes)
  else:
    print("usage: \n\
  [epCode]: episode to annotate\n\
  all: annotate all episodes")

if __name__ == "__main__":
  main()