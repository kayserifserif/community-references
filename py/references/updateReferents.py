import json
from collections import OrderedDict

def update():

  with open("./data/community/references.json", "r") as f:
    data = json.load(f)

  people = {}
  titles = {}

  for epCode in data:
    episode = data[epCode]
    for instance in episode["people"]:
      reference = instance["reference"]
      reference["epCode"] = epCode
      season = epCode[:3]
      details = instance["referent"]
      name = details["name"]
      if name not in people:
        people[name] = {
          "count": 1,
          "countBySeason": {
            "s01": 0,
            "s02": 0,
            "s03": 0,
            "s04": 0,
            "s05": 0,
            "s06": 0,
          },
          "details": details,
          "references": [reference]
        }
        people[name]["countBySeason"][season] = 1
      else:
        people[name]["count"] += 1
        people[name]["countBySeason"][season] += 1
        people[name]["references"].append(reference)
    for instance in episode["titles"]:
      reference = instance["reference"]
      reference["epCode"] = epCode
      details = instance["referent"]
      title = details["title"]
      if title not in titles:
        titles[title] = {
          "count": 1,
          "countBySeason": {
            "s01": 0,
            "s02": 0,
            "s03": 0,
            "s04": 0,
            "s05": 0,
            "s06": 0,
          },
          "details": details,
          "references": [reference]
        }
        titles[title]["countBySeason"][season] = 1
      else:
        titles[title]["count"] += 1
        titles[title]["countBySeason"][season] += 1
        titles[title]["references"].append(reference)

  people = OrderedDict(sorted(people.items(), key=lambda x: x[1]["count"], reverse=True))
  titles = OrderedDict(sorted(titles.items(), key=lambda x: x[1]["count"], reverse=True))

  referents = {}
  referents["people"] = people
  referents["titles"] = titles

  try:
    j = json.dumps(referents, indent=2)
    with open("./data/community/referents.json", "w") as f:
      print(j, file=f)
      print("Successfully saved to file ./data/community/referents.json!")
  except IOError:
    print("Could not write to file.")

def main():
  update()

if __name__ == "__main__":
  main()