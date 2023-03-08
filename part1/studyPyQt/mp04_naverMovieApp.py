import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # ui 아이콘 변경
from NaverApi import *
import webbrowser # 웹브라우저 모듈

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApiMovie.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/newspaper.png')) # 아이콘 변경(파일경로) 파일 따로 다운받아서 폴더에 넣기
        
        # 시그널) 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 시그널) texbox 검색어 입력 후 엔터를 치면 처리 (이 작업 안하면 엔터해도 검색안됨)
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        # 시그널) 더블클릭 했었을 때 
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)

    
    def txtSearchReturned(self): # 검색어 입력후 엔터
        self.btnSearchClicked() 

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '': # 검색에 아무것도 안적고 검색
            QMessageBox.warning(self, '경고', '영화명을 입력하세요!') # warning -> 메세지창에 ! 앞에 붙음, about은 안뜸
            return
        else:
            api = NaverApi() # NaverApi 클래스 객체 생성
            node = 'movie' # movie로 변경하면 영화검색
            # outputs = [] # 결과 담을 리스트변수. 안써서 주석처리함
            display = 100 # 100개 출력
            
            result = api.get_naver_search(node, search, 1, display) # 1 -> start 어차피 1부터
            #print(result)
           

            # 테이블위젯에 출력 기능
            items = result['items'] # json결과 중에서 items 아래 배열만 추출. 위에 result 안에 itmes만 추출
            self.makeTable(items) # makeTable: 테이블 위젯에 데이터들을 할당하는 함수
   
    def tblResultDoubleClicked(self):
        # row = self.tblResult.currentIndex().row()
        # column = self.tblResult.currentIndex().column()
        # print(row, column) 실행 후 더블클릭하면 행,열 표시됨
        selected = self.tblResult.currentRow() # 현재 선택된 열의 row가 나옴
        url = self.tblResult.item(selected, 5).text() # url 링크컬럼 변경
        webbrowser.open(url) # 네이버영화 웹사이트 오픈


    # 테이블 위젯에 데이터 표시 -- 네이버 영화 결과에 맞춰서 변경
    def makeTable(self, items) -> None:
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection) # 단일선택
        # setSelectionMode: 선택모드를 몇개로 할것인가, singleseltion: 단일선택
        self.tblResult.setColumnCount(7) # column 컬럼(행) 갯수 
        self.tblResult.setRowCount(len(items)) # 밑으로 몇개를 만들것인가. 현재100개 행 생성
        self.tblResult.setHorizontalHeaderLabels(['영화제목', '개봉년도', '감독', '배우진', '평점', '링크', '포스터'])
        self.tblResult.setColumnWidth(0, 150) # 첫번째 컬럼행 크기 설정
        self.tblResult.setColumnWidth(1, 60) # 두번째 컬럼행 크기 설정, 개봉년도
        self.tblResult.setColumnWidth(4, 50) # 평점 컬럼 크기
        # 컬럼 데이터를 수정금지
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, post in enumerate(items): # 0, 영화 ...등 나옴
            title = self.replaceHtmlTag(post['title']) # HTML 특수문자 변환
            pubDate = post['pubDate']
            director = post['director']
            actor = post['actor']
            userRating = post['userRating']
            link = post['link']
            # imgData = urlopen(post['image']).read()
            # image = QPixmap()
            # if imgData != None:
            #     image.loadFromData(imgData)            
            #     imgLabel = QLabel()
            #     imgLabel.setPixmap(image)
            #     imgLabel.setGeometry(0, 0, 60, 100)
            #     imgLabel.resize(60, 100)

            # setItem(행, 열(컬럼값), 넣을데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title)) # i번째 행, 컬럼에 0, num
            self.tblResult.setItem(i, 1, QTableWidgetItem(pubDate))
            self.tblResult.setItem(i, 2, QTableWidgetItem(director))
            self.tblResult.setItem(i, 3, QTableWidgetItem(actor))
            self.tblResult.setItem(i, 4, QTableWidgetItem(userRating))
            self.tblResult.setItem(i, 5, QTableWidgetItem(link))
            # if imgData != None:
            #     self.tblResult.setCellWidget(i, 6, imgLabel)

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