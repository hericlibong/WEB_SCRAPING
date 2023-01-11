import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class OccasesSpider(CrawlSpider):
    name = 'occases'
    allowed_domains = ['deals.jumia.sn']
    start_urls = ['http://deals.jumia.sn/voitures']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='announcement-container']//a[@class='post-link post-vip']"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"))
    )

    def parse_item(self, response):
        name = response.xpath("//h1/span[@itemprop='name']/text()").get()
        price = response.xpath("//section[@itemprop='offers']//span/span/@content").get()
        marque = response.xpath("//h3/span/a/text()").get()
        model = response.xpath("//div[@class='new-attr-style']/h3[2]/span/text()").get()
        transmission = response.xpath("//div[@class='new-attr-style']/h3[3]/span/text()").get()
        carburant = response.xpath("//div[@class='new-attr-style']/h3[4]/span/text()").get()
        year = response.xpath("//div[@class='new-attr-style']/h3[5]/span/text()").get()
        kilometrage = response.xpath("//div[@class='new-attr-style']/h3[6]/span/text()").get()
        
        yield {
            'nom':name,
            'prix':price,
            'marque':marque,
            'model':model,
            'transmission': transmission,
            'carburant':carburant,
            'annee': year,
            'kilometrage':kilometrage
        }
        
        
