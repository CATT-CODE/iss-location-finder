import os
from tkinter import E
import requests
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()
URL1Secret = os.getenv('URL1SECURE')
URL3Secret = os.getenv('URL3SECURE')

def show_location(request):
	if request.method == 'GET':
		return render(request, 'app/base.html')

	if request.method == 'POST':
			URL = 'http://api.open-notify.org/iss-now.json'

			r = requests.get(url = URL)
			data = r.json()

			issLatitude = data['iss_position']['latitude']
			issLongitude = data['iss_position']['longitude']

			URL1 = URL1Secret
			PARAMS = {'lat':issLatitude, 'lon':issLongitude}
			
			try:
				r1 = requests.get(url = URL1, params = PARAMS)
				data1 = r1.json()
			except:
				context = {'error': "API 1 ERROR"}
				return render(request, 'app/base.html', context)
			
			URL2 = 'https://ipapi.co/json/'

			try:
				r2 = requests.get(url = URL2)
			except:
				context = {'error': "API 2 ERROR"}
				return render(request, 'app/base.html', context)

			data2 = r2.json()
			currCity = data2['city']
			currLat = data2['latitude']
			currLong = data2['longitude']

			URL3 = "https://distance-calculator.p.rapidapi.com/distance/simple"
			querystring = {"lat_1": issLatitude, "long_1": issLongitude, "lat_2": currLat, "long_2": currLong, "unit": "miles", "decimal_places": "0"}

			headers = {
				"Content-Type": "application/json",
				"X-RapidAPI-Host": "distance-calculator.p.rapidapi.com",
				"X-RapidAPI-Key": URL3Secret
			}

			try:
				r3 = requests.request("GET", URL3, headers=headers, params=querystring)
			except:
				context = {'error': "API 3 ERROR"}
				return render(request, 'app/base.html', context)
				
			data3 = r3.json()
			distance = data3['distance']

			if 'error' in data1:
				context = {'water': "Over Water", 'distance': distance, 'currCity': currCity}
				return render(request, 'app/base.html', context)
			else:
				context = {'country': data1['address']['country'], 'state': data1['address']['state'], 'distance': distance, 'currCity': currCity}
				
				return render(request, 'app/base.html', context)

def show_people(request):
	URL1A = 'http://api.open-notify.org/astros.json'
	
	try:
		r1A = requests.get(url = URL1A)
	except:
		context = {'error': "API 1A ERROR"}
		return render(request, 'app/peeps.html', context)
	
	data1A = r1A.json()

	x = [i['name']for i in data1A['people']]
	numPeeps = len(x)

	context = {'numPeeps': numPeeps}

	return render(request, 'app/peeps.html', context)




