import bs4
import requests

# Naver 뉴스의 메뉴에서 랭킹 선택
url = "https://news.naver.com/main/ranking/popularDay.naver"
selector = "#wrap > div.rankingnews._popularWelBase._persist > div.rankingnews_box_wrap._popularRanking > div > div > ul > li > div > a"


res = requests.get(url)
if res.status_code == 200:
    soup = bs4.BeautifulSoup(res.text, "lxml")
    a_list = soup.select(selector)
    result_list = []
    print(len(a_list))
    for a_tag in a_list:
        print(a_tag["href"], a_tag.text)
        break