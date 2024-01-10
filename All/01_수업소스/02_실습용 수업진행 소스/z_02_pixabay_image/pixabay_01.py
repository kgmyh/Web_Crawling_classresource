# pixabay.com image 크롤링
# - https://pixabay.com/
#     - 무료 이미지 제공 사이트
#     - 메인 페이지의 맨 아래 버튼을 클릭하면 전체 이미지를 볼 수 있다.
#         - url: https://pixabay.com/images/search/?pagi=페이지번호
#     - 전체 페이지 수는 **상단 오른쪽**에 보인다.
#     - 특정 주제의 이미지만 검색후 볼 수 있다.
#         - url: https://pixabay.com/images/search/검색어/
#
#
# - img 의 링크는 src가 /static/img/blank.gif 인경우 data-lazy 속성을 읽는다. (이미지가 지연로딩처리되 있음)
#     - image가 있는 경우는 data-lazy 속성이 없다. 그래서 src를 먼저 읽고 그게 blank.gif이면 data-lazy를 읽는다.
# - 이미지 지연로딩
#     - 현재 보이는 화면에 나오는 이미지만 로딩하고 화면밖의 이미지는 화면에 나올때 나중에 로딩시켜 초기 로딩속도를 개선하는 방식

#########################################################################
# 메인페이지 이미지 크롤링
#########################################################################
# 페이지 분석
# - 이미지 컨테이너: div.flex_grid.credits
# - 각 이미지의 컨테이너 : 이미지 컨테이너 내의 div.item
# - 이미지: 각 이미지 컨테이너(div.item) 안의 `<a> 내의 <img>`
#     - img의 src 속성에 이미지 링크가 있다. 
#     - src='/static/img/blank.gif' 인 것들은 lazy 로딩이다. 나중에 로딩할 이미지 경로를 data-lazy 속성으로 제공
#
#
import requests
from bs4 import BeautifulSoup
import os

# 이미지 저장 디렉토리 확인후 없으면 생성
img_directory = './pixabay_img' #저장 디렉토리
if not os.path.isdir(img_directory):
    os.mkdir(img_directory)

# 요청
# - **tag.content**: binary 
# - **tag.text**: text
base_url = 'https://pixabay.com'
res = requests.get(base_url)
if res.status_code==200:    
    soup = BeautifulSoup(res.text, 'lxml')
#     print(soup.prettify());
    div_items = soup.select('div.flex_grid.credits > div.item')
    
    for div_item in div_items:
#       div 하위의 img 태그 조회
        img = div_item.find('img') #이미지의 src를 추출하기 위해

#       img태그의 src 속성 조회 (이미지 경로 조회 - lazy loading 을 이용했기 때문에 조회결과가 /static/img/blank.gif 인경우 data-lazy 속성을 조회)
        img_src = img.get('src').strip()

#         print(img_src) #출력해서 /static/img/blank.gif (자리잡기위한 이미지) 것들 보여주고 이미지 지연로딩 설명

        if img_src == '/static/img/blank.gif':
            img_src = img.get('data-lazy').strip()
        
#       이미지 경로에서 파일명만 추출(저장시 사용)
        tmp = img_src.split('/')
        file_name = tmp[len(tmp)-1]

#      이미지 요청해서 파일로 저장
        with open(os.path.join(img_directory, file_name), 'wb') as f:
            img_res = requests.get(img_src)
            if img_res.status_code == 200:
                f.write(img_res.content) #binary는 content로 읽는다.    
else:
    print('요청에 대한 응답을 # 메인페이지의 이미지 목록에서 이미지들 가져오기.')
# 1. 메인페이지를 가져오기.
# 2. 각 image파일들을 요청해서 가져온다.


# 메인페이지 url : https://pixabay.com/ko/
# 전체이미지 목록페이지: https://pixabay.com/ko/images/search/
#     페이징 처리: 왼쪽 상단에 전체 페이지수
#                      https://pixabay.com/ko/images/search/?pagi=3
#
# 이미지 검색: https://pixabay.com/ko/images/search/{검색어}/
#             https://pixabay.com/ko/images/search/tiger/?pagi=3

import os
import requests
from bs4 import BeautifulSoup

# 이미지들을 저장할 디렉토리 생성.
img_path = './pixabay_imgs'
if not os.path.isdir(img_path):
    os.mkdir(img_path)


url = 'https://pixabay.com/ko/'
res = requests.get(url)
# print(res.status_code)
# response.text : 텍스트를 읽는다. (html)
# response.content: binary 파일을 읽는다. (이미지, 동영상, 압축파일)
if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'lxml')

    # selector : div.item
    item_list = soup.select('div.item')
    for item in item_list:
        # item - div.item 에서 <img> 태그 가져오기.
        img_tag = item.select_one('img')
        img_url = img_tag.get('src') #src 속성의 이미지 url 조회
        if img_url == '/static/img/blank.gif':
            img_url = img_tag.get('data-lazy')

        # 이미지 파일명만 추출
        tmp = img_url.split('/')
        filename = tmp[-1]

        # 이미지 파일 요청 - 저장
        img_res = requests.get(src_attr)
        if img_res.status_code == 200:
            with open(img_path+'/'+filename, 'wb') as f:
                f.write(img_res.content) # 이미지 저장
        else:
            print("{} 저장실패".format(filename))
        

else:
    print("응답을 못받음. 코드:{}".format(res.status_code))  #  받지 못함',res.status_code)