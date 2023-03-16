# dinoRun
import pygame
import os

pygame.init()

ASSETS = './studyPyGame/Assets/' # ASSETS 할때마다 사용 할려고
SCREEN = pygame.display.set_mode((1100, 600)) # win을 SCREEN으로 바꾼것일뿐
icon = pygame.image.load('./studyPyGame/dinoRun2.png') # 아이콘 만들기
pygame.display.set_icon(icon)
# 배경이미지 로드 (게임은 무조건 이미지는 다 적용시켜야함)
BG = pygame.image.load(os.path.join(f'{ASSETS}Other', 'Track.png')) # ASSETS폴더에 Other폴더, track.png 가져옴
# 공룡이미지 로드  
RUNNING = [pygame.image.load(f'{ASSETS}Dino/DinoRun1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoRun2.png')] 
# 1.load(os.path.join), 2. load(f'./studyPyGame/Assets/Dino/DinoRun.png') 해도되는데 다르게해봄
DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoDuck2.png')]
JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png')

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

# 메인함수
def main():
    run = True
    clock = pygame.time.Clock()
    dino = Dino()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255,255,255)) # 배경 흰색
        userInput = pygame.key.get_pressed()

        dino.draw(SCREEN) # 공룡을 화면에 그려줘야함
        dino.update(userInput)

        clock.tick(30)
        pygame.display.update() # 중요! 초당 30번 update 수행

if __name__ == '__main__':
    main()