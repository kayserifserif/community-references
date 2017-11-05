from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

films = []

# scrape data
def scrape(webpage):
	page = urlopen(webpage)
	soup = BeautifulSoup(page, 'html.parser')
	sources = soup.select('.film-detail-content')
	# title_tags = soup.select('.film-detail-content h2 > a')
	# year_tags = soup.select('.film-detail-content h2 small a')
	for source in sources:
		film = {}
		film['title'] = source.contents[1].contents[0].contents[0]
		film['year'] = int(source.contents[1].contents[2].contents[0].contents[0])
		comment = ''
		try:
			for element in source.contents[5].contents[1].contents:
				comment += str(element)
		except:
			for element in source.contents[3].contents[1].contents:
				comment += str(element)
		else:
			pass
		film['comment'] = comment
		films.append(film)

def export():
	with open('letterboxd.csv', 'w') as csv_file:
		fieldnames = ['title', 'year', 'comment']
		writer = csv.DictWriter(csv_file, fieldnames)
		writer.writeheader()
		writer.writerows(films)

scrape('https://letterboxd.com/bookwormgirl910/list/communitys-pop-culture-references/detail/')
scrape('https://letterboxd.com/bookwormgirl910/list/communitys-pop-culture-references/detail/page/2/')
# print(films)
export()