# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import Compose, MapCompose, TakeFirst
from w3lib.html import remove_tags

def split_columns(_iter):
    return dict(zip(_iter[::2],_iter[1::2]))

def clean_text(_iter):    
    sentence = _iter.replace('\n', ' ').replace('\r', '')
    return " ".join(sentence.split())

class Product(scrapy.Item):
    nome = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    descricaoLonga = scrapy.Field(input_processor=MapCompose(remove_tags, clean_text, unicode.strip), output_processor=TakeFirst())
    descricaoLongaHtml = scrapy.Field(output_processor=TakeFirst())
    #detalhes = scrapy.Field(input_processor=MapCompose(remove_tags, unicode.strip), output_processor=Compose(split_columns))
    preco = scrapy.Field(input_processor=MapCompose(unicode.strip), output_processor=TakeFirst())
    image = scrapy.Field(output_processor=TakeFirst())
    categorias = scrapy.Field()
