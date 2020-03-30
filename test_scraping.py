import requests
from bs4 import BeautifulSoup

# página a la que le queremos hacer scraping
str = ""
page = request.get(str)

# ver la respuesta que hemos obtenido del servidor
respuesta = page.status_code

# para obtener el contenido bruto de la ágina usamos page.content
soup = BeautifulSoup(page.content)

#obtenemos la estructura anidada con la funcion prettify
dom_structure = soup.prettify
print(dom_structure)

# para extraer todo el texto
print(dom_structure.get_text())
