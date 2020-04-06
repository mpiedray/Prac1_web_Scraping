import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import time
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


def createDataFrame(data):
    df = pd.DataFrame(data, columns=["fecha", "autor_critica", "autor_portada", "nombre_portada",
                                     "url", "url_imagen", "news_keywords", "keywords", "descripcion", "id"])
    df.to_csv(r'new_yorker.csv', index=False)


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

        fecha = soup.time.text.split(",")[0] + soup.time.text.split(",")[1]
        # cambiamos la forma de mostrar la fecha
        conv = time.strptime(fecha, "%B %d %Y")
        fecha_cambiada = time.strftime("%Y-%m-%d", conv)

        au_critica = soup.find("a", {"class": "byline__name-link"}).text

        datos["fecha"] = fecha_cambiada if len(fecha_cambiada) > 0 else ''
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
    createDataFrame(result)
    #print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))


def formatingDate(user_date):
    user_date = str(user_date).strip()
    if user_date.strip() == "":
        sdate = date(2007, 1, 1)   # start date
        edate = date.today()   # end date

    elif user_date.find(":") >= 0 or len(user_date) == 4:
        if len(user_date) > 4:
            if user_date.find(":") >= 0:
                if user_date.find("-") >= 0:
                    try:
                        inicio = user_date.split(":")[0]
                        final = user_date.split(":")[1]

                        sdate = date(
                            int(inicio.split("-")[1]), int(inicio.split("-")[0]), 1)
                        edate = date(
                            int(final.split("-")[1]), int(final.split("-")[0]), 1)
                        # TODO COMPROBAR QUE SDATE ES MENOR QUE EDATE
                    except IndexError:
                        print("Se han introducido mal los valores de la fecha")
                    except:
                        print("Un Error inesperado ha ocurrido")
                else:
                    try:
                        sdate = date(int(user_date.split(":")[0]), 1, 1)
                        edate = date(int(user_date.split(":")[1]), 12, 31)
                    except ValueError:
                        print("Los valores proporcionados no son válidos")
                    except:
                        print("Un Error inesperado ha ocurrido")

        if len(user_date) == 4:
            try:
                user_date = int(user_date)
                sdate = date(user_date, 1, 1)   # start date
                edate = date.today()   # end date
            except ValueError:
                print("Los valores proporcionados no son válidos")
            except:
                print("Un Error inesperado ha ocurrido")
    elif user_date.find("-") >= 0 and len(user_date) > 4:
        try:
            myMonday = user_date.split("-")
            sdate = date(int(myMonday[0]), int(myMonday[1]), int(myMonday[2]))
            edate = ''
        except IndexError:
            print("Se han introducido mal los valores de la fecha al introducir un lunes")
        except:
            print("Un Error inesperado ha ocurrido")


def initialProgram():
    opc = input(
        "Bienvenido a la practica 1 de Tipología y ciclo de vida de los dato, \n Debe saber que esta práctica extrae informacion del magazine New Yorker \n" +
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
        createDate(monday)
    elif opc == "4":
        print("Ha elegido la opción 4, Salir del programa, Hasta pronto!... ")
    else:
        print("La opcion seleccionada no es correcta, por favor vuelva a intentarlo.")


# initial_code
initialProgram()
#url_base = "https://www.newyorker.com/culture/cover-story/cover-story-"
# url = "https://www.newyorker.com/culture/cover-story/cover-story-2018-10-08"
#getInfoStructureDOM(url_base, '2018-10-08')
