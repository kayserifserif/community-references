import csv
import spacy
from spacy import displacy
# from collections import Counter
# import pprint
# from pathlib import Path
import re

# desired_labels = ["PERSON", "WORK_OF_ART", "ORG", "FAC"]
desired_labels = ["PERSON", "WORK_OF_ART", "ORG"]

all_people = []
with open("./data/name.basics.min.tsv", newline='') as f_open:
  f_open = csv.reader(f_open, delimiter='\t')
  next(f_open) # skip header
  for row in f_open:
    all_people.append(row[1]) # add name

all_titles = []
with open("./data/title.basics.min.tsv", newline='') as f_open:
  f_open = csv.reader(f_open, delimiter='\t')
  next(f_open) # skip header
  for row in f_open:
    all_titles.append(row[2]) # add name

exclude_ents = []
with open("./data/community-entities.txt", "r") as f_open:
  f_open = csv.reader(f_open, delimiter='\n')
  for row in f_open:
    exclude_ents.append(row[0])

# https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
# https://rasa.com/
nlp = spacy.load("en_core_web_sm")
data = ""
with open("./transcripts/community-s01e01.txt", "r") as f_open:
  data = f_open.read()
data = re.sub("\n", " ", data)
text = nlp(data)

people = []
titles = []

# each recognised entity
for ent in text.ents:
  # one of the desired labels
  if ent.label_ in desired_labels:
    # not names from the show
    if ent.text not in exclude_ents:
      # either person or title
      if ent.text in all_people:
        people.append(ent.text)
      elif ent.text in all_titles:
        titles.append(ent.text)

print("PEOPLE")
print(people)
print("TITLES")
print(titles)

# html = displacy.render(processed, page=True, style='ent', options={"ents": ["PERSON"]})
# html = displacy.render(text, page=True, style='ent', options={"ents": labels})
# output_path = Path("./output/displacy.html")
# output_path.open("w", encoding="utf-8").write(html)