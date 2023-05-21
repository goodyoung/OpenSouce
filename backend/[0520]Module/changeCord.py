import requests
import json

class ChangeAddress:
    def __init__(self,address):
        self.address = address
        self.result = self.changeAddress(self.address)
        
    def changeAddress(self, address):
        url = f'https://dapi.kakao.com/v2/local/search/address.json?query={address}'
        headers = {"Authorization": "KakaoAK ddade78155e5ff37aab8ddc00f07c0df"} #kakao rest api key
        address_json = requests.get(url, headers=headers).json()['documents'][0]
        return address_json['x'],address_json['y']