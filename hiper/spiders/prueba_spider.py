from pathlib import Path
from scrapy.loader import ItemLoader
from hiper.items import HiperItem
import json
import scrapy


class HiperSpider(scrapy.Spider):
	name = "hiper"
	

	def __init__(self, proxy=None, *args, **kwargs):
		super(HiperSpider, self).__init__(*args, **kwargs)
		if proxy:
			self.proxy = proxy
		else:
			self.proxy = None


	allowed_domains = ["www.hiperlibertad.com.ar"]
	start_urls = [
		"https://www.hiperlibertad.com.ar/\
			api/catalog_system/pub/category/tree/50",
	]


	def start_requests(self):
		url = self.start_urls[0]
		if self.proxy:
			yield scrapy.Request(
				url,
				meta={'proxy' : self.proxy},
				callback=self.parse_urls
			)
		else:
			yield scrapy.Request(url, callback=self.parse_urls)


	def get_urls(self, json_cat, lista):
		path_api = "/api/catalog_system/pub/products/search"
		arg_api = "?O=OrderByTopSaleDESC&_from=0&_to=23&ft"
		arg_suc = "&sc=1"
		for dic in json_cat:
			if dic.get("hasChildren"):
				self.get_urls(dic.get("children"), lista)
			else:
				url = dic.get("url").split("/")
				url.insert(3, path_api)
				url = "/".join(url)
				lista.append(url + arg_api + arg_suc)


	def parse_urls(self, response):
		list_urls = []
		json_resp = json.loads(response.body)
		self.get_urls(json_resp, list_urls)
		for url in list_urls:
			if self.proxy:
				yield scrapy.Request(
					url,
					meta={'proxy' : self.proxy},
					callback=self.parse_urls
				)
			else:
				yield scrapy.Request(url, callback=self.parse)


	def parse(self, response):
		json_resp = json.loads(response.body)
		cargador = ItemLoader(item=HiperItem(), response=response)
		#for prod in json_resp:
		#Por ahora imprimo solo el primer producto
		prod = json_resp[0]
		cargador.add_value("nombre", prod["productName"])
		cargador.add_value(
			"precio_reg",
			prod["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]
		)
		cargador.add_value(
			"precio_pub",
			prod["items"][0]["sellers"][0]["commertialOffer"]["Price"]
		)
		cargador.add_value("categoria", prod["categories"][0])
		cargador.add_value("sku", prod["items"][0]["itemId"])
		cargador.add_value("url_prod", prod["link"])
		cargador.add_value(
			"stock",
			prod["items"][0]["sellers"][0]\
				["commertialOffer"]["AvailableQuantity"]
		)
		cargador.add_value("descripcion", prod["description"])
		return cargador.load_item()