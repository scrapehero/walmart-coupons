#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import html  
import csv
import requests
import re
import json
import argparse
import traceback

def parse(store_id):
	"""
	Function to retrieve coupons in a particular walmart srore
	:param store_id: walmart store id, you can get this id from the output of walmart store location script
	(https://github.com/scrapehero/walmart-coupons/blob/master/walmart_store_locator.py) 
	"""
	#sending request to get coupon related meta details
	url = "https://www.walmart.com/store/%s/coupons"%store_id
	headers = {"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
				"accept-encoding":"gzip, deflate, br",
				"accept-language":"en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
				"referer":"https://www.walmart.com/store/finder",
				"upgrade-insecure-requests":"1",
				"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
	}

	#adding retry
	for retry in range(5):
		try:
			response = requests.get(url, headers=headers)
			raw_coupon_url_details = re.findall('"couponsData":({.*?})',response.text)
			
			if raw_coupon_url_details:
				coupons_details_url_info_dict = json.loads(raw_coupon_url_details[0])
				#these variables are used to create coupon page url
				pid = coupons_details_url_info_dict.get('pid')
				nid = coupons_details_url_info_dict.get('nid')
				zid = coupons_details_url_info_dict.get('zid')
				#coupons details are rendering from the following url
				#example link :https://www.coupons.com/coupons/?pid=19251&nid=10&zid=vz89&storezip=20001
				coupons_details_url = "https://www.coupons.com/coupons/?pid={0}&nid={1}&zid={2}".format(pid,nid,zid)
				print("retrieving coupon page")
				coupon_headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
									"Accept-Encoding":"gzip, deflate, br",
									"Accept-Language":"en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
									"Host":"www.coupons.com",
									"Upgrade-Insecure-Requests":"1",
									"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
				}
				response = requests.get(coupons_details_url,headers=coupon_headers)
				coupon_raw_json = re.findall("APP_COUPONSINC\s?=\s?({.*});",response.text)
				print("processing coupons data")
				
				if coupon_raw_json:
					data = []
					coupon_json_data =  json.loads(coupon_raw_json[0])	
					coupons = coupon_json_data.get('contextData').get('gallery').get('podCache')
					
					for coupon in coupons:
						price = coupons[coupon].get('summary')
						product_brand = coupons[coupon].get('brand')
						details = coupons[coupon].get('details')
						expiration = coupons[coupon].get('expiration')
						activated = coupons[coupon].get('activated')

						wallmart_data={
								"offer":price,
								"brand":product_brand,
								"description":details,
								"activated_date":activated,
								"expiration_date":expiration,
								"url":coupons_details_url
						}
						data.append(wallmart_data)
					return data
		except:
			print(traceback.format_exc())
	return []

if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('store_id',help = 'walmart store id')
	args = argparser.parse_args()
	store_id = args.store_id
	scraped_data = parse(store_id)
	
	if scraped_data:
		print ("Writing scraped data to %s_coupons.csv"%(store_id))	
		with open('%s_coupons.csv'%(store_id),'w') as csvfile:
			fieldnames = ["offer","brand","description","activated_date","expiration_date","url"]
			writer = csv.DictWriter(csvfile,fieldnames = fieldnames,quoting=csv.QUOTE_ALL)
			writer.writeheader()
			for data in scraped_data:
				writer.writerow(data)
