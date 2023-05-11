SELECT id,
	   Home_Id,
	   Room_Name,
	   Sensing_DateTime,
       Temp,
       Humid
  FROM smarthomesensor
 WHERE Room_Name = 'Bed'
   AND DATE_FORMAT(Sensing_DateTime, '%Y-%m-%d') BETWEEN '2023-05-09' AND '2023-05-10'
