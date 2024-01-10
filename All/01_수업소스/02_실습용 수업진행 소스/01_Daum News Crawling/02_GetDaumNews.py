# 01_GetDaumNews.py 함수화

import requests
from bs4 import BeautifulSoup 


#
#  TODO: 매개변수로 다음 뉴스기사 url을 받아  뉴스의 기자이름,작성일, 수정일,뉴스제목,내용을 묶어서 tuple로 반환하는 함수
#
# 기사는 : 기자이름, 작성일, 수정일이 모두 있는 것인데 하고 나서 없는 것들도 있다고 하면서 고치도록
#  
# - 셋다 있는 경우
# - 둘만 있는 경우: 기자명, 입력일
# - 하나만 있는 경우: 기자명 또는 입력일

def get_daum_news(url):
    '''다음 뉴스 URL을 받아 뉴스의 작성일, 수정일, 작성기자, 제목, 내용을 반환
    매개변수
        url: str 뉴스 url
    반환값
        tuple: (제목, 기자이름, 작성일시,수정일시, 내용))
    '''        
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')

            #제목 가져오기
        title_tag = soup.select_one('h3.tit_view')
        info1_tag = soup.select_one('span.info_view > span.txt_info:nth-child(1)')
        info2_tag = soup.select_one('span.info_view > span.txt_info:nth-child(2)')
        info3_tag = soup.select_one('span.info_view > span.txt_info:nth-child(3)')
        news_tag = soup.select_one('div.news_view')


        return (title_tag.text, info1_tag.text, info2_tag.text, info3_tag.text, news_tag.text)

        ################None 처리 ############################
        # title = title_tag.text.strip() if title_tag else None
        # news = news_tag.text.strip() if news_tag else None
        # reporter= None
        # write_date=None
        # modify_date = None
        # 
        # info1이 기자명 또는 입력일 인 경우가 있다.
        # 그래서 info1,2,3 다있으면 기자명,입력일,수정일 다 넣고 둘만 있으면 기자명, 입력일, 하나만 있으면 입력으로 시작하면 입력일 아니면 기자명을 설정
        # if info1_tag and info2_tag and info3_tag:
        #     reporter = info1_tag.text.strip()
        #     write_date = info2_tag.text.strip() 
        #     modify_date = info3_tag.text.strip()
        # elif info1_tag and info2_tag and info3_tag==None:
        #     reporter = info1_tag.text.strip()
        #     write_date = info2_tag.text.strip()
        # elif info1_tag and info2_tag==None and info3_tag==None:
        #     if info1_tag.text.startswith("입력"):
        #         write_date = info1_tag.text.strip()
        #     else:
        #         reporter = info1_tag.text.strip()
                    
        # return (title, reporter, write_date, modify_date, news)
    else:
        raise Exception("요청 결과를 가져오지 못함. %d" % res.status_code)

if __name__ == '__main__':
    url = 'https://news.v.daum.net/v/20191025171501898'
    print(get_daum_news(url))