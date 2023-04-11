import json
import os
import glob
import re
from pydash import omit


DIR = os.path.dirname(os.path.abspath(__file__))


dataku = {}



kota = "Bangkalan"
file = open('alamat.txt').readlines()
for line in file:
    try:
        if re.search(r'Indonesia', line):
            data = line.strip().replace(', Indonesia', '')
        else:
            data = line.strip()

        alm = data.split(',')  
        desa= alm[-4].strip()
        kec = alm[-3]
        print(kec)
        
        
        
        
        for kecm in json.load(open(f'{DIR}/{kota}/kecamatan.json')):
            kecmm = kecm['name']
            print(kecmm)
            if re.search(rf'{kecmm}', kec):
                ft = omit(kecm, "name")
                ft.update({
                    "kota": kota,
                    "kecamatan": kecmm
                    })
                if os.path.exists(f'{DIR}/{kota}/data/{kecmm}.json'):
                    js = json.load(open(f'{DIR}/{kota}/data/{kecmm}.json'))
                    for cek in js:
                        desas = cek['name']
                        if re.search(rf'{desa}', desas):
                            id_desa     = cek['subDistrictId']
                            nama_desa   = cek['name']
                            kode_pos    = cek['postalCode']
                            ft.update({
                                "subDistrictId": id_desa,
                                "desa": nama_desa,
                                "pos": kode_pos,
                                "alamat": line
                            })
                            dataku.update(ft)
    except:
        print(f"Alamat tidak ditemukan: {line.strip()}")                        


js = json.dumps(dataku, indent=4)
print(js)