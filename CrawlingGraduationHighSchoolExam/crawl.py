import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import json
import csv

class LegacyRenegotiationAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.options |= 0x4  
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', LegacyRenegotiationAdapter())

folder_path = './data/'
for year in range(2022, 2025):
    with open(f'{folder_path}raw{year}.csv', "w", newline='') as csvfile:
        fieldnames = ["Code", "Toan", "NguVan", "NgoaiNgu", "VatLi", "HoaHoc", "SinhHoc","KHTN", "DiaLi", "LichSu", "GDCD", "KHXH"]
        #fieldnames = ["message", "success", "result"]
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        provincecode = "64"
        with session as S:
            for j in range(15000):
                try:
                    sid = str(j).zfill(6)
                    link = f'https://diemthi.vnanet.vn/Home/SearchBySobaodanh?code={provincecode}{sid}+&nam={year}'
                    response_API = S.get(link)
                    #print(response_API.text)
                    responsetext=''
                    responsetext+='[{'
                    responsetext += str(response_API.text)[44:-1:] 
                    idx = responsetext.find("ResultGroup")
                    responsetext=responsetext[:idx-2:]
                    responsetext+='}]'
                        # print(responsetext)
                    responsejson=json.loads(responsetext)
                        # print(responsejson)
                    for row in responsejson:
                        writer.writerow(row)
                except:
                    pass
        