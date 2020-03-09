import json

with open("./output/referents.json", "r") as f:
  data = json.load(f)

people = data["people"]
titles = data["titles"]

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