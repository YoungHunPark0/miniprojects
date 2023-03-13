# mp09_pyqtComInfoApp.py
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # ui 아이콘 변경, QIcon은 여기있음
from PyQt5.QtCore import * # Qt.white...

import psutil
import socket
import requests 
import re

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPython/comInfo.ui', self)
        self.setWindowTitle('내컴퓨터 정보 v0.2') # 실행창 제목
        self.setWindowIcon(QIcon('./studyPython/settings.png'))

        self.btnRefresh.clicked.connect(self.btnRefreshClicked)
        self.initInfo()

    def btnRefreshClicked(self):
        self.initInfo()

    # 작업관리자 - 성능 들어가서 맞는지 확인
    def initInfo(self):
        cpu = psutil.cpu_freq()
        cpu_ghz = round(cpu.current / 1000, 2) 
        # round(반올림)(해당테이블.current / 나눌단위, 반올림 할 소수점자리기준), ghz = 기가헤르츠 단위로 변환
        self.lblCPU.setText(f'{cpu_ghz:.2f} GHz') # 값 + GHz 출력
        core = psutil.cpu_count(logical=False)
        logical = psutil.cpu_count(logical=True)
        self.lblCore.setText(f'{core} 개 / 논리프로세서 {logical} 개')

        memory = psutil.virtual_memory()
        mem_total = round(memory.total / 1024**3) # 1024 3승 으로 나눔
        self.lblMemory.setText(f'{mem_total} GB')

        disks = psutil.disk_partitions()
        for disk in disks:
            if disk.fstype == 'NTFS': # 디스크중 NTFS만
                du = psutil.disk_usage(disk.mountpoint)
                du_total = round(du.total / 1024**3)
                msg = f'{disk.mountpoint} {disk.fstype} - {du_total} GB'
                
                self.lblDisk.setText(msg)
                break
        
        # print(psutil.net_if_addrs())
        in_addr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        in_addr.connect(('www.google.com', 443))
        self.lblInnerNet.setText(in_addr.getsockname()[0]) # 내부아이피

        req = requests.get('http://ipconfig.kr')
        out_addr = req.text[req.text.find('<font color=red>')+17:req.text.find('</font><br>')] # <font color=red> =17개
        self.lblExtraNet.setText(out_addr) # 외부아이피

        net_stat = psutil.net_io_counters()
        sent = round(net_stat.bytes_sent / 1024**2, 1)
        recv = round(net_stat.bytes_recv / 1024**2, 1) # recv = 리시브
        self.lblNetStat.setText(f'송신 - {sent} MB / 수신 - {recv} MB')

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())