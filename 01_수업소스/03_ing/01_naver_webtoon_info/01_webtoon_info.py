# pip install requests beautifulsoup4
## 네트워크 탭에서 Fetch/XHR  확인#
import requests
from bs4 import BeautifulSoup


webtoon_id = 662774
url = f"https://comic.naver.com/api/article/list?titleId={webtoon_id}"

response = requests.get(url)
data = response.json()
print(data.keys())
print(data['pageInfo'])