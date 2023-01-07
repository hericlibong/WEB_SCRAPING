import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlingauchanSpider(CrawlSpider):
    name = 'crawlingauchan'
    allowed_domains = ['auchan.sn']
    start_urls = ['http://www.auchan.sn/105-maison-loisirs',
                  'http://www.auchan.sn/104-epicerie-salee',
                  'http://www.auchan.sn/128-bio',
                  'http://www.auchan.sn/91-epicerie-sucree',
                  'http://www.auchan.sn/172-boulangerie-patisserie',
                  'http://www.auchan.sn/137-boissons',
                  'http://www.auchan.sn/121-produits-frais',
                  'http://www.auchan.sn/232-produits-surgeles',
                  'http://www.auchan.sn/151-hygiene-beaute-parapharmacie',
                  'http://www.auchan.sn/146-bebe-puericulture',
                  'http://www.auchan.sn/158-entretien-de-la-maison',
                  'http://www.auchan.sn/165-petfood-animalerie'
                  ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3/a[@class='product_name']"), callback='parse_item', follow=True),
        Rule (LinkExtractor(restrict_xpaths="//li/a[@rel='next']"))
    )

    def parse_item(self, response):
        product_name = response.xpath("//h1[@class='h1 namne_details']/text()").get()
        produt_link = response.xpath("//h3/a[@class='product_name']/@href").get()
        product_image  = response.xpath("//img[@class='js-qv-product-cover']/@src").get()
        product_reference  = response.xpath("//p[@class='reference']/text()").get()
        product_price =  response.xpath("//div/span[@itemprop='price'][1]/text()").get().replace('\xa0', '')
        yield {
            'Produit':product_name,
            'Lien':produt_link,
            'Image':product_image,
            'Reference':product_reference,
            'Prix':product_price
            }
        
        
