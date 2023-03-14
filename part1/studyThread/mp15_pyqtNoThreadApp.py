# 스레드 미사용 앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # ui 아이콘 변경, QIcon은 여기있음
from PyQt5.QtCore import * # Qt.white...

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyThread/threadApp.ui', self)
        self.setWindowTitle('노스레드앱 v0.4') # 실행창 제목
        self.pgbTask.setValue(0) # pgbTask 24%로 나와서 0으로 초기화시킴

        self.btnStart.clicked.connect(self.btnStartClicked)

    def btnStartClicked(self):
        self.pgbTask.setRange(0, 999999) # 0 ~ 100 초기화
        for i in range(0, 1000000): # 0 ~ 100까지
            print(f'노스레드 출력 > {i}')
            self.pgbTask.setValue(i)
            self.txbLog.append(f'노스레드 출력 > {i}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())