# 암호해제 앱 (무차별대입공격)
import itertools
import time
import zipfile # 압축파일 모듈

passwd_string = '0123456789' # 패스워드에 영문자도 들어있으면
# passwd_string = '0123456789abcdefghijk....xyzABCDEF...XYZ'

file = zipfile.ZipFile('./studyPython/passwordZip.zip')
isFind = False # 암호를 찾았는지 물어보는것

for len in range(1, 5):
    attempts = itertools.product(passwd_string, repeat=len) # repeat 반복
    for attempt in attempts:
        try_pass = ''.join(attempt)
        print(try_pass)
        # time.sleep(0.05)
        try:
            file.extractall(pwd=try_pass.encode(encoding='utf-8'))
            print(f'암호는 {try_pass} 입니다')
            isFind = True; break # 찾으면 트루. 빠져나가지만 이중for문 못나감
        except:
            pass

    if isFind == True: break # 암호가 참이면 이중for문 빠져나감