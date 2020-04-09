import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import time
from datetime import datetime, date, timedelta
import random


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.2704.103 Safari/537.36'}


def createDataFrame(data, name_csv):
    df = pd.DataFrame(data, columns=["fecha", "autor_critica", "autor_portada", "titulo_portada",
                                     "url", "url_imagen", "news_keywords", "keywords", "descripcion", "id"])
    # with open(name_csv + '.json', 'w') as f:
    #     json.dump(data, f, ensure_ascii=False)
    df.to_csv(name_csv + '.csv', index=False, encoding='utf-8')


# def TakeInfo(url):


def getInfoStructureDOM(url, fecha):
    url_final = url + fecha
    print("-- leyendo datos --" + url_final)
    result = requests.get(url_final, headers=headers)

    if result.status_code == 200:
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        datos = {}
        link = soup.find(
            "span", {"class": "ImageCaption__caption___1EOQO ImageCaption__caption___1EOQO"})
        if link is not None:
            if len(soup.find("span", {"class": "ImageCaption__caption___1EOQO ImageCaption__caption___1EOQO"}).findAll("a")) > 0:
                print('nuevo')
                fecha_entrada = soup.find("div", {"class": "MagazineHeader__header___2wMTg"}).find(
                    "h2", recursive=False)

                nombre = soup.find("span", {"class": "ImageCaption__caption___1EOQO ImageCaption__caption___1EOQO"}).find(
                    "p", recursive=False)
                image = soup.find("picture", {
                                  "class": "component-responsive-image"}).find("img", recursive=False)
                enlace = soup.find("span", {
                                   "class": "ImageCaption__caption___1EOQO ImageCaption__caption___1EOQO"}).find("a")

                current_url = enlace['href'] if len(
                    enlace['href']) > 0 else 'missing'

                datos['url'] = current_url
                if fecha_entrada is not None:
                    datos['fecha'] = fecha_entrada.text if len(
                        fecha_entrada.text) > 0 else 'missing'

                if nombre is not None:
                    datos['autor_critica'] = nombre.text if len(
                        nombre.text) > 0 else 'missing'

                if image is not None:
                    datos['url_imagen'] = image['src'] if len(
                        image['src']) > 0 else 'missing'

                # if current_url > 0
                #     obj = TakeInfo(current_url)
            else:
                print('viejo')
                fecha_entrada = soup.find("div", {"class": "MagazineHeader__header___2wMTg"}).find(
                    "h2", recursive=False)

                nombre = soup.find("span", {"class": "ImageCaption__caption___1EOQO ImageCaption__caption___1EOQO"}).find(
                    "p", recursive=False)
                image = soup.find("picture", {
                                  "class": "component-responsive-image"}).find("img", recursive=False)
                if fecha_entrada is not None:
                    datos['fecha'] = fecha_entrada.text if len(
                        fecha_entrada.text) > 0 else 'missing'

                if nombre is not None:
                    datos['autor_critica'] = nombre.text if len(
                        nombre.text) > 0 else 'missing'

                if image is not None:
                    datos['url_imagen'] = image['src'] if len(
                        image['src']) > 0 else 'missing'
                datos['autor_portada'] = 'missing'
                datos['titulo_portada'] = 'missing'
                datos['url'] = 'missing'
                datos['news_keywords'] = 'missing'
                datos['keywords'] = 'missing'
                datos['descripcion'] = 'missing'
                datos['id'] = 'missing'
        else:
            print('No tengo nombre')
            fecha_entrada = soup.find("div", {"class": "MagazineHeader__header___2wMTg"}).find(
                "h2", recursive=False)

            image = soup.find("picture", {
                              "class": "component-responsive-image"}).find("img", recursive=False)
            if fecha_entrada is not None:
                datos['fecha'] = fecha_entrada.text if len(
                    fecha_entrada.text) > 0 else 'missing'
            datos['autor_critica'] = 'missing'

            if image is not None:
                datos['imagen'] = image['src'] if len(
                    image['src']) > 0 else 'missing'
            datos['autor_portada'] = 'missing'
            datos['titulo_portada'] = 'missing'
            datos['url'] = 'missing'
            datos['news_keywords'] = 'missing'
            datos['keywords'] = 'missing'
            datos['descripcion'] = 'missing'
            datos['id'] = 'missing'

        # fecha = soup.time.text.split(",")[0] + soup.time.text.split(",")[1]
        # # cambiamos la forma de mostrar la fecha
        # conv = time.strptime(fecha, "%B %d %Y")
        # fecha_cambiada = time.strftime("%Y-%m-%d", conv)

        # au_critica = soup.find("a", {"class": "byline__name-link"}).text

        # datos["fecha"] = fecha_cambiada if len(
        #     fecha_cambiada) > 0 else 'missing'
        # datos["autor_critica"] = au_critica if len(
        #     au_critica) > 0 else 'missing'

        # name_datos = soup.h1.text.split('“')

        # datos["autor_portada"] = name_datos[0].strip() if len(
        #     name_datos[0].strip()) > 0 else ''
        # datos["nombre_portada"] = name_datos[1].split('”')[0].strip() if len(
        #     name_datos[1].split('”')[0].strip()) > 0 else 'missing'

        # current_url = soup.find("meta", property="og:url")
        # datos['url'] = current_url["content"] if len(
        #     current_url["content"]) > 0 else 'missing'

        # image = soup.find("meta", property="og:image")
        # datos["image-16-9"] = image["content"] if len(
        #     image["content"]) > 0 else 'missing'

        # meta_tags = soup.find_all('meta')
        # for meta in meta_tags:
        #     if meta.get('name') == 'news_keywords':
        #         datos['news_keywords'] = meta.get('content') if len(
        #             meta.get('content')) > 0 else 'missing'

        #     if meta.get('name') == 'keywords':
        #         datos['keywords'] = meta.get('content') if len(
        #             meta.get('content')) > 0 else 'missing'

        #     if meta.get('name') == 'description':
        #         datos['descripcion'] = meta.get('content') if len(
        #             meta.get('content')) > 0 else 'missing'

        #     if meta.get('name') == 'id':
        #         datos['id'] = meta.get('content') if len(
        #             meta.get('content')) > 0 else 'missing'

        print(url_final + "-- DONE --")
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
    # sdate = date(2008, 1, 1)
    sdate = date(2011, 1, 1)
    edate = date(2011, 12, 31)

    sdate += timedelta(days=1 - sdate.isoweekday())

    while sdate <= edate:
        current_monday = sdate.strftime("%Y/%m/%d")
        sdate += timedelta(days=7)
        url_base = "https://www.newyorker.com/magazine/"
        sec_sleep = random.randint(1, 5)
        time.sleep(sec_sleep)
        salida = getInfoStructureDOM(url_base, current_monday)
        if salida is not None:
            result.append(salida)

    print(result)
    name_csv = str(sdate.year) + '_' + str(edate.year) + '_' + 'newYorker'
    print(name_csv)
    createDataFrame(result, name_csv)
    # print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))


# initial_code
createDate()


# def drug_data():
#     url = 'https://www.newyorker.com/culture/cover-story'

#     while url:
#         print(url)
#         r = requests.get(url, headers=headers1)
#         soup = BeautifulSoup(r.text, "lxml")
#         url = soup.findAll('a', {'class': 'Link__link___3dWao', 'rel': 'next'})
#         print(url)
#         if url:
#             url = 'https://www.newyorker.com/' + \
#                 url[0].get('href')
#         else:
#             break


# drug_data()
