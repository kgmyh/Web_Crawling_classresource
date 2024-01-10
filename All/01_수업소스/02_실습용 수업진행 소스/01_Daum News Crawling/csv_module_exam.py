import csv

# csv: csv 형식에 맞게 출력 및 읽어주는 모듈.
# open()으로 생성한 파일 객체를 받아 처리한다.
c = [['a','b','c'],[1,2,3],['가','나','다']]

with open('test.csv', 'w', encoding='UTF-8', newline='') as f:

    # 출력 stream을 넣어 출력처리 객체를 받아온다.
    wr = csv.writer(f)
    #writerow(리스트): 한줄출력
    # writerows(리스트>리스트): 한번에 모두 출력
    wr.writerows(c)  

# 읽기    
# csv.reader(file) : _csv_reader 객체. 반복문을 이용해 한줄씩 읽어 온다. 
with open('test.csv', 'r', encoding='UTF-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
    
