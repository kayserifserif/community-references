import json
import spacy
from spacy.symbols import *
from spacy import displacy
from collections import OrderedDict

references = {}
referents = {}

with open("./output/references.json", "r") as f:
  references = json.load(f)
with open("./output/referents.json", "r") as f:
  referents = json.load(f)
  people = referents["people"]
  titles = referents["titles"]

# print("------------")
# print("PEOPLE")
# print("------------")
# print("* Number of referenced people:")
# print(len(list(people)))
# print("* Top 10 referenced people:")
# print(list(people)[:10])
# print("------------")
# print("TITLES")
# print("------------")
# print("* Number of referenced titles:")
# print(len(list(titles)))
# print("* Top 10 referenced titles:")
# print(list(titles)[:10])

# print("------------")
# print("SIMILES")
# print("------------")

nlp = spacy.load("en_core_web_sm")
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
docs = []
for epCode in references:
  episode = references[epCode]
  if epCode == "s01e01":
    for refType in episode:
      instances = episode[refType]
      for instance in instances:
        sentence = instance["reference"]["sentence"]
        doc = nlp(sentence)
        docs.append(doc)
displacy.serve(docs, style="dep", options={ "compact": True })

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

# # DISCLAIMER KINDA PROBLEMATIC ONLY BINARY "ACTOR" AND "ACTRESS" LABELS
# print("------------")
# print("ACTORS AND ACTRESSES")
# print("------------")
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