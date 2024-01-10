import requests
from bs4 import BeautifulSoup 


# 뉴스기사 하나에서 제목, 입력일자, 내용 추출
# url = 'https://news.v.daum.net/v/20191025171501898'
# url = 'https://news.v.daum.net/v/20191025103559221'
url = 'https://news.v.daum.net/v/20200722102359305'
res = requests.get(url)

if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'lxml')

    # 찾을 때 ctr + f 로 해서 태그의 class나 id가 중복되어 있는 지 찾아본다.
    #제목 : h3.tit_view
    #기자: span.info_view > span.txt_info:nth-child(1) # 가끔 기자이름이 없는 경우도 있다. 
    #작성일: span.info_view > span.txt_info:nth-child(2)
    #수정일: span.info_view > span.txt_info:nth-child(3)
    #뉴스내용: div.news_view

    #제목 가져오기
    title_tag = soup.select_one('h3.tit_view')
    info1_tag = soup.select_one('span.info_view > span.txt_info:nth-child(1)')
    info2_tag = soup.select_one('span.info_view > span.txt_info:nth-child(2)')
    info3_tag = soup.select_one('span.info_view > span.txt_info:nth-child(3)')
    news_tag = soup.select_one('div.news_view')


    print('제목:',title_tag.text.strip())
    print('기자:',info1_tag.text.strip())
     try:
        print('입력일자:',info2_tag.text.strip())
    except:
        print('입력일자: 없음')
    print(news_tag.text)
    # content = re.sub('\n+', '\n', news.text)
    # print(content)
else:
    print("연결 실패 - %d" % res.status_code)    