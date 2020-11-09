import json
import requests
from bs4 import BeautifulSoup
import sys

def get_existing_eps():
  file = "db/community/episodes.json"
  try:
    with open(file) as f:
      epData = json.load(f)
    return epData
  except IOError:
    print(f"Could not open file {file}.")
    return

def get_ep_details(episodes):
  for ep_code in episodes:
    tconst = episodes[ep_code]["tconst"]
    
    # get jsonLD (linked data) from imdb page
    ep_url = "https://www.imdb.com/title/" + tconst
    ep_soup = BeautifulSoup(requests.get(ep_url).text, features="html.parser") # parse page
    jsonLD = json.loads(ep_soup.select_one("script[type='application/ld+json']").contents[0])

    # title
    episodes[ep_code]["title"] = jsonLD["name"]
    # image
    episodes[ep_code]["image"] = jsonLD["image"]
    # description
    description = ep_soup.select_one("meta[name='description']")["content"]
    episodes[ep_code]["description"] = ". ".join(description.split(". ")[2:])
    # date
    episodes[ep_code]["date"] = jsonLD["datePublished"]
    # ratings
    episodes[ep_code]["ratings"] = jsonLD["aggregateRating"]
    episodes[ep_code]["ratings"].pop("@type")
    # writers
    episodes[ep_code]["writers"] = []
    for creator in jsonLD["creator"]:
      if creator["@type"] == "Person":
        creator.pop("@type")
        creator["nconst"] = creator["url"][6:-1]
        creator.pop("url")
        if creator not in episodes[ep_code]["writers"]:
          episodes[ep_code]["writers"].append(creator)

    print(json.dumps(episodes[ep_code], indent=2))
  
  return episodes

def write(episodes):
  file = "./db/community/episodes_new.json"
  try:
    j = json.dumps(episodes, indent=2)
    with open(file, "w") as f:
      print(j, file=f)
      print(f"Successfully saved to file {file}!")
  except IOError:
    print(f"Could not write to file {file}.")

def scrape():
  existing_eps = get_existing_eps()
  updated_eps = get_ep_details(existing_eps)
  write(updated_eps)

def main(argv):
  if len(sys.argv) == 2 and sys.argv[1] == "scrape":
    scrape()
  else:
    print("usage: scrape\n\
      scrape: scrape IMDb for episode data and save to episodes.json")

if __name__ == "__main__":
  main(sys.argv)