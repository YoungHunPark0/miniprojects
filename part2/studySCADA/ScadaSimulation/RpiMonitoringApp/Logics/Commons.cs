﻿using MahApps.Metro.Controls;
using MahApps.Metro.Controls.Dialogs;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using uPLibrary.Networking.M2Mqtt;

namespace SmartHomeMonitoringApp.Logics
{
    public class Commons
    {
        // 화면마다 공유할 MQTT 브로커 IP담을 변수
        public static string BROKERHOST { get; set; } = "192.168.0.10"; // 본인 IP

        public static string MQTTTOPIC { get; set; } = "pknu/rpi/control/"; // 마지막 / 필수! 안하면 에러남

        public static string MYSQL_CONNSTRING { get; set; } = "Server=localhost;" +
                                                              "Port=3306;" +
                                                              "Database=miniproject;" +
                                                              "Uid=root;" +
                                                              "Pwd=12345;";
        
        // MQTT 클라이언트 공용 객체
        public static MqttClient MQTT_CLIENT { get; set; }

        // UserControl같이 자식클래스면서 MetroWindow를 직접사용하지 않아, MahApps.Metro에 있는 Metro메세지창을 못쓸때
        public static async Task<MessageDialogResult> ShowCustomMessageAsync(string title, string message,
            MessageDialogStyle style = MessageDialogStyle.Affirmative)
        {
            return await ((MetroWindow)Application.Current.MainWindow).ShowMessageAsync(title, message, style, null);
        }
    }
}
