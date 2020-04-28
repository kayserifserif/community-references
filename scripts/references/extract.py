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
# desired_labels = ["PERSON", "WORK_OF_ART", "ORG"]

# all_people = {}
# all_titles = {}

def getNames():
  file = "./db/name.basics.min.tsv"
  try:
    with open(file, "r") as f:
      reader = csv.DictReader(f, dialect="excel-tab")
      # names = []
      names = {}
      print(f"Reading {file}...")
      for row in reader:
        newRow = {}
        # newRow["nconst"] = row["nconst"]
        newRow["name"] = row["name"]
        if row["birthYear"].isdigit():
          newRow["birthYear"] = int(row["birthYear"])
        else:
          newRow["birthYear"] = row["birthYear"]
        if row["deathYear"].isdigit():
          newRow["deathYear"] = int(row["deathYear"])
        else:
          newRow["deathYear"] = row["deathYear"]
        newRow["professions"] = row["professions"].split(",")
        newRow["knownFor"] = row["knownFor"].split(",")
        # names.append(newRow)
        names[row["nconst"]] = newRow
      return names
  except IOError:
    print(f"Could not open {file}.")
    return

def getTitles():
  file = "./db/title.basics.min.tsv"
  try:
    with open(file, "r") as f:
      reader = csv.DictReader(f, dialect="excel-tab")
      # titles = []
      titles = {}
      print(f"Reading {file}...")
      for row in reader:
        newRow = {}
        # newRow["tconst"] = row["tconst"]
        newRow["titleType"] = row["titleType"]
        newRow["title"] = row["title"]
        if row["startYear"].isdigit():
          newRow["startYear"] = int(row["startYear"])
        else:
          newRow["startYear"] = row["startYear"]
        if row["endYear"].isdigit():
          newRow["endYear"] = int(row["endYear"])
        else:
          newRow["endYear"] = row["endYear"]
        newRow["genres"] = row["genres"].split(",")
        # titles.append(newRow)
        titles[row["tconst"]] = newRow
      return titles
  except IOError:
    print(f"Could not open {file}.")
    return

def getRatings():
  file = "./db/title.ratings.min.tsv"
  try:
    with open(file, "r") as f:
      reader = csv.DictReader(f, dialect="excel-tab")
      # ratings = []
      ratings = {}
      print(f"Reading {file}...")
      for row in reader:
        newRow = {}
        # newRow["tconst"] = row["tconst"]
        newRow["averageRating"] = float(row["averageRating"])
        newRow["numVotes"] = int(row["numVotes"])
        # ratings.append(newRow)
        ratings[row["tconst"]] = newRow
      return ratings
  except IOError:
    print(f"Could not open {file}.")
    return

def getDictionary():
  file = "/usr/share/dict/words"
  try:
    with open(file) as f:
      dictionary = f.read().splitlines()
      return dictionary
  except IOError:
    print(f"Could not read {file}.")
    return

def getShowEnts():
  file = "./db/show_ents.txt"
  try:
    with open(file, "r") as f:
      transcript = f.read().splitlines()
      return transcript
  except IOError:
    print(f"Could not open {file}.")
    return

def getTranscript(code):
  file = f"./transcripts/{code}.txt"
  try:
    with open(file, "r") as f:
      transcript = f.read()
      return transcript
  except IOError:
    print(f"Could not open {file}.")
    return

def write(data, file):
  try:
    j = json.dumps(data, indent=2)
    with open(file, "w") as f:
      print(j, file=f)
      print(f"Successfully saved to {file}!")
  except IOError:
    print(f"Could not write to {file}.")


# # # # # # # # # # # # #
# GET EPISODE REFERENCES #
# # # # # # # # # # # # #

def isInNamesInstances(namesInstances, name):
  for nconst in namesInstances:
    nameToCheck = namesInstances[nconst][0][0]
    if name == nameToCheck or name == " ".join(nameToCheck.split(" ")[1:]):
      return True
  return False

def isFirstName(names, name):
  for nconst in names:
    if name == names[nconst]["name"].split(" ")[0]:
      return True
  return False

def getEpRefs(names, titles, ratings, dictionary, show_ents, nlp, code):

  print(f"Generating results for {code}...")

  transcript = getTranscript(code)
  if not transcript:
    return

  epRefs = {}

  namesInstances = {}
  punc = re.compile("[,.?!—'():;\"# ]")
  transcriptSplit = punc.split(transcript.replace("\n", " "))
  for nconst in names:
    nameFull = names[nconst]["name"]
    name = " ".join(punc.split(nameFull))
    nameFullSplit = nameFull.split(" ")
    nameSplit = name.split(" ")
    if len(nameSplit) > 1:
      surnameFull = " ".join(nameFullSplit[1:])
      surname = " ".join(nameSplit[1:])
      surnameSplit = surname.split(" ")
    const = int(nconst[2:])

    if nameFull in transcript and nameSplit[0] in transcriptSplit:
      # if nameFull in namesInstances:
      if isInNamesInstances(namesInstances, nameFull):
        continue
      if nameFull in show_ents:
        continue
      firstIndex = transcriptSplit.index(nameSplit[0])
      context = " ".join(transcriptSplit[firstIndex - 3 : firstIndex + len(nameSplit) + 3])
      if len(nameSplit) > 1: # name has first and last name
        if name == " ".join(transcriptSplit[firstIndex : firstIndex + len(nameSplit)]):
          print(nameFull, nconst)
          instances = re.finditer(name, transcript)
          for instance in instances:
            context = transcript[instance.start() - 20 : instance.end() + 20]
            if name in namesInstances:
              namesInstances[nconst].append([nameFull, context])
            else:
              namesInstances[nconst] = [[nameFull, context]]
            print("-", context.encode("unicode_escape").decode("utf-8"))
      else: # name is mononym
        if const < 100:
          print(nameFull, nconst)
          instances = re.finditer(name, transcript)
          for instance in instances:
            context = transcript[instance.start() - 20 : instance.end() + 20  ]
            if name in namesInstances:
              namesInstances[nconst].append([nameFull, context])
            else:
              namesInstances[nconst] = [[nameFull, context]]
            print("-", context.encode("unicode_escape").decode("utf-8"))
    elif surnameFull in transcript and surnameSplit[0] in transcriptSplit:
      if nconst == "nm1143053":
        print(surnameFull, nconst)
      if len(surnameFull) <= 3:
        continue
      if nlp.vocab[surnameFull.lower()].is_stop:
        continue
      if surnameFull in show_ents:
        continue
      if isInNamesInstances(namesInstances, surnameFull):
        continue
      firstIndex = transcriptSplit.index(surnameSplit[0])
      if surname == " ".join(transcriptSplit[firstIndex : firstIndex + len(surnameSplit)]):
        # if const < 1500 and surnameFull.lower() not in dictionary:
        if surnameFull not in dictionary and nlp(surnameFull)[0].lemma_ not in dictionary:
          print(surnameFull, nconst)
          instances = re.finditer(surname, transcript)
          for instance in instances:
            context = transcript[instance.start() - 20 : instance.end() + 20]
            if nconst in namesInstances:
              namesInstances[nconst].append([surnameFull, context])
            else:
              namesInstances[nconst] = [[surnameFull, context]]
            print("-", context.encode("unicode_escape").decode("utf-8"))
  
  # if surname is another first name in names database
  print("Checking commonness of surnames by matching with first names...")
  for nconst, v in list(namesInstances.items()):
    name = v[0][0]
    if len(name.split(" ")) < 2:
      if isFirstName(names, name):
        print(f"Removing {name}.")
        del namesInstances[nconst]

  # if total votes for of a person's all knownFor titles is above a threshold
  votesThreshold = 5000
  print(f"Checking popularity of names by checking if their total votes are over {votesThreshold}...")
  for nconst, v in list(namesInstances.items()):
    name = names[nconst]["name"]
    knownFor = names[nconst]["knownFor"]
    totalVotes = 0
    for tconst in knownFor:
      if tconst in ratings:
        totalVotes += ratings[tconst]["numVotes"]
    # print(name, totalVotes)
    threshold = 5000
    if totalVotes < threshold:
      print(f"Removing {name} ({totalVotes} total votes).")
      del namesInstances[nconst]

  print(namesInstances)

  # epNames = []
  # epTitles = []

  # displacy.serve(text, style="ent")
  
  # each recognised entity
  # for ent in text.ents:
    # print(ent.text, ent.label_)
    # # one of the desired labels
    # if ent.label_ in desired_labels:
    #   # not names from the show
    #   if ent.text not in stop_ents:
    #     # either person or title
    #     ent_info = {}
    #     reference_info = {
    #       "entity": ent.text,
    #       "sentence": ent.sent.text,
    #       "startIndex": ent.start_char,
    #       "endIndex": ent.end_char
    #     }
    #     ent_info["reference"] = reference_info
    #     if ent.text in all_people:
    #       person_info = {
    #         "name": ent.text,
    #         "nconst": all_people[ent.text][0],
    #         "birthYear": all_people[ent.text][1],
    #         "deathYear": all_people[ent.text][2]
    #       }
    #       ent_info["referent"] = person_info
    #       people.append(ent_info)
    #     elif ent.text in all_titles:
    #       title_info = {
    #         "title": ent.text,
    #         "tconst": all_titles[ent.text][0],
    #         "titleType": all_titles[ent.text][1],
    #         "startYear": all_titles[ent.text][2],
    #         "endYear": all_titles[ent.text][3],
    #         "genres": all_titles[ent.text][4]
    #       }
    #       ent_info["referent"] = title_info
    #       titles.append(ent_info)

  # ep_data["people"] = people
  # ep_data["titles"] = titles

  # return ep_data, text
  return epRefs



# # # # # # # # # # #
# RESPOND TO INPUT #
# # # # # # # # # #
def main(argv):
  # get option from command line input
  if len(sys.argv) is 2 and re.match(r"s\d\de\d\d", sys.argv[1]):

    names = getNames()
    titles = getTitles()
    ratings = getRatings()
    dictionary = getDictionary()
    show_ents = getShowEnts()
    nlp = spacy.load("en_core_web_sm")
    nlp.vocab[u"okay"].is_stop = True
    results = getEpRefs(names, titles, ratings,
      dictionary, show_ents, nlp,
      sys.argv[1])
    # ep_data = results[0]
    # text = results[1]
    # print("people:", ep_data["people"])
    # print("titles:", ep_data["titles"])
    # displacy.serve(text, style="ent")

  elif len(sys.argv) is 2 and sys.argv[1] == "all":

    # get list of all episode codes
    epCodes = sorted([f[:-4] for f in listdir("./transcripts") if isfile(join("./transcripts", f))])[1:]

    # get data for all episodes in list
    refs = {}
    for epCode in epCodes:
      refs[epCode] = getEpRefs(epCode)

    # write(epData, "./data/references1.json")

  else:
    print("usage:\n\
  commands:\n\
    [episodeCode]\n\
    all\n\
  arguments:\n\
    [episodeCode]: code of episode to analyse, in the form of s01e01")

if __name__ == "__main__":
  main(sys.argv)