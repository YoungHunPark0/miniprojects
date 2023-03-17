# dinoRun
import pygame
import os
import random

pygame.init()

ASSETS = './studyPyGame/Assets/' # ASSETS 할때마다 사용 할려고
SCREEN_WIDTH = 1100 # 변수화. 게임 윈도우 넓이
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, 600)) # win을 SCREEN으로 바꾼것일뿐
icon = pygame.image.load('./studyPyGame/dinoRun2.png') # 아이콘 만들기
pygame.display.set_icon(icon)
# 배경이미지 로드 (게임은 무조건 이미지는 다 적용시켜야함)
BG = pygame.image.load(os.path.join(f'{ASSETS}Other', 'Track.png')) # ASSETS폴더에 Other폴더, track.png 가져옴
# 공룡이미지 로드  
RUNNING = [pygame.image.load(f'{ASSETS}Dino/DinoRun1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoRun2.png')] 
# 1.load(os.path.join), 2. load(f'./studyPyGame/Assets/Dino/DinoRun.png') 해도되는데 다르게해봄
DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoDuck2.png')] # Dodge 피하다(=duck)
JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png')
# 구름이미지
CLOUD = pygame.image.load(f'{ASSETS}Other/Cloud.png') # 클라우드가 Other폴더에 있음
# 익룡이미지 로드
BIRD = [pygame.image.load(f'{ASSETS}Bird/Bird1.png'),
        pygame.image.load(f'{ASSETS}Bird/Bird2.png')]
# 선인장이미지 로드. Assets폴더->큰거/작은거 2종류 // 애니메이션을 위한게 아니라 선인장 종류가 3개씩
LARGE_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/LargeCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus3.png')]
SMALL_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/SmallCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus3.png')]

class Dino: # 공룡 클래스. 공룡자체의 위치값이 필요함
    X_POS = 80; Y_POS = 310; Y_POS_DUCK = 340; JUMP_VEL = 9.0

    def __init__(self) -> None:
        self.run_img = RUNNING; self.duck_img = DUCKING; self.jump_img = JUMPING
        self.dino_run = True; self.dino_duck = False; self.dino_jump = False # 공룡상태

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL # 점프 초기값 9.0
        self.image = self.run_img[0] # run_img[0] == DinoRun1
        self.dino_rect = self.image.get_rect() # 이미지 사격형 정보 다나옴
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput) -> None:
        if self.dino_run:
            self.run()
        elif self.dino_duck:
            self.duck()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10: self.step_index = 0 # 애니메이션 스텝
        
        if userInput[pygame.K_UP] and not self.dino_jump: # dino_jump가 참이 아니면 점프
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
            self.dino_rect.y = self.Y_POS # 이게 없으면 공룡이 하늘로 날아감
        elif userInput[pygame.K_DOWN] and not self.dino_jump: # 수그리기
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]): # 런
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

    def run(self):
        self.image = self.run_img[self.step_index // 5] # rum_img 달리기, 5로 나눴을 때 나머지값 1,0 구분. / 10 0, 1
        self.dino_rect = self.image.get_rect() # 이미지 사격형 정보 다나옴
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = self.duck_img[self.step_index // 5] # duck_img 수그리기
        self.dino_rect = self.image.get_rect() # 이미지 사격형 정보 다나옴
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK # 이미지 높이가 작으니까 늘려줘야함 (line22에서 340으로 늘림)
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img # jump_img는 하나밖에 없기때문에
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL: # -9.0이 되면 점프중단
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL # 9.0으로 초기화 (안하면 공룡이 지하로 꺼짐)

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud: # 구름 클래스
    def __init__(self) -> None: # 초기화 할게 없더라도 클래스 만들면 반드시! __init__만들기! 생성자만들기!
        self.x = SCREEN_WIDTH + random.randint(300, 500)  # x값, y값 만들기. 첫번째 구름 300,500
        self.y = random.randint(50, 100) # 구름은 하늘에 떠있으니, 창 상단 50,100 정도 라인에 구름생성
        self.image = CLOUD # 구름이미지가 여러개가 아니기에 배열안만듬. 2개이상이면 배열만들어서 하기
        self.width = self.image.get_width() # 구름이 흘러가게 만들기 위해서
        

    def update(self) -> None:
        self.x -= game_speed
        if self.x < -self.width: # 화면 밖으로 벗어나면
            self.x = SCREEN_WIDTH + random.randint(1300, 2000) # 두번째 구름생성 바로나오면 이상해서 간격 1300,2000으로 늘림 
            self.y = random.randint(50, 100)

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle: # 장애물 클래스(부모클래스)
    def __init__(self, image, type) -> None:
        self.image = image
        self.type = type # type==키워드
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH # 1100

    def update(self) -> None:
        self.rect.x -= game_speed
        if self.rect.x <= -self.rect.width: # 왼쪽 화면 밖으로 벗어나면 장애물은 사라지니까
            obstacles.pop() # 장애물 리스트에서 하나 꺼내오기 
            # 장애물(배열-리스트) - 구름, 익룡, 선인장->장애물

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image[self.type], self.rect)

class Bird(Obstacle): # 장애물 클래스 상속클래스
    def __init__(self, image) -> None:
        self.type = 0 # 새는 0
        super().__init__(image, self.type)
        self.rect.y = 250 # 새니까 하늘에 그림그려야 해서 
        self.index = 0 # 새는 이미지가 2개. 0번이미지로 시작
    
    def draw(self, SCREEN) -> None: # draw 재정의. 객체지향 생각하기. draw는 새로그린다
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class LargeCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type = random.randint(0, 2) # 큰 선인장 종류 3개니까 하나를 고름(랜덤) 0, 1, 2
        super().__init__(image, self.type)
        self.rect.y = 300

class SmallCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type = random.randint(0, 2) # 작은 선인장 종류 3개니까 하나를 고름(랜덤) 0, 1, 2
        super().__init__(image, self.type)
        self.rect.y = 325

# 메인함수
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles # game_speed=게임속도를 관장하기 위한, x,y_pos_bg-백그라운드, points-점수
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0 # 개인점수는 0부터 시작
    run = True
    clock = pygame.time.Clock()
    dino = Dino() # 공룡객체 생성
    cloud = Cloud() # 구름객체 생성
    game_speed = 14
    obstacles = [] # 장애물 리스트

    font = pygame.font.Font(f'{ASSETS}NanumGothicBold.ttf', 20) # 나눔고딕, 사이즈크기=20

    # 함수 내 함수(점수표시)
    def score(): 
        global points, game_speed
        points += 1
        if points % 100 == 0: # 100, 200, 300..100단위로 나눴을 때 0이면
            game_speed += 1 # 점수가 높아지면 속도가 증가

        txtScore = font.render(f'SCORE : {points}', True, (83,83,83)) # 공룡색-회색
        txtRect = txtScore.get_rect() # 2d여서 x,y축을 사용해서 get_rect 많이씀
        txtRect.center = (1000, 40) # 점수 위치
        SCREEN.blit(txtScore, txtRect)

    # 함수 내 함수(배경그리기)
    def background(): # 땅바닥(배경=background) update, draw를 동시에 해주는 함수
        global x_pos_bg, y_pos_bg # 바깥에서 쓰던 함수를 안에서도 쓸 수 있음.
        image_width = BG.get_width() # get_width-전체넓이 가져옴. 2404가 나옴
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg)) # 0, 380 먼저 그림
        SCREEN.blit(BG, (image_width+x_pos_bg, y_pos_bg)) # 배경은 두번겹치면 자연스러워져서 씀. 2404+0, 380
        if x_pos_bg <= -image_width:
            # SCREEN_WIDTH.blit(BG, (image_width+x_pos_bg, y_pos_bg))
            x_pos_bg = 0

        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255,255,255)) # 배경 흰색
        userInput = pygame.key.get_pressed()

        background() # 사용할려면 반드시!
        score() # 사용할려면 반드시!

        # 구름이 공룡보다 먼저 그려져야 됨. 배경이니까, 뒤에 적으면 구름이 공룡보다 앞으로 나옴
        cloud.draw(SCREEN) # 구름은 자기가 알아서 움직임. 구름이 애니메이션
        cloud.update() 

        dino.draw(SCREEN) # 공룡을 화면에 그려줘야함
        dino.update(userInput) # 공룡은 눌러야 움직임

        if len(obstacles) == 0: # 장애물 변수 만들기
            if random.randint(0, 2) == 0: # 작은선인장
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1: # 큰선인장
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2: # 
                obstacles.append(Bird(BIRD))

        for obs in obstacles:
            obs.draw(SCREEN)
            obs.update()
            # Collision(충돌) Dection(발견,간파,탐지) 
            if dino.dino_rect.colliderect(obs.rect): # colliderect 충돌감지
                pygame.draw.rect(SCREEN, (255,0,0), dino.dino_rect, 3)

        clock.tick(40) # 30 기본, 40으로 올리면 빨라짐
        pygame.display.update() # 중요! 초당 30번 update 수행

if __name__ == '__main__':
    main()