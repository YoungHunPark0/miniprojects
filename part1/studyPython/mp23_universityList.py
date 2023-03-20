# 전국대학교 지도표시
# pandas - 빅테이터분석할 때 씀. 데이터 분석 모듈. pip install pandas
import pandas as pd # pandas를 as사용해서 pd라는 별명으로 바꿈

filePath = './studyPython/university_list_2020.xlsx'
df_excel = pd.read_excel(filePath, engine='openpyxl') # pip install openpyxl
df_excel.columns = df_excel.loc[4].tolist() # loc = location
df_excel = df_excel.drop(index=list(range(0, 5))) # 실제 데이터 이외 행을 날려버림

print(df_excel.head()) # 상위 5개만

print(df_excel['학교명'].values)
print(df_excel['주소'].values)