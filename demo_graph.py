import sys
import os
from PyQt5.QtWidgets import * #QApplication, QWidget, QLabel, QPushButton, QInputDialog
from PyQt5.QtGui import QIcon

import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt

class App(QWidget):
    val = {
        "temp": [], "hum": [], "result": []
    }
    # input1 = ""
    # input2 = ""
    # table = ""
    # dialog = ""

    def __init__(self):
        super().__init__()
        self.title = 'Main Window'
        self.left = 300
        self.top = 300
        self.width = 640
        self.height = 480
        self.initUI()
        
    def initUI(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)

            label1 = QLabel('온도(℃)', self)
            label1.move(20, 370)
            self.input1 = QLineEdit("",self)
            self.input1.move(70, 365)
            self.input1.setStyleSheet("width: 50px")

            label2 = QLabel('습도(%)', self)
            label2.move(20, 400)
            self.input2 = QLineEdit("",self)
            self.input2.move(70, 395)
            self.input2.setStyleSheet("width: 50px")

            label3 = QLabel('결과', self)
            label3.move(20, 430)
            self.input3 = QLineEdit("",self)
            self.input3.move(70, 425)
            self.input3.setStyleSheet("width: 50px")

            label4 = QLabel('(비=0, 눈=1)', self)
            label4.move(73, 450)

            btn_push = QPushButton("삽입", self)
            btn_push.move(150, 365)
            btn_push.setStyleSheet("height: 70px")
            btn_push.clicked.connect(self.pushData)

            btn_clear = QPushButton("전체 삭제", self)
            btn_clear.move(230, 365)
            btn_clear.setStyleSheet("height: 70px")
            btn_clear.clicked.connect(self.clearData)

            btn_save = QPushButton("현재 데이터 저장", self)
            btn_save.move(430, 50)
            btn_save.setStyleSheet("width: 130px; height: 30px")
            btn_save.clicked.connect(self.saveData)

            btn_load = QPushButton("파일 가져오기", self)
            btn_load.move(430, 150)
            btn_load.setStyleSheet("width: 130px; height: 30px")
            btn_load.clicked.connect(self.loadData)
            label5 = QLabel('※ temp, hum, result 컬럼이 있어야 함', self)
            label5.move(410, 195)

            btn_graph = QPushButton("Graph 보기", self)
            btn_graph.move(420, 365)
            btn_graph.setStyleSheet("width: 170px; height: 70px")
            btn_graph.clicked.connect(self.openGraph)

            self.initTable()

            self.show()
    
    def initTable(self):
        self.table = QTableWidget(self)
        self.table.resize(400,350)
        self.table.setStyleSheet("top: 100")
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Temp(℃)", "Hum(%)", "Result"])

    def pushData(self):   
        try:
            a = int(self.input3.text())
            if a==0 or a==1:
                try:
                    self.val["temp"].append(int(self.input1.text()))
                    self.val["hum"].append(int(self.input2.text()))
                    self.val["result"].append(a)
                    self.printList()
                    self.input1.setText("")
                    self.input2.setText("")
                    self.input3.setText("")
                except:
                    QMessageBox.about(self, "Warning", "숫자 필수        ")
            else:
                QMessageBox.about(self, "Warning", "결과는 0 또는 1     ")
            try:
                plt.close()
            except:
                pass
        except:
            QMessageBox.about(self, "Warning", "숫자 필수        ")

    def printList(self):
        self.table.setRowCount(len(self.val["temp"]))
        for i in range(0,len(self.val["temp"])):
            self.table.setItem(i, 0, QTableWidgetItem(str(self.val["temp"][i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.val["hum"][i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.val["result"][i])))

    def clearData(self):
        self.val["temp"].clear()
        self.val["hum"].clear()
        self.val["result"].clear()
        self.printList()

    def saveData(self):
        try:
            path = os.path.join(os.path.expanduser('~'),'Desktop')
            df = pd.DataFrame(self.val)
            df.to_csv(path+"/data.csv", index=False, encoding="cp949")
            QMessageBox.about(self, "Save", "저장 완료\n(경로: 바탕화면)    ")
        except:
            QMessageBox.about(self, "Fail", "저장 실패")
    
    def loadData(self):
        path = QFileDialog.getOpenFileName(self, 'Open file', './')
        if path[0]:
            try:
                data = pd.read_csv(path[0], encoding='utf-8-sig').to_dict()
                try:
                    self.val["temp"].clear()
                    self.val["hum"].clear()
                    self.val["result"].clear()
                    for i in range(0,len(data["temp"])):
                        self.val["temp"].append(data["temp"][i])
                        self.val["hum"].append(data["hum"][i])
                        self.val["result"].append(data["result"][i])
                except:
                    QMessageBox.about(self, "Warning", "파일 형식이 맞지 않음     ")
                self.printList()
            except:
                QMessageBox.about(self, "Warning", ".csv 파일이 아님        ")

    def openGraph(self):
        df = pd.DataFrame(self.val)
        sb.scatterplot(x='temp', y='hum', data=df, hue="result")
        # sb.lmplot(x='temp', y='hum', data=df, fit_reg=False, markers=["o", "x"], hue="result")
        # df2 = pd.read_csv("data/csv/res2.csv")
        # sb.lmplot(x='기온(°C)', y='습도(%)', data=df2, fit_reg=False, markers=["o", "x"], hue="눈비")
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    ex = App()
    sys.exit(app.exec_())