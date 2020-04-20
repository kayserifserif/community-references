import requests
from bs4 import BeautifulSoup
import re

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
  with open("./scrape/community-" + code + ".txt", "w") as output:
    output.write(script)