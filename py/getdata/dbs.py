import csv
import time

# titleType: ['short', 'movie', 'tvMovie', 'tvSeries', 'tvEpisode', 'tvShort', 'tvMiniSeries', 'tvSpecial', 'video', 'videoGame']
# primaryProfession: ['soundtrack', 'actor', 'miscellaneous', 'actress', 'producer', 'writer', 'director', 'make_up_department', 'composer', 'music_department', 'assistant_director', 'camera_department', 'cinematographer', 'casting_director', 'editor', 'set_decorator', 'art_director', 'stunts', 'editorial_department', 'costume_department', 'animation_department', 'art_department', 'executive', 'special_effects', 'production_designer', 'production_manager', 'sound_department', 'talent_agent', 'casting_department', 'costume_designer', 'visual_effects', 'location_management', 'transportation_department', 'script_department', 'manager', '', 'legal', 'assistant', 'publicist']

def readDb(file):
  try:
    with open(file, "r", encoding="UTF-8") as f:
      reader = csv.DictReader(f, dialect="excel-tab")
      db = []
      # db = {}
      print(f"Reading {file}...")
      start = time.time()
      if "name.basics" in file:
        for row in reader:
          # db.append(row)
          db.append({
            "nconst": row["nconst"],
            "name": row["primaryName"],
            "birthYear": row["birthYear"],
            "deathYear": row["deathYear"],
            "professions": row["primaryProfession"],
            "knownFor": row["knownForTitles"]
            })
          print("Row: {:7}".format(len(db)), end="\r")
      elif "title.basics" in file:
        for row in reader:
          # if row["runtimeMinutes"].isdigit():
            # row["runtimeMinutes"] = int(row["runtimeMinutes"])
          # db.append(row)
          db.append({
            "tconst": row["tconst"],
            "titleType": row["titleType"],
            "title": row["primaryTitle"],
            "startYear": row["startYear"],
            "endYear": row["endYear"],
            "genres": row["genres"]
            })
          # tconst = row["tconst"]
          # row.pop("tconst", None)
          # db[tconst] = row
          print("Row: {:7}".format(len(db)), end="\r")
      elif "title.ratings.tsv" in file:
        for row in reader:
          # db.append(row)
          tconst = row["tconst"]
          row.pop("tconst", None)
          db[tconst] = row
          print("Row: {:7}".format(len(db)), end="\r")
      end = time.time()
      delta = end - start
      print(f"Read {str(len(db))} rows in {'{0:.2f}'.format(delta)} seconds.")
      return db
  except IOError:
    print(f"Could not read {file}.")
    return

def writeDb(db, file):
  try:
    with open(file, "w", encoding="UTF-8") as f:
      writer = csv.DictWriter(f, fieldnames=db[0].keys(), dialect="excel-tab")
      # fields = ["tconst", "averageRating", "numVotes"]
      # writer = csv.DictWriter(f, fieldnames=fields, dialect="excel-tab")
      writer.writeheader()
      print(f"Writing to {file}...")
      for row in db:
        writer.writerow(row)
      # for tconst in db:
        # writer.writerow({
        #   "tconst": tconst,
        #   "averageRating": db[tconst]["averageRating"],
        #   "numVotes": db[tconst]["numVotes"]
        #   })
      print(f"Successfully saved to {file}!")
  except IOError:
    print(f"Could not write to {file}.")
    return

# return True to keep, False to remove
def keepEntry(entry, condsToRemove, mustMatchAll):
  keep = True

  for cond in condsToRemove:
    match = False
    if cond[2] == 0:
      match = entry[cond[0]] == cond[1]
    elif cond[2] == -1:
      if type(cond[1]) == int:
        try:
          match = int(entry[cond[0]]) < int(cond[1])
        except ValueError:
          return True
      else:
        match = len(entry[cond[0]]) < len(cond[1])
    elif cond[2] == 1:
      if type(cond[1]) == int:
        try:
          match = int(entry[cond[0]]) > int(cond[1])
        except ValueError:
          return True
      else:
        match = len(entry[cond[0]]) > len(cond[1])
    elif cond[2] == 2:
      match = cond[1] in entry[cond[0]]
    
    if match:
      keep = False
      if not mustMatchAll:
        # print(entry)
        return False
    else:
      if mustMatchAll:
        return True
  
  # if not keep:
    # print(entry)
  return keep

def removeEntries(db, condsToRemove, mustMatchAll=True):
  print(f"Removing entries where {condsToRemove} and mustMatchAll={mustMatchAll}...")
  start = time.time()
  newDb = [x for x in db if keepEntry(x, condsToRemove, mustMatchAll)]
  end = time.time()
  delta = end - start
  print(f"Removed {str(len(db) - len(newDb))} entries in {'{0:.2f}'.format(delta)} seconds.")
  return newDb

def constInDb(db, const):
  constType = const[0] + "const"
  return const in [y[constType] for y in db]

def intersect(db, dbToMatch, key):
  print(f"Removing entries in `db` that aren't in `dbToMatch` according to `key`...")
  start = time.time()
  newDb = {key : value for (key, value) in db.items() if key in dbToMatch}
  end = time.time()
  delta = end - start
  print(f"Removed {str(len(db) - len(newDb))} entries in {'{0:.2f}'.format(delta)} seconds.")
  return newDb

def main():
  # titlesFile = "./db/title.basics.tsv"
  # # titlesFile = "./db/title.basics.min.tsv"
  # titles = readDb(titlesFile)
  # print("Titles: " + "{:7}".format(len(titles)) + " rows")
  # titles = removeEntries(titles, [
  #   ("titleType", "short", 0),
  #   ("titleType", "tvEpisode", 0),
  #   ("titleType", "tvShort", 0),
  #   ("titleType", "video", 0),
  #   ("titleType", "videoGame", 0)
  # ], mustMatchAll=False) # remaining: movie, tvMovie, tvSeries, tvMiniSeries, tvSpecial
  # titles = removeEntries(titles, [("isAdult", "1", 0)])
  # titles = removeEntries(titles, [("startYear", "\\N", 0), ("endYear", "\\N", 0)])
  # titles = removeEntries(titles, [("titleType", "movie", 0), ("runtimeMinutes", "\\N", 0)])
  # titles = removeEntries(titles, [("titleType", "tvSeries", 0), ("runtimeMinutes", "\\N", 0)])
  # titles = removeEntries(titles, [("titleType", "movie", 0), ("runtimeMinutes", 60, -1)])
  # titles = removeEntries(titles, [("titleType", "tvSeries", 0), ("runtimeMinutes", 60, -1)])
  # titles = removeEntries(titles, [("genres", "Biography", 2)])
  # titles = removeEntries(titles, [("genres", "\\N", 0)])
  # print("Titles: " + "{:7}".format(len(titles)) + " rows")
  # writeDb(titles, "./db/title.basics.min1.tsv")
  
  namesFile = "./db/name.basics.tsv"
  # namesFile = "./db/name.basics.min.tsv"
  names = readDb(namesFile)
  print("Names: " + "{:7}".format(len(names)) + " rows")
  names = removeEntries(names, [("birthYear", "\\N", 0)])
  names = removeEntries(names, [("knownFor", "tt0000000,", -1)])
  names = removeEntries(names, [
    ("professions", "", 0),
    ("professions", "legal", 2),
    ("professions", "publicist", 2),
    ("professions", "art_director", 2),
    ("professions", "animation_department", 2),
    ("professions", "art_department", 2),
    ("professions", "special_effects", 2),
    ("professions", "sound_department", 2),
    ("professions", "talent_agent", 2),
    ("professions", "casting_department", 2),
    ("professions", "visual_effects", 2),
    ("professions", "location_management", 2),
    ("professions", "transportation_department", 2)
  ], mustMatchAll=False)
  print("Names: " + "{:7}".format(len(names)) + " rows")
  writeDb(names, "./db/name.basics.min.tsv")
  
  # ratingsFile = "./db/title.ratings.tsv"
  # ratings = readDb(ratingsFile)
  # print("Ratings: " + "{:7}".format(len(ratings)) + " rows")
  # ratings = intersect(ratings, titles, "tconst")
  # print("Ratings: " + "{:7}".format(len(ratings)) + " rows")
  # writeDb(ratings, "./db/title.ratings.min.tsv")

  return

if __name__ == "__main__":
  main()