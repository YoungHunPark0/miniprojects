# 쓰레드 App
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # QIcon
from PyQt5.QtCore import * # Qt.white
import time

MAX = 100000

class BackgroundWorker(QThread): # PyQt5에 스레드를 위한 클래스가 존재
    procChanged = pyqtSignal(int) # 커스텀 시그널(마우스 클릭같은 시그널을 따로 만드는 것)



    def __init__(self, count=0, parent=None) -> None:
        super().__init__()
        self.main = parent
        self.working = False # 스레드 동작여부 - 최초의 동작은 ㄴㄴ
        self.count = count

    def run(self): # thread.start() 하면 run()실행
        # self.parent.pgbTask.setRange(0, 100)
        # for i in range(0, 101):
        #     print(f'스레드 출력 > {i}')
        #     self.parent.pgbTask.setValue(i)
        #     self.parent.txbLog.append(f'스레드 출력 > {i}') - 이 모든것들은 스레드를 위한 것
        while self.working:
            if self.count <= MAX:    
                self.procChanged.emit(self.count) # 시그널을 내보냄
                self.count += 1 # 값 증가 // 업무프로세스가 동작하는 위치
                time.sleep(0.0001) # time.sleep을 안주면 No Thread랑 같이 응답없음 뜸 - 가장 적당한 시간은 0.001 or 0.0001
                # 시간 타임을 0.0000001정도로 주면 GUI처리를 제대로 하지 못하더라..
            else: 
                self.working = False

class qtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyThread/threadApp.ui', self)
        self.setWindowTitle('ThreadApp v0.5')
        self.pgbTask.setValue(0)

        self.btnStart.clicked.connect(self.btnStartClicked) # 내장 시그널
        # 스레드 생성
        self.worker = BackgroundWorker(parent=self, count=0)
        # 백그라운드 워커에 있는 시그널을 접근해서 처리해주기 위한 슬롯함수
        self.worker.procChanged.connect(self.procUpdated) 

        # 초기화
        self.pgbTask.setRange(0, MAX)
    
    # @pyqtSlot(int) # 데코레이션
    def procUpdated(self, count):
        self.txbLog.append(f'스레드 출력 > {count}')
        self.pgbTask.setValue(count)
        print(f'스레드 출력 > {count}')

    # @pyqtSlot()
    def btnStartClicked(self):
        self.worker.start() # 스레드 클래스 함수가 실행
        self.worker.working = True
        self.worker.count = 0 # 스타트 버튼 누르면 다시 스레드가 시작함



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())