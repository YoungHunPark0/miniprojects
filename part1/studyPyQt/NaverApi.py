# NaverApi 클래스 -> OpenApi는 인터넷을 통해서 데이터를 전달 받음
from urllib.request import Request, urlopen 
# request는 클래스, urlopen은 함수
from urllib.parse import quote # quote함수에 encoding 기능이 있음. search는 에러날 가능성이 있어서 사용!
import datetime # 현재시간 사용
import json # 결과는 json으로 return 받을 것 이기에 선언!

class NaverApi:
    # 생성자 - 클래스는 생성자부터 만들기!
    def __init__(self) -> None:
        print(f'[{datetime.datetime.now()}] Naver API 생성')

    # Naver API를 요청(호출) 함수! 핵심!
    def get_request_url(self, url): 
        req = Request(url)
        # Naver API 개인별 인증
        # https://developers.naver.com/apps/#/myapps/ol2ZJlYiqa5w8P1yvDjN/overview
        # ->에 있는 client id, secret 사용
        # 핵심!!
        req.add_header('X-Naver-Client-Id', 'ol2ZJlYiqa5w8P1yvDjN')
        req.add_header('X-Naver-Client-Secret', 'ZXaCRc6M3M')

        try:
            res = urlopen(req) # 요청 결과가 바로 돌아옴
            if res.getcode() == 200: # response OK 제데로 값을 돌려받음
                print(f'[{datetime.datetime.now()}] NaverAPI 요청 성공') # 성공한 시간과 일시 나옴
                return res.read().decode('utf-8') # 한글쓰면 에러날 수 있기에 decode('utf-8)
            
            else:
                print(f'[{datetime.datetime.now()}] NaverAPI 요청 실패')
                return None # 실패하면 값을 돌려줄게 없음
        except Exception as e: # 예외처리하고 받을 때 뭐가 예외처리 한지 알아야함
            print(f'[{datetime.datetime.now()}] 예외발생 : {e}')
            return None

    # 실제 호출함수
    def get_naver_search(self, node, search, start, display): # self를 제외한 4개의 변수를 받음
        base_url = 'https://openapi.naver.com/v1/search'
        node_url = f'/{node}.json' # 위 노드랑 다름. 
        params = f'?query={quote(search)}&start={start}&display={display}' # 어떠한 값이 들어갈 것
        # quote함수에 encoding 기능이 있음. search는 에러날 가능성이 있어서 사용!
        
        url = base_url + node_url + params
        retData = self.get_request_url(url)
        
        if retData == None:
            return None
        else:
            return json.loads(retData) # json으로 return

    # json으로 받은 데이터를 --> list로 변환
    def get_post_data(self, post, outputs):
        title = post['title']
        description = post['description']
        originallink = post['originallink']
        link = post['link']

        # 'Tue, 07 Mar 2023 14:23:00 +0900' 문자열로 들어온걸 날짜형으로 변경
        pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
        pubDate = pDate.strftime('%Y-%m-%d %H:%M:%S') # 2023-03-07 17:04:00 형식으로 변경

        # outputs에 옮기기. mp03_naversearchapp.py에서 outputs = [] 리스트로 되어있기에 리스트 안에 값넣기
        outputs.append({'title':title, 'description':description,
                        'originallink':originallink, 'link':link,
                        'pubDate':pubDate})