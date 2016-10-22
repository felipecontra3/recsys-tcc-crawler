import scrapy
import re

from scrapy.contrib.loader import ItemLoader
from product_crawler.items import Product
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.selector import Selector

class AmericanasSpider(scrapy.Spider):
    name = 'product_crawler'    

    #start_urls = ["http://busca.americanas.com.br/busca.php?q=jogos+xbox&sort=6&page="+str(i) for i in range(1, 76)]
    start_urls = ["http://busca.americanas.com.br/busca.php?q=jogos+xbox&sort=6&page="+str(i) for i in range(1, 10)]
    #for i in range(1, 30):
        #start_urls.append("http://busca.americanas.com.br/busca.php?Livros_titulo=&Livros_autor=&Livros_editora=&Livros_categoria=&ba=3&sort=6&page="+str(i))
        #start_urls.append("http://busca.americanas.com.br/busca.php?Filmes_titulo=&Filmes_artista=&Filmes_categoria=&Filmes_ano_producao=&ba=1&sort=6&page="+str(i))
        
    def parse(self, response):
        for a in response.css('section.products-area article div.top-area-product > a').extract(): 
            url = re.search(r'href=[\"|\'](?P<href>[^\"\']+)[\"|\']', a).groupdict()['href']
            yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response):
        p = ItemLoader(item=Product(), response=response)
        p.add_css('nome', 'h1 > span[itemprop=name]::text')
        p.add_value('url', response.url)
        p.add_css('descricaoLongaHtml','.infoProdBox')
        p.add_css('descricaoLonga','.infoProdBox')
        p.add_css('image','ul.a-carousel-list > li > img', re='src=[\"|\'](?P<src>[^\"\']+)[\"|\']')
        p.add_css('categorias','div[class=breadcrumb-box] span[itemprop=name]::text')
        yield p.load_item()


#executar no mongo
#db.produto.remove({'categorias.0': {$exists: false}})
#db.produto.remove({'categorias.0': {$nin: [' Games', ' Livros', ' DVDs e Blu-ray']}})
