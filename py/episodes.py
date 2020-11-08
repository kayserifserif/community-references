from os import listdir
from os.path import isfile, join
import csv
import json
import requests
from bs4 import BeautifulSoup
import re
import sys

file = "./data/community/episodes.json"

def getEpData():
  try:
    with open(file) as f:
      epData = json.load(f)
    return epData
  except IOError:
    print(f"Could not open file {file}.")
    return

def getEpConsts():
  epCodes = sorted([f[:-4] for f in listdir("./transcripts") if isfile(join("./transcripts", f))])[1:]
  showTconst = "tt1439629"
  tconsts = {}
  try:
    with open("./db/title.episode.tsv", "r") as f:
      reader = csv.DictReader(f, dialect="excel-tab")
      counter = 0
      for row in reader:
        counter += 1
        if len(tconsts) > len(epCodes):
          continue
        if row["parentTconst"] == showTconst:
          season = int(row["seasonNumber"])
          season = "{:02}".format(season)
          episode = int(row["episodeNumber"])
          episode = "{:02}".format(episode)
          epCode = "s" + season + "e" + episode
          tconsts[epCode] = {"tconst": row["tconst"]}
    return tconsts
  except IOError:
    print(f"Could not open {file}.")
    return

def getEpPages(episodes):
  for epCode in episodes:
    print(epCode)
    
    plotUrl = "https://www.imdb.com/title/" + episodes[epCode]["tconst"] + "/plotsummary"
    plotRequest = requests.get(plotUrl)
    plotSoup = BeautifulSoup(plotRequest.text, features="html.parser") # parse page
    description = plotSoup.find(id="plot-summaries-content").find("p").get_text().strip()
    episodes[epCode]["description"] = description

    creditsUrl = "https://www.imdb.com/title/" + episodes[epCode]["tconst"] + "/fullcredits"
    creditsRequest = requests.get(creditsUrl)
    creditsSoup = BeautifulSoup(creditsRequest.text, features="html.parser")
    table = creditsSoup.findAll("table")[1]
    rows = table.findAll("tr")
    writers = []
    for row in rows:
      tds = row.findAll("td")
      if len(tds) == 3:
        nameA = tds[0].find("a")
        creditTd = tds[2]
        name = nameA.get_text().strip()
        nconst = nameA["href"].split("/")[2]
        credit = re.compile("[()]").split(creditTd.get_text().strip())[1]
        writer = {
          "name": name,
          "nconst": nconst,
          "credit": credit
        }
        if writer not in writers:
          writers.append(writer)
    episodes[epCode]["writers"] = writers
  
  return episodes

def write(episodes):
  file = "./data/community/episodes.json"
  try:
    j = json.dumps(episodes, indent=2)
    with open(file, "w") as f:
      print(j, file=f)
      print(f"Successfully saved to file {file}!")
  except IOError:
    print(f"Could not write to file {file}.")

def scrape():
  # tconsts = getEpConsts()
  existingEps = getEpData()
  newEps = getEpPages(existingEps)
  # write(newEps)

def main(argv):
  if len(sys.argv) == 2 and sys.argv[1] == "scrape":
    scrape()
  else:
    print("usage: scrape\n\
      scrape: scrape IMDb for episode data and save to episodes.json")

if __name__ == "__main__":
  main(sys.argv)