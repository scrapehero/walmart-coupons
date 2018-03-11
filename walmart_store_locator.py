import csv
import requests
import json
import argparse
import traceback

def locate_stores(zip_code):
	"""
	Function to locate walmart stores
	"""
	url = "https://www.walmart.com/store/finder/electrode/api/stores?singleLineAddr=%s&serviceTypes=pharmacy&distance=50"%(zip_code)
	headers = {	'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'accept-encoding':'gzip, deflate, br',
				'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
				'cache-control':'max-age=0',
				'upgrade-insecure-requests':'1',
				'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
	}
	stores = []
	print("retrieving stores")
	for retry in range(10):
		try:
			get_store = requests.get(url, headers=headers, verify=False)
			store_response = get_store.json()
			stores_data = store_response.get('payload',{}).get("storesData",{}).get("stores",[])
			
			if not stores_data:
				print("no stores found near %s"%(zip_code))
				return []
			print("processing store details")
			#iterating through all stores
			for store in stores_data:
				store_id = store.get('id')
				display_name = store.get("displayName")
				address = store.get("address").get("address")
				postal_code = store.get("address").get("postalCode")
				city = store.get("address").get("city")
				phone = store.get("phone")
				distance = store.get("distance")

				data = {
						"name":display_name,
						"distance":distance,
						"address":address,
						"zip_code":postal_code,
						"city":city,
						"store_id":store_id,
						"phone":phone,
				}
				stores.append(data)
			return stores
		except:
			print(trackback.format_exc())
	
	return []	

if __name__=="__main__":
	
	argparser = argparse.ArgumentParser()
	argparser.add_argument('zip_code',help = 'zip code to search')
	args = argparser.parse_args()
	zip_code = args.zip_code
	scraped_data = locate_stores(zip_code)
	
	if scraped_data:
		print ("Writing scraped data to %s_stores.csv"%(zip_code))
		with open('%s_stores.csv'%(zip_code),'wb') as csvfile:
		    fieldnames = ["name","store_id","distance","address","zip_code","city","phone"]
		    writer = csv.DictWriter(csvfile,fieldnames = fieldnames,quoting=csv.QUOTE_ALL)
		    writer.writeheader()
		    for data in scraped_data:
		        writer.writerow(data)