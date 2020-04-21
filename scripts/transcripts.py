import requests
from bs4 import BeautifulSoup
import re
import os
import sys

def scrape():
  url = "https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=community"
  request = requests.get(url)
  soup = BeautifulSoup(request.text, features="html.parser") # parse page
  seasons = soup.find_all(class_="season-episodes") # find season divs
  all_episodes = []
  for season in seasons:
    # get links for each season
    season_episodes = season.find_all(class_="season-episode-title")
    for episode in season_episodes:
      all_episodes.append("https://www.springfieldspringfield.co.uk/" + episode["href"])
  # get page for each episode
  for episode in all_episodes:
    request = requests.get(episode)
    soup = BeautifulSoup(request.text, features="html.parser")
    code = re.findall(r"s\d\de\d\d", soup.h1.string)[0] # season-episode code
    # get script text
    text = soup.find(class_="scrolling-script-container")
    script = ""
    for string in text.strings:
      script += string.strip() + "\n"
    # write to file
    with open("./scrape/" + code + ".txt", "w") as output:
      output.write(script)

# def rename():
#   epCodes = sorted([f[10:16] for f in os.listdir("./transcripts") if os.path.isfile(os.path.join("./transcripts", f))])[1:]
#   for epCode in epCodes:
#     os.rename("./transcripts/community-" + epCode + ".txt", "./transcripts/" + epCode + ".txt")

def main():
  if len(sys.argv) is 2 and sys.argv[1] == "scrape":
    scrape()
  # elif len(sys.argv) is 2 and sys.argv[1] == "rename":
    # rename()
  else:
    print("usage: \n\
  scrape: scrape transcripts into scrape/\n\
  rename: rename transcripts from community-epCode to epCode")

if __name__ == "__main__":
  main()