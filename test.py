import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import time
from datetime import datetime, date, timedelta


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.2704.103 Safari/537.36'}


def createDataFrame(data):
    df = pd.DataFrame(data, columns=["fecha", "autor_critica", "autor_portada", "nombre_portada",
                                     "url", "url_imagen", "news_keywords", "keywords", "descripcion", "id"])
    df.to_csv(r'new_yorker.csv', index=False)


def getInfoStructureDOM(url, fecha):
    print("-- leyendo datos --" + url)
    url_final = url + fecha
    result = requests.get(url_final, headers=headers)

    if result.status_code != 200:
        url_final = url + "cover-story-" + fecha
        result = requests.get(url_final, headers=headers)

    if result.status_code == 200:
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        datos = {}

        fecha = soup.time.text.split(",")[0] + soup.time.text.split(",")[1]
        # cambiamos la forma de mostrar la fecha
        conv = time.strptime(fecha, "%B %d %Y")
        fecha_cambiada = time.strftime("%Y-%m-%d", conv)

        au_critica = soup.find("a", {"class": "byline__name-link"}).text

        datos["fecha"] = fecha_cambiada if len(fecha_cambiada) > 0 else 'NA'
        datos["autor_critica"] = au_critica if len(au_critica) > 0 else 'NA'

        name_datos = soup.h1.text.split('“')

        datos["autor_portada"] = name_datos[0].strip() if len(
            name_datos[0].strip()) > 0 else ''
        datos["nombre_portada"] = name_datos[1].split('”')[0].strip() if len(
            name_datos[1].split('”')[0].strip()) > 0 else 'NA'

        current_url = soup.find("meta", property="og:url")
        datos['url'] = current_url["content"] if len(
            current_url["content"]) > 0 else 'NA'

        image = soup.find("meta", property="og:image")
        datos["image-16-9"] = image["content"] if len(
            image["content"]) > 0 else 'NA'

        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            if meta.get('name') == 'news_keywords':
                datos['news_keywords'] = meta.get('content') if len(
                    meta.get('content')) > 0 else 'NA'

            if meta.get('name') == 'keywords':
                datos['keywords'] = meta.get('content') if len(
                    meta.get('content')) > 0 else 'NA'

            if meta.get('name') == 'description':
                datos['descripcion'] = meta.get('content') if len(
                    meta.get('content')) > 0 else 'NA'

            if meta.get('name') == 'id':
                datos['id'] = meta.get('content') if len(
                    meta.get('content')) > 0 else 'NA'

        print(datos['url'] + "-- DONE --")
        return datos


def createDate(fechas):
    result = []
    url_base = "https://www.newyorker.com/culture/cover-story/"
    if fechas[1] != '':
        sdate = fechas[0]
        edate = fechas[1]

        sdate += timedelta(days=1 - sdate.isoweekday())

        while sdate <= edate:
            current_monday = sdate.strftime("%Y-%m-%d")
            sdate += timedelta(days=7)

            salida = getInfoStructureDOM(url_base, current_monday)
            if salida is not None:
                result.append(salida)
    else:

        current_monday = fechas[0].strftime("%Y-%m-%d")
        print(current_monday)
        salida = getInfoStructureDOM(url_base, current_monday)
        if salida is not None:
            result.append(salida)

    # print(result)
    createDataFrame(result)
    #print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))


def formatingDate(user_date):
    fechas = []
    user_date = str(user_date).strip()
    sdate = ''
    edate = ''
    try:
        if user_date.strip() == "":
            sdate = date(2007, 1, 1)   # start date
            edate = date.today()   # end date
        elif user_date.find(":") >= 0 or len(user_date) == 4:
            if len(user_date) > 4:
                if user_date.find(":") >= 0:
                    if user_date.find("-") >= 0:
                        inicio = user_date.split(":")[0]
                        final = user_date.split(":")[1]

                        sdate = date(
                            int(inicio.split("-")[1]), int(inicio.split("-")[0]), 1)
                        edate = date(
                            int(final.split("-")[1]), int(final.split("-")[0]), 1)
                        # TODO COMPROBAR QUE SDATE ES MENOR QUE EDATE
                    else:
                        mydate = user_date.split(":")
                        if mydate[0] < mydate[1]:
                            sdate = date(int(mydate[0]), 1, 1)
                            edate = date(int(mydate[1]), 12, 31)
                        else:
                            sdate = date(int(mydate[1]), 1, 1)
                            edate = date(int(mydate[0]), 12, 31)
            if len(user_date) == 4:
                user_date = int(user_date)
                sdate = date(user_date, 1, 1)   # start date
                edate = date.today()   # end date
        elif user_date.find("-") >= 0 and len(user_date) > 4:
            myMonday = user_date.split("-")
            sdate = date(int(myMonday[0]), int(myMonday[1]), int(myMonday[2]))
        else:
            print("Formato no valido")
    except IndexError:
        print("Se han introducido mal los valores de la fecha")
        sdate = ''
        edate = ''
    except ValueError:
        print("Los valores proporcionados no son válidos")
        sdate = ''
        edate = ''
    except:
        print("Un Error inesperado ha ocurrido")
        sdate = ''
        edate = ''

    # es la misma fecha
    if edate != '':
        if edate < sdate:
            item = sdate
            sdate = edate
            edate = item

    fechas.append(sdate)
    fechas.append(edate)
    createDate(fechas)


def initialProgram():
    opc = input(
        "Bienvenido a la practica 1 de Tipología y ciclo de vida de los dato, \nDebe saber que esta práctica extrae informacion del magazine New Yorker \n" +
        "Esta revista publica todos los lunes de mes, así que  si desea in dia en concreto debe ser un Lunes, para que la busqueda devuelva datos. \n" +
        "El formato de entrada que esperamos es una fecha, con el siguiente formato Año-mes-dia, o solo el Año según la opción.  \n" +
        "En esta practica dispones de varias opciones para extraer los datos \n" +
        "Las opciones de las que dispone son las siguientes: \n" +
        "1. - Todos los datos desde 2007 hasta la fecha actual \n" +
        "2. - Un periodo determinado de tiempo, por ejemplo si desea desde el año 2015 en adelante solo escriba 2015 \n" +
        "Si desea un rango de tiempo por ejemplo desde 2015 hasta 2017, escriba 2015:2017 \n" +
        "Si desea solo los últimos 6 meses de 2015  debe escribir 06-2015:12-2015 \n" +
        "3. - Un Lunes concreto, en el siguiente formato Año-mes-dia \n" +
        "4. - Salir del programa \n" +
        "Elija una opción:  \n")

    if opc == "1":
        print("Ha elegido la opción 1, todos los datos desde 2007 hasta la fecha actual")
        fecha = ""
        formatingDate(fecha)
    elif opc == "2":
        print("Ha elegido la opción 2, un rango de tiempo")
        fecha_rango = input(
            "Ejemplo de entrada de datos: \n" +
            "Si desea desde el año 2015 en adelante solo escriba solo 2015 \n" +
            "Si desea un rango de tiempo por ejemplo desde 2015 hasta 2017, escriba 2015:2017 \n" +
            "Si desea solo los últimos 6 meses de 2015  debe escribir 06-2015:12-2015 \n")
        formatingDate(fecha_rango)
    elif opc == "3":
        print("Ha elegido la opción 3, una fecha en concreto")
        monday = input(
            "Ejemplo de entrada de datos: \n" +
            "Un Lunes concreto, en el siguiente formato Año-mes-dia \n")
        formatingDate(monday)
    elif opc == "4":
        print("Ha elegido la opción 4, Salir del programa, Hasta pronto!... ")
    else:
        print("La opcion seleccionada no es correcta, por favor vuelva a intentarlo.")


# initial_code
initialProgram()
#url_base = "https://www.newyorker.com/culture/cover-story/cover-story-"
# url = "https://www.newyorker.com/culture/cover-story/cover-story-2018-10-08"
#getInfoStructureDOM(url_base, '2018-10-08')


# 3 julio 2017 https://www.newyorker.com/culture/cover-story/kadir-nelsons-bright-star
# https://www.newyorker.com/culture/culture-desk/cover-story-2016-07-11
# https://www.newyorker.com/culture/culture-desk/cover-story-2016-06-27
# https://www.newyorker.com/culture/culture-desk/cover-story-2016-06-27
# https://www.newyorker.com/culture/cover-story/cover-story-2019-02-04
# https://www.newyorker.com/culture/cover-story/cover-story-2019-08-5


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
