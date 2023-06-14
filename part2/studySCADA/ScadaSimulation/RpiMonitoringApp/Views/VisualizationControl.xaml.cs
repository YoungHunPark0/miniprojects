using Google.Protobuf.WellKnownTypes;
using MySql.Data.MySqlClient;
using OxyPlot.Series;
using OxyPlot;
using SmartHomeMonitoringApp.Logics;
using SmartHomeMonitoringApp.Models;
using System;
using System.Collections.Generic;
using System.Data;
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

namespace SmartHomeMonitoringApp.Views
{
    using OxyPlot;
    using OxyPlot.Legends;
    using OxyPlot.Series;

    /// <summary>
    /// VisualizationControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class VisualizationControl : UserControl
    {
        List<string> Divisions = null;

        string FirstSensingDate = string.Empty;

        int TotalDataCount = 0; // 검색된 데이터 수

        public VisualizationControl()
        {
            InitializeComponent();
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            // 룸선택 콤보박스 초기화
            Divisions = new List<string> {"SELECT", "LIVING", "DINING", "BED", "BATH"};
            CboRoomName.ItemsSource = Divisions;
            CboRoomName.SelectedIndex = 0; // SELECT를 기본으로 선택

            // 검색시작일 날짜 - DB에서 제일 오래된 날짜를 가져와서 할당(뿌림)
            using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
            {
                conn.Open();
                // dtQuery 날짜를 가져옴 
                // 대문자 Y = 2023, 소문자 y = 23
                var dtQuery = @"SELECT F.Sensing_Date 
                                  FROM (
	                                SELECT date_format(Sensing_DateTime, '%Y-%m-%d') AS Sensing_Date 
	                                  FROM smarthomesensor
                                ) AS F 
                              GROUP BY F.Sensing_Date
                              ORDER BY F.Sensing_Date ASC Limit 1;";
                MySqlCommand cmd = new MySqlCommand(dtQuery, conn);
                var result = cmd.ExecuteScalar(); // 실행결과는 오브젝트
                Debug.WriteLine(result.ToString());
                FirstSensingDate = DtpStart.Text = result.ToString();
                // 주의사항! 검색시작일이 종료일보다 앞이여야 하는데 설정을 안하면 마음대로 바꿀 수 있음!
                // 검색종료일 현재일자를 가져와서 할당
                DtpEnd.Text = DateTime.Now.ToString("yyyy-MM-dd"); // 언어마다 날짜포맷이 다르기에 string표현을 주의해야함!
            }
        }

        // 검색버튼 클릭 이벤트 핸들러
        private async void BtnSearch_Click(object sender, RoutedEventArgs e)
        {
            // 검증 isvalid가 트루면
            bool isValid = true;
            string errorMsg = string.Empty;
            DataSet ds = new DataSet(); // DB상에 있던 SensingData 담는 데이터셋

            // 검색할 때 가장 중요한 것!
            // 검색, 저장, 수정, 삭제 전에 입력받은 값에 반드시 검증(Validation)을 해야함!
            // 검증!!
            if (CboRoomName.SelectedValue.ToString() == "SELECT") // 값이 SELECT면 검색되면 안됨
            {
                isValid = false;
                errorMsg += "방구분을 선택하세요.\n";
                //await Commons.ShowCustomMessageAsync("검색", "방구분을 선택하세요.");
                //return;
            }

            // 시스템 시작된 날짜보다 더 옛날 날짜로 검색하려면
            if (DateTime.Parse(DtpStart.Text) < DateTime.Parse(FirstSensingDate))
            {
                isValid = false;
                errorMsg += $"검색 시작일은 {FirstSensingDate} 이후로 선택하세요.\n";
                //await Commons.ShowCustomMessageAsync("검색", $"검색 시작일은 {FirstSensingDate} 이후로 선택하세요.");
                //return;
            }

            // 오늘날짜 이후 날짜로 검색하려는건 안됨! 막아야함!
            if (DateTime.Parse(DtpEnd.Text) > DateTime.Now) 
            {
                isValid = false;
                errorMsg += $"검색 종료일은 오늘까지 가능합니다.\n";
                //await Commons.ShowCustomMessageAsync("검색", $"검색 종료일은 오늘까지 가능합니다.");
                //return;
            }

            // 검색시작일이 검색종료일보다 이후면
            if (DateTime.Parse(DtpStart.Text) > DateTime.Parse(DtpEnd.Text))
            {
                isValid = false;
                errorMsg += $"검색 시작일이 검색 종료일보다 최신일수 없습니다.\n"; // 잘못적었다는 얘기// 둘이같은건 상관x
                //await Commons.ShowCustomMessageAsync("검색", $"검색 시작일이 검색 종료일보다 최신일수 없습니다."); 
                //return; 
            }

            if (isValid == false) 
            {
                await Commons.ShowCustomMessageAsync("검색", errorMsg);
                return;
            }
            // 검증끝

            // 검색시작
            TotalDataCount = 0;
            // DB에서 데이터값 들고옴
            try
            {
                using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                {
                    conn.Open();
                    var searchQuery = @"SELECT id,
	                                           Home_Id,
	                                           Room_Name,
	                                           Sensing_DateTime,
                                               Temp,
                                               Humid
                                          FROM smarthomesensor
                                         WHERE UPPER(Room_Name) = @Room_Name
                                           AND DATE_FORMAT(Sensing_DateTime, '%Y-%m-%d') 
                                       BETWEEN @StartDate AND @EndDate";
                    MySqlCommand cmd = new MySqlCommand(searchQuery, conn);
                    cmd.Parameters.AddWithValue("@Room_Name", CboRoomName.SelectedItem.ToString());
                    cmd.Parameters.AddWithValue("@StartDate", DtpStart.Text);
                    cmd.Parameters.AddWithValue("@EndDate", DtpEnd.Text);
                    MySqlDataAdapter adapter = new MySqlDataAdapter(cmd); // 어댑터를 안만들면 넘어온 데이터를 리더에 하나하나씩 옮겨야함
                    // 어댑터에 담은 다음 dataset에 담으면 끝남
                    
                    adapter.Fill(ds, "smarthomesensor");
                    // MessageBox.Show("TotalData", ds.Tables["smarthomesensor"].Rows.Count.ToString()); // 데이터갯수 확인
                }
            }
            catch (Exception ex)
            {
                await Commons.ShowCustomMessageAsync("DB검색", $"DB검색 오류 {ex.Message}");
            }

            // Create the plot model // 선택한 방의 이름이 타이틀로 나오도록 
            var tmp = new PlotModel { Title = $"{CboRoomName.SelectedValue} ROOM" };
            var legend = new Legend
            {
                LegendBorder = OxyColors.DarkGray,
                LegendBackground = OxyColor.FromArgb(150, 255, 255, 255),
                LegendPosition = LegendPosition.TopRight,
                LegendPlacement = LegendPlacement.Outside,
            };
            tmp.Legends.Add(legend); // 범례추가

            // Create two line series (markers are hidden by default)
            // 온도차트선 오랜지색 변경
            var tempSeries = new LineSeries
            {
                Title = "Temperature(℃)",
                MarkerType = MarkerType.Circle,
                Color = OxyColors.DarkOrange,   // 라인색상 온도는 주황색 
            };
            // 습도차트선 물색 변경
            var humidSeries = new LineSeries
            {
                Title = "Humidity(%)",
                MarkerType = MarkerType.Square,
                Color = OxyColors.Aqua // 라인색상 습도는 물색
            };

            // DB에서 가져온 데이터 차트에 뿌리도록 처리
            if (ds.Tables[0].Rows.Count > 0)
            {
                TotalDataCount = ds.Tables[0].Rows.Count;
                
                var count = 0;
                foreach (DataRow row in ds.Tables[0].Rows)
                {
                    tempSeries.Points.Add(new DataPoint(count++, Convert.ToDouble(row["Temp"]))); // 온도(temp) 시리즈 내용이 들어감
                    humidSeries.Points.Add(new DataPoint(count++, Convert.ToDouble(row["Humid"]))); // humid 시리즈 내용이 들어감
                }
            }
            tmp.Series.Add(tempSeries);
            tmp.Series.Add(humidSeries);

            OpvSmartHome.Model = tmp;

            LblTotalCount.Content = $"검색데이터 {TotalDataCount}개";
        }
    }
}