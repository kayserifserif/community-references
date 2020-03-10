import json

with open("./output/references.json", "r") as f:
  references = json.load(f)

print("------------")
print("SIMILES")
print("------------")

print("* Simile'd people:")
for epcode in references:
  episode = references[epcode]
  people = episode["people"]
  titles = episode["titles"]
  for instance in people:
    reference = instance["reference"]
    sentence = reference["sentence"]
    entity = reference["entity"]
    index = sentence.find(entity)
    ctxBefore = sentence[:index].strip().lower()
    ctxBeforeWords = ctxBefore.split(" ")
    if ctxBeforeWords[-1] == "like":
      print(sentence)

print("* Simile'd titles:")
for epcode in references:
  episode = references[epcode]
  titles = episode["titles"]
  for instance in titles:
    reference = instance["reference"]
    sentence = reference["sentence"]
    entity = reference["entity"]
    index = sentence.find(entity)
    ctxBefore = sentence[:index].strip().lower()
    ctxBeforeWords = ctxBefore.split(" ")
    if ctxBeforeWords[-1] == "like":
      print(sentence)

with open("./output/referents.json", "r") as f:
  referents = json.load(f)

people = referents["people"]
titles = referents["titles"]

print("------------")
print("PEOPLE")
print("------------")
print("* Number of referenced people:")
print(len(list(people)))
print("* Top 10 referenced people:")
print(list(people)[:10])
print("------------")
print("TITLES")
print("------------")
print("* Number of referenced titles:")
print(len(list(titles)))
print("* Top 10 referenced titles:")
print(list(titles)[:10])