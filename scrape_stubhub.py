import datetime
import gzip
import json
import requests

# events per request
rows = 5000
listing_endpoint = 'http://www.stubhub.com/listingCatalog/select'
payload = {
    'rows': rows,
    'wt': 'json',
    'q': 'stubhubDocumentType:event',
}


if __name__ == '__main__':
    times = 0
    while True and times < 10:
        data = []
        try:
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
            break
        except Exception as e:
            raise e
            times += 1
            continue
    else:
        # failed
        now = datetime.datetime.now()
        with open('snapshot_{}_{}_{}_{}_{}_FAILED.json'.format(now.month, now.day, now.year, now.hour, now.minute), 'wt') as outfile:
            outfile.write('FAIL')
