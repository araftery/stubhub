#!/usr/bin/env python

import datetime
import gzip
import json
import os
import requests

# events per request
rows = 10000
listing_endpoint = 'http://www.stubhub.com/listingCatalog/select'
payload = {
    'rows': rows,
    'wt': 'json',
    'q': 'stubhubDocumentType:event',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,sl;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.stubhub.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
    'Cookie':"""D_SID=65.112.10.198:tZNRZeDB+GwQurQamAeyjpdgnIDkzUkaeByq8dlZBOM; __uvt=; __gads=ID=925f3c7a31d8bf59:T=1447282312:S=ALNI_MaD9IFZMSxV7eyH0bjLSy3NM0uqHw; _br_uid_1=uid%3D9644577258732; uvts=3nEpUJDs7SA0JyGo; S_ACCT=stubhub; SH_VI=fd7f70bdbb944a18ac6ed041a4d816f0; STUB_SESSION=; AMCV_1AEC46735278551A0A490D45%40AdobeOrg=1304406280%7CMCAAMB-1447887107%7CNRX38WO0n5BH8Th-nqAG_A%7CMCAAMLH-1447652149%7C7%7CMCAID%7C2B20185A8507BEC1-40000105C001BD45%7CMCIDTS%7C16751%7CMCMID%7C19413938854763524971188353192824411326; TLTSID=AB85CA4089801089F9A2DAA602C86A31; STUB_INFO=filler%7E%5E%7E0%7Cu2%7E%5E%7E2457A52BA9DD08B7E054001B21D98A04%7E%5E%7E11%2F12%2F2015%7CSTUB_DEF_CUR%7E%5E%7EUSD%7E%5E%7E11%2F12%2F2015%7CSTUB_PRE_CUR%7E%5E%7EUSD%7E%5E%7E11%2F12%2F2015%7CSTUB_BOB_CUR%7E%5E%7EUSD%7E%5E%7E11%2F12%2F2015; STUB_PERSISTENT=filler%7E%5E%7E1%7Cstub_uid%7E%5E%7E84469744%7E%5E%7E11%2F12%2F2015; DC=origin1; STUB_SESS=filler%7E%5E%7E0%7Cguid%7E%5E%7E238EC4ACAE26515C781313368CE8B60A%7E%5E%7E11%2F12%2F2015%7Ccobrand_id%7E%5E%7E47%7E%5E%7E11%2F12%2F2015%7Clname%7E%5E%7Eiy3agqk%2F4gU%3D%7E%5E%7E11%2F12%2F2015%7Ccobrand%7E%5E%7Ewww%7E%5E%7E11%2F12%2F2015%7Ceadd%7E%5E%7E5Qrvp6HITJE%2FGk9trM68K7weUo0YuZEC8NWYJOWeYpo%3D%7E%5E%7E11%2F12%2F2015%7Capp_token%7E%5E%7EBImXAmYKv7MZjdJqQiBaUOcoa2HXA3Bgr5nl%2Fie9i9Y%3D%7E%5E%7E11%2F13%2F2015%7Cloaded_ip_number%7E%5E%7E1613664769%7E%5E%7E11%2F12%2F2015%7Czcode%7E%5E%7EdSH0%2Bp1AfDY%3D%7E%5E%7E11%2F12%2F2015%7Cloaded_stub_uid%7E%5E%7E84469744%7E%5E%7E11%2F12%2F2015%7Cfname%7E%5E%7ESy%2BIods0I7o%3D%7E%5E%7E11%2F12%2F2015%7Cstub_sid%7E%5E%7E0%7E%5E%7E11%2F12%2F2015; hz_amChecked=1; mbox=PC#1447047348872-933053.17_01#1481669072|check#true#1447454732|session#1447454671789-523943#1447456532; optimizelySegments=%7B%222649650440%22%3A%22direct%22%2C%222666690309%22%3A%22gc%22%2C%222684360667%22%3A%22false%22%7D; optimizelyEndUserId=oeu1447454671955r0.9546505671460181; optimizelyBuckets=%7B%7D; _br_uid_2=uid%3D9644577258732%3Av%3D11.5%3Ats%3D1447282427807%3Ahc%3D2; s_pers=%20s_dfa%3Dstubhub%7C1447456472317%3B%20s_vs%3D1%7C1447456472878%3B%20s_nr%3D1447454672884-Repeat%7C1481582672884%3B; s_sess=%20s_cc%3Dtrue%3B%20s_cpc%3D1%3B%20s_sq%3D%3B; D_PID=87AB7ED2-8D56-356A-A322-74070C642CD5; D_IID=63A68263-33E8-3557-9D69-6756712305E4; D_UID=D0371DA5-E35E-36D7-B6E9-A82281626366; D_HID=+NGpyff/nyfEpIw+c2KdbaAS5TmDR6R7lFu5IdVk5YY; s_vi=[CS]v1|2B20185A8507BEC1-40000105C001BD45[CE]; JSESSIONID=1B22B0E67BFBA6A06C4A04650E4ECDD0; fsr.s={"v2":-2,"v1":1,"rid":"de358f8-93793656-f249-9e05-af1f6","cp":{"Unified_StubHub":"N","TLSessionID":"AB85CA4089801089F9A2DAA602C86A31","campaign_name":"UEHP008: Reco Authenticated (PROD)","campaign_recipe_name":"HP Reco Personalized","userid":"84469744","pagetype":"Browse_genre","url":"http://www.stubhub.com/search/doSearch","genre":"default","genreid":"","event":"default","eventid":"default","genreparentid":"","cobrandid":"47","pgeo":"","ipgid":"674","salemethod":"'null'","price":"'null'","fee":"","TT_variant":""},"to":5,"c":"http://www.stubhub.com/search/doSearch","pv":10,"lc":{"d3":{"v":4,"s":true},"d0":{"v":5,"s":true},"d2":{"v":1,"s":false}},"cd":0,"f":1447454709516,"sd":0,"v":1}; TLTHID=5A02C8488A58108A4454D666311E6DD6""",
}

auth = requests.auth.HTTPProxyAuth('username', 'password')
proxies = {'http': 'http://us-ca.proxymesh.com:31280'}


if __name__ == '__main__':
    data = []
    now = datetime.datetime.now()
    directory = 'snapshots/snapshot_{}_{}_{}_{}_{}'.format(now.month, now.day, now.year, now.hour, now.minute)
    os.mkdir(directory)
    try:
        last_found = 1
        i = 0
        while last_found > 0:
            payload['start'] = i * rows
            r = requests.get(listing_endpoint, params=payload, headers=headers, proxies=proxies, auth=auth)
            r.raise_for_status()
            response = r.json()
            events = response['response']['docs']
            last_found = len(events)
            data = events
            with gzip.open('{}/{}.json'.format(directory, i), 'wt') as outfile:
                json.dump(data, outfile)
            i += 1
            print i, r.url
    print "DONE"
    except:
        # failed
        with open('{}/FAILED.txt'.format(directory), 'wt') as outfile:
            outfile.write('FAIL')