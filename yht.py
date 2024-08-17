import requests
import datetime
import time
import msvcrt
from win10toast import ToastNotifier
toaster = ToastNotifier()
route_url="https://api-yebsp.tcddtasimacilik.gov.tr/sefer/seferSorgula"
cart_url="https://api-yebsp.tcddtasimacilik.gov.tr/vagon/vagonHaritasindanYerSecimi"
headers={
    'Authorization': 'Basic ZGl0cmF2b3llYnNwOmRpdHJhMzQhdm8u'
    }
cities=['Ankara Gar','Eskişehir','Sivas']
id=[234516259,234516254,234517773]
print(cities)
bin=input('Hangi şehirden? (Numara yaz)')
bin_id=id[int(bin)-1]
print(cities)
inn=input('Hangi şehire? (Numara yaz)')
in_id=id[int(inn)-1]
tarih=input('Hangi tarihte? (YYYY-MM-DD)')

def format_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%b %d, %Y")
def finder():
    formatted_date=format_date(tarih)
    body={"kanalKodu": 3,
        "dil": 0,
        "seferSorgulamaKriterWSDVO": {
            "satisKanali": 3,
            "binisIstasyonu": cities[int(bin)-1],
            "inisIstasyonu": cities[int(inn)-1],
            "binisIstasyonId": bin_id,
            "inisIstasyonId": in_id,
            "binisIstasyonu_isHaritaGosterimi": False,
            "inisIstasyonu_isHaritaGosterimi": False,
            "seyahatTuru": 1,
            "gidisTarih": f"{formatted_date} 00:00:00 AM",
            "bolgeselGelsin": False,
            "islemTipi": 0,
            "yolcuSayisi": 1,
            "aktarmalarGelsin": True,}
    }
    data=requests.post(route_url,json=body,headers=headers).json()
    if data['cevapBilgileri']['cevapKodu'] == '000':
        for route in data['seferSorgulamaSonucList']:
            route_time=datetime.datetime.strptime(route['binisTarih'], "%b %d, %Y %I:%M:%S %p")
            check_route(route)   

def check_route(route):
    print(f"Checking for time: {route['binisTarih']}")
    empty=0
    for cart in route['vagonTipleriBosYerUcret']:
        for cart_detail in cart['vagonListesi']:
            cart_no=cart_detail['vagonSiraNo']
            print(f"Checking for cart: {cart_no}")
            empty+=check_specific_seats(route['seferId'], cart_no) 
    if empty!=0:    
        toaster.show_toast(f'{route['binisTarih']}'+' de '+f'{empty}'+' boş yer var',' ',
            icon_path=None,
            duration=None,
            threaded=True)        
def check_specific_seats(routeId, cart_no):
    body = {
        "kanalKodu": "3",
        "dil": 0,
        "seferBaslikId": routeId,
        "vagonSiraNo": cart_no,
        "binisIst": cities[int(bin)-1],
        "InisIst": cities[int(inn)-1]
    }
    empty=0
    data=requests.post(cart_url,json=body,headers=headers).json()
    if data['cevapBilgileri']['cevapKodu'] == '000':
        for seat in data['vagonHaritasiIcerikDVO']['koltukDurumlari']:
            if seat['durum'] == 0:
                if not seat['koltukNo'].endswith('h'): 
                    empty+=1 
    return empty                
def start():
    while True:
        finder()
        for n in range(600):
            time.sleep(0.1)  
            if msvcrt.kbhit():      #kills the process with a keystroke on terminal
                return 0  
start()            
        
    
        

    

