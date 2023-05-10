from pathlib import Path
import json
import scrapy


class HiperSpider(scrapy.Spider):
	name = "hiper"
	start_urls = [
		#'https://www.hiperlibertad.com.ar/',
		'https://www.hiperlibertad.com.ar/api/catalog_system/pub/category/tree/50'
	]

	def parse(self, response):
		filename = f'hiper.txt'
		Path(filename).write_bytes(response.body)
		self.log(f'Se guardó el archivo {filename}')