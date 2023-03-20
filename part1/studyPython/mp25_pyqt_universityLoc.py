# PyQt에 folium 지도 표시
import folium
from PyQt5 import uic # pyqt파일에서 긁어오기
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # ui 아이콘 변경, QIcon은 여기있음
from PyQt5.QtCore import * # QUrl 함수 사용하기위한 모듈
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
import sys
import io # 파일 저장. io = input, output
import pandas as pd

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('전국대학교 위치')
        self.width, self.height = 1400, 900
        self.setMinimumSize(self.width, self.height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        filePath = './studyPython/university_locations.xlsx'
        df_excel = pd.read_excel(filePath, engine='openpyxl', header=None) # hearder=none 안하면 첫번째 서울여대를 제목으로 인식함
        df_excel.columns = ['학교명', '주소', 'lng', 'lat'] # lng=경도, lat=위도 // 실행시 컬럼생성
        # print(df_excel)

        name_list = df_excel['학교명'].to_list() # 학교명 446개 리스트
        addr_list = df_excel['주소'].to_list()
        lng_list = df_excel['lng'].to_list()
        lat_list = df_excel['lat'].to_list()

        # url = 'https://www.naver.com'
        m = folium.Map(location=[37.553175, 126.989326], zoom_start=10)
        
        for i in range(len(name_list)): # 446번 반복
            if lng_list[i] != 0: # != 아니면// 위도,경도 값이 0이 아니면
                marker = folium.Marker([lat_list[i], lng_list[i]], popup=name_list[i],
                               icon=folium.Icon(color='blue'))
                marker.add_to(m)
        
        data = io.BytesIO()
        m.save(data, close_file=False)

        webview = QWebEngineView()
        # webview.load(QUrl(url))
        webview.setHtml(data.getvalue().decode())  
        layout.addWidget(webview)

# PyQt 폴더파일에서 긁어오기
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())