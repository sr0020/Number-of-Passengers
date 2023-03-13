# 서울특별시 지하철 호선별 역별 시간대별 승하차 인원 
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.QtWidgets import *
import openpyxl

class Passengers(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(400, 300)
        self.setWindowTitle("UI")
        
        # show, cancel
        show_btn = QPushButton("Show")
        cancel_btn = QPushButton("Cancel")

        self.line = QLineEdit()
        self.line.setText('호선명')

        self.station = QLineEdit()
        self.station.setText('역 이름')

        # text box 레이아웃
        text_lay = QVBoxLayout()
        text_lay.addWidget(self.line)
        text_lay.addWidget(self.station)

        # button 레이아웃
        btn_lay = QHBoxLayout()
        btn_lay.addWidget(show_btn)
        btn_lay.addWidget(cancel_btn)

        # UI Layout
        main_lay = QVBoxLayout()
        main_lay.addLayout(text_lay)
        main_lay.addLayout(btn_lay)

        # event 발생하는 부분
        self.setLayout(main_lay)
        show_btn.clicked.connect(self.main)
        cancel_btn.clicked.connect(self.close)


    # 엑셀 파일 추출
    def main(self):

        df = pd.read_csv('num_of_passengers.csv', encoding='euc-kr')

        # 202302월의 3호선 이용자 추출
        self.result = df[df['사용월'].astype(str).str.contains('202302')]
        # self.result = self.result[self.result['호선명'].astype(str).str.contains('3호선')]
        self.result = self.result[self.result['호선명'].astype(str).str.contains(str(self.line.text()))]
        # print(str(self.line.text()))

        # 각 시간대별 승차인원 추출 (하차인원 들어간 열 제외)
        self.result = self.result.drop('작업일자', axis=1)
        self.result = self.result[self.result.columns.drop(list(self.result.filter(regex='하차')))]

        # result = result[result.columns.drop(list(result.filter(regex='사용월')))]
        # result = result[result.columns.drop(list(result.filter(regex='호선명')))]

        self.result.drop(labels=['사용월', '호선명'], axis=1, inplace=True)

        self.result.set_index(keys=[self.result['지하철역']], inplace=True)
        self.result = self.result.T
        
        self.remove_str()
        self.plot()
        self.message()

        self.result.to_csv('result.csv', encoding='euc-kr')

    # 엑셀 인덱스에서 특정 문자('승차인원') 제거
    def remove_str(self):

        # result.index[16].replace('승차인원', '')

        temp = []

        for i in range(len(self.result.index)):
            temp.append(self.result.index[i].replace('승차인원', ''))
            # print(self.result.index[i].replace('승차인원', ''))
        
        # print(temp)
        self.result.index = temp
        
        # print(result.index)

    # 그래프 추출
    def plot(self):

        # temp = result.loc[result['지하철역'] == '고속터미널']

        # 행렬 추출(plot 위한)
        xs = self.result.index.to_list()
        # ys = self.result['고속터미널'].to_list()
        ys = self.result[str(self.station.text())].to_list()
        # print(str(self.station.text()))

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
        plt.savefig('./result_bargraph.png', dpi=500)

    # 알림창 띄우기 (입력받은 역의 승객 수 알림)
    def message(self):

        passengers = self.result[str(self.station.text())]
        QMessageBox.information(self, 'Passengers', str(passengers))

if __name__== '__main__':
    app = QApplication([])
    dialog = Passengers()
    dialog.show()
    app.exec_()
    print("DONE~")