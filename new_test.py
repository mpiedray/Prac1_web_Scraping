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
    df = pd.DataFrame(data, columns=["fecha", "autor_portada", "nombre portada", "autor_critica", "nombre_critica"
                                     "url", "url_imagen", "news_keywords", "keywords", "descripcion", "id"])
    # with open(name_csv + '.json', 'w') as f:
    #     json.dump(data, f, ensure_ascii=False)
    df.to_csv(name_csv + '.csv', index=False, encoding='utf-8')


def TakeInfo(url):
    result_info = requests.get(url, headers=headers)
    if result_info.status_code == 200:
        src_info = result_info.content
        soup_info = BeautifulSoup(src_info, 'lxml')
        more_info = {}
        autores_critica = ''

        if len(soup_info.findAll("a", {"class": "byline__name-link"})) > 0:
            ac = soup_info.findAll("a", {"class": "byline__name-link"})
            for item in ac:
                au_critica = autores_critica + item.text

        more_info['autor_critica'] = au_critica

        if len(soup_info.h1) > 0:
            nombre_critica_completo = soup_info.h1.text
            texto_buscar = 'Cover Story:'
            if texto_buscar in nombre_critica_completo:
                nombre_critica = nombre_critica_completo.split(':')[1]

        more_info['nombre_critica'] = nombre_critica

        meta_tags = soup_info.find_all('meta')
        if len(meta_tags) > 0:
            for meta in meta_tags:
                if meta.get('name') == 'news_keywords':
                    more_info['news_keywords'] = meta.get('content') if len(
                        meta.get('content')) > 0 else 'missing'

                if meta.get('name') == 'keywords':
                    more_info['keywords'] = meta.get('content') if len(
                        meta.get('content')) > 0 else 'missing'

                if meta.get('name') == 'description':
                    more_info['descripcion'] = meta.get('content') if len(
                        meta.get('content')) > 0 else 'missing'

                if meta.get('name') == 'id':
                    more_info['id'] = meta.get('content') if len(
                        meta.get('content')) > 0 else 'missing'
        else:
            more_info['news_keywords'] = 'missing'
            more_info['keywords'] = 'missing'
            damore_infotos['descripcion'] = 'missing'
            more_info['id'] = 'missing'

    return more_info


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
                fe = soup.find(
                    "div", {"class": "MagazineHeader__header___2wMTg"}).findAll("h2")
                if len(fe) == 2:
                    fecha_entrada = fe[1].text
                else:
                    fecha_entrada = fe[0].text

                nombre = soup.find("span", {"class": "ImageCaption__caption___1EOQO ImageCaption__caption___1EOQO"}).find(
                    "p", recursive=False)
                image = soup.find("picture", {
                                  "class": "component-responsive-image"}).find("img", recursive=False)
                enlace = soup.find("span", {
                                   "class": "ImageCaption__caption___1EOQO ImageCaption__caption___1EOQO"}).find("a")

                current_url = enlace['href'] if len(
                    enlace['href']) > 0 else 'missing'

                datos['url'] = current_url
                if fe is not None:

                    fecha_entrada = fecha_entrada if len(
                        fecha_entrada) > 0 else 'missing'

                    parte1 = fecha_entrada.split(',')[0].strip()
                    parte2 = fecha_entrada.split(',')[1].strip()
                    fecha_entrada = parte1 + parte2

                    datos['fecha'] = fecha_entrada

                if nombre is not None:
                    datos_persona = nombre.text
                    np = datos_persona.split('by')[0].strip()
                    ap = datos_persona.split('by')[1].strip()

                    datos['autor_portada'] = ap if len(
                        ap) > 0 else 'missing'

                    datos['titulo_portada'] = np if len(
                        np) > 0 else 'missing'

                if image is not None:
                    datos['url_imagen'] = image['src'] if len(
                        image['src']) > 0 else 'missing'

                if current_url != 'missing':
                    obj = TakeInfo(current_url)

                    datos['autor_critica'] = obj['autor_critica']
                    datos['nombre_critica'] = obj['nombre_critica']
                    datos['news_keywords'] = obj['news_keywords']
                    datos['keywords'] = obj['keywords']
                    datos['descripcion'] = obj['descripcion']
                    datos['id'] = obj['id']
            else:
                print('viejo')
                fe = soup.find(
                    "div", {"class": "MagazineHeader__header___2wMTg"}).findAll("h2")
                if len(fe) == 2:
                    fe = fe[1].text
                else:
                    fe = fe[0].text

                parte1 = fe.split(',')[0].strip()
                parte2 = fe.split(',')[1].strip()
                fecha_entrada = parte1 + parte2

                nombre = soup.find("span", {"class": "ImageCaption__caption___1EOQO ImageCaption__caption___1EOQO"}).find(
                    "p", recursive=False)
                image = soup.find("picture", {
                                  "class": "component-responsive-image"}).find("img", recursive=False)

                if fe is not None:
                    fecha_entrada = fecha_entrada if len(
                        fecha_entrada) > 0 else 'missing'

                datos['fecha'] = fecha_entrada

                if nombre is not None:
                    datos_persona = nombre.text
                    np = datos_persona.split('by')[0].strip()
                    ap = datos_persona.split('by')[1].strip()

                    datos['autor_portada'] = ap if len(
                        ap) > 0 else 'missing'

                    datos['titulo_portada'] = np if len(
                        np) > 0 else 'missing'

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
            fe = soup.find(
                "div", {"class": "MagazineHeader__header___2wMTg"}).findAll("h2")
            if len(fe) == 2:
                fecha_entrada = fe[1].text
            else:
                fecha_entrada = fe[0].text

            image = soup.find("picture", {
                              "class": "component-responsive-image"}).find("img", recursive=False)

            if fe is not None:
                fecha_entrada = fecha_entrada if len(
                    fecha_entrada) > 0 else 'missing'

                parte1 = fecha_entrada.split(',')[0].strip()
                parte2 = fecha_entrada.split(',')[1].strip()
                fecha_entrada = parte1 + parte2

                datos['fecha'] = fecha_entrada

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
    edate = date(2011, 9, 30)

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
    createDataFrame(result, name_csv)
    # print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))


# initial_code
createDate()
