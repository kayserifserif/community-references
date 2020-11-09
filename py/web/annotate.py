# THIS IS MESSY

# import sys
# from os import listdir, makedirs
# from os import path
# import json
# import re
# import html
# from bs4 import BeautifulSoup
# from collections import OrderedDict

# def makeAnnotations(epCode, epCodes):
#   # get transcript for this episode
#   with open("./transcripts/community/" + epCode + ".txt", "r") as f:
#     transcript = f.read()
#   # get all references
#   with open("./data/community/references.json", "r") as f:
#     references = json.load(f)
#     epRefs = references[epCode]

#   nameCounts = {}
#   titleCounts = {}
#   counts = {"name": {}, "title": {}}
#   # for ref in epRefs["people"]:
#   #   referent = ref["referent"]
#   #   entity = referent["name"]
#   #   if entity in nameCounts:
#   #     nameCounts[entity] += 1
#   #   else:
#   #     nameCounts[entity] = 1
#   # for ref in epRefs["titles"]:
#   #   referent = ref["referent"]
#   #   entity = referent["title"]
#   #   if entity in titleCounts:
#   #     titleCounts[entity] += 1
#   #   else:
#   #     titleCounts[entity] = 1
#   for ref in epRefs:
#     referent = ref["referent"]
#     refType = "name" if "name" in referent else "title"
#     nametitle = referent[refType]
#     if nametitle in counts[refType]:
#       counts[refType][nametitle] += 1
#     else:
#       counts[refType][nametitle] = 1

#   counts["name"] = OrderedDict(sorted(counts["name"].items(), key=lambda x: x[1], reverse=True))
#   counts["title"] = OrderedDict(sorted(counts["title"].items(), key=lambda x: x[1], reverse=True))

#   # set up lines
#   lines = ""
# #   soup = BeautifulSoup("\
# # <!DOCTYPE html>\
# # <html lang='en'>\
# # <head>\
# # <meta charset='UTF-8'>\
# # <link rel='stylesheet' href='../../assets/styles.css'>\
# # </head>\
# # <body>\
# # <nav class='nav'></nav>\
# # <h1 id='title'></h1>\
# # <div id='transcript'></div>\
# # <nav class='nav'></nav>\
# # <script src='../../assets/scripts.js'></script>\
# # </body>\
# # </html>", "html.parser")
#   # print(soup)
#   # collect all indices
#   indices = []
#   # for instance in epRefs["people"]:
#   #   reference = instance["reference"]
#   #   referent = instance["referent"]
#   #   indices.append([
#   #     reference["startInDoc"],
#   #     reference["endInDoc"],
#   #     reference["entity"],
#   #     "people",
#   #     referent["name"],
#   #     referent["nconst"],
#   #     referent["birthYear"],
#   #     referent["deathYear"],
#   #     referent["professions"],
#   #     referent["knownFor"]
#   #   ])
#   #   # indices.append(instance)
#   # for instance in epRefs["titles"]:
#   #   reference = instance["reference"]
#   #   referent = instance["referent"]
#   #   indices.append([
#   #     reference["startInDoc"],
#   #     reference["endInDoc"],
#   #     reference["entity"],
#   #     "titles",
#   #     referent["title"],
#   #     referent["tconst"],
#   #     referent["titleType"],
#   #     referent["startYear"],
#   #     referent["endYear"],
#   #     referent["genres"]
#   #   ])
#   for instance in epRefs:
#     reference = instance["reference"]
#     referent = instance["referent"]
#     indices.append(reference + referent)
#   # indices = sorted(indices)
#   # print(indices)
#   # indices = sorted(indices, key=lambda x: x["reference"]["startInDoc"])
#   # print(indices)
#   # if there are any references
#   if len(indices) > 0:
#   # doc = soup.find(id="transcript")
#   # doc.append(BeautifulSoup("<p>" + transcript[:references]))
#   # print(OrderedDict(epRefs))
#   # for refType in epRefs:
#     # for ref in epRefs[refType]:
#       # print(ref)
#     # add the transcript up until the first reference
#     lines += transcript[:indices[0][0]]
#     # wrap the reference and add it
#     for i, indexSet in enumerate(indices):
#       # print(i, indexSet)
#       ref = "<span class='ref'>"
#       reference = f"<span class='reference {indexSet[3]}'>{indexSet[2]}</span>";
#       ref += reference
#       popup = "<span class='popup'>"
#       label = "<span class='label'>"
#       if indexSet[3] == "people":
#         label += f"<a href='https://www.imdb.com/name/{indexSet[5]}'>{indexSet[4]}</a></span>"
#       else:
#         label += f"<a href='https://www.imdb.com/title/{indexSet[5]}'>{indexSet[4]}</a></span>"
#       popup += label
#       if indexSet[3] == "titles":
#         popup += f"<span class='titleType'>{indexSet[6]}</span>"
#       years = "<span class='years'>"
#       if indexSet[3] == "people":
#         if indexSet[6] != "\\N":
#           years += str(indexSet[6])
#         years += "&ndash;"
#         if indexSet[7] != "\\N":
#           years += str(indexSet[7])
#       else:
#         if indexSet[7] != "\\N":
#           years += str(indexSet[7])
#         years += "&ndash;"
#         if indexSet[8] != "\\N":
#           years += str(indexSet[8])
#       years += "</span>"
#       popup += years
#       if indexSet[3] == "people":
#         professions = "<span class='profs popupList'>"
#         for p in indexSet[8]:
#           professions += f"<span class='tag prof'>{p}</span>"
#         professions += "</span>"
#         popup += professions
#         knownFor = "<span class='knownFor popupList'>"
#         for k in indexSet[9]:
#           knownFor += f"<span class='tag knownFor'><a href='https://www.imdb.com/title/{k}'>{k}</a></span>"
#         knownFor += "</span>"
#         popup += knownFor
#       if indexSet[3] == "titles":
#         genres = "<span class='genres popupList'>"
#         for g in indexSet[9]:
#           genres += f"<span class='tag genre'>{g}</span>"
#         genres += "</span>"
#         popup += genres
#       popup += "</span>"
#       ref += popup
#       ref += "</span>"
#       lines += ref
#       # continue adding the transcript up until the next reference
#       end = indexSet[1]
#       if (i is not (len(indices) - 1)):
#         # print(indices)
#         # print(indices[i+1])
#         newStart = indices[i+1][0]
#         lines += transcript[end:newStart]
#       else:
#         lines += transcript[end:]
#   # if there are no references
#   else:
#     lines += transcript
#   # wrap lines in p tags
#   lines = re.sub(r'^', "<p>", lines, flags=re.MULTILINE)
#   lines = re.sub(r'$', "</p>", lines, flags=re.MULTILINE)
#   # set up html
#   html = "<!DOCTYPE html>\n<html lang='en'>\n"
#   head = "<head>\n" \
#        + "<meta charset='UTF-8'>\n" \
#        + "<link rel='stylesheet' href='../../assets/styles.css'>\n" \
#        + "</head>\n"
#   html += head
#   body = "<body>\n"
#   body += "<nav id='nav'>\n\
#   <a href='/site/byEntity'>By Entity</a>\n\
#   <a href='/site/byEpisode' class='current'>By Episode</a>\n\
#   <a href='/site/byYear'>By Year</a>\n\
# </nav>\n"
#   body += "<a href='#' id='random'>Random episode</a>\n"
#   nav = "<nav class='epNav'>"
#   # print(epCodes.index(epCode))
#   index = epCodes.index(epCode)
#   if index > 0:
#     # previous
#     prevCode = epCodes[index - 1]
#     nav += f"<a href='../{prevCode}'>← {prevCode.upper()}</a>"
#   if index < len(epCodes) - 1:
#     # next
#     nextCode = epCodes[index + 1]
#     nav += f"<a href='../{nextCode}'>{nextCode.upper()} →</a>"
#   nav += "</nav>\n"
#   body += nav

#   title = f"<h1 id='title'>{epCode.upper()}</h1>\n"
#   body += title

#   summary = "<div id='summary'>\n"
#   summary += "<h2>Summary</h2>\n"
#   nameList = "<ul class='list' id='peopleList'>\n"
#   nameList += "<h3 class='listHeader'>People</h3>\n"
#   for name in nameCounts:
#     nameList += f"<li><span class='entity'>{name}</span><span class='count'>{nameCounts[name]}</span></li>\n"
#   nameList += "</ul>\n"
#   summary += nameList
#   titleList = "<ul class='list' id='titlesList'>\n"
#   titleList += "<h3 class='listHeader'>Titles</h3>\n"
#   for title in titleCounts:
#     titleList += f"<li><span class='entity'>{title}</span><span class='count'>{titleCounts[title]}</span></li>\n"
#   titleList += "</ul>\n"
#   summary += titleList
#   summary += "</div>\n"
#   summary += "<svg>\n\
# <defs>\n\
# <linearGradient id='linGrad'>\n"
#   numStops = 20
#   for x in range(numStops):
#     summary += f"<stop offset='{x / numStops}'/>\n"
#   summary += "<stop offset='1.0'/>"
#   summary += "</linearGradient>\n\
# </defs>\n\
# </svg>\n"
#   body += summary

#   body += "<div id='transcript'>\n"
#   body += lines
#   body += "\n</div>\n"
#   body += nav
#   body += "<script src='https://cdnjs.cloudflare.com/ajax/libs/d3/5.15.0/d3.min.js'></script>\n"
#   body += "<script src='../../assets/scripts.js'></script>\n"
#   body += "</body>\n"
#   html += body
#   html += "</html>"
#   # print(html)
#   # output html file
#   newDir = "./site/byEpisode/ep/" + epCode
#   if not path.exists(newDir):
#     makedirs(newDir)
#   newFile = newDir + "/index.html"
#   with open(newFile, "w") as f:
#     f.write(html.format(htmlText=html))
#     print(f"Successfully saved {epCode} to file {newFile}!")

# def updateIndex(epCodes):
#   indexFile = "./site/byEpisode/index.html"
#   with open(indexFile, "r") as f:
#     soup = BeautifulSoup(f, "html.parser")
#   seasons = soup.find_all(class_="season")
#   for s in seasons:
#     s.ul.clear()
#   for epCode in epCodes:
#     season = epCode[:3]
#     seasonList = soup.find(id=season).ul
#     epItem = soup.new_tag("li")
#     epLink = soup.new_tag("a", href="ep/" + epCode)
#     epLink.string = epCode.upper()
#     epItem.append(epLink)
#     seasonList.append(epItem)
#   soup.prettify()
#   with open(indexFile, "w") as f:
#     f.write(str(soup))
#     print(f"Successfully updated index {indexFile}!")

# def populateAll(epCodes):
#   allFile = "./site/byEpisode/all/index.html"
#   with open(allFile, "r") as f:
#     soup = BeautifulSoup(f, "html.parser")
#   for epCode in epCodes:
#     season = epCode[:3]
#     seasonCont = soup.find(id=season)
#     el = soup.new_tag("div")
#     el["class"] = "episode"
#     heading = BeautifulSoup(f"<h2>{epCode}</h2>")
#     el.append(heading)
#     svg = soup.new_tag("svg")
#     el.append(svg)
#     seasonCont.append(el)
#   with open(allFile, "w") as f:
#     f.write(str(soup))
#     print(f"Successfully updated all page {allFile}!")

# def main(argv):
#   epCodes = sorted([f[:-4] for f in listdir("./transcripts/community/") if path.isfile(path.join("./transcripts/community/", f))])[1:]
#   if len(sys.argv) is 2 and re.match(r"s\d\de\d\d", sys.argv[1]):
#     makeAnnotations(sys.argv[1], epCodes)
#     # updateIndex(epCodes)
#   elif len(sys.argv) is 2 and sys.argv[1] == "all":
#     for epCode in epCodes:
#       makeAnnotations(epCode, epCodes)
#     updateIndex(epCodes)
#   elif len(sys.argv) is 2 and sys.argv[1] == "index":
#     updateIndex(epCodes)
#   elif len(sys.argv) is 2 and sys.argv[1] == "allPage":
#     populateAll(epCodes)
#   else:
#     print("usage: \n\
#   [epCode]: episode to annotate\n\
#   all: annotate all episodes\n\
#   index: update index page\n\
#   allPage: populate page with all episodes")

# if __name__ == "__main__":
#   main(sys.argv)