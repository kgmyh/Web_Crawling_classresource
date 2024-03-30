import json

books = {
    'total':30,  #값: 리터럴
    'category':['소설','시','에세이'], #값: 리스트(튜플)
    'search':{'keyword':'영화', 'publisher':'우리출판사'},#값: dict
    'book_list':[
        {'title':'제목1','publisher':'우리출판사1','page':200},
        {'title':'제목2','publisher':'우리출판사2','page':300},
        {'title':'제목3','publisher':'우리출판사3','page':400},
        {'title':'제목4','publisher':'우리출판사4','page':500}
    ]  #값: 리스트 - 원소:dict들 
}


#딕셔너리 조회. dic['키'], dic.get('키'), dic.get('키', 기본값)
# books['aaaa']
print(books.get('aaaa'), books.get('aaa','없음'))
# total값 - 30
# print(books['total'])
# # category의 시
# print(books['category']) #값:list
# print(books['category'][1])
# # search의 publisher - 우리출판사
# print(books['search']['publisher'])

# book_list의 제목1
print(books['book_list'][0]['title'])
# book_list의 제목3
print(books['book_list'][2]['title'])
# book_list의 우리출판사 4
print(books['book_list'][3]['publisher'])
# book_list의 우리출판사 2
print(books['book_list'][1]['publisher'])
# book_list의 300
print(books['book_list'][1]['page'])
# book_list의 500
print(books['book_list'][3]['page'])
# book_list의 200
print(books['book_list'][0]['page'])

l = books['book_list']
d = l[0]
print(d['page'])

# dictionay -> json(string) : json.dumps(dic)
# json(string) -> dictionay : json.loads(string)
json_str = json.dumps(books)
print(type(json_str))
print(json_str)

json_dict = json.loads(json_str)
print(type(json_dict))
print(json_dict['total'])