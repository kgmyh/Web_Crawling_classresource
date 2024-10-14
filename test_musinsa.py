import requests
# XMLHTTP 로 요청하는 것을 찾음.
url = 'https://api.musinsa.com/api2/dp/v1/brand/brand-shop/musinsastandard/ranking-goods?gf=A&sortCode=REALTIME&size=100'
header = {
    "origin":"https://www.musinsa.com",
    "referer":"https://www.musinsa.com/",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}
res = requests.get(url, headers=header) #응답 결과를 반환(requests.models.Response)

print(res.status_code)
data = res.json()
from pprint import pprint
# pprint(data)
print(len(data['data']['goodsList']))
print(data['data']['goodsList'][0])


