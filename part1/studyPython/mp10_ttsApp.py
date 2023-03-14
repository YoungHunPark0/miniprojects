# TTS (Google Text TO Speech)
# pip install gTTS  gTTS = 설치모듈, gtts = 실제모듈
# pip install playsound // 설치할때 DEPRECATION: 나오면 문제있다는것
from gtts import gTTS
from playsound import playsound

text = '안녕하세요, 박영훈입니다.'

tts = gTTS(text=text, lang='ko', slow=False) # slow=false 없어도됨
tts.save('./studyPython/output/hi.mp3')
print('완료!') # 실행시 output 폴더에 hi.mp3 저장됨!
print('생성완료!')
playsound('./studyPython/output/hi.mp3')
print('음성출력 완료!')