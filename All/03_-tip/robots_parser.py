from urllib import robotparser

rp = robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
rp.read()
# print(rp)
url = 'http://example.webscraping.com/'
user_agent = 'BadCrawler'
print(rp.can_fetch(user_agent, url))

user_agent = 'GoodCrawler'
print(rp.can_fetch(user_agent, url))
print(rp.crawl_delay(user_agent))
