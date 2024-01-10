import scrapy

# 제목 css 셀렉터 : div.post-header > h2 > a::text
# 제목 xpath     :  //div[@class="post-header"]/h2/a/text()
class ScrapinghubSpider(scrapy.Spider):
    name = 'scrapinghub'
    allowed_domains = ['blog.scrapinghub.com']
    start_urls = ['https://blog.scrapinghub.com/']

 
    # 응답을 처리하는 함수 - parse메소드 => generator로 구현
    # generator :   yield 반환값
    # 반환값 : Request - 다음 요청
    #         Item/Dictionary - 최종 조회 결과 - 1개씩
    #         None
    def parse(self, response):
        # getall()==extract() - 조회한 내용들을 string(문자열) 리스트로 묶어서 반환
        # get()==extract_first() - 조회한 내용들중 첫번째 element를 string(문자열)로 반환
        # result_list = response.css('div.post-header > h2 > a::text').getall()
        result_list = response.xpath('//div[@class="post-header"]/h2/a/text()').extract()
        for title in result_list:
            yield {'title':title}