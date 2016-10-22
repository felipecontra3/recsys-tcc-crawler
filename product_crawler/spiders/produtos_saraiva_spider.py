import scrapy
import re

from scrapy.contrib.loader import ItemLoader
from product_crawler.items import Product
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.selector import Selector

class ProductSpider(scrapy.Spider):
    name = 'product_crawler'

    #livros
    start_urls = ["http://busca.saraiva.com.br/pages/livros/administracao?page="+str(i) for i in range(1, 15)]
    for i in range(1, 15):
        start_urls.append("http://busca.saraiva.com.br/pages/livros/artes?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/autoajuda?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/ciencias-biologicas?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/ciencias-exatas?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/ciencias-humanas-e-sociais?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/esoterismo?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/espiritismo?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/esportes-e-lazer?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/gastronomia?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/hqs?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/literatura-estrangeira?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/literatura-infantojuvenil?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/literatura-brasileira?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/livros/religiao?page="+str(i))
        #start_urls.append("http://busca.saraiva.com.br/pages/livros/psicologia-e-psicanalise?page="+str(i))

    #filmes
    for i in range(1, 74):
        start_urls.append("http://busca.saraiva.com.br/pages/filmes/blurayfilmes?page="+str(i))

    #shows
    for i in range(1, 8):
        start_urls.append("http://busca.saraiva.com.br/pages/musica/blurayshows?page="+str(i))
        
    #jogos
    start_urls.append("http://busca.saraiva.com.br/pages/cat/games/wii-u/jogos-acao-e-aventura/cat/games/wii-u/jogos-esportes/cat/games/wii-u/jogos-musicais/cat/games/wii-u/jogos-corrida-e-simuladores/cat/games/wii-u/jogos-rpg/cat/games/wii-u/jogos-tiro-e-guerra")

    for i in range(1, 6):
        start_urls.append("http://busca.saraiva.com.br/pages/cat/games/playstation-4/jogos-de-acao-e-aventura/cat/games/playstation-4/jogos-de-esporte/cat/games/playstation-4/jogos-de-tiro-e-guerra/cat/games/playstation-4/jogos-de-corrida-e-simuladores/cat/games/playstation-4/jogos-rpg/cat/games/playstation-4/jogos-musicais/cat/games/playstation-4/jogos-de-estrategia-e-raciocinio?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/cat/games/xbox-one/jogos-acao-e-aventura/cat/games/xbox-one/jogos-esportes/cat/games/xbox-one/jogos-tiro-e-guerra/cat/games/xbox-one/jogos-corrida-e-simuladores/cat/games/xbox-one/jogos-rpg/cat/games/xbox-one/jogos-musicais?page="+str(i))
        start_urls.append("http://busca.saraiva.com.br/pages/cat/games/jogos-para-pc/arcade/cat/games/jogos-para-pc/corrida-e-simuladores/cat/games/jogos-para-pc/esporte/cat/games/jogos-para-pc/estrategia-e-raciocinio/cat/games/jogos-para-pc/jogos-de-tiro-e-guerra/cat/games/jogos-para-pc/jogos-musicais/cat/games/jogos-para-pc/rpg?page="+str(i))

    def parse(self, response):
        for a in response.css('div.u-clearfix div.cs-product-container > a').extract(): 
            url = re.search(r'href=[\"|\'](?P<href>[^\"\']+)[\"|\']', a).groupdict()['href']
            yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response):
        p = ItemLoader(item=Product(), response=response)
        p.add_css('nome', 'h1.livedata::text')
        p.add_value('url', response.url)
        p.add_css('descricaoLonga','.desc-info')
        p.add_css('image','div.container-product-image a.image-link > img', re='src=[\"|\'](?P<src>[^\"\']+)[\"|\']')
        p.add_css('categorias','span[itemprop=title]::text')
        yield p.load_item()


#executar no mongo
#db.produto.remove({'categorias.0': {$exists: false}})
#db.produto.remove({'categorias.0': {$nin: [' Games', ' Livros', ' DVDs e Blu-ray']}})

#deleta produtos duplicados
#var duplicates = [];

#db.produto_novo.aggregate([
    #{"$group" : { "_id": "$nome", "count": { "$sum": 1 }, "dups": { "$addToSet": "$_id" },  }},
    #{"$match": {"_id" :{ "$ne" : null } , "count" : {"$gt": 1} } }]
    #,{allowDiskUse: true},{cursor:{}} 
#).result.forEach(function(doc) {
    #doc.dups.shift();
    #doc.dups.forEach( function(dupId){ 
        #duplicates.push(dupId);
        #}
    #)    
#})
#printjson(duplicates); 
#db.produto_novo.remove({_id:{$in:duplicates}})  