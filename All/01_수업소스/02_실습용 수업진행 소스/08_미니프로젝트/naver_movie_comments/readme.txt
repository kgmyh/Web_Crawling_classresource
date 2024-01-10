# 네어버 영화 댓글 - 평점
scrapy startproject naver_movie_comments
cd naver_movie_comments
scrapy genspider naver_movie_comment naver.com


scrapy crawl naver_movie_comment