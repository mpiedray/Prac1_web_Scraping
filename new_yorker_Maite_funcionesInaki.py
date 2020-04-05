#!/usr/bin/env python
# coding: utf8
try:
    import requests, bs4, selenium

except ModuleNotFoundError as error:
    print("No tienes instalado el/los paquete(s)", error)
    pass  # module doesn't exist, deal with it.

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, date, timedelta
import time
import random
import json
import pandas

CONFIG_PATH = "config.json"
SUPPORTED_BROWSERS = ['chrome', 'firefox']

# Lectura de la configuracion desde el fichero config.json
def config():
    with open(CONFIG_PATH) as config_file:
        data = json.load(config_file)
        return data

def config_browser(config):
  # Validate and return the browser choice from the config data
  if 'browser' not in config:
    raise Exception('El archivo de configuracion config.json necesita un elemento "browser" con una seleccion')
  elif config['browser'] not in SUPPORTED_BROWSERS:
    raise Exception(f'"{config["browser"]}" no está soporado')
  return config['browser']

# configuracion que pasamos al 'browser' que utilizaremos en 
def navegador(config):
  if config['browser'] == 'chrome':
      driver = webdriver.Chrome()
  elif config['browser'] == 'Firefox':
      driver = webdriver.Firefox()
  else:
      raise Exception(f'"{config["browser"]}" no está soportado"')
  # driver.implicitly_wait(config['wait_time']) # para forzar esperas
  return driver
  driver.quit()

def año_eval(config):
  if (int(config['seleccion']) > 2007 or int(config['seleccion']) < 2020):
      año = config['seleccion']
  else:
      raise Exception(f'"Selecciona un año entre 2007 y 2020"')
  return int(año)

#año = año_eval(config)
driver = navegador(config())
print("el driver", driver)
año = año_eval(config())

def seleccion_aleatoria_de_ua():
    seleccion_ua = ''
    ua_file = 'ua_list.txt'
    try:
        with open(ua_file) as f:
            lines = f.readlines()
        if len(lines) > 0:
            prng = np.random.RandomState()
            index = prng.permutation(len(lines) - 1)
            idx = np.asarray(index, dtype=np.integer)[0]
            seleccion_ua = lines[int(idx)]
    except Exception as ex:
        print('Se ha producido un error in el generador aleatorio de ua')
        print(str(ex))
    finally:
        return seleccion_ua

user_agent = seleccion_aleatoria_de_ua()
headerstest = {
        'user-agent': user_agent,
    }


def getInfoMetadatos(url):
	result = requests.get(url, headers=headerstest)
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


def Loslunes(year):
    d = date(year, 1, 1)                    # Uno de Enero del año pasado como parámetro
    d += timedelta(days = 7 - d.weekday())  # Primer Lunes
    while d.year == year:
        yield str(d)
        d += timedelta(days = 7)
# Inicializamos los lunes
lunes = []

''' Preguntamos al usuario por un año en concreto para calcular las 54 fechas de los Lunes '''
''' Para esta práctica únicamente ejecutamos una fecha. Se podría descomentar para bajar un año completo.'''

for d in Loslunes(año):
   lunestemporal = "https://www.newyorker.com/culture/cover-story/cover-story-" + str(d)
   lunes.append(lunestemporal)
print("Los lunes", lunes)
# Elegimos una fecha al azar (random) como prueba e imprimimos por pantalla.
#url1 = random.choice(lunes)
#print("La url seleccionada es:", url1)

resultados = []
#print(getInfoMetadatos(url1))
#print("Los Lunes del año son:", lunes )
for x in lunes:
	salida = getInfoMetadatos(x)
	resultados.append(salida)
	#resultados.update(salida)
#		ficheroJSON = json.dump(resultados, file_write)
# with open('resultados.json', "w") as file_write:
#resultados=dict(resultados)
with open('resultados.json', "w") as file_write:
	ficheroJSON = json.dump(resultados, file_write, ensure_ascii=True, allow_nan=True)


#dfresultadosscrap = pandas.DataFrame.from_dict(resultados, orient="columns")
#print(dfresultadosscrap.T)
   
''' def createDate():
	dt_string = "2017-01-01"

	# Considering date is in dd/mm/yyyy format
	#initial_date = datetime.strptime(dt_string, "%Y-%m-%d").date()
	final_date = date.today().strftime("%Y-%m-%d")

	sdate = date(2016, 1, 1)   # start date
	edate = date.today()   # end date

	sdate += timedelta(days=1-sdate.isoweekday())

	while sdate <= edate :
		current_monday = sdate.strftime("%Y-%m-%d")
		sdate += timedelta(days=7)
		url1 = "https://www.newyorker.com/culture/cover-story-" + current_monday
		print("La url de Maite", url1)

year = '2019'
dates_09 = [{'month': '09' ,'mondays':['02','09','16','23','30']}, 
						{'month': '10' ,'mondays':['07','14','21','28']},
						{'month': '11' ,'mondays':['04','11','18','28']},
						{'month': '12' ,'mondays':['02','09','16','23','30']},]
'''