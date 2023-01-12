import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AtlantacrawlSpider(CrawlSpider):
    name = 'atlanta'
    allowed_domains = ['yellowpages.com']
    start_urls = ['https://www.yellowpages.com/search?search_terms=Coffee+Shops&geo_location_terms=Atlanta%2C+GA']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='media-thumbnail']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='next ajax-page']"),callback='parse_item',follow=True)
    )

    def parse_item(self, response):
        business_name = response.xpath("//*[@id='main-header']/article/div/h1/text()").get()
        website = response.xpath("//p[@class='website']/a/@href").get()
        address = response.xpath("//*[@id='details-card']/p[2]/text()").get()
        email = response.xpath("//a[@class='email-business']/@href").get()
        phone_number = response.xpath("//*[@id='details-card']/p[1]/text()").get()
        categories =[cat.xpath('.//text()').get() for cat in response.xpath("//dd[@class='categories']/div[@class='categories']/a")]
        yellowpage_url = response.xpath(' //html/head/link[2]/@href').get()
        yield {
            'user_agent':str(response.request.headers['User-Agent']),
            'Business Name':business_name,
            'Website': website,
            'Address':address,
            'Email':email,
            'Phone Number':phone_number,
            'Categories':categories,
            'YellowPage Url':yellowpage_url
        }
