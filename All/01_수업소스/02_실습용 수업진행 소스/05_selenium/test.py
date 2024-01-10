from bs4 import BeautifulSoup 
import requests
url = 'https://www.tripadvisor.co.kr/Restaurant_Review-g294197-d3200324-Reviews-Jungsik-Seoul.html'

res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')
l = soup.select('a.nav.next.taLnk.ui_button.primary')
print(l[0].get_text())