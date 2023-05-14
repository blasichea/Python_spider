# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HiperItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	nombre = scrapy.Field()
	precio_reg = scrapy.Field()
	precio_pub = scrapy.Field()
	categoria = scrapy.Field()
	sku = scrapy.Field()
	url_prod = scrapy.Field()
	stock = scrapy.Field()
	descripcion = scrapy.Field()
