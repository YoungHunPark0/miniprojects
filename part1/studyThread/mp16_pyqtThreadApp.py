# 스레드 사용 앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # ui 아이콘 변경, QIcon은 여기있음
from PyQt5.QtCore import * # Qt.white...
import time

# class Background 부모 -> class qtApp
class BackgroundWorker(QThread): # PyQt5 스레드를 위한 클래스 존재
    procChanged = pyqtSignal(int)
    def __init__(self, count=0, parent=None) -> None:
        super().__init__()
        self.main = parent
        self.working = True # 스레드 동작여부
        self.count = count

    def run(self):
        # ui 활용해서 하니 오류남 -> qthread 클래스 적용했기때문
        # self.parent.pgbTask.setRange(0, 100)
        # for i in range(0, 101):
        #     print(f'스레드 출력 > {i}')
        #     self.parent.pgbTask.setValue(i)
        #     self.parent.txbLog.append(f'스레드 출력 > {i}')
        while self.working:
            # emit == 시그널을 보냄(신호를 내보내다, 값을 보내줌)
            self.procChanged.emit(f'스레드 출력 > {self.count}') 
            self.count += 1 # 값 증가만. 나머진 처리x
            time.sleep(0.0001)

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyThread/threadApp.ui', self)
        self.setWindowTitle('스레드앱 v0.4') # 실행창 제목
        self.pgbTask.setValue(0) # pgbTask 24%로 나와서 0으로 초기화시킴

        self.btnStart.clicked.connect(self.btnStartClicked)
        # 스레드 초기화
        self.worker = BackgroundWorker(parent=self, count=0)
        # 백그라운드 워커에 있는 시그널을 접근 처리해주기위한 슬롯함수
        self.worker.procChanged.connect(self.procUpdated)
        self.pgbTask.setRange(0, 1000000)

    @pyqtSlot(int)
    def procUpdated(self, count): 
        self.txbLog.append(f'스레드 출력 > {count}')
        self.pgbTask.setValue(count)
        print(f'스레드 출력 > {count}')

    @pyqtSlot()
    def btnStartClicked(self):
        self.worker.start()
        self.worker.working = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())