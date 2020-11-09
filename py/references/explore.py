import sys
from argparse import ArgumentParser

import json
# import spacy
# from spacy.symbols import *
# from spacy import displacy

from collections import OrderedDict

import re

def get_references() -> dict:
  file = "./data/community/references.json"
  try:
    with open(file, "r") as f:
      references = json.load(f)
    return references
  except IOError:
    print(f"Could not read {file}.")
    return

def populate_referents(names = None, titles = None) -> dict:
  file = "./data/community/referents.json"
  try:
    with open(file, "r") as f:
      referents = json.load(f)
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
  except IOError:
    print(f"Could not read {file}.")
    return

def get_episodes() -> dict:
  file = "./db/community/episodes.json"
  try:
    with open(file, "r") as f:
      episodes = json.load(f)
    return episodes
  except IOError:
    print(f"Could not read {file}.")
    return

def total(data: dict) -> int:
  return len(list(data))

def top(data: dict, num: int = 5) -> list:
  keys = list(data)
  lines = []
  for x in range(num):
    marker = str(x + 1) + ". "
    key = keys[x]
    count = data[key]["count"]
    lines.append(marker + key + " (" + str(count) + ")")
  return "\n".join(lines)

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
  #   for refType in episode:
  #     instances = episode[refType]
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
  #     for refType in episode:
  #       instances = episode[refType]
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

def analyse_all(args):
  names = {}
  titles = {}
  referents = populate_referents(names, titles)
  references = get_references()
  analyse_names(None, names)
  analyse_titles(None, titles)
  analyse_episodes(None, references)

def analyse_names(args, names=None):
  if not names:
    names = {}
    populate_referents(names, None)
  # people = referents["people"]
  print("--- NAMES ---")
  print()
  print("Total names:")
  print(total(names))
  print()
  print("Top names:")
  print(top(names))
  print()

def analyse_titles(args, titles=None):
  if not titles:
    titles = {}
    populate_referents(None, titles)
  # titles = referents["titles"]
  print("--- TITLES ---")
  print()
  print("Total titles:")
  print(total(titles))
  print()
  print("Top titles:")
  print(top(titles))
  print()

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

def analyse_episodes(args, references=None, episodes=None):
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
    print()

def printRefs(epRefs, refType):
  for ref in epRefs[refType]:
    reference = ref["reference"]
    referent = ref["referent"]
    print(reference["entity"], "/", reference["sentence"], "/", end=" ")
    if referent["refType"]:
      print(referent["name"], referent["nconst"])
    else:
      print(referent["title"], referent["tconst"])

def list_refs(args):
  ep_code = args.ep_code
  references = get_references()
  epRefs = references[ep_code]
  refType = args.type[0]
  if refType == "all":
    printRefs(epRefs, "people")
    printRefs(epRefs, "titles")
  elif refType == "names":
    printRefs(epRefs, "people")
  elif refType == "titles":
    printRefs(epRefs, "titles")

def ep_code_type(argStr):
  if not re.match(r"s\d{2}e\d{2}", argStr):
    raise argparse.ArgumentTypeError("Couldn't parse episode code. For example, for season 1 episode 1, the episode code should be s01e01.")
  return argStr

def main(argv):
  parser = ArgumentParser(
    description="Explore references and referents data.")
  subparsers = parser.add_subparsers(
    description="command", required=True)

  parser_analyse = subparsers.add_parser("analyse",
    help="analyse referents",
    description="Analyse referents data.")
  analyse_subparsers = parser_analyse.add_subparsers(
    description="command", required=True)
  parser_all = analyse_subparsers.add_parser("all",
    help="all of the commands",
    description="Execute all of the commands.")
  parser_all.set_defaults(func=analyse_all)
  parser_names = analyse_subparsers.add_parser("names",
    help="analyse names",
    description="Analyse referent names.")
  parser_names.set_defaults(func=analyse_names)
  parser_titles = analyse_subparsers.add_parser("titles",
    help="analyse titles",
    description="Analyse referent titles.")
  parser_titles.set_defaults(func=analyse_titles)
  parser_titles = analyse_subparsers.add_parser("episodes",
    help="analyse episodes",
    description="Analyse reference counts in episodes.")
  parser_titles.set_defaults(func=analyse_episodes)

  parser_list = subparsers.add_parser("list",
    help="list references in episode",
    description="List references in episode.")
  parser_list.add_argument("ep_code",
    help="episode code, e.g. s01e01 for season 1 episode 1",
    type=ep_code_type)
  parser_list.add_argument("--type", "-t",
    help="type of reference, e.g. names or titles",
    default="all",
    nargs=1)
  parser_list.set_defaults(func=list_refs)

  args = parser.parse_args(argv[1:]) if len(argv) > 1 else parser.parse_args(argv)
  args.func(args)
  # analyse(argv)

if __name__ == "__main__":
  main(sys.argv)