from pathlib import Path
import json
import scrapy


class HiperSpider(scrapy.Spider):
	name = "hiper"

	start_urls = [
		# 'https://www.hiperlibertad.com.ar/',
		# 'https://www.hiperlibertad.com.ar/bebes-y-ninos/lactancia-y-alimentacion/vajilla--infantil',
		# 'https://www.hiperlibertad.com.ar/api/catalog_system/pub/products/search/bebes-y-ni%C3%B1os/lactancia-y-alimentacion/vajilla--infantil?O=OrderByTopSaleDESC&_from=0&_to=23&ft&sc=1',
		 'https://www.hiperlibertad.com.ar/api/catalog_system/pub/category/tree/50'
		# 'https://www.hiperlibertad.com.ar/tecnologia/tv-y-video/tv-led-y-smart-tv',
		# 'https://www.hiperlibertad.com.ar/tecnologia/tv-y-video/accesorios-de-tv-y-video',
		# 'https://www.hiperlibertad.com.ar/tecnologia/audio/equipos-de-musica',
		# 'https://www.hiperlibertad.com.ar/tecnologia/audio/auriculares',
		# 'https://www.hiperlibertad.com.ar/tecnologia/audio/parlantes',
		# 'https://www.hiperlibertad.com.ar/tecnologia/audio/soundbars'
	]

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url, callback=self.parse)

	def get_urls(self, json_cat, lista):
		for dic in json_cat:
			if dic.get("hasChildren"):
				self.get_urls(dic.get("children"), lista)
			else:
				lista.append(dic.get("url"))

	def parse_urls(self, response):
		list_urls = []
		json_resp = json.loads(response.body)
		self.get_urls(json_resp, list_urls)
		for url in list_urls:
			yield scrapy.Request(url, callback=self.parse)

	def parse(self, response):
		self.log(f'******* VISITE URL :::> {response.url}')