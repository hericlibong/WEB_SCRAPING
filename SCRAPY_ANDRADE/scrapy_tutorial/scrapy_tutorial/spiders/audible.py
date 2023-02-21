import scrapy


class AudibleSpider(scrapy.Spider):
    name = 'audible'
    allowed_domains = ['audible.com']
    start_urls = ['https://www.audible.com/search/']

    def parse(self, response):
        product_list = response.xpath("//div[@class='adbl-impression-container ']//li[contains(@class, 'productListItem')]")
        for product in product_list:
            title = product.xpath(".//h3[contains(@class, 'bc-heading')]/a/text()").get()
            author = product.xpath(".//li[contains(@class, 'authorLabel')]/span/a/text()").getall()
            runtime = product.xpath(".//li[contains(@class, 'runtimeLabel')]/span/text()").get().replace('Length:', '')
            yield {
                'title': title,
                'author': author,
                 'runtime':runtime,
            #     
             }
        pagination = response.xpath("//ul[contains(@class, 'pagingElements ')]")
        next_page_url = pagination.xpath(".//li/span[contains(@class, 'nextButton')]/a/@href").get()
        
        if next_page_url:
            yield response.follow(url = next_page_url, callback = self.parse)
        
        
            
