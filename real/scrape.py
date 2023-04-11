from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
import re
import json
import os
import random
from pydash import omit
import uuid
import glob


DIR = os.path.dirname(os.path.abspath(__file__))

class Tls(threading.local):
    def __init__(self) -> None:
        self.playwright = sync_playwright().start()



class Worker:
    tls = Tls()

    def rt__(self):
        return random.randrange(1, 10)

    def rw__(self):
        return random.randrange(1, 15)

    def uuid__(self):
        return str(uuid.uuid4())[:5]
    
    def run__(self, goleki, kota): 
        dataku = []  
        try:
            browser = self.tls.playwright.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto('https://www.google.com/maps', timeout=10000)
            page.wait_for_timeout(3000)
            page.locator('//input[@id="searchboxinput"]').fill(goleki)
            page.wait_for_timeout(3000)
            page.keyboard.press('Enter')
            page.wait_for_timeout(3000)

            page.hover('(//div[@role="article"])[1]')            
            for i in range(10): 
                page.mouse.wheel(0, 10000)
                page.wait_for_timeout(3000)
                listings = page.locator('//div[@role="article"]').all()

            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(3000)
                    address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                    alamat = page.locator(address_xpath).inner_text()

                    hs = json.load(open(f"{DIR}/jatim/data/{kota}/kecamatan.json"))
                    ck = ["Kec. " + x['name'] for x in hs]
                    if re.search(r', Indonesia', alamat):
                        alt = alamat.replace(', Indonesia', '')
                    else:
                        alt = alamat

                    if re.search(r'RT.', alamat):
                        real_alamat = alamat
                    else:
                        real_alamat = f'RT.{self.rt__()}/RW.{self.rw__()} {alamat}'

                    s__ = re.split(',', alt)
                    nama_kec = s__[-3].strip()
                    if not re.search(r'Kec. ', nama_kec):
                        kcmt = "Kec. " + nama_kec
                    else:
                        kcmt = nama_kec
                    if kcmt in str(ck):
                        js = json.load(open(f"{DIR}/jatim/data/{kota}/data/{kcmt.split('.')[1].strip()}.json"))
                        ds = s__[-4].strip()
                        for desa in js:
                            nama__kec = kcmt.split('.')[1].strip()
                            if ds in desa['name']:
                                hsl = omit(desa, "name")
                                hsl.update({
                                "desa": desa['name'],
                                "kecamatan": nama__kec,
                                "kota": kota,
                                "alamat": real_alamat
                                })
                                dataku.append(hsl)
                                print(hsl)
                except:continue
            browser.close()
            datakux = json.dumps(dataku, indent=4)
            if dataku:
                with open(f'{DIR}/jatim/data/{kota}/libs/{self.uuid__()}.json', 'w', encoding="utf-8") as f:
                    f.write(datakux)
            else:
                pass
        except:
            browser.close()



if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=1) as executor:
        list_keyword = ['kos', 'sekolah', 'masjid', 'mushola', 'gereja', 'warung',
                        'pom', 'kopi', 'konter', 'kantor', 'lapangan', 'tugu', 'toko',
                        'store', 'rumahku', 'warung', 'mbok', 'mak', 'pasar', 'coffe', 'jajan']
        for i in json.load(open(f'{DIR}/jatim/kabupaten.json')):
            if re.search(r'Kota', i['name']):
                kota = i['name']
            else:
                kota = i['name'].split()[1]
            fs = json.load(open(f'{DIR}/jatim/data/{kota}/kecamatan.json'))
            dt = [x['name'] for x in fs]
            for g in list_keyword:
                for c in dt:
                    keyi = f"{g} di {c} {kota}"
                    worker = Worker()
                    executor.submit(worker.run__, keyi, kota)

