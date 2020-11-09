import json

def get_references() -> dict:
  file = "data/community/references.json"
  try:
    with open(file) as f:
      references = json.load(f)
      return references
  except IOError:
    print("Could not write to file.")
    return

def generate_referents(references) -> dict:
  referents = {}

  for ep_code in references:
    ep = references[ep_code]
    for instance in ep:
      reference = instance["reference"]
      referent = instance["referent"]
      nametitle = referent[referent["refType"]]
      season = int(ep_code[2])
      if nametitle in referents:
        referents[nametitle]["count"] += 1
        referents[nametitle]["countBySeason"][season - 1] += 1
        referents[nametitle]["references"].append(reference)
      else:
        count_by_season = [0 for x in range(6)]
        count_by_season[season - 1] = 1
        referents[nametitle] = {
          "count": 1,
          "countBySeason": count_by_season,
          "details": referent,
          "references": [reference]
        }

  return referents

def write(referents) -> None:
  file = "data/community/referents_new.json"
  try:
    j = json.dumps(referents, indent=2)
    with open(file, "w") as f:
      print(j, file=f)
      print(f"Successfully saved to {file}!")
  except IOError:
    print("Could not write to file.")

def main():
  references = get_references()
  referents = generate_referents(references)
  write(referents)

if __name__ == "__main__":
  main()