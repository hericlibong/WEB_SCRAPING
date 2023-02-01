# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, TakeFirst, MapCompose
from w3lib.html import remove_tags

def clean_price(priceval):
    price = priceval.replace('$', '')
    return price

def clean_date(dateval):
    date = dateval.replace('Paperback –', '')
    return date

def clean_rating(rateval):
    rate = rateval.replace('ratings', '')
    return rate


class AmazonFantasyItem(scrapy.Item):
    BookTitle = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()
    )
    Date = scrapy.Field(
        input_processor = MapCompose(clean_date,),
        output_processor = TakeFirst()
    )
    Author = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        #output_processor = TakeFirst()
    )
    PriceBkindle = scrapy.Field(
        input_processor = MapCompose(clean_price),
        outout_processor = TakeFirst()
    )
    PriceAPaperback = scrapy.Field(
        input_processor = MapCompose(clean_price, remove_tags),
        output_processor =TakeFirst()
    )
    Ratings = scrapy.Field(
        input_processor = MapCompose(clean_rating, remove_tags),
        output_processor =TakeFirst()
    )
    SummaryAuthor = scrapy.Field(
         input_processor = MapCompose(remove_tags),
         #output_processor = TakeFirst()
     )
    XcoverPicture =scrapy.Field(
        input_processor= MapCompose(remove_tags)
        
    )
    
   
    
