﻿using MahApps.Metro.Controls;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
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
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// RealTimeControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RealTimeControl : UserControl
    {
        public RealTimeControl()
        {
            InitializeComponent();

            // 모든 차트의 최초값을 0으로 초기화
            LvcLivingTemp.Value = LvcDiningTemp.Value = LvcBathTemp.Value = LvcBathTemp.Value = 0;
            LvcLivingHumid.Value = LvcDiningHumid.Value = LvcBathHumid.Value = LvcBathHumid.Value = 0;
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {   // commons의 mqtt client가 null이 아니고, isconnected가 true면
            if (Commons.MQTT_CLIENT != null && Commons.MQTT_CLIENT.IsConnected) 
            { // DB 모니터링을 실행한 뒤 실시간 모니터링으로 넘어왔다면
                // mqtt client의 메세지를 public으로 처리할 수 있는 이벤트 만듬. += 하고 탭만 누르면 자동생성됨
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
            }
            else
            { // DB 모니터링을 실행하지 않고 바로 실시간 모니터링 메뉴를 클릭했으면
                Commons.MQTT_CLIENT = new MqttClient(Commons.BROKERHOST);
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                Commons.MQTT_CLIENT.Connect("MONITOR");
                Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC },
                                              new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE });
            }
        }

        // MQTTclient는 단독스레드 사용, UI스레드에 직접 접근이 안됨
        // 그래서 사용하는 것이 this.Invoke(); --> UI스레드 안에 있는 리소스에 접근가능
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            Debug.WriteLine(msg);
            var currSensor = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg); // DeserializeObject == 역직렬화

            if (currSensor["DEV_ID"] == "IOT56") // iot56으로 변경
            {
                this.Invoke(() =>
                {
                    var dfValue = DateTime.Parse(currSensor["CURR_DT"]).ToString("yyyy-MM-dd HH:mm:ss");
                    LblSensingDt.Content = $"Sensing DateTime : {dfValue}";
                    /*
                     * $"Sensing DateTime : {currSensor["Sensing_DateTime"]}"; 으로 출력하면
                     * Sensing_DateTime": "2023-05-10T10:43:30.3522197+09:00" 으로 출력되니
                     * DateTime.Parse(currSensor["Sensing_DateTime"]).ToString("yyyy-MM--dd HH:mm:ss");
                     */

                });
                switch ("LIVING".ToUpper()) // CurrSensor["Room_Name"]을 안받기 때문에 Living으로 고정 // ToUpper == 대문자변환. 소문자일 때 오류 날 수 있어서
                {
                    case "LIVING":
                        this.Invoke(() =>{
                            // Value에 들어갈 값은 double. -> convert.todouble, math.round => 소수점 자리정해서 자르는 함수
                            // Living
                            var tmp = currSensor["STAT"].Split('|'); // 29.0 | 45.0 으로 잘라준 다음
                            var temp = tmp[0].Trim(); // tmp의 앞의 값. "29.0 " trim() 공백제거
                            var humid = tmp[1].Trim(); // 45.0" trim() 공백제거
                    
                            LvcLivingTemp.Value = Math.Round(Convert.ToDouble(temp), 1); 
                            LvcLivingHumid.Value = Convert.ToDouble(humid);
                        });
                        break;

                    case "DINING":
                        this.Invoke(() => {
                            LvcDiningTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1); // Value에 들어갈 값은 double.
                            LvcDiningHumid.Value = Convert.ToDouble(currSensor["Humid"]);
                        });
                        break;

                    case "BED":
                        this.Invoke(() => {
                            LvcBedTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1); // Value에 들어갈 값은 double.
                            LvcBedHumid.Value = Convert.ToDouble(currSensor["Humid"]);
                        });
                        break;

                    case "BATH":
                        this.Invoke(() => {
                            LvcBathTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1); // Value에 들어갈 값은 double.
                            LvcBathHumid.Value = Convert.ToDouble(currSensor["Humid"]);
                        });
                        break;

                    default: 
                        break;
                }
            }

        }

        private void BtnOpen_Click(object sender, RoutedEventArgs e)
        {
            // Json으로 서브모터 90도 오픈한다는 데이터 생성
            var topic = "pknu/monitor/control/";

            JObject origin_data = new JObject();
            origin_data.Add("DEV_ID", "MONITOR");
            origin_data.Add("CURR_DT", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
            origin_data.Add("STAT", "OPEN");
            string pub_data = JsonConvert.SerializeObject(origin_data, Formatting.Indented); // Formatting.Indented 들여쓰기할때 json을 줄맞춰주기함 like Chrome

            Commons.MQTT_CLIENT.Publish(topic, Encoding.UTF8.GetBytes(pub_data)); // byte 형식으로 변환 
            // 1.topic 2.message 메세지는 json형식으로 변경할것
            LblDoorStat.Content = "OPEN!!";
        }

        private void BtnClose_Click(object sender, RoutedEventArgs e)
        {
            // Json으로 서브모터 90도 오픈한다는 데이터 생성
            var topic = "pknu/monitor/control/";

            JObject origin_data = new JObject();
            origin_data.Add("DEV_ID", "MONITOR");
            origin_data.Add("CURR_DT", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
            origin_data.Add("STAT", "CLOSE");
            string pub_data = JsonConvert.SerializeObject(origin_data, Formatting.Indented); // Formatting.Indented 들여쓰기할때 json을 줄맞춰주기함 like Chrome

            Commons.MQTT_CLIENT.Publish(topic, Encoding.UTF8.GetBytes(pub_data)); // byte 형식으로 변환 
            // 1.topic 2.message 메세지는 json형식으로 변경할것
            LblDoorStat.Content = "CLOSE!!";
        }
    }
}
