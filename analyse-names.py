import json
import csv
import statistics



# # # #
# DATA #
# # # #

all_people = {}
with open("./data/name.basics.min.tsv", newline='') as f_open:
  f_open = csv.reader(f_open, delimiter='\t')
  next(f_open) # skip header
  for row in f_open:
    name = row[1]
    all_people[name] = {
      "birthYear": row[2],
      "deathYear": row[3],
      "primaryProfession": [x for x in row[4].split(",")]
    }

data = ""
with open("./output/all.json", "r") as f:
  data = json.load(f)



# # # # # #
# ANALYSIS #
# # # # # #

people = {}
for ep in data:
  for p in data[ep]["people"]:
    if p in people:
      people[p] += 1
    else:
      people[p] = 1
people = [[k, v] for k, v in sorted(people.items(), key=lambda item: item[1], reverse=True)]
print("number of people:", len(people))
print("top 5:", [x for x in people[:5]])

professions = {}
for p in people:
  prof = all_people[p[0]]["primaryProfession"][0]
  if prof in professions:
    professions[prof] += 1
  else:
    professions[prof] = 1
professions = [[k, v] for k, v in sorted(professions.items(), key=lambda item: item[1], reverse=True)]
print("professions:", professions)

birthYears = {}
for p in people:
  year = all_people[p[0]]["birthYear"]
  try:
    year = int(year)
    if year in birthYears:
      birthYears[year].append(p[0])
    else:
      birthYears[year] = [p[0]]
  except ValueError:
    pass
print("earliest birth year:", min(birthYears), birthYears[min(birthYears)])
print("latest birth year:", max(birthYears), birthYears[max(birthYears)])
print("median birth year:", statistics.median(birthYears), birthYears[statistics.median(birthYears)])

isAlive = {"alive": 0, "dead": 0}
for p in people:
  year = all_people[p[0]]["deathYear"]
  try:
    year = int(year)
    isAlive["alive"] += 1
  except ValueError:
    isAlive["dead"] += 1
print("alive", isAlive["alive"], "dead", isAlive["dead"])