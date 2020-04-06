opc = input(
    "Bienvenido a la practica 1 de Tipología y ciclo de vida de los dato, \n Debe saber que esta práctica extrae informacion del magazine New Yorker \n" +
    "Esta revista publica todos los lunes de mes, así que  si desea in dia en concreto debe ser un Lunes, para que la busqueda devuelva datos. \n" +
    "El formato de entrada que esperamos es una fecha, con el siguiente formato Año-mes-dia, o solo el Año según la opción.  \n" +
    "En esta practica dispones de varias opciones para extraer los datos \n" +
    "Las opciones de las que dispone son las siguientes: \n" +
    "1. - Todos los datos desde 2007 hasta la fecha actual \n" +
    "2. - Un periodo determinado de tiempo, por ejemplo si desea desde el año 2015 en adelante solo escriba 2015 \n" +
    "Si desea en un rango de tiempo por ejemplo desde 2015 hasta 2017, escriba 2015:2017 \n" +
    "Si desea solo los últimos 6 meses de 2015  debe escribir 06-2015:12-2015 \n" +
    "3. - Un Lunes concreto, en el siguiente formato Año-mes-dia \n" +
    "4. - Salir del programa \n" +
    "Elija una opción:  \n")

if opc == "1":
    print("Ha elegido la opción 1, todos los datos desde 2007 hasta la fecha actual")
elif opc == "2":
    print("Ha elegido la opción 2, un rango de tiempo")
elif opc == "3":
    print("Ha elegido la opción 3, una fecha en concreto")
elif opc == "4":
    print("Ha elegido la opción 4, Salir del programa, Hasta pronto!... ")
else:
    print("La opcion seleccionada no es correcta, por favor vuelva a intentarlo.")
