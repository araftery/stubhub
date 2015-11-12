import datetime
import gzip
import json
import requests

data = []

# events per request
rows = 5000
listing_endpoint = 'http://www.stubhub.com/listingCatalog/select'
payload = {
    'rows': rows,
    'wt': 'json',
    'q': 'stubhubDocumentType:event',
}

last_found = 1

i = 0
while last_found > 0:
    payload['start'] = i * rows
    r = requests.get(listing_endpoint, params=payload)
    r.raise_for_status()
    response = r.json()
    events = response['response']['docs']
    last_found = len(events)
    data += events
    i += 1


now = datetime.datetime.now()
with gzip.open('snapshot_{}_{}_{}_{}_{}.json'.format(now.month, now.day, now.year, now.hour, now.minute), 'wt') as outfile:
    json.dump(data, outfile)
