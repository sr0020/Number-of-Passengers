# 서울특별시 지하철 호선별 역별 시간대별 승하차 인원 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import openpyxl

# 엑셀 파일 추출
def main():

    df = pd.read_csv('num_of_passengers.csv', encoding='euc-kr')
    # print(df)

    # 202302월의 3호선 이용자 추출
    result = df[df['사용월'].astype(str).str.contains('202302')]
    result = result[result['호선명'].astype(str).str.contains('3호선')]

    # 각 시간대별 승차인원 추출 (하차인원 들어간 열 제외)
    result = result.drop('작업일자', axis=1)
    result = result[result.columns.drop(list(result.filter(regex='하차')))]

    # result = result[result.columns.drop(list(result.filter(regex='사용월')))]
    # result = result[result.columns.drop(list(result.filter(regex='호선명')))]

    result.drop(labels=['사용월', '호선명'], axis=1, inplace=True)

    result.set_index(keys=[result['지하철역']], inplace=True)
    result = result.T
    
    remove_str(result)
    plot(result)

    result.to_csv('result.csv', encoding='euc-kr')

# 엑셀 인덱스에서 특정 문자('승차인원') 제거
def remove_str(result):

    # result.index[16].replace('승차인원', '')

    temp = []

    for i in range(len(result.index)):
        temp.append(result.index[i].replace('승차인원', ''))
        print(result.index[i].replace('승차인원', ''))
    
    print(temp)
    result.index = temp
    
    print(result.index)

# 그래프 추출
def plot(result):

    # temp = result.loc[result['지하철역'] == '고속터미널']

    # 행렬 추출(plot 위한)
    xs = result.index.to_list()
    ys = result['고속터미널'].to_list()

    # print(type(xs[1]), '\n', type(ys[1]))
    # print(xs, '\n', ys) 

    plt.rcParams['font.family'] = 'Malgun Gothic'

    plt.figure(figsize=(40, 25))	
    plt.xlabel('Time')		
    plt.ylabel('Num of Passengers')	

    # ys는 현재 '지하철역 이름(str)'과 '승차인원 수(int)' 동시에 들어간 상태
    # ys 리스트에서 [0]번 인덱스(지하철역 이름) 삭제
    ys.pop(0)
    # print(ys)

    # print(len(xs), len(ys))
    # xs와 ys의 길이가 맞지 않아 valueerror(shape mismatch) 발생. 
    # x의 '지하철역' 인덱스도 삭제
    xs.pop(0)
    # print(xs)

    # 막대그래프 그리기
    # 일부분만 사용할 경우, xs[12:18] 이런식으로 인덱싱
    plt.bar(xs, ys, width=0.6, color='navy')
    plt.show()

    plt.plot(xs, ys)
    # plt.savefig('./result.png', dpi=500)

    print('Done Plot!!')

if __name__== '__main__':
    
    main()
    print("DONE~")