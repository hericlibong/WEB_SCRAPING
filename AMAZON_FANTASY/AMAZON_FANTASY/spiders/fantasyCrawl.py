import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import AmazonFantasyItem
from scrapy.loader import ItemLoader



class FantasycrawlSpider(CrawlSpider):
    name = 'fantasyCrawl'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/english/s?k=english&i=stripbooks&rh=n%3A283155%2Cn%3A25&dc&ds=v1%3AKUTeAEW2%2BPHIMz%2FyrLikihfaQuIWohJ4RDOZbYr%2F5ag&qid=1673869812&rnid=283155&ref=sr_nr_n_27']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h2/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']"))
    )

    def parse_item(self, response):
        title = response.xpath("//h1[@id='title']/span[1]/text()").get()
        date = response.xpath("//h1[@id='title']/span[2]/text()").get()
        author = response.xpath("//a[@class='a-link-normal contributorNameID']/text()").get()
        kindle_price = response.xpath("//a//span[@class='a-size-base a-color-secondary']/text()").get()
        paperback_price = response.xpath("//a//span[@class='a-size-base a-color-price a-color-price']/text()").get()
        ratings = response.xpath("//span[@id='acrCustomerReviewText']/text()").get()
        #short_text = response.xpath("//div[@aria-expanded='false']//span/following-sibling :: node()/text()[1]").get()
    
        # books = AmazonFantasyItem()
        # books['Title']=title
        # books['PaperDate'] = date
        # books['Author'] = author
        # books['KindlePrice']=kindle_price
        # books['PaperbackPrice']= paperback_price
        # books['Ratings'] = ratings
        # books['Resume'] = short_text
        
        # yield books
        
        
        l = ItemLoader(item=AmazonFantasyItem(), response=response)
        l.add_xpath("Title","//h1[@id='title']/span[1]/text()")
        l.add_xpath("PaperDate","//h1[@id='title']/span[2]/text()")
        l.add_xpath("Author","//a[@class='a-link-normal contributorNameID']/text()")
        l.add_xpath("KindlePrice", "//a//span[@class='a-size-base a-color-secondary']/text()")
        l.add_xpath("PaperbackPrice","//a//span[@class='a-size-base a-color-price a-color-price']/text()")
        l.add_xpath("Ratings", "//span[@id='acrCustomerReviewText']/text()")
        #l.add_xpath("Resume","//div[@aria-expanded='false']//span/following-sibling :: node()/text()[1]" )
        
        yield l.load_item()
        
                       
      
        
        
        
       
        
    
            
            
       
        
