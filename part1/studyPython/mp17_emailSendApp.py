# 이메일 보내는 App
import smtplib # 메일 전송프로토콜
from email.mime.text import MIMEText

send_email = 'tlxmscksals@naver.com'
send_pass = 'facetime36134@#$'

recv_email = 'tlxmscksals2@gmail.com'

smtp_name = 'smtp.naver.com'

smtp_port = 587 # 포트번호

text = '''메일 내용입니다. 긴급이래요. 조심하세요!'''

msg = MIMEText(text)
msg['subject'] = '메일 제목입니다'
msg['From'] = send_email # 보내는 사람
msg['To'] = recv_email # 받는 사람

# print(msg.as_string())

mail = smtplib.SMTP(smtp_name, smtp_port) # SMTP 객체생성
mail.starttls() # 전송계층 보안 시작

mail.login(send_email, send_pass)
mail.sendmail(send_email, recv_email, msg=msg.as_string())
mail.quit()
print('전송완료')