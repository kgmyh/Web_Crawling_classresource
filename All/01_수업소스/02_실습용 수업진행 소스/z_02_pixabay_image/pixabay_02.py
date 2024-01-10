# 메인페이지 Discover more 클릭하면 제공 이미지 모두를 받을 수 있다.
# 페이지는 페이징 처리되어 Next 버튼을 클릭하면 다음페이지로 이동한다.

# 1 ~ 10 페이지의 image들을 다운 받는다.

# 1 페이지의 이미지를 다운받는 함수를 만든다.
# - 매개변수 : 1페이지의 html text
# - BeautifulSoup을 이용해 그페이지의 이미지들을 다운 받는다.

# 페이지 : https://pixabay.com/ko/images/search/?pagi={페이지번호}

# 검색 :https://pixabay.com/ko/images/search/{검색키워드}/

# 페이지, 검색: https://pixabay.com/ko/images/search/{검색키워드}/?pagi={페이지번호}
import os
import time
import requests
from bs4 import BeautifulSoup

def download_image_list(end_page=1, keyword=None):
    """pixabay 이미지 목록에 있는 사진들을 다운받는 함수
    
    Keyword Arguments:
        end_page {int} -- 다운받을 목록의 마지막 페이지 (default: {1})
        keyword {str} -- 검색키워드 (default: {None})
    """
    # 이미지 저장 디렉토리 생성
    dir = './pixabay_image2'
    if not os.path.isdir(dir):
        os.mkdir(dir)

    base_url = 'https://pixabay.com/ko/images/search/'
    if keyword:  #keyword!=None
        base_url = base_url+keyword+'/'

    base_url = base_url+'?pagi={}'

    for page in range(1, end_page+1):
        url = base_url.format(page)
        
        # 요청
        res = requests.get(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'lxml')
            img_tag_list = soup.select('div.item img')

            # 이미지 하나씩 가져오기.
            for img in img_tag_list:
                src_attr = img.get('src') # <img src='xxxx'> src속성값(xxxx)
                
                if src_attr == '/static/img/blank.gif': #lazy-loading
                    src_attr = img.get('data-lazy')
                
                # 이미지 요청 및 저장
                filepath = dir+"/"+src_attr.split('/')[-1]
                
                #이미지 요청
                img_res = requests.get(src_attr)
                if img_res.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(img_res.content) # 이미지 저장
                else:
                    print("{} 저장실패".format(filepath))
                # 다음 요청까지 잠깐의 간격을 준다.
                print('.', end='')
                time.sleep(0.5)

        else:
            print("페이지 {} 요청실패".format(page))



if __name__ == '__main__':
    download_image_list(keyword='lion', end_page=2)