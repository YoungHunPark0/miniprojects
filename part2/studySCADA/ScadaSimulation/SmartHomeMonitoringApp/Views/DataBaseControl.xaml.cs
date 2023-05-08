using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using Newtonsoft.Json;
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
using uPLibrary.Networking.M2Mqtt.Messages;
using MySql;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// DataBaseControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class DataBaseControl : UserControl
    {
        public bool IsConnected { get; set; }

        public DataBaseControl()
        {
            InitializeComponent();
        }

        // 유저컨트롤 로드이벤트 핸들러
        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            TxbBrokerUrl.Text = Commons.BROKERHOST;
            TxbMqttTopic.Text = Commons.MQTTTOPIC;
            TxtConnstring.Text = Commons.MYSQL_CONNSTRING;

            IsConnected = false; // 아직 접속이 안되었음
            BtnConnDb.IsChecked = false; 
        }

        // 토글버튼 클릭(1번누르면 : 접속, 1번더누르면 : 접속끊기) 이벤트 핸들러
        private void BtnConnDb_Click(object sender, RoutedEventArgs e)
        {
            // isconnected가 true면
            if (IsConnected == false) // 최초에는 false고 
            {   
                // MQTT 브로커 생성
                Commons.MQTT_CLIENT = new uPLibrary.Networking.M2Mqtt.MqttClient(Commons.BROKERHOST);

                // MQTT 사용하기위해서 중요!
                try
                {
                    // MQTT Subscribe(구독할) 로직
                    if (Commons.MQTT_CLIENT.IsConnected == false) 
                    {
                        // MQTT 접속
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Connect("MONITOR"); // clientId = 모니터
                        Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC},
                                new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE}); // QOS는 네트워크 통신옵션 // AT_LEAST_ONCE 적어도 한번은 보낸다
                        UpdateLog(">>> MQTT Broker Connected");

                        // try, catch로 인해 오류뜰 수 있으니 다끝나고
                        BtnConnDb.IsEnabled = true;
                        IsConnected = true; // 예외발생하면 true로 변경할 필요 없음
                    }
                }
                catch
                {
                    // Pass
                }
            }
            // isconnected가 false면
            else
            {
                BtnConnDb.IsEnabled = false;
                IsConnected = false;
            }
        }

        private void UpdateLog(string msg)
        {
            // 에외처리 필요!
            this.Invoke(() => {
                TxtLog.Text += $"{msg}\n"; // 로그를 비동기로 찍음
                TxtLog.ScrollToEnd();
            }); 
        }

        // Subscribe가 발생했을 때 이벤트핸들러 (mqtt데이터 전달받으면 작업)
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            UpdateLog(msg);
            SetToDataBase(msg, e.Topic); // 실제 DB에 저장처리
        }

        // DB 저장처리 메서드
        private void SetToDataBase(string msg, string topic)
        {
            var currValue = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg);
            if (currValue != null) 
            {
                //Debug.WriteLine(currValue["Home_Id"]);
                //Debug.WriteLine(currValue["Room_Name"]);
                //Debug.WriteLine(currValue["Sensing_DateTime"]);
                //Debug.WriteLine(currValue["Temp"]);
                //Debug.WriteLine(currValue["Humid"]);
                try
                {
                    using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                    {
                        if (conn.State == System.Data.ConnectionState.Closed) conn.Open();
                        string insQuery = "INSERT INTO smarthomesensor ...";

                        MySqlCommand cmd = new MySqlCommand(insQuery, conn);
                        cmd.Parameters.AddWithValue("Home_Id", currValue["Home_Id"]);
                        cmd.Parameters.AddWithValue("Room_Name", currValue["Room_Name"]);
                        cmd.Parameters.AddWithValue("Sensing_DateTime", currValue["Sensing_DateTime"]);
                        cmd.Parameters.AddWithValue("Temp", currValue["Temp"]);
                        cmd.Parameters.AddWithValue("Humid", currValue["Humid"]);

                        if(cmd.ExecuteNonQuery() == 1) // 결과는 무조건 1개. 1개면
                        {
                            UpdateLog(">>> DB Insert succed.");
                        }
                        else
                        {
                            UpdateLog(">>> DB Insert failed"); // 일어날일이 거의 없음
                        }
                    }

                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! Erorr 발생 : {ex.Message}");
                }
            }
        }
    }
}
