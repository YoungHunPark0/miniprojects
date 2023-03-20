import pandas as pd
import folium # pip install folium

filePath = './studyPython/university_locations.xlsx'
df_excel = pd.read_excel(filePath, engine='openpyxl', header=None) # hearder=none 안하면 첫번째 서울여대를 제목으로 인식함
df_excel.columns = ['학교명', '주소', 'lng', 'lat'] # lng=경도, lat=위도 // 실행시 컬럼생성
# print(df_excel)

name_list = df_excel['학교명'].to_list() # 학교명 446개 리스트
addr_list = df_excel['주소'].to_list()
lng_list = df_excel['lng'].to_list()
lat_list = df_excel['lat'].to_list()

fMap = folium.Map(location=[37.553175, 126.989326], zoom_start=10)

for i in range(len(name_list)): # 446번 반복
    if lng_list[i] != 0: # != 아니면// 위도,경도 값이 0이 아니면
        marker = folium.Marker([lat_list[i], lng_list[i]], popup=name_list[i],
                               icon=folium.Icon(color='blue'))
        marker.add_to(fMap)

fMap.save('./studyPython/Korea_unversities.html')