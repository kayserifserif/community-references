import json
import matplotlib.pyplot as plt
from pprint import pprint

# import spacy
# from spacy.symbols import *
# from spacy import displacy

# # # #
# DATA #
# # # #

def get_references() -> dict:
  file = "./data/community/references.json"
  try:
    with open(file, "r") as f:
      references = json.load(f)
  except IOError:
    print(f"Could not read {file}.")
    return
  return references

def populate_referents(names = None, titles = None) -> dict:
  file = "./data/community/referents.json"
  try:
    with open(file, "r") as f:
      referents = json.load(f)
  except IOError:
    print(f"Could not read {file}.")
    return
  for nametitle in referents:
    ref = referents[nametitle]
    ref_type = ref["details"]["refType"]
    if ref_type == "name":
      if names != None:
        names[nametitle] = ref
    else:
      if titles != None:
        titles[nametitle] = ref
  return referents

def get_episodes() -> dict:
  file = "./db/community/episodes.json"
  try:
    with open(file, "r") as f:
      episodes = json.load(f)
  except IOError:
    print(f"Could not read {file}.")
    return
  return episodes

# # # # # #
# ANALYSIS #
# # # # # #

def total(data: dict) -> int:
  return len(list(data))

def top(data: dict, key = "count", num: int = 5) -> list:
  keys = list(data)
  lines = []
  for x in range(num):
    marker = str(x + 1) + ". "
    item = keys[x]
    count = data[item][key]
    lines.append(marker + item + " (" + str(count) + ")")
  return "\n".join(lines)

def top_count(counts_by_ep, count_type=""):
  top_count = 0
  top_count_ep = ""
  for ep_code in counts_by_ep:
    if not count_type:
      count = counts_by_ep[ep_code]["name"] + counts_by_ep[ep_code]["title"]
    else:
      count = counts_by_ep[ep_code][count_type]
    if count > top_count:
      top_count = count
      top_count_ep = ep_code
  return (top_count_ep, top_count)

def similes():
  return
  # nlp = spacy.load("en_core_web_sm")
  # sentence = references["s01e01"]["people"][0]["reference"]["sentence"]
  # sentence = "You're like Jodie Foster or Susan Sarandon."
  # sentence = "And I made you all a little gift, because you're like my new family."
  # doc = nlp(sentence)
  # for token in doc:
    # if token.pos == ADP and (token.text.lower() == "like" or token.text.lower() == "as"):
      # print(token)
      # children = token.children
      # for child in children:
      #   if child.pos == PROPN:
      #     pobj = [child.text]
      #     grandchildren = child.children
      #     for grandchild in grandchildren:
      #       gcdep = grandchild.dep
      #       # if grandchild.dep_ == "compound" or (grandchild.dep == conj and grandchild.pos == PROPN):
      #       if grandchild.pos == PROPN:
      #         pobj.insert(-1, grandchild.text)
      #       else:
      #         print("(", grandchild, grandchild.dep_, grandchild.pos_, ")")
      #     print(" ".join(pobj))
      #   else:
      #     print("(", child, [grandchild for grandchild in child.children], ")")
      # print("------")
  # displacy.serve(doc, style="dep")
  # for ep_code in references:
  #   episode = references[ep_code]
  #   for ref_type in episode:
  #     instances = episode[ref_type]
  #     for instance in instances:
  #       sentence = instance["reference"]["sentence"]
  #       doc = nlp(sentence)
  #       for token in doc:
  #         if token.pos == ADP and (token.text.lower() == "like" or token.text.lower() == "as"):
            # print(token)
            # children = token.children
            # for child in children:
            #   if child.pos == PROPN:
            #     pobj = [child.text]
            #     grandchildren = child.children
            #     for grandchild in grandchildren:
            #       gcdep = grandchild.dep
            #       # if grandchild.dep_ == "compound" or (grandchild.dep == conj and grandchild.pos == PROPN):
            #       if grandchild.pos == PROPN:
            #         pobj.insert(-1, grandchild.text)
            #       else:
            #         print("(", grandchild, grandchild.dep_, grandchild.pos_, ")")
            #     print(" ".join(pobj))
            #   else:
            #     print("(", child, [grandchild for grandchild in child.children], ")")
            # print("------")
  # docs = []
  # for ep_code in references:
  #   episode = references[ep_code]
  #   if ep_code == "s01e01":
  #     for ref_type in episode:
  #       instances = episode[ref_type]
  #       for instance in instances:
  #         sentence = instance["reference"]["sentence"]
  #         doc = nlp(sentence)
  #         docs.append(doc)
  # displacy.serve(docs, style="dep", options={ "compact": True })

  # print("* Simile'd people:")
  # for epcode in references:
  #   episode = references[epcode]
  #   people = episode["people"]
  #   titles = episode["titles"]
  #   for instance in people:
  #     reference = instance["reference"]
  #     sentence = reference["sentence"]
  #     entity = reference["entity"]
  #     index = sentence.find(entity)
  #     ctxBefore = sentence[:index].strip().lower()
  #     ctxBeforeWords = ctxBefore.split(" ")
  #     if ctxBeforeWords[-1] == "like":
  #       print(sentence)

  # print("* Simile'd titles:")
  # for epcode in references:
  #   episode = references[epcode]
  #   titles = episode["titles"]
  #   for instance in titles:
  #     reference = instance["reference"]
  #     sentence = reference["sentence"]
  #     entity = reference["entity"]
  #     index = sentence.find(entity)
  #     ctxBefore = sentence[:index].strip().lower()
  #     ctxBeforeWords = ctxBefore.split(" ")
  #     if ctxBeforeWords[-1] == "like":
  #       print(sentence)

def genders():
  return
  # # DISCLAIMER KINDA PROBLEMATIC ONLY BINARY "ACTOR" AND "ACTRESS" LABELS
  # actors = {}
  # actresses = {}
  # for name in people:
  #   professions = people[name]["details"]["professions"]
  #   if "actor" in professions:
  # #     actors += 1
  #     actors[name] = people[name]["count"]
  #   if "actress" in professions:
  # #     actresses += 1
  #     actresses[name] = people[name]["count"]
  # actors = OrderedDict(actors)
  # actresses = OrderedDict(actresses)
  # print("* Actors: ")
  # print(len(actors))
  # print(list(actors.items())[:10])
  # print("* Actresses: ")
  # print(len(actresses))
  # print(list(actresses.items())[:10])

# # # # # #
# ACTIONS #
# # # # # #

def analyse_all():
  references = get_references()
  names = {}
  titles = {}
  referents = populate_referents(names, titles)
  episodes = get_episodes()

  analyse_names(names)
  analyse_titles(titles)
  analyse_seasons(references, episodes)
  analyse_episodes(references, episodes)
  analyse_writers(references, episodes)

def analyse_names(names=None):
  if not names:
    names = {}
    populate_referents(names, None)
  print("--- NAMES ---")
  print()
  print("Total names:")
  print(total(names))
  print()
  print("Top names:")
  print(top(names))
  print()

def analyse_titles(titles=None):
  if not titles:
    titles = {}
    populate_referents(None, titles)
  print("--- TITLES ---")
  print()
  print("Total titles:")
  print(total(titles))
  print()
  print("Top titles:")
  print(top(titles))
  print()

def analyse_seasons(references=None, episodes=None):
  if not references:
    references = get_references()
  if not episodes:
    episodes = get_episodes()

  # count references per episode per season
  seasons = [[] for x in range(6)]
  for ep_code in references:
    s_num = int(ep_code[2])
    ep_num = int(ep_code[-2:])
    while len(seasons[s_num - 1]) < ep_num:
      seasons[s_num - 1].append(0)
    ep = references[ep_code]
    for instance in ep:
      seasons[s_num - 1][ep_num - 1] += 1
  seasons_combined = [ep for s in seasons for ep in s]

  # plot
  # fig, axs = plt.subplots(2, 1, figsize=(15, 9))
  fig, ax = plt.subplots(figsize=(15, 9))
  fig.suptitle("Community references")
  # by season
  # for s in range(len(seasons)):
  #   axs[0].plot([x + 1 for x in range(len(seasons[s]))], seasons[s], label="Season " + str(s + 1))
  # axs[0].set_title("References through each season")
  # axs[0].set_xlabel("Episode number of season")
  # axs[0].set_ylabel("Number of references")
  # axs[0].set_ylim(0)
  # axs[0].legend()
  # through series
  ax.plot([x + 1 for x in range(len(seasons_combined))], seasons_combined)
  ax.set_title("References throughout the series")
  ax.set_xlabel("Episode number of series")
  ax.set_ylabel("Number of references")
  ax.set_ylim(0)
  last_ep_nums = []
  for s in range(len(seasons)):
    if len(last_ep_nums) == 0:
      last_ep_nums.append(len(seasons[s]))
    else:
      last_ep_nums.append(len(seasons[s]) + last_ep_nums[-1])
  ax.vlines([e + 0.5 for e in last_ep_nums], 0, 1, transform=ax.get_xaxis_transform(), colors='r')
  top_ep_codes = []
  for s in range(len(seasons)):
    top_ep = 0
    for ep in range(len(seasons[s])):
      if seasons[s][ep] > seasons[s][top_ep]:
        top_ep = ep
    top_ep_codes.append((s, top_ep))
  for ep in top_ep_codes:
    s_num = ep[0] + 1
    ep_num = ep[1] + 1
    cumulative_num = ep_num - 1
    for x in range(s_num - 1):
      cumulative_num += len(seasons[x])
    code = f"s{s_num:02}e{ep_num:02}"
    ax.text(cumulative_num, seasons_combined[cumulative_num], code + " (" + str(seasons_combined[cumulative_num]) + ")", horizontalalignment="center")
    ax.text(cumulative_num, seasons_combined[cumulative_num] - 1, episodes[code]["title"], horizontalalignment="center")
  plt.show()

def analyse_episodes(references=None, episodes=None):
  if not references:
    references = get_references()
  if not episodes:
    episodes = get_episodes()
  counts_by_ep = {}
  for ep_code in references:
    ep = references[ep_code]
    counts = {"name": 0, "title": 0}
    for instance in ep:
      ref_type = instance["referent"]["refType"]
      counts[ref_type] += 1
    counts_by_ep[ep_code] = counts
  print("--- EPISODES ---")
  print()
  print("Total episodes:")
  print(total(counts_by_ep))
  print()
  for ref_type in ["name", "title", ""]:
    count = top_count(counts_by_ep, ref_type)
    ref_type_print = "combined" if not ref_type else ref_type
    print(f"Highest {ref_type_print} count:")
    title = episodes[count[0]]["title"]
    print(f"{count[0]}: {title} ({count[1]})")
    description = episodes[count[0]]["description"]
    print(description)
    writers = episodes[count[0]]["writers"]
    print(f"Written by: {', '.join([writer['name'] for writer in writers])}")
    print()

def analyse_writers(references=None, episodes=None):
  if not references:
    references = get_references()
  if not episodes:
    episodes = get_episodes()

  # count episodes for each writer
  writers = {}
  for ep_code in episodes:
    ep = episodes[ep_code]
    for writer in ep["writers"]:
      name = writer["name"]
      if name in writers:
        writers[name]["episodes"].append(ep_code)
      else:
        writers[name] = {
          "episodes": [ep_code],
          "references": 0,
          "refsPerEp": 0
        }

  # count references for each writer
  for ep_code in references:
    for name in writers:
      writer = writers[name]
      if ep_code in writer["episodes"]:
        for instance in references[ep_code]:
          writer["references"] += 1
          writer["refsPerEp"] = writer["references"]/len(writer["episodes"])

  writers_regulars = {}
  regular_threshold = 10
  for name in writers:
    if len(writers[name]["episodes"]) > regular_threshold:
      writers_regulars[name] = writers[name]

  print("--- WRITERS ---")
  print()
  print("Total writers:")
  print(total(writers))
  print()
  print(f"Total \"regular\" writers (on more than {regular_threshold} episodes):")
  print(total(writers_regulars))
  print()
  print("Writers by references:")
  writers = dict(sorted(writers.items(), key=lambda item: len(item[1]["episodes"]), reverse=True))
  print(top(writers, "references"))
  print()
  print("Regular writers by references per episode:")
  writers_regulars = dict(sorted(writers_regulars.items(), key=lambda item: item[1]["refsPerEp"], reverse=True))
  print(top(writers_regulars, "refsPerEp"))
  print()

def analyse(args):
  if args.type == "names":
    analyse_names()
  elif args.type == "titles":
    analyse_titles()
  elif args.type == "seasons":
    analyse_seasons()
  elif args.type == "episodes":
    analyse_episodes()
  elif args.type == "writers":
    analyse_writers()
  else:
    analyse_all()
