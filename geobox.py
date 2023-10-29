#!/usr/local/bin/python3
# Shoddy python disclaimer: I don't really use python so this script can probably be cleaned up a lot

import sys
from datetime import datetime

import requests

if len(sys.argv) != 4:
    print('Usage: python3 geobox.py <url to netbox instance> <netbox api key> <output location>')
    exit()

netboxBase = sys.argv[1]
netboxKey = sys.argv[2]
outputFile = sys.argv[3]

prefixes = []
nextURL = netboxBase + '/api/ipam/prefixes/'

while nextURL is not None:
    print('Fetching geofeed from ' + nextURL)
    r = requests.get(nextURL, headers={
        'Accept': 'application/json',
        'Authorization': 'Token ' + netboxKey
    })
    data = r.json()

    if r.status_code < 200 or r.status_code > 299:
        print('Error while fetching prefixes: ', data)
        exit()

    nextURL = data['next']
    results = data['results']
    prefixes.extend(results)
    print('Got ' + str(len(results)) + ' prefixes')

print('Found a total of ' + str(len(prefixes)) + ' prefixes')

print('Building geofeed')
i = 0
feed = '# Generated with GeoBox (https://github.com/FrumentumNL/GeoBox) on ' + datetime.now().isoformat() + '\n'
for entry in prefixes:
    fields = entry['custom_fields']
    if not fields['geoloc_has_location']:
        # Explicitly no geoloc, all fields should be empty
        feed += entry['prefix'] + ',,,,\n'
        i += 1
        continue

    country = fields['geoloc_country']
    region = fields['geoloc_region']
    city = fields['geoloc_city']
    if country is None and region is None and city is None:
        # Just let it inherit
        continue

    country = '' if country is None else country
    region = '' if region is None else country
    city = '' if city is None else country

    feed += entry['prefix'] + ',' + country + ',' + region + ',' + city + ',\n'
    i += 1

print('Geofeed built, contains ' + str(i) + ' prefixes')

print('Saving to ' + outputFile)
f = open(outputFile, "w")
f.write(feed)
f.close()
print('Saved to ' + outputFile)

print('Finished! Thanks for using GeoBox.')
