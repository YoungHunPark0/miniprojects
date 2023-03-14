# 스레드 학습
import threading
import time # 스레드 할 때는 time 필수

# Thread를 상속받은 백그라운드작업 클래스
class BackgroundWorker(threading.Thread): # 스레딩에 스레드를 상속
    # 생성자
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = f'{threading.current_thread().getName()} : {name}'

    def run(self) -> None:
        print(f'BackgroundWorker start : {self._name}')
        time.sleep(2)
        print(f'BackgroundWorker end : {self._name}')

if __name__ == '__main__':
    print('기본프로세스 시작') # 기본프로세스 == 메인스레드
    
    for i in range(5):
        name = f'서브스레드{i}'
        th = BackgroundWorker(name) # th = thread
        th.start() # run이 실행됨

    print('기본프로세스 종료')