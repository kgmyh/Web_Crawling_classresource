scrapy startproject exam06_paging

scrapy genspider daum_news news.daum.net

start_url : https://news.daum.net/breakingnews/digital (전체뉴스 - 맨맨 아래)



settings.py : FEED_EXPORT_ENCODING = 'utf-8' 이거 잡는다. 한글 한글
상세기사가 redirect 된다. 그래서 allowed_domain은 daum.net으로 잡는다.
//////user-agent 잡는다.// 안잡아도 된다.