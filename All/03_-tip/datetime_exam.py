import os


from datetime import datetime
from datetime import timedelta

# datetime 패키지 제공 클래스
# datetime: 날짜 시간 저장
# date    : 날짜 저장
# time    : 시간 저장
# timedelta: 날짜, 시간의 범위(차이) 저장. 몇일후, 몇주전 식으로 날짜 계산시 사용한다.



# 문자열 -> 날짜
# https://docs.python.org/ko/3.8/library/datetime.html#strftime-and-strptime-behavior 
print(datetime.strptime("2017-01-02 14:44:22", "%Y-%m-%d %H:%M:%S"))
print(datetime.strptime("2019-01-01", "%Y-%m-%d"))
print(datetime.strptime("20190111", "%Y%m%d"))

# datetime - datetime : 두 datetime 간의 날짜 차이 반환 (+, *, / 연산은 없다.)
# 피연산자는 datetime, date. (time은 연산이 안된다.)
from datetime import date
d1 = date(2000,10,2)
d2 = date(2000,11,2)
print("---------------------")
print(d2-d1)
print("---------------------")

# time은 연산이 안된다.
# from datetime import time
# t1 = time(10,20,10)
# t2 = time(9,10,20)
# print(t1 + t2)

# 날짜 비교 ==, !=, >, >=, <,<=
# 미래가 과거보다 더 크다.
print('==비교')
print(datetime(2001,10,20) == datetime(2001,10,20))
print("날짜 크기 비교 : 미래가 과거보다 더 크다.")
print(datetime(2001,10,10) < datetime(2001,10,11))

diff = datetime(2001,10,10) - datetime(2001,10,11)
print(diff, type(diff))




def date_range(s_date:'YYYYMMDD', e_date:'YYYYMMDD')->list:
    s_date = datetime.strptime(s_date, '%Y%m%d')
    e_date = datetime.strptime(e_date, '%Y%m%d')
    date_list = []
    d_diff = timedelta(days=1)
    while s_date <= e_date:
        date_list.append(s_date)
        s_date += d_diff
    return date_list

# 판다스 이용
import pandas as pd
def date_range2(s_date:'YYYYMMDD', e_date:'YYYYMMDD')->list:
    dt_index = pd.date_range(s_date, e_date)
    # DatetimeIndex 를 파이썬 datetime을 변환하는 함수. (ndarray로 반환)
    l = dt_index.to_pydatetime()
    # print(type(l))
    date_list = [d for d in l]
    return date_list


if __name__ == '__main__':
    print("#"*50)
    lst = date_range('20101010','20101020')
    lst = date_range2('20101010','20101020')
    print(lst)
    print(type(lst[0]))
    