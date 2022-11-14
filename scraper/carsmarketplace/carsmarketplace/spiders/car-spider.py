# import the necessary packages
from timecoverspider.items import MagazineCover
import datetime
import scrapy

class CarSpider(scrapy.Spider):
	name = "car-spider"
	start_urls = ["https://www.ouicar.fr/france?km=100&end=2022-11-12&end_period=2&start=2022-11-11&start_period=2&search_type=city&where=Paris%2C%20France&where_lat=48.856614&where_lng=2.3522219&zone_ne_lat=48.9021475&zone_ne_lng=2.4698509&zone_sw_lat=48.8155622&zone_sw_lng=2.2242191&zoom=13&zip_code=&city=Paris&department=D%C3%A9partement%20de%20Paris&country=France&trackingId=22ba7b40-61a8-11ed-b869-8f599bd96fd3&searchItemId=2394aea0-61a8-11ed-b5de-6bc8080e8471"]


	def parse(self, response):
		# let's only gather Time U.S. magazine covers
		url = response.css("div.refineCol ul li").xpath("a[contains(., 'TIME U.S.')]")
		yield scrapy.Request(url.xpath("@href").extract_first(), self.parse_page)
