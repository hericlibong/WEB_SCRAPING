import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlsendoctorSpider(CrawlSpider):
    name = 'crawlsendoctor'
    allowed_domains = ['annuaire-senegal.com']
    start_urls = ['http://www.annuaire-senegal.com/medecin']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@itemprop='url']"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='page-link']"))
    )

    def parse_item(self, response):
        name = response.xpath("//h1[@itemprop='name']/text()").get()
        address = response.xpath("//tr/td/address/text()").get()
        thema = response.xpath("//td[@class='infos_details']/a[@class='link_black_grey']/text()").get()
        town = response.xpath("//td[@itemprop='addressRegion']/text()").get()
        tel = response.xpath("//td[@itemprop='telephone']/a/text()").get()
        geoLink = response.xpath("//td[@itemprop='streetAddress']//a/@href").get()
        yield {
            'user_agent':str(response.request.headers['User-Agent']),
            'Name':name,
            'Address':address,
            'Theme':thema,
            'Town':town,
            'Tel':tel,
            'Geolink':geoLink
        }
        
        
        
        