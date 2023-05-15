from pathlib import Path
from scrapy.loader import ItemLoader
from hiper.items import HiperItem
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
			yield scrapy.Request(url, callback=self.parse_urls)

	def get_urls(self, json_cat, lista):
		path_api = '/api/catalog_system/pub/products/search'
		arg_api = '?O=OrderByTopSaleDESC&_from=0&_to=23&ft'
		arg_suc = '&sc=1'
		for dic in json_cat:
			if dic.get("hasChildren"):
				self.get_urls(dic.get("children"), lista)
			else:
				url = dic.get("url").split('/')
				url.insert(3, path_api)
				url = '/'.join(url)
				lista.append(url + arg_api + arg_suc)

	def parse_urls(self, response):
		list_urls = []
		json_resp = json.loads(response.body)
		self.get_urls(json_resp, list_urls)
		for url in list_urls:
			yield scrapy.Request(url, callback=self.parse)

	def parse(self, response):
		self.log(f'******* VISITE URL :::> {response.url}')
		json_resp = json.loads(response.body)
		cargador = ItemLoader(item=HiperItem(), response=response)
		#for prod in json_resp:
		#Por ahora imprimo solo el primer producto
		prod = json_resp[0]
		# precio_lista = prod["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]
		# nombre_prod = prod["productName"]
		# sku = prod["productId"]
		# print("**** PRODUCTO ****\n", nombre_prod)
		# print("-Codigo: ", sku)
		# print("-Precio: ", precio_lista)
		
		cargador.add_value("nombre", prod["productName"])
		cargador.add_value("sku", prod["productId"])
		cargador.add_value("precio_reg", prod["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"])
		return cargador.load_item()