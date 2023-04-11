import json
import os
import requests


DIR = os.path.dirname(os.path.abspath(__file__))



headers = {
        "Host": "www.blibli.com",
        "accept": "application/json",
        "x-userid": "2caf8add-4bff-4afe-9741-853eecc549a8",
        "x-sessionid": "a97e9dff-ad9e-4c6f-b09b-753c9d99a0f4",
        "x-requestid": "689892f8-93f4-4095-89ab-c5291f635603",
        "user-agent": "BlibliAndroid/9.8.0(6029) 2caf8add-4bff-4afe-9741-853eecc549a8 Dalvik/2.1.0 (Linux; U; Android 11; Redmi 8 Build/PKQ1.190319.001)",
        "accept-language": "id",
        "build-no": "6029",
        "content-type": "application/json; charset\u003dUTF-8",
        "channelid": "android",
        "storeid": "10001",
        "authorization": "bearer AT-9D0F7805-08A9-4743-A3FB-9196E8C5026C",
        "x-blibli-user-email": "muajuk@hpku.me",
        "accept-encoding": "gzip"
    }

import re

kab = json.load(open('kabupaten.json'))
for ids in kab:

    id_cty = ids['cityId']
    if re.search(r'Kota', ids['name']):
        nm_cty = ids['name']
    else:
        nm_cty = ids['name'].split()[1]
        
    try:
        os.makedirs(f'{DIR}/data/{nm_cty}')
        os.makedirs(f'{DIR}/data/{nm_cty}/libs')
        os.makedirs(f'{DIR}/data/{nm_cty}/data')
    except:
        print(f'folder ada: {nm_cty}')
        
    url         = f"https://www.blibli.com/backend/common/region/countries/ID/provinces/11/cities/{id_cty}/districts"
    res         = requests.get(url=url, headers=headers).json()
    kec         = res['data']
    js__        = json.dumps(kec, indent=4)
    open(f'{DIR}/data/{nm_cty}/kecamatan.json', 'w').write(js__)
    x = json.load(open(f'{DIR}/data/{nm_cty}/kecamatan.json'))
    for line in x:
        ids = line["districtId"]
        nmm = line['name']
        url = f"https://www.blibli.com/backend/common/region/countries/ID/provinces/11/cities/{id_cty}/districts/{ids}/subDistricts"
        res = requests.get(url=url, headers=headers).json()
        open(f'{DIR}/data/{nm_cty}/data/{nmm}.json', 'w').write(json.dumps(res['data'], indent=4))





