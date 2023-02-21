import scrapy


class WorldmeterSpider(scrapy.Spider):
    name = 'worldmeter'
    allowed_domains = ['worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a")
        
        for countrie in countries:
            country_name = countrie.xpath(".//text()").get()
            link  = countrie.xpath(".//@href").get()
            
            #### differentes methodes to get absolute links ####
            #absolute_link = f'https://www.worldometers.info/{link}'
           # absolute_link = response.urljoin(link)
            #absolute_link = response.follow(url=link)
        
            yield response.follow(url=link, callback = self.parse_country, meta = {'country': country_name})
            
    def parse_country(self, response):
        #rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]")
        rows = response.xpath("(//table[contains(@class,'table')])[1]/tbody/tr")
        for row in rows:
            country = response.request.meta['country']
            year  = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yearly_change_percent = row.xpath(".//td[3]/text()").get()
            yearly_change = row.xpath(".//td[4]/text()").get()
            
            yield {
                'country': country,
                'year': year,
                'population': population,
                'yearlyChangePercent': yearly_change_percent,
                'yearlyChange': yearly_change
            }
            