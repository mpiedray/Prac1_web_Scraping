import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, date, timedelta

def getInfoMetadatos(url):
	result = requests.get(url)
	datos = {}
	if result.status_code == 200 :
		src = result.content
		soup = BeautifulSoup(src, 'lxml')
		
		subcadena = " “"
		inicio_subcadena = "image-16-9"
		fin_subcadena = "image-1-1"
		# coger la informacion a travez de los metas.
		meta_tags = soup.find_all('meta')
		

		for meta in meta_tags:
			#print(meta)
			#print(meta.get('name'))
			if meta.get('name') == 'author':
				datos['author_critica'] = meta.get('content')
			if meta.get('name') == 'description':
				datos['description'] = meta.get('content')
			if meta.get('name') == 'id':
				datos['id']= meta.get('content')
			if meta.get('name') == 'keywords':
				datos['keywords'] = meta.get('content')
			if meta.get('name') == 'news_keywords':
				datos['news_keywords'] = meta.get('content')
			if meta.get('name') == 'parsely-metadata':
				multiple_info = meta.get('content') #image-16-9 para coger la imagen
				inicio_pos_img = multiple_info.find(inicio_subcadena)
				final_pos_img = multiple_info.find(fin_subcadena)
				temp_url = multiple_info[inicio_pos_img : final_pos_img-1]
				temp_url = temp_url[multiple_info.find(":") -1 : len(temp_url) -2]
				datos['image-16-9'] = temp_url

			current_title = soup.find("meta", property="og:title")
			current_title = current_title["content"]

			pos = current_title.find(subcadena)
			datos['autor_portada'] =  current_title[0: pos-1]
			datos['nombre_portada'] = current_title[pos:len(current_title)]

			current_url = soup.find("meta", property="og:url")
			datos['url'] = current_url["content"]

	return datos

					


def getInfoStructure(url):
	result = requests.get(url)
	if result.status_code == 200 :
		src = result.content
		soup = BeautifulSoup(src, 'lxml')
		# ver lo que he capturado con formato
		#print(soup.prettify())

		# primera ocurrencia de h1 y lo mismo es soup.find('h1')
		print(soup.h1.text)

		print(soup.h1.name)
		#print(soup.find_all('picture'))

#https://www.newyorker.com/culture/cover-story/2020-03-30
#https://www.newyorker.com/culture/cover-story/cover-story-2020-04-06
#https://www.newyorker.com/culture/cover-story/2020-03-23
#https://www.newyorker.com/culture/cover-story/cover-story-2020-03-09

#https://www.newyorker.com/magazine/2020/03/09

def createDate():
	dt_string = "2017-01-01"

	# Considering date is in dd/mm/yyyy format
	#initial_date = datetime.strptime(dt_string, "%Y-%m-%d").date()
	final_date = date.today().strftime("%Y-%m-%d")

	sdate = date(2007, 1, 1)   # start date
	edate = date.today()   # end date

	sdate += timedelta(days=1-sdate.isoweekday())

	while sdate <= edate :
		current_monday = sdate.strftime("%Y-%m-%d")
		sdate += timedelta(days=7)
		url = "https://www.newyorker.com/culture/cover-story/" + current_monday
		print(url)

year = '2019'
dates_09 = [{'month': '09' ,'mondays':['02','09','16','23','30']}, 
						{'month': '10' ,'mondays':['07','14','21','28']},
						{'month': '11' ,'mondays':['04','11','18','28']},
						{'month': '12' ,'mondays':['02','09','16','23','30']},  
						]


createDate()
# url = url + year
# result = []
# for x in dates_09:
# 	final = ''
# 	for j in x['mondays']:
# 		final= url + '-' + x['month'] + '-' + j
# 		print(final)
# 		salida = getInfoMetadatos(final)
# 		result.append(salida)


#print(fecha_inicio)





