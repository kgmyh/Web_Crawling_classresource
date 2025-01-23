
    # if idx == 21:
    #     break
    # res = requests.get(url)
    
    # try:
    #     if res.status_code == 200:
    #         soup = BeautifulSoup(res.text, 'lxml')

    #         title = soup.select_one('h3#articleTitle').get_text()
    #         content_container = soup.select_one('div#articleBodyContents')

    #     #     javascript코드 상관없이 내용 읽어들이기
    #         content = soup.select_one('div#articleBodyContents').get_text()  #여기선 주석은 알아서 빼준다.


            
    #     #  <script> 태그 제거 & 주석
    #         #간단버전
    #         content = content.replace('// flash 오류를 우회하기 위한 함수 추가','').replace('function _flash_removeCallback() {}','')
            
    #         # Comment 객체 또는 Tag객체인데 태그명이 script인 것은 뺀다.
    #         # NavigableString의 경우는 그냥 content에 붙인다.
            
            
    #     #     content = ''
    #     #     for item in content_container:
    #     #         if type(item) == Comment or (type(item) == Tag and item.name == 'script'): #하나씩 할 때는 주석을 빼야 한다.
    #     #             continue

    #     #         if type(item) == Tag:
    #     #             content += item.get_text().strip()
    #     #         else: #NavigableString
    #     #             content += item

    #         news_title.append(title.strip())
    #         news_content.append(content.strip())
            
    #     else:
    #         print('오류발생:', res.status_code)
    #         print(res.text)
            
    # except:
    #     print("{}번째 url 기사 읽는 도중 오류".format(idx))
    #     continue