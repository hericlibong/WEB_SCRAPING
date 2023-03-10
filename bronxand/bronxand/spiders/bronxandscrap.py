import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BronxandscrapSpider(CrawlSpider):
    name = 'bronxandscrap'
    allowed_domains = ['bronxandbanco.com']
    start_urls = ['https://bronxandbanco.com/product-category/summer-2023/', 
                  'https://bronxandbanco.com/product-category/resort-2023/'
                  ]

    rules = [Rule(LinkExtractor(restrict_xpaths="//a[@class='cd chp']"), callback='parse_item', follow=True)]

    def parse_item(self, response):
        product_name = response.xpath("//h1[@class='product_title entry-title']/text()").get()
        product_price = response.xpath("//p[@class='price']/span/bdi/text()").get()
        product_sku = response.xpath("//div[@class='product_meta']//span[@class='sku']/text()").get()
        product_categories = response.xpath("//div[@class='product_meta']//span[@class='posted_in']/a/text()").getall()
        # color = response.xpath("//tr[1]/td/p/text()").get()
        # belt = response.xpath("//tr[2]/td/p/text()").get()
        product_image = response.xpath("//a/img[@decoding[1]='async']/@src").get()
        
        
        yield{
            'ProductName':product_name,
            'ProductPrice':product_price,
            'SKU':product_sku,
            'Categories':product_categories,
            # 'Color':color,
            # 'Belt':belt,
            'Image': product_image
        }

