from scrapy.loader import ItemLoader
from hiper.items import HiperItem
import json
import scrapy


class HiperSpider(scrapy.Spider):
	name = "hiper"
	

	def __init__(self, proxy=None, sucursal=1, *args, **kwargs):
		super(HiperSpider, self).__init__(*args, **kwargs)
		if proxy:
			self.proxy = proxy
		else:
			self.proxy = None
		if sucursal:
			self.sucursal = sucursal
		else:
			self.sucursal = 1
		self.items_per_req = 30


	allowed_domains = ["www.hiperlibertad.com.ar"]
	start_urls = [
		"https://www.hiperlibertad.com.ar/\
			api/catalog_system/pub/category/tree/50",
	]


	def myRequest(self, url, callback):
		if self.proxy:
			return scrapy.Request(
				url,
				meta={'proxy':self.proxy},
				callback=callback
			)
		else:
			return scrapy.Request(url, callback=callback)


	def start_requests(self):
		url = self.start_urls[0]
		yield self.myRequest(url, self.parse_urls)


	def get_urls(self, json_cat, lista):
		path_api = "/api/catalog_system/pub/products/search"
		arg_api = f"?_from=0&_to={self.items_per_req - 1}"
		arg_suc = f"&sc={self.sucursal}"
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
			yield self.myRequest(url, self.parse)


	def pagination(self, url):
		url2 = url.split("=")
		inicio = int(url2[1].split("&")[0]) + self.items_per_req
		fin = int(url2[2].split("&")[0]) + self.items_per_req
		url2[1] = f"{inicio}&_to"
		url2[2] = f"{fin}&sc"
		url2 = "=".join(url2)
		return url2


	def parse(self, response):
		json_resp = json.loads(response.body)
		
		for prod in json_resp:
			cargador = ItemLoader(item=HiperItem(), response=response)
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
			#cargador.add_value("descripcion", prod["description"])
			yield cargador.load_item()
		#Paginación
		if (len(json_resp) == self.items_per_req):
			yield self.myRequest(self.pagination(response.url), self.parse)
