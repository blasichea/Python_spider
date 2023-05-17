import scrapy


class HiperItem(scrapy.Item):
	nombre = scrapy.Field()
	precio_reg = scrapy.Field()
	precio_pub = scrapy.Field()
	categoria = scrapy.Field()
	sku = scrapy.Field()
	url_prod = scrapy.Field()
	stock = scrapy.Field()
	descripcion = scrapy.Field()
