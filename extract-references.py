import csv
import spacy
from spacy import displacy
import sys
import re
import json



# # # # # # # # # # #
# VARIABLES AND DATA #
# # # # # # # # # # #

# desired_labels = ["PERSON", "WORK_OF_ART", "ORG", "FAC"]
desired_labels = ["PERSON", "WORK_OF_ART", "ORG"]

all_people = []
with open("./data/name.basics.min.tsv", newline='') as f_open:
  f_open = csv.reader(f_open, delimiter='\t')
  next(f_open) # skip header
  for row in f_open:
    all_people.append(row[1]) # add name

all_titles = []
with open("./data/title.basics.min.tsv", newline='') as f_open:
  f_open = csv.reader(f_open, delimiter='\t')
  next(f_open) # skip header
  for row in f_open:
    all_titles.append(row[2]) # add name

stop_ents = []
with open("./data/community-entities.txt", "r") as f_open:
  f_open = csv.reader(f_open, delimiter='\n')
  for row in f_open:
    stop_ents.append(row[0])

nlp = spacy.load("en_core_web_sm")



# # # # # # # # # #
# GET EPISODE DATA #
# # # # # # # # # #

def get_episode_data(code):

  ep_data = {}

  try:

    data = ""

    with open("./transcripts/community-" + code + ".txt", "r") as f_open:
      data = f_open.read()
      data = re.sub("\n", " ", data)

    print("Generating results for " + code + "...")

    text = nlp(data)

    people = []
    titles = []

    # each recognised entity
    for ent in text.ents:
      # one of the desired labels
      if ent.label_ in desired_labels:
        # not names from the show
        if ent.text not in stop_ents:
          # either person or title
          if ent.text in all_people:
            people.append([ent.text, ent.sent])
          elif ent.text in all_titles:
            titles.append([ent.text, ent.sent])

    ep_data["people"] = people
    ep_data["titles"] = titles

  except IOError:
    print("Could not read file.")

  return ep_data, text



# # # # # # # # # #
# RESPOND TO INPUT #
# # # # # # # # # #

# get option from command line input
if len(sys.argv) is 2 and re.match(r"s\d\de\d\d", sys.argv[1]):

  results = get_episode_data(sys.argv[1])
  ep_data = results[0]
  text = results[1]
  print("people:", ep_data["people"])
  print("titles:", ep_data["titles"])
  displacy.serve(text, style="ent")

elif len(sys.argv) is 2 and sys.argv[1] == "all":

  # get list of all episode codes
  episode_list = []
  season = 1
  episode = 1
  s_valid = True
  while s_valid:
    try:
      code = "s" + "{:02}".format(season) + "e" + "{:02}".format(episode)
      # add episode code if file exists
      with open("./transcripts/community-" + code + ".txt", "r") as f_open:
        episode_list.append(code)
        episode += 1
    except IOError:
      if episode > 1:
        # go to next season
        season += 1
        episode = 1
      else:
        # assume no more episodes
        s_valid = False

  # get data for all episodes in list
  episode_data = {}
  for ep in episode_list:
    episode_data[ep] = get_episode_data(ep)

  # write data to json file
  try:
    j = json.dumps(episode_data, indent=2)
    with open("./output/all.json", "w") as f:
      print(j, file=f)
      print("Successfully saved to file ./output/all.json!")
  except IOError:
    print("Could not write to file.")

else:
  print("Usage: \"python extract-references.py\", followed by season-episode code (e.g. \"s01e01\") OR \"all\"")
