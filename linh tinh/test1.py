import requests
import json
import csv
with open("rawHG2023.csv", "w", newline='') as csvfile:
    fieldnames = ["Code", "Toan", "NguVan", "NgoaiNgu", "VatLi", "HoaHoc", "SinhHoc","KHTN", "DiaLi", "LichSu", "GDCD", "KHXH"]
    #fieldnames = ["message", "success", "result"]
    writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
    writer.writeheader()
    provincecode = '64'
    for j in range(800001):
        try:
            sid = str(j).zfill(6)
            link = 'https://diemthi.vnanet.vn/Home/SearchBySobaodanh?code='+provincecode+sid+'&nam=2023'
            response_API = requests.get(link)
            #print(response_API.text)
            responsetext=''
            responsetext+='[{'
            responsetext += str(response_API.text)[44:-1:] 
            idx = responsetext.find("ResultGroup")
            responsetext=responsetext[:idx-2:]
            responsetext+='}]'
            #print(responsetext)
            responsejson=json.loads(responsetext)
            #print(responsejson)
            for row in responsejson:
                writer.writerow(row)
        except:
            pass
       