import requests
from pprint import pprint

# url: http 로 요청한다.
# api_key는 encoding/decoding 하나씩 시도해본다.
url = "https://apis.data.go.kr/1613000/BUSINESS_CAR/T_OD_BUSINESS_CAR_BRN_INFO"
api_key = "laglZqyWw2mLMtqjyw9zoItPpOt3ChysDk/RvZnvfD+ejQHlbetkWSrYTKrpBcgrYjRdW+MP5b6d7ArwHxVj4g=="

params  = {
    "serviceKey": api_key,
    "numOfRows": 10,
    "pageNo": 1,
    "resultType": "json",
    "crtr_yr": 2022,
    "mtrpl_lcgv_nm": "서울",
}

response = requests.get(url, params=params, verify=False)
# verify=False: SSL 인증서 검증을 하지 않음
# verify=True: SSL 인증서 검증을 함
if response.status_code == 200:
    data = response.json()
    pprint(data)
else:
    print(f"Error: {response.status_code}")