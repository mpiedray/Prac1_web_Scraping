import scrapy
from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join
from bs4 import BeautifulSoup
import requests


class NewYorkerItem(Item):
    nombre_portada = Field()
    autor_portada = Field()
    autor_critica = Field()
    fecha = Field()
    url = Field()
    imagen = Field()
    id_portada = Field()
    descripcion = Field()
    news_keywords = Field()
    keywords = Field()


class NewYorkerCrawler(CrawlSpider):
    name = 'newyorkercrawler'
    allowed_domains = ['https://www.newyorker.com/']
    start_url = ['https://www.newyorker.com/culture/cover-story']

    # ahora definimos las reglas para hacer el crawling vertical y horizontal.
    rules = (
        Rule(LinkExtractor(allow=r'/page/\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/culture/cover-story/'),
             follow=True, callback='parse_items')
    )

    def parse_items(self, response):

        soup = BeautifulSoup(response.body)

        item = scrapy.loader.ItemLoader(NewYorkerItem(), response)

        au_critica = soup.find("a", {"class": "byline__name-link"}).text
        name_datos = soup.h1.text.split('“')

        autor_portada = name_datos[0].strip() if len(
            name_datos[0].strip()) > 0 else 'NA'

        titulo_portada = name_datos[1].split('”')[0].strip() if len(
            name_datos[1].split('”')[0].strip()) > 0 else 'NA'

        current_url = soup.find("meta", property="og:url")
        url = current_url["content"] if len(
            current_url["content"]) > 0 else 'NA'

        image = soup.find("meta", property="og:image")
        image_16_9 = image["content"] if len(
            image["content"]) > 0 else 'NA'

        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            if meta.get('name') == 'news_keywords':
                news_keywords = meta.get('content') if len(
                    meta.get('content')) > 0 else 'NA'

            if meta.get('name') == 'keywords':
                keywords = meta.get('content') if len(
                    meta.get('content')) > 0 else 'NA'

            if meta.get('name') == 'description':
                descripcion = meta.get('content') if len(
                    meta.get('content')) > 0 else 'NA'

            if meta.get('name') == 'id':
                id_portada = meta.get('content') if len(
                    meta.get('content')) > 0 else 'NA'

        item.add_value('titulo_portada', titulo_portada)
        item.add_value('autor_portada', autor_portada)
        item.add_value('autor_critica', au_critica)
        item.add_value('url', url)
        item.add_value('imagen', image_16_9)
        item.add_value('news_keywords', news_keywords)
        item.add_value('keywords', keywords)
        item.add_value('descripcion', descripcion)
        item.add_value('id_portada', id_portada)

        yield item.load_item()
