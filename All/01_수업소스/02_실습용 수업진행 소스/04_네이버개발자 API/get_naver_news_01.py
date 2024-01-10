# 수업때는 그냥 쓰자. 

# 클라우드 조회 예제
with open('./account.txt') as f:
    client_id = f.readline().strip()
    client_secret = f.readline().strip()

# Documnets에서 서비스 API 의 검색 클릭하면 기본 예제 나온다. 
# 거기서 url과 header값 설명


import requests
from pprint import pprint
# keyword = input('검색할 단어:')
keyword = "손흥민"

# url 뒤의 blog를 news로 변경 (news 검색이므로)
url = "https://openapi.naver.com/v1/search/news?query={}".format(keyword) # json 결과

headers = {
    "X-Naver-Client-Id":client_id,
    "X-Naver-Client-Secret":client_secret
}
res = requests.get(url, headers=headers)

if(res.status_code==200):
    result = res.json() #json을 dictionary로 읽어줌
    # pprint(result) 
    # 이거 찍어 보고(가져오는 내용 설명하고) 뉴스 링크만 가져 오는 아래 코드 추가
    items = result['items']
    news_link_list = [] #url 저장할 리스트
    for item in items:
        link = item['link']
        if 'news.naver.com' in link: #링크중 naver 링크가 아닌 것들이 있다. 그것들은 문서 포멧이 다르므로 내용 조회가 안된다. (제목, 내용들을 나중에 상세에서 따로 조회한다고 했을때) 그래서 뺀다.
            news_link_list.append(link)
#     news_link = [item['link'] for item in items if 'naver' in item['link']]
    print(len(news_link_list))
    pprint(news_link_list)
else:
    print("Error Code:%d" % res.status_code)
    print(res.text)

# 기본적으로 10개의 기사가 조회된다.
# 제목(title), 기사내용(desciption) 전체가 나오는 것이 아니라 일부만 나온다. 그래서 글중에 ... 이 있다.
# 그러므로 기사 크롤링을 위해서는 url을 가져와서 실제 그 기사로 이동해 가져 와야 한다.
# 조회항목: https://developers.naver.com/docs/search/news/ 참고
# display : 몇개의 내용이 조회되었는지
# originallink : 기사가 있는 신문사 url
# link : 검색결과 클릭하면 이동할 url
#	  -네이버에서 기사를 제공할 경우 네이버 url, 아니면 originallink와 동일
#     - 네이버 기사는 news.naver.com 이 들어간다.
# pubDate: 기사제공시간. 
#    - Wed, 06 Nov 2019 21:05:42 +0900  =? +0900은 잘라낸다. (표준시 기준 9시간 후 표시)
#    - 형식문자 : %a, %d %b %Y %H:%M:%S