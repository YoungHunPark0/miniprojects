using Bogus;
using FakeIotDeviceApp.Models;
using MahApps.Metro.Controls;
using MahApps.Metro.Controls.Dialogs;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Web.Compilation;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using uPLibrary.Networking.M2Mqtt;

namespace FakeIotDeviceApp
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        Faker<SensorInfo> FakeHomeSensor { get; set; } = null; // 가짜 스마트홈 센서값 변수
        MqttClient Client { get; set; }
        Thread MqttThread { get; set; }
        public MainWindow()
        {
            InitializeComponent();

            InitFakeData();
        }

        private void InitFakeData()
        {
            var Rooms = new[] { "Bed", "Bath", "Living", "Dining" };

            FakeHomeSensor = new Faker<SensorInfo>()
                .RuleFor(s => s.Home_Id, "D101H703") // 임의로 픽스된 홈아이디 101동 703호
                .RuleFor(s => s.Room_Name, f => f.PickRandom(Rooms)) // var rooms에 만들고싶은 데이터를 배열로 만들고
                                                                     // 실행할때마다 방이름이 계속 변경-bogus의 장점
                .RuleFor(s => s.Sensing_DateTime, f => f.Date.Past(0)) // 현재시각이 생성
                .RuleFor(s => s.Temp, f => f.Random.Float(20.0f, 30.0f)) // 20~30도 사이의 온도값이 생성
                .RuleFor(s => s.Humid, f => f.Random.Float(40.0f, 64.0f)); // 40~64% 사이의 습도값이 생성 // 마지막에 ;
        }

        private async void BtnConnect_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(TxtMqttBrokerIp.Text)) 
            {
                await this.ShowMessageAsync("오류", "브로커아이피를 입력하세요");
                return;
            }

            // 브로커아이피로 접속
            ConnectMqttBroker();
            // 하위의 로직을 무한반복 -> 센싱은 가짜스마트홈센서값-전송-출력 계속 반복하기때문
            StartPublish();
        }

        // 핵심처리 센싱된 데이터값을 MQTT브로커로 전송
        private void StartPublish()
        {
            MqttThread = new Thread(() =>
            {
                while (true) // 무한반복
                {
                    // 1. 가짜 스마트홈 센서값 생성 ( 전송하든 안하든 만들어야함)
                    SensorInfo info = FakeHomeSensor.Generate();
                    // 릴리즈(배포)때는 주석처리/삭제
                    Debug.WriteLine($"{info.Home_Id} / {info.Room_Name} / {info.Sensing_DateTime} / {info.Temp}");
                    // 객체 직렬화 (객체데이터를 xml이나 json등의 문자열로 변환)
                    var jsonValue = JsonConvert.SerializeObject(info, Formatting.Indented); // 인덴트 안하면 가로로 쭉나열된 json인데 하면 세로로 나열됨 보기좋음
                    // 센서값 MQTT브로커에 전송(Publish)
                    Client.Publish("SmartHome/IoTData/", Encoding.Default.GetBytes(jsonValue)); // getbytes = 2진바이트로 변환시켜줌
                                                                                                // jsonvalue는 문자열이라 그대로 쓰면 tcp에서 인식못하기에 encoding해야함.
                                                                                                // 실행하고 mqtt explorer에서 확인해보면 나옴
                    // 스레드와 UI스레드간 충돌이 안나도록 변경
                    this.Invoke(new Action(() => {
                        // RtbLog에 출력
                        RtbLog.AppendText($"{jsonValue}\n");
                        RtbLog.ScrollToEnd(); // 스크롤 자동으로 제일 밑으로 보내기. 안하면 사용자가 직접 내려야함
                    }));
                    
                    // 1초동안 대기
                    Thread.Sleep(1000);
                }

            });
            MqttThread.Start();
        }

        private void ConnectMqttBroker()
        {
            Client = new MqttClient(TxtMqttBrokerIp.Text);
            Client.Connect("SmartHomeDev"); // publish Client ID를 지정
        }

        private void MetroWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (Client != null && Client.IsConnected == true) 
            { 
                Client.Disconnect(); // 접속을 끊어주고
            }

            if (MqttThread != null) 
            {
                MqttThread.Abort(); //[중요!] 여기가 없으면 프로그램 종료후에도 메모리에 남아있음!!
            }
        }
    }
}
