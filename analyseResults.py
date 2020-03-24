import json
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