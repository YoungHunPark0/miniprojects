# 미니프로젝트 Part2
기간 2023.05.02 ~ 2023.05.16

## WPF 학습
- SCADA 시뮬레이션(SmartHome시스템)
	- C# WPF
	- MahApps.Metro (MetroUI 디자인 라이브러리)
	- Bogus(데미데이터 생성 라이브러리)
	- Newtonsort.json
	- M2Mqtt(통신 라이브러리) 
	<!-- 
		https://docs.google.com/document/d/1w8bwWmcdKkmAEHf2eehEX7crsmTkfO2LuITxig8gKSE/edit# 참고

https://mosquitto.org/download/
mosquitto-2.0.15-install-windows-x64.exe (64-bit build, Windows Vista and up, built with Visual Studio Community 2019)
다운받기
파일경로 C:\DEV\Server\mosquitto
설치완료 후 
실행 services.msc -> 서비스 -> mosquitto broker 자동-시작 

http://mqtt-explorer.com/ 조금 내려서 windows installer 설치

왼쪽상단 + connections 
My Local mqtt localhost ->save

topic : IOT/temp - raw - 23.6 publish
	-->
	- DB 데이터바인딩(MySQL)
	- LiveCharts
	- OxyPlot
	
- SmartHome 시스템 문제점
	- 실행 후 시간이 소요되면 UI제어가 느려짐 - TextBox에 텍스트가 과도 - 해결!
	- LiveCharts는 대용량 데이터 차트는 무리(LiveCharts v.2 동일)
	- 대용량 데이터 차트는 OxyPlot를 사용

온습도 더미데이터 시뮬레이터	

<img
src="https://raw.githubusercontent.com/YoungHunPark0/miniprojects/main/images/smarthome_publisher.gif" width="510">

스마트홈 모니터링 앱

<img
src="https://raw.githubusercontent.com/YoungHunPark0/miniprojects/main/images/smarthome_monitor1.gif" width="780">

스마트홈 모니터링 시각화

<img
src="https://raw.githubusercontent.com/YoungHunPark0/miniprojects/main/images/smarthome_monitor2.png" width="780">