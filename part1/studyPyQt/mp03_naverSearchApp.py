import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from NaverApi import *

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApiSearch.ui', self)

        # 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # texbox 검색어 입력 후 엔터를 치면 처리 (이 작업 안하면 엔터해도 검색안됨)
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)

    def txtSearchReturned(self): # 검색어 입력후 엔터
        self.btnSearchClicked() 

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '': # 검색에 아무것도 안적고 검색
            QMessageBox.warning(self, '경고', '검색어를 입력하세요!') # warning -> 메세지창에 ! 앞에 붙음, about은 안뜸
            return
        else:
            api = NaverApi() # NaverApi 클래스 객체 생성
            node = 'news' # movie로 변경하면 영화검색
            outputs = [] # 결과 담을 리스트변수
            display = 100 # 100개 출력
            
            result = api.get_naver_search(node, search, 1, display) # 1 -> start 어차피 1부터
            # print(result)
            # 리스트뷰에 출력 기능
            while result != None and result['display'] != 0:
                for post in result['items']: # 100개의 post(글) 만들어짐
                    api.get_post_data(post, outputs) # (넣을값, 돌려받을값), NaverAPI 클래스에서 처리

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())