import csv
import spacy

def getTitles():
  file = "./db/title.basics.min.tsv"
  try:
    with open(file, encoding="ISO-8859-1") as f:
      db = []
      reader = csv.DictReader(f, dialect="excel-tab")
      print(f"Reading {file}...")
      for row in reader:
        db.append(row)
      return db
  except IOError:
    print(f"Could not read {file}.")
    return

def main():
  titles = getTitles()
  nlp = spacy.load("en_core_web_sm")
  for entry in titles:
    title = entry["title"]
    split = title.split(" ")
    token = None
    if len(split) == 1:
      token = nlp(title)[0]
      if token.pos_ == "NOUN" or token.pos_ == "PROPN":
        lemma = token.lemma_
        if title.lower() != lemma:
          print(title, lemma)
    elif len(split) == 2 and split[0] == "The":
      token = nlp(split[1])[0]
      if token.pos_ == "NOUN" or token.pos_ == "PROPN":
        lemma = token.lemma_
        if split[1].lower() != lemma:
          print(title, lemma)

if __name__ == "__main__":
  main()