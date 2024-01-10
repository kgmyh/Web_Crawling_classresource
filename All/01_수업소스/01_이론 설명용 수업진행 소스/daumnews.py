
import re
import requests
from bs4 import BeautifulSoup

def get_daumnews_info(url):
    """
    [파라미터]
        url : 다음 기사 url
    [반환값]
        tuple: (제목, 기자이름, 입력일, 기사내용)
    """
    res = requests.get(url)
    if res.status_code==200:
        soup = BeautifulSoup(res.text, 'html.parser')
        title_tag = soup.select_one('h3.tit_view')
        reporter_tag = soup.select_one('span.info_view span.txt_info:nth-child(1)')
        input_date_tag = soup.select_one('span.info_view span.txt_info:nth-child(2)')
        news_tag = soup.select_one('div#harmonyContainer')
        
        title = title_tag.text.strip()
        reporter = reporter_tag.text.strip()
        input_date = input_date_tag.span.text.strip()
        news = re.sub(r'\s+', ' ', news_tag.text)
        return title, reporter, input_date, news
    else:
        raise Exception("요청 결과를 가져오지 못함. %d" % res.status_code)
