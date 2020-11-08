import sys
from argparse import ArgumentParser

import json
# import spacy
# from spacy.symbols import *
# from spacy import displacy

from collections import OrderedDict

import re

def getReferences() -> dict:
  file = "./data/community/references.json"
  try:
    with open(file, "r") as f:
      references = json.load(f)
    return references
  except IOError:
    print(f"Could not read {file}.")
    return

def getReferents() -> dict:
  file = "./data/community/referents.json"
  try:
    with open(file, "r") as f:
      referents = json.load(f)
    return referents
  except IOError:
    print(f"Could not read {file}.")
    return

def total(data: dict) -> int:
  return len(list(data))

def top(data: dict, num: int = 5) -> list:
  # top = list(data)[:num]
  datalist = list(data)
  lines = []
  for x in range(num):
    lines.append(str(x + 1) + ". " + datalist[x] + " (" + str(data[datalist[x]]["count"]) + ")")
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
  # for epCode in references:
  #   episode = references[epCode]
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
  # for epCode in references:
  #   episode = references[epCode]
  #   if epCode == "s01e01":
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
  referents = getReferents()
  references = getReferences()
  analyse_names(None, referents)
  analyse_titles(None, referents)
  analyse_episodes(None, references)

def analyse_names(args, referents=None):
  if not referents:
    referents = getReferents()
  people = referents["people"]
  print("--- NAMES ---")
  print("Total names:", total(people))
  print("Top names:")
  print(top(people))

def analyse_titles(args, referents=None):
  if not referents:
    referents = getReferents()
  titles = referents["titles"]
  print("--- TITLES ---")
  print("Total titles:", total(titles))
  print("Top titles:")
  print(top(titles))

def topCount(countsByEp, countType=2):
  topCount = 0
  topCountEp = ""
  for epCode in countsByEp:
    if countType == 2:
      count = countsByEp[epCode][0] + countsByEp[epCode][1]
    else:
      count = countsByEp[epCode][countType]
    if count > topCount:
      topCount = count
      topCountEp = epCode
  return (topCount, topCountEp)

def analyse_episodes(args, references=None):
  if not references:
    references = getReferences()
  countsByEp = {}
  for epCode in references:
    ep = references[epCode]
    nameCount = 0
    titleCount = 0
    for name in ep["people"]:
      nameCount += 1
    for title in ep["titles"]:
      titleCount += 1
    countsByEp[epCode] = [nameCount, titleCount]
  print("--- EPISODES ---")
  print("Total episodes:", len(countsByEp))
  nameCount = topCount(countsByEp, 0)
  print("Highest name count:", str(nameCount[0]) + " (" + nameCount[1] + ")")
  titleCount = topCount(countsByEp, 1)
  print("Highest title count:", str(titleCount[0]) + " (" + titleCount[1] + ")")
  combinedCount = topCount(countsByEp, 2)
  print("Highest combined count:", str(combinedCount[0]) + " (" + combinedCount[1] + ")")

def printRefs(epRefs, refType):
  for ref in epRefs[refType]:
    reference = ref["reference"]
    referent = ref["referent"]
    print(reference["entity"], "/", reference["sentence"], "/", end=" ")
    if "name" in referent:
      print(referent["name"], referent["nconst"])
    else:
      print(referent["title"], referent["tconst"])

def list_refs(args):
  epCode = args.epCode
  references = getReferences()
  epRefs = references[epCode]
  refType = args.type[0]
  if refType == "all":
    printRefs(epRefs, "people")
    printRefs(epRefs, "titles")
  elif refType == "names":
    printRefs(epRefs, "people")
  elif refType == "titles":
    printRefs(epRefs, "titles")

def epCodeType(argStr):
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
  parser_list.add_argument("epCode",
    help="episode code, e.g. s01e01 for season 1 episode 1",
    type=epCodeType)
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