# import the necessary packages
from carsmarketplace.items import CarsmarketplaceItem
import datetime
import scrapy
import time
from user_agent import generate_user_agent
import json
import requests
import os.path

# scrapy crawl pyimagesearch-cover-spider -o output.json


class CarSpider(scrapy.Spider):
	name = "car-spider"
	url = "https://api-production.ouicar.fr/graphql"
	headers = {
		# 'Accept': '*/*',
		# 'Accept-Encoding': 'gzip, deflate, br',
		# 'Accept-Language': 'en-US,en;q=0.5',
		# 'Cache-Control': 'no-cache',
		# 'Connection': 'keep-alive',
		'content-type': 'application/json',
		# 'Host': 'api-production.ouicar.fr',
		# 'Origin': 'https://www.ouicar.fr',
		# 'Pragma': 'no-cache',
		# 'Referer': 'https://www.ouicar.fr/',
		# 'TE': 'trailers',
		# 'User-Agent': generate_user_agent()
	}
	data = {"urls":[]}


	def start_requests(self):

		#Get the body on 'inspect_element>Network>graphql>Preview'
		body = [
		    {
		        "operationName": "Search",
		        "variables": {
		            "filters": {
		                "availability": {
		                    "start": "2022-11-26T11:00:00Z",
		                    "end": "2022-11-27T22:59:59Z"
		                },
		                "km": 200
		            },
		            "issuer": None,
		            "location": {
		                "lat": 45.764043,
		                "lng": 4.835659,
		                "radius": 1000
		            },
		            "page": 1,
		            "results": 1000
		        },
		        "query": "query Search($page: Int!, $results: Int, $location: CarSearchInputLocation!, $filters: CarSearchInputFilters, $tracking_id: ID, $issuer: CarSearchInputIssuer) {\n  search(\n    page: $page\n    results: $results\n    location: $location\n    filters: $filters\n    tracking_id: $tracking_id\n    issuer: $issuer\n  ) {\n    ...SearchFragment\n    __typename\n  }\n}\n\nfragment SearchFragment on SearchResults {\n  data {\n    car {\n      brand\n      category\n      connect\n      country_code\n      doors\n      energy\n      gearbox\n      id\n      image {\n        original\n        __typename\n      }\n      instant_booking\n      is_new\n      keyless\n      model\n      options\n      owner {\n        firstname\n        gender\n        id\n        image {\n          original\n          __typename\n        }\n        response_time\n        __typename\n      }\n      rating\n      rating_number\n      seats\n      year\n      __typename\n    }\n    distance\n    delivery {\n      checkin_availabilities {\n        start\n        end\n        __typename\n      }\n      checkout_availabilities {\n        start\n        end\n        __typename\n      }\n      __typename\n    }\n    location {\n      city_name\n      is_primary\n      kind\n      lat\n      lng\n      location_or_place_id\n      place_name\n      thoroughfare\n      seo_id\n      __typename\n    }\n    prices {\n      distance\n      duration\n      price_day\n      price_km\n      service_fee\n      total\n      young_driver_fee\n      __typename\n    }\n    prices_v2 {\n      ...Price_v2Fragment\n      __typename\n    }\n    __typename\n  }\n  pagination {\n    page\n    page_count\n    item_count\n    __typename\n  }\n  tracking_id\n  __typename\n}\n\nfragment Price_v2Fragment on SearchResultPriceV2 {\n  amounts {\n    assistance_owner\n    assistance_renter\n    insurance_owner\n    insurance_renter\n    intermediation_owner\n    intermediation_renter\n    __typename\n  }\n  car_price_day\n  car_price_km\n  degressivity_rate\n  rates {\n    assistance_owner\n    assistance_renter\n    insurance_owner\n    insurance_renter\n    intermediation_owner\n    intermediation_renter\n    __typename\n  }\n  rental_price_day\n  rental_price_km\n  rental_total\n  service_fee\n  total_renter_price\n  young_driver_fee\n  __typename\n}\n"
		    }
		]

		print("HHHHHEEEEEERRRRREEEEEE")

		# start Requesting
		yield scrapy.Request(
			url=self.url,
			callback=self.parse,
			method='POST',
			body=json.dumps(body),
			headers=self.headers,
			)


	def parse(self, response):
			# let's only gather Time U.S. magazine covers
			#url = response.css("div.refineCol ul li").xpath("a[contains(., 'TIME U.S.')]")	
			#yield scrapy.Request(url.xpath("@href").extract_first(), self.parse_page)

			#srcset="https://media.ouicar.fr/Product/Cars/cf6bb94c-7dab-4527-be24-3f52fbc47041/F29A0BC9-1D1D-4FE0-BCDF-0C088D6F5594.jpg?w=114&h=114 1x, https://media.ouicar.fr/Product/Cars/cf6bb94c-7dab-4527-be24-3f52fbc47041/F29A0BC9-1D1D-4FE0-BCDF-0C088D6F5594.jpg?w=228&h=228 2x"
			body_unicode = response.body.decode('utf-8')
			body = json.loads(body_unicode)			
			cars_list = body[0]["data"]["search"]["data"]

			for car in cars_list:

				if car["car"]["image"] is not None:
					
					img_url = car["car"]["image"]["original"]
					filename = img_url.split('/')[-1]

					print("img_url :", img_url)
					print("filename :", filename)
					print()

					self.data["urls"].append((img_url, filename))

				with open('outputs.json', 'w') as f:
					json.dump(self.data, f)
			
			#yield CarsmarketplaceItem(name=name, file_urls=[imageURL])



	def close(spider, reason):

		for img in spider.data:
			if not os.path.exists("./outputs/"  + img[1]):
				#time.sleep(5)
				r = requests.get(img[0], allow_redirects=False)
				open("./outputs/"  + img[1], 'wb').write(r.content)

		print("FINISHED")







		
