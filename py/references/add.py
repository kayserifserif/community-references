from PyInquirer import prompt
import json
import re
import csv

titleTypes = [
  "movie",
  "tvSeries",
  "tvMovie",
  "tvMiniSeries",
  "tvEpisode"
  "short",
  "video"  
]

# load referents.json
def getReferents() -> dict:
  try:
    with open("./data/community/referents.json", "r") as f:
      referents = json.load(f)
      return referents
  except IOError:
    print("Could not open referents file.")
  return

# validate user-entered episode code
def validateEpCode(val: str) -> bool:
  if not re.match(r"s\d{2}e\d{2}", val):
    return "Episode code should be in the form of \"s01e01\"."
  try:
    with open(f"./transcripts/community/{val}.txt", "r") as f:
      f.read()
      return True
  except IOError:
    return "Could not find episode file."

# get instances of entity in transcript
def getInstances(answers: dict) -> list:
  if answers["entity"] == "\\N":
    return
  try:
    with open(f"./transcripts/community/{answers['epCode']}.txt", "r") as f:
      transcript = f.read()
      transcript = re.sub("\n", " ", transcript)
    results = re.finditer(answers["entity"], transcript)
    instances = []
    for result in results:
      resStr = ""
      resStr += f"{'{:5}'.format(result.start())} {'{:5}'.format(result.end())} "
      resStr += "…" + transcript[result.start() - 20 : result.start()] + \
        "[" + result[0] + "]" + \
        transcript[result.end() : result.end() + 20] + "…"
      instances.append(resStr)
    return instances
  except IOError:
    print("Could not open transcript file.")

# check if entity exists in referents
def findExistingEntity(entity: str) -> dict or None:
  referents = getReferents()
  for refType in referents:
    for ref in referents[refType]:
      if ref == entity:
        details = referents[refType][ref]["details"]
        return details
  return

# query user for reference
def askForReference(prevAnswers: dict = None) -> dict:
  questions = [
    {
      "type": "input",
      "name": "epCode",
      "message": "Episode code:",
      "default": lambda answers: prevAnswers and prevAnswers["epCode"] or "",
      "validate": validateEpCode
    },
    {
      "type": "input",
      "name": "entity",
      "message": "Entity:",
      "default": lambda answers: prevAnswers and prevAnswers["entity"] or "",
      "validate": lambda val: True if len(val) > 0 else "Length of entity must be longer than 0."
    },
    {
      "type": "list",
      "name": "instance",
      "message": "Instance:",
      "when": lambda answers: True if getInstances(answers) else False,
      "choices": getInstances,
      "filter": lambda val: [ \
          [int(x) for x in val.strip().replace("  ", " ").split(" ")[:2]], \
          " ".join(val.strip().replace("  ", " ").split(" ")[2:]).replace("[", "").replace("]", "") \
        ]
    },
    {
      "type": "input",
      "name": "startInDoc",
      "message": "Start index in doc:",
      "when": lambda answers: "instance" not in answers,
      "filter": lambda val: "\\N" if (val == "" or not val.isdigit()) else int(val)
    },
    {
      "type": "input",
      "name": "endInDoc",
      "message": "End index in doc:",
      "when": lambda answers: "startInDoc" in answers,
      "default": lambda answers: str(answers["startInDoc"] + len(answers["entity"])),
      "filter": lambda val: "\\N" if (val == "" or not val.isdigit()) else int(val)
    },
    {
      "type": "input",
      "name": "sentence",
      "message": "Sentence:",
      "default": lambda answers: ("instance" in answers) and str(answers["instance"][1].replace("…", "")) or "",
      "validate": lambda val: True if len(val) > 0 else "Length of sentence must be longer than 0.",
      "filter": lambda val: "\\N" if val == "" else val.strip()
    },
    {
      "type": "input",
      "name": "startInSent",
      "message": "Start index in sentence:",
      "when": lambda answers: answers["sentence"] != "\\N",
      "default": lambda answers: str(answers["sentence"].find(answers["entity"])),
      "filter": lambda val: "\\N" if (val == "" or not val.isdigit()) else int(val)
    },
    {
      "type": "input",
      "name": "endInSent",
      "message": "End index in sentence:",
      "when": lambda answers: "startInSent" in answers,
      "default": lambda answers: str(answers["sentence"].find(answers["entity"]) + len(answers["entity"])),
      "filter": lambda val: "\\N" if (val == "" or not val.isdigit()) else int(val)
    }
  ]
  print("\
*********\n\
REFERENCE\n\
*********")
  answers = prompt(questions)
  answers["startInDoc"] = answers["instance"][0][0]
  answers["endInDoc"] = answers["instance"][0][1]
  answers.pop("instance", None)
  print(json.dumps(answers, indent=2))
  nextStep = list(prompt(
    [
      {
        "type": "expand",
        "name": "nextStep",
        "message": "Proceed with this reference?",
        "choices": [
          {
            "key": "p",
            "name": "Proceed to referent",
            "value": "proceed"
          },
          {
            "key": "e",
            "name": "Edit reference",
            "value": "edit"
          },
          {
            "key": "q",
            "name": "Quit program",
            "value": "quit"
          }
        ]
      }
    ]
  ).values())[0]
  if nextStep == "quit":
    print("Okay, exiting program.")
    return
  elif nextStep == "edit":
    askForReference(answers)
  else:
    return answers
  return answers

# load database and search through for entity
def loadAndSearchDb(refType: str, entity: str) -> dict or list:
  includePartial = list(prompt({
    "type": "confirm",
    "name": "include",
    "message": "Include partial matches?"  
  }).values())[0]
  if includePartial:
    interimMessage = "Searching through database for all matches..."
    failMessage = "Match could not be found."
  else:
    interimMessage = "Searching through database for exact matches..."
    failMessage = "Exact match could not be found."
  database = []
  try:
    with open("./db/" + refType + ".basics.tsv", encoding="ISO-8859-1") as f:
      reader = csv.DictReader(f, dialect="excel-tab")
      print(interimMessage)
      for row in reader:
        match = False
        if refType == "name":
          newRow = {
            "nconst": row["nconst"],
            "name": row["primaryName"],
            "birthYear": int(row["birthYear"]) if row["birthYear"].isdigit() else row["birthYear"],
            "deathYear": int(row["deathYear"]) if row["deathYear"].isdigit() else row["deathYear"],
            "professions": row["primaryProfession"].split(","),
            "knownFor": row["knownForTitles"].split(",")
          }
          if includePartial:
            if entity in newRow["name"]:
              match = True
          else:
            if newRow["name"] == entity:
              match = True
        else:
          newRow = {
            "tconst": row["tconst"],
            "titleType": row["titleType"],
            "title": row["primaryTitle"],
            "startYear": int(row["startYear"]) if row["startYear"].isdigit() else row["startYear"],
            "endYear": int(row["endYear"]) if row["endYear"].isdigit() else row["endYear"],
            "genres": (lambda row: row["genres"].split(",") if "genres" in row else "\\N")(row)
          }
          if includePartial:
            if entity in newRow["title"]:
              match = True
          else:
            if newRow["title"] == entity:
              match = True
        database.append(newRow)
        print("Row: {:8}".format(len(database)), end="\r")
        if match:
          print()
          print(f"Match found at row {len(database)}!")
          print(json.dumps(newRow, indent=2))
          if list(prompt({
            "type": "confirm",
            "name": "use",
            "message": "Use this referent?"
          }).values())[0]:
            return newRow
          else:
            print(interimMessage)
    
    print(failMessage)
    return database
  except IOError:
    print("Could not open database file.")

# look for partial match in database
def findPartialMatch(database: list, entity: str) -> dict or None:
  interimMessage = "Searching through database for partial matches..."
  print(interimMessage)
  for row in database:
    match = False
    if "name" in row:
      if entity in row["name"]:
        match = True
    else:
      if entity in row["title"]:
        match = True
    print("Row: {:8}".format(len(database)), end="\r")
    if match:
      print()
      print(f"Match found at row {len(database)}!")
      print(json.dumps(newRow, indent=2))
      if list(prompt({
        "type": "confirm",
        "name": "use",
        "message": "Use this referent?"
      }).values())[0]:
        return newRow
      else:
        print(interimMessage)
  print("Partial match could not be found.")
  return

# query user for referent
def askForReferent(refType: str, prevAnswers: dict = None) -> dict:
  questions = [
    {
      "type": "input",
      "name": refType,
      "message": (lambda refType: "Name:" if refType == "name" else "Title:")(refType),
      "default": (lambda prevAnswers: (prevAnswers["name"] if "name" in prevAnswers else prevAnswers["title"]) if prevAnswers else "")(prevAnswers)
    },
    {
      "type": "input",
      "name": (lambda refType: "nconst" if refType == "name" else "tconst")(refType),
      "message": (lambda refType: "IMDb nconst:" if refType == "name" else "IMDb tconst:")(refType),
      "default": (lambda prevAnswers: (prevAnswers["nconst"] if "nconst" in prevAnswers else prevAnswers["tconst"]) if prevAnswers else "")(prevAnswers),
      "validate": lambda val: len(val) is 9 and (val[:2] == "nm" or val[:2] == "tt")
    },
    {
      "type": "list",
      "name": "titleType",
      "message": "Title type:",
      "choices": titleTypes,
      "default": (lambda prevAnswers: titleTypes.index(prevAnswers["titleType"]) if prevAnswers else 0)(prevAnswers)
    },
    {
      "type": "input",
      "name": (lambda refType: "birthYear" if refType == "name" else "startYear")(refType),
      "message": (lambda refType: "Birth year:" if refType == "name" else "Start year:")(refType),
      "default": (lambda prevAnswers: (str(prevAnswers["birthYear"]) if "birthYear" in prevAnswers else str(prevAnswers["startYear"])) if prevAnswers else "")(prevAnswers),
      "filter": lambda val: "\\N" if (val == "" or not val.isdigit()) else int(val)
    },
    {
      "type": "input",
      "name": (lambda refType: "deathYear" if refType == "name" else "endYear")(refType),
      "message": (lambda refType: "Death year:" if refType == "name" else "End year:")(refType),
      "default": (lambda prevAnswers: (str(prevAnswers["deathYear"]) if "deathYear" in prevAnswers else str(prevAnswers["endYear"])) if prevAnswers else "\\N")(prevAnswers),
      "filter": lambda val: "\\N" if (val == "" or not val.isdigit()) else int(val)
    },
    {
      "type": "input",
      "name": "professions",
      "message": "Professions (separated by commas, no spaces):",
      "when": lambda answers: True if refType == "name" else False,
      "default": (lambda prevAnswers: prevAnswers["professions"] if (prevAnswers and "professions" in prevAnswers) else "")(prevAnswers)
    },
    {
      "type": "input",
      "name": "knownFor",
      "message": "Known for (tconsts, separated by commas, no spaces):",
      "when": lambda answers: True if refType == "name" else False,
      "default": (lambda prevAnswers: prevAnswers["knownFor"] if (prevAnswers and "knownFor" in prevAnswers) else "")(prevAnswers)
    },
    {
      "type": "input",
      "name": "genres",
      "message": "Genres (separated by commas, no spaces)",
      "when": lambda answers: True if refType == "title" else False,
      "default": (lambda prevAnswers: prevAnswers["genres"] if (prevAnswers and "genres" in prevAnswers) else "")(prevAnswers)
    }
  ]
  answers = prompt(questions)
  print(json.dumps(answers, indent=2))
  nextStep = list(prompt(
    [
      {
        "type": "expand",
        "name": "nextStep",
        "message": "Proceed with this referent?",
        "choices": [
          {
            "key": "p",
            "name": "Proceed to saving",
            "value": "proceed"
          },
          {
            "key": "e",
            "name": "Edit referent",
            "value": "edit"
          },
          {
            "key": "q",
            "name": "Quit program",
            "value": "quit"
          }
        ]
      }
    ]
  ).values())[0]
  if nextStep == "quit":
    print("Okay, exiting program.")
    return
  elif nextStep == "edit":
    askForReferent(refType, answers)
  else:
    return answers
  return answers

# search for referent in existing file or in database
def searchForReferent(reference: dict, prevAnswers: dict = None) -> dict or None:
  print("\
********\n\
REFERENT\n\
********")
  entity = reference["entity"]
  referent = findExistingEntity(entity)
  if referent:
    print("Existing referent detected!")
    print(json.dumps(referent, indent=2))
    if list(prompt(
      [
        {
          "type": "confirm",
          "name": "confirm",
          "message": "Proceed with this referent?"
        }
      ]
    ).values())[0]:
      print("Adding to data files...")
      return referent
    else:
      print("Okay, exiting program.")
      return
  else:
    print("Referent could not be detected.")
    refType = list(prompt(
      [
        {
          "type": "list",
          "name": "refType",
          "message": "Which type of entity is this referent?",
          "choices": [
            "name",
            "title"
          ]
        }
      ]
    ).values())[0]
    dbResult = loadAndSearchDb(refType, entity)
    if (type(dbResult) is dict):
      referent = dbResult
      return referent
    else:
      database = dbResult
      partialResult = findPartialMatch(database, entity)
      if partialResult:
        return partialResult
      else:
        referent = askForReferent(refType)
    return

# save new ref to references file
def writeToReferences(newRef: dict):
  refFile = "./data/community/references.json"
  try:
    with open(refFile, "r") as f:
      references = json.load(f)
  except IOError:
    print("Could not open file.")

  epCode = newRef["reference"]["epCode"]
  newRef["reference"].pop("epCode", None)

  # if "name" in newRef["referent"]:
  #   references[epCode]["people"].append(newRef)
  # else:
  #   references[epCode]["titles"].append(newRef)
  references[epCode].append(newRef())

  j = json.dumps(references, indent=2)
  try:
    with open(refFile, "w") as f:
      print(j, file=f)
      print(f"Successfully saved to file {refFile}!")
  except IOError:
    print("Could not write to references file.")

# query user for input on reference and referent
def getInput(prevReference: dict = None, prevReferent: dict = None, editItem: str = None) -> dict or None:
  if not editItem:
    reference = askForReference()
    if not reference:
      return
    referent = searchForReferent(reference)
    if not referent:
      return
  else:
    if editItem == "reference":
      reference = askForReference(prevReference)
      if not reference:
        return
    else:
      referent = askForReference(prevReferent)
      if not referent:
        return

  newRef = {
    "reference": reference,
    "referent": referent
  }
  print(json.dumps(newRef, indent=2))
  save = list(prompt(
    [
      {
        "type": "expand",
        "name": "save",
        "message": "Save?",
        "choices": [
          {
            "key": "s",
            "name": "Save",
            "value": "save"
          },
          {
            "key": "e",
            "name": "Edit",
            "value": "edit"
          },
          {
            "key": "q",
            "name": "Quit program",
            "value": "quit"
          }
        ]
      }
    ]
  ).values())[0]
  if save == "quit":
    print("Okay, exiting program.")
    return
  elif save == "edit":
    editItem = list(prompt(
      [
        {
          "type": "expand",
          "name": "item",
          "message": "Which item?",
          "choices": [
            {
              "key": "c",
              "name": "Reference",
              "value": "reference"
            },
            {
              "key": "t",
              "name": "Referent",
              "value": "referent"
            }
          ]
        }
      ]
    ).values())[0]
    getInput(reference, referent, editItem)
  else:
    return newRef

# main function
def main():
  newRef = getInput()
  if not newRef:
    return
  writeToReferences(newRef)

if __name__ == "__main__":
  main()