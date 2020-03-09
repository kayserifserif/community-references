import json
from collections import OrderedDict

with open("./output/references.json", "r") as f:
  data = json.load(f)

people = {}
titles = {}

for epcode in data:
  episode = data[epcode]
  for instance in episode["people"]:
    reference = instance["reference"]
    details = instance["referent"]
    name = details["name"]
    if name not in people:
      people[name] = {
        "count": 1,
        "details": details,
        "references": [reference]
      }
    else:
      people[name]["count"] += 1
      people[name]["references"].append(reference)
  for instance in episode["titles"]:
    reference = instance["reference"]
    details = instance["referent"]
    title = details["title"]
    if title not in titles:
      titles[title] = {
        "count": 1,
        "details": details,
        "references": [reference]
      }
    else:
      titles[title]["count"] += 1
      titles[title]["references"].append(reference)

people = OrderedDict(sorted(people.items(), key=lambda x: x[1]["count"], reverse=True))
titles = OrderedDict(sorted(titles.items(), key=lambda x: x[1]["count"], reverse=True))

referents = {}
referents["people"] = people
referents["titles"] = titles

try:
  j = json.dumps(referents, indent=2)
  with open("./output/referents.json", "w") as f:
    print(j, file=f)
    print("Successfully saved to file ./output/referents.json!")
except IOError:
  print("Could not write to file.")