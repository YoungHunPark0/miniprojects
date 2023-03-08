import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # ui 아이콘 변경
from NaverApi import *
import webbrowser # 웹브라우저 모듈

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApiSearch.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/newspaper.png')) # 아이콘 변경(파일경로) 파일 따로 다운받아서 폴더에 넣기
        
        # 시그널) 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 시그널) texbox 검색어 입력 후 엔터를 치면 처리 (이 작업 안하면 엔터해도 검색안됨)
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        # 시그널) 더블클릭 했었을 때 
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)

    def tblResultDoubleClicked(self):
        # row = self.tblResult.currentIndex().row()
        # column = self.tblResult.currentIndex().column()
        # print(row, column) 실행 후 더블클릭하면 행,열 표시됨
        selected = self.tblResult.currentRow() # 현재 선택된 열의 row가 나옴
        url = self.tblResult.item(selected, 1).text() # 더블클릭하면 url나옴
        webbrowser.open(url) # 뉴스기사 웹사이트 오픈


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
            # while result != None and result['display'] != 0:
            #     for post in result['items']: # 100개의 post(글) 만들어짐
            #         api.get_post_data(post, outputs) # (넣을값, 돌려받을값), NaverAPI 클래스에서 처리

            # 테이블위젯에 출력 기능
            items = result['items'] # json결과 중에서 items 아래 배열만 추출. 위에 result 안에 itmes만 추출
            self.makeTable(items) # makeTable: 테이블 위젯에 데이터들을 할당하는 함수

    # 테이블 위젯에 데이터 표시
    def makeTable(self, items) -> None:
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection) # 단일선택
        # setSelectionMode: 선택모드를 몇개로 할것인가, singleseltion: 단일선택
        self.tblResult.setColumnCount(2) # column 컬럼(행) 갯수 설정
        self.tblResult.setRowCount(len(items)) # 밑으로 몇개를 만들것인가. 현재100개 행 생성
        self.tblResult.setHorizontalHeaderLabels(['기사제목', '뉴스링크'])
        self.tblResult.setColumnWidth(0, 310) # 첫번째 컬럼행 크기 설정
        self.tblResult.setColumnWidth(1, 260) # 두번째 컬럼행 크기 설정
        # 컬럼 데이터를 수정금지
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, post in enumerate(items): # 0, 뉴스 ...등 나옴
            #num = i + 1 # 0부터 시작하니 뉴스번호를 1부터 지정
            title = self.replaceHtmlTag(post['title']) # HTML 특수문자 변환
            originallink = post['originallink']
            
            # setItem(행, 열(컬럼값), 넣을데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title)) # i번째 행, 컬럼에 0, num
            self.tblResult.setItem(i, 1, QTableWidgetItem(originallink))

    def replaceHtmlTag(self, sentence) -> str: # title(기사제목)에서 &,<b>등 html특수문자 수정작업함수.
        result = sentence.replace('&lt;', '<').replace('&gt;', '>').replace('<b>', '').replace('</b>',
                     '').replace('&apos', "'").replace('&quot', '"')
        # lt == lesser than ~작다 (<)
        # gt == greater than ~크다 (>)
        # b = bold. 앱화면에 글자를 진하게 표시할 방법이 없어서 없앰
        # apos = apostopy 홑따옴표(')
        # quot = quotation mark 쌍따옴표(")
        # 변환 안된 특수문자가 나타나면 여기부분에 추가할 것

        return result

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())