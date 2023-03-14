# pip install pyttsx3
import pyttsx3

tts = pyttsx3.init() # 초기화
tts.say('안녕하세요') # say장점! mp3 안쓰고 바로가능
tts.runAndWait()