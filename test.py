import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime, date, timedelta

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
    */*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "no-cache",
    "dnt": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\
    37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}

headers1 = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.2704.103 Safari/537.36'}


def loadCSVFile(data):
    data = json.loads(data)
    csv_file = csv.writer(
        open("new_yorker.csv", "w", newline='', encoding='utf-8'))
    # fieldnames = ["fecha", "autor_critica", "autor_portada", "nombre_portada",
    #               "url", "url_imagen", "news_keywords", "keywords", "descripcion", "id"]

    for item in data:
        csv_file.writerow({item["fecha"],
                           item["autor_critica"],
                           item["autor_portada"],
                           item["nombre_portada"],
                           item["url"],
                           item["image-16-9"],
                           item["news_keywords"],
                           item["keywords"],
                           item["descripcion"],
                           item["id"]})

    #print("-- CSV Created --")


def getInfoStructureDOM(url, fecha):
    url_final = url + fecha
    result = requests.get(url_final, headers=headers1)

    if result.status_code != 200:
        url_final = url + "cover-story-" + fecha
        result = requests.get(url_final, headers=headers1)

    if result.status_code == 200:
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        datos = {}

        fecha = soup.time.text
        au_critica = soup.find("a", {"class": "byline__name-link"}).text

        datos["fecha"] = fecha if len(fecha) > 0 else ''
        datos["autor_critica"] = au_critica if len(au_critica) > 0 else ''

        name_datos = soup.h1.text.split('“')

        datos["autor_portada"] = name_datos[0].strip() if len(
            name_datos[0].strip()) > 0 else ''
        datos["nombre_portada"] = name_datos[1].split('”')[0].strip() if len(
            name_datos[1].split('”')[0].strip()) > 0 else ''

        current_url = soup.find("meta", property="og:url")
        datos['url'] = current_url["content"] if len(
            current_url["content"]) > 0 else ''

        image = soup.find("meta", property="og:image")
        datos["image-16-9"] = image["content"] if len(
            image["content"]) > 0 else ''

        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            if meta.get('name') == 'news_keywords':
                datos['news_keywords'] = meta.get('content') if len(
                    meta.get('content')) > 0 else ''

            if meta.get('name') == 'keywords':
                datos['keywords'] = meta.get('content') if len(
                    meta.get('content')) > 0 else ''

            if meta.get('name') == 'description':
                datos['descripcion'] = meta.get('content') if len(
                    meta.get('content')) > 0 else ''

            if meta.get('name') == 'id':
                datos['id'] = meta.get('content') if len(
                    meta.get('content')) > 0 else ''

        print(datos['url'] + "-- DONE --")
        return datos


def createDate():
    dt_string = "2017-01-01"
    # Considering date is in dd/mm/yyyy format
    # initial_date = datetime.strptime(dt_string, "%Y-%m-%d").date()
    final_date = date.today().strftime("%Y-%m-%d")

    result = []

    # sdate = date(2007, 1, 1)   # start date
    # edate = date.today()   # end date

    # datos de prueb solo el ano 2018
    sdate = date(2018, 1, 1)
    edate = date(2019, 1, 1)

    sdate += timedelta(days=1 - sdate.isoweekday())

    while sdate <= edate:
        current_monday = sdate.strftime("%Y-%m-%d")
        sdate += timedelta(days=7)
        url_base = "https://www.newyorker.com/culture/cover-story/"
        salida = getInfoStructureDOM(url_base, current_monday)
        if salida is not None:
            result.append(salida)

    # print(result)
    loadCSVFile(json.dumps(result))
    #print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))


# initial_code
createDate()
#url_base = "https://www.newyorker.com/culture/cover-story/cover-story-"
# url = "https://www.newyorker.com/culture/cover-story/cover-story-2018-10-08"
#getInfoStructureDOM(url_base, '2018-10-08')
