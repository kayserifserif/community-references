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

all_people = {}
all_titles = {}

def loadData():
  with open("./data/name.basics.min.tsv", newline='') as f_open:
    f_open = csv.reader(f_open, delimiter='\t')
    next(f_open) # skip header
    for row in f_open:
      # all_people.append(row[1]) # add name
      nconst = row[0]
      birthYear = row[2]
      try:
        birthYear = int(birthYear)
      except ValueError:
        birthYear = birthYear
      deathYear = row[3]
      try:
        deathYear = int(deathYear)
      except ValueError:
        deathYear = deathYear
      professions = row[4].split(",")
      knownFor = row[5].split(",")
      all_people[row[1]] = [nconst, birthYear, deathYear, professions, knownFor]

  with open("./data/title.basics.min.tsv", newline='') as f_open:
    f_open = csv.reader(f_open, delimiter='\t')
    next(f_open) # skip header
    for row in f_open:
      # all_titles.append(row[2]) # add name
      tconst = row[0]
      titleType = row[1]
      startYear = row[5]
      try:
        startYear = int(startYear)
      except ValueError:
        startYear = startYear
      endYear = row[6]
      try:
        endYear = int(endYear)
      except ValueError:
        endYear = endYear
      genres = row[8].split(",")
      all_titles[row[2]] = [tconst, titleType, startYear, endYear, genres]

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

  loadData()

  ep_data = {}

  try:

    data = ""

    with open("./transcripts/" + code + ".txt", "r") as f_open:
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
          ent_info = {}
          reference_info = {
            "entity": ent.text,
            "sentence": ent.sent.text,
            "startIndex": ent.start_char,
            "endIndex": ent.end_char
          }
          ent_info["reference"] = reference_info
          if ent.text in all_people:
            person_info = {
              "name": ent.text,
              "nconst": all_people[ent.text][0],
              "birthYear": all_people[ent.text][1],
              "deathYear": all_people[ent.text][2]
            }
            ent_info["referent"] = person_info
            people.append(ent_info)
          elif ent.text in all_titles:
            title_info = {
              "title": ent.text,
              "tconst": all_titles[ent.text][0],
              "titleType": all_titles[ent.text][1],
              "startYear": all_titles[ent.text][2],
              "endYear": all_titles[ent.text][3],
              "genres": all_titles[ent.text][4]
            }
            ent_info["referent"] = title_info
            titles.append(ent_info)

    ep_data["people"] = people
    ep_data["titles"] = titles

  except IOError:
    print("Could not read file.")

  return ep_data, text



# # # # # # # # # # #
# FIND SEARCH STRING #
# # # # # # # # # # #

def find(code, search, type):
  if type:
    loadData()
  try:
    with open("./transcripts/" + code + ".txt", "r") as f_open:
      data = f_open.read()
      data = re.sub("\n", " ", data)
    results = re.finditer(search, data)
    counter = 0
    for result in results:
      counter += 1
      print(result.start(), result.end())
      print(data[result.start() - 20 : result.end() + 20])
    if type == "p":
      if search in all_people:
        person_info = all_people[search].copy()
        person_info.insert(0, search)
        print(person_info)
    elif type == "t":
      if search in all_titles:
        title_info = all_titles[search].copy()
        title_info.insert(0, search)
        print(title_info)
    if counter is 0:
      print("No results found.")
  except IOError:
    print("Could not read file.")



# # # # # # # # # # #
# RESPOND TO INPUT #
# # # # # # # # # #
def main():
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
        with open("./transcripts/" + code + ".txt", "r") as f_open:
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
    # episode_list = ["s01e01"]

    # get data for all episodes in list
    episode_data = {}
    for ep in episode_list:
      # episode_data[ep] = get_episode_data(ep)
      episode_data[ep] = get_episode_data(ep)[0]

    # write data to json file
    try:
      j = json.dumps(episode_data, indent=2)
      # print(j)
      with open("./output/all.json", "w") as f:
        print(j, file=f)
        print("Successfully saved to file ./output/all.json!")
    except IOError:
      print("Could not write to file.")

  elif len(sys.argv) is 3:
    find(sys.argv[1], sys.argv[2], None)

  elif len(sys.argv) is 4:
    find(sys.argv[1], sys.argv[2], sys.argv[3])

  else:
    print("usage:\n\
  commands:\n\
    [episodeCode]\n\
    [episodeCode] [searchString] [entityType]\n\
    all\n\
  arguments:\n\
    [episodeCode]: code of episode to analyse, in the form of s01e01\n\
    [searchString]: string to search for, in quotes\n\
    [entityType]: expected entity type, as t for title or p for person")

if __name__ == "__main__":
  main()