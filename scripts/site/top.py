import json
from collections import OrderedDict
from bs4 import BeautifulSoup

def top():

  with open("./data/references.json", "r") as f:
    references = json.load(f)

  countByEp = {}
  for epCode in references:
    counter = 0
    for refType in references[epCode]:
      for ref in references[epCode][refType]:
        counter += 1
    countByEp[epCode] = counter
  countByEp = OrderedDict(sorted(countByEp.items(), key=lambda x: x[1], reverse=True))
  numTop = 10
  top = list(countByEp.items())[:10]
  # print(top)

  soup = BeautifulSoup(f"\
  <html lang='en'>\n\
  <head>\n\
  <meta charset='UTF-8'>\n\
  <link rel='stylesheet' href='top.css'>\n\
  </head>\n\
  <body>\n\
  <h1>Top {numTop}</h1>\n\
  <div id='container'>\n\
  </div>\n\
  <script src='https://cdnjs.cloudflare.com/ajax/libs/d3/5.15.0/d3.min.js'></script>\n\
  <script src='top.js'></script>\n\
  </body>\n\
  </html>", "html.parser")
  container = soup.find(id="container")
  counter = 0
  for item in top:
    counter += 1
    newItem = soup.new_tag("div")
    newItem["id"] = item[0]
    newItem["class"] = "episode"
    heading = soup.new_tag("h2")
    heading.string = item[0]
    heading["class"] = "epCode"
    newItem.append(heading)
    svg = soup.new_tag("svg")
    svg["class"] = "svg"
    defs = soup.new_tag("defs")
    linGrad = soup.new_tag("linearGradient")
    linGrad["id"] = "linGrad" + str(counter)
    linGrad["class"] = "linGrad"
    numStops = 20
    for x in range(numStops):
      stop = soup.new_tag("stop")
      stop["offset"] = x / numStops
      linGrad.append(stop)
    defs.append(linGrad)
    svg.append(defs)
    newItem.append(svg)
    container.append(newItem)
    container.append("\n")

  outFile = "./site/top/index.html"
  with open(outFile, "w") as f:
    f.write(str(soup))
    print(f"Successfully wrote to file {outFile}!")

def main():
  top()

if __name__ == "__main__":
  main()