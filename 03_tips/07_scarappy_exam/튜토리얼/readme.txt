exam01 - blog.scrapinghub.com
- 기본 (프로젝트 만들고 실행 해보기 - response.url 등 확인)
exam02 -  blog.scrapinghub.com
- 메인페이지 제목 파싱 (css, xpath 추출)
exam03 -  blog.scrapinghub.com
- 순환 조회 - 메인페이지에서 링크 - parse_blog에서 내용 조회

exam04 
- exam03 카피해서 만든다.
	- scrapy.cfg 변경
	- settings.py 모듈명 변경(최상단)
- item 사용
- 파이프라인 DB 적용
	- encoding pipeline구현
            - DB적용
- settings.py 파일저장 옵션

exam05 - 파이프라인 기본 예제
 - 알렉사
 - rank 1 ~ 30만 저장 (출력은 로그가 아니라 파일에 저장하는 것을 말한다.)
 - sqlite3이용해 저장
 - 오라클 이용해 저장