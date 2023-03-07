# PyQt 복습 (python - day09) - 직접 디자인 코딩
import sys
from PyQt5.QtWidgets import *
# PyQt 다운 cmd -> pip install pyqt5 -> pip install --upgrade pip 
# -> pip install PyQt5Designer -> 
# 버튼만들기 1. QPushButton from절에 추가하기
# from 절 계속 추가하면 많으니 (QApplication, QWidget, QPushButton) *로 표시

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lblMessage = QLabel('메세지', self) # 버튼클릭 메세지 출력 1
        self.lblMessage.setGeometry(10, 10, 300, 50) # 버튼클릭 메세지 출력 2, .move는 사이즈 조절이 안됨
    

        btnOK = QPushButton('OK', self) # - 버튼만들기 2
        btnOK.setGeometry(280, 250, 100, 40) # - 버튼만들기 3 크기지정
        # PyQt 이벤트(시그널) -> 이벤트핸들러(슬롯)
        btnOK.clicked.connect(self.btnOK_clicked) # 버튼클릭 메세지 출력 3

        # ui크기설정 함수 - geometry(x, y, 넓이, 높이)
        self.setGeometry(300, 200, 400, 300) # 1.위젯만들기
        self.setWindowTitle('복습PyQt') # 1.위젯타이틀
        self.show() # 1.위젯만들기 출력

    def btnOK_clicked(self): # 버튼클릭 메세지 출력 4
        self.lblMessage.clear() # 버튼클릭 메세지 출력 5
        self.lblMessage.setText('메시지: OK!!!') # 버튼클릭 메세지 출력 6 클릭하면 출력됨


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    sys.exit(app.exec_())