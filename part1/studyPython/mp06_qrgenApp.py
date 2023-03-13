# QR코드 생성앱
import qrcode # pip install qrcode 설치

qr_data = 'https://www.python.org' # qr_data에 넣을 것 적용
qr_img = qrcode.make(qr_data) # (매개변수)

qr_img.save('./studyPython/site.png') # ./문자열 만들기

qrcode.run_example()