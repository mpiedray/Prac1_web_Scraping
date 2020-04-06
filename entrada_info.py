import time
from datetime import datetime, date, timedelta
# opc = input(
#     "Bienvenido a la practica 1 de Tipología y ciclo de vida de los dato, \n Debe saber que esta práctica extrae informacion del magazine New Yorker \n" +
#     "Esta revista publica todos los lunes de mes, así que  si desea in dia en concreto debe ser un Lunes, para que la busqueda devuelva datos. \n" +
#     "El formato de entrada que esperamos es una fecha, con el siguiente formato Año-mes-dia, o solo el Año según la opción.  \n" +
#     "En esta practica dispones de varias opciones para extraer los datos \n" +
#     "Las opciones de las que dispone son las siguientes: \n" +
#     "1. - Todos los datos desde 2007 hasta la fecha actual \n" +
#     "2. - Un periodo determinado de tiempo, por ejemplo si desea desde el año 2015 en adelante solo escriba 2015 \n" +
#     "Si desea un rango de tiempo por ejemplo desde 2015 hasta 2017, escriba 2015:2017 \n" +
#     "Si desea solo los últimos 6 meses de 2015  debe escribir 06-2015:12-2015 \n" +
#     "3. - Un Lunes concreto, en el siguiente formato Año-mes-dia \n" +
#     "4. - Salir del programa \n" +
#     "Elija una opción:  \n")

# if opc == "1":
#     print("Ha elegido la opción 1, todos los datos desde 2007 hasta la fecha actual")
#     fecha = ""
# elif opc == "2":
#     print("Ha elegido la opción 2, un rango de tiempo")
#     fecha_rango = input(
#         "Ejemplo de entrada de datos: \n" +
#         "Si desea desde el año 2015 en adelante solo escriba solo 2015 \n" +
#         "Si desea un rango de tiempo por ejemplo desde 2015 hasta 2017, escriba 2015:2017 \n" +
#         "Si desea solo los últimos 6 meses de 2015  debe escribir 06-2015:12-2015 \n")
# elif opc == "3":
#     print("Ha elegido la opción 3, una fecha en concreto")
#     monday = input(
#         "Ejemplo de entrada de datos: \n" +
#         "Un Lunes concreto, en el siguiente formato Año-mes-dia \n")
# elif opc == "4":
#     print("Ha elegido la opción 4, Salir del programa, Hasta pronto!... ")
# else:
#     print("La opcion seleccionada no es correcta, por favor vuelva a intentarlo.")


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


este = "2017-13"
formatingDate(este)
