# Python Game - PyGame Game Framework
# pip install pygame
import pygame

pygame.init() # 게임초기화 중요1. (반드시 필수!)
width = 500
height = 500

win = pygame.display.set_mode((width, height)) # 윈도우 창 만들기/ 500x500으로 만들겠다
pygame.display.set_caption('게임만들기')
icon = pygame.image.load('./studyPyGame/game.png') # 아이콘 만들기
pygame.display.set_icon(icon)

# object
x = 250 # 정중앙
y = 250
radius = 10 # 반지름
vel_x = 10 # 속도
vel_y = 10
jump = False

run = True

while run:
    win.fill((0,0,0)) # 전체배경을 검은색으로
    pygame.draw.circle(win, (255,255,255), (x, y), radius) 

    # 이벤트 = Python의 시그널
    for event in pygame.event.get(): # 중요2. 이벤트 받기
        if event.type == pygame.QUIT:
            run = False
    
    # 객채이동(움직임) 키보드로 누르면 움직임
    userInput = pygame.key.get_pressed() # 사용자가 입력
    if userInput[pygame.K_LEFT] and x > 10:
        x -= vel_x # 왼쪽으로 10씩 이동
    if userInput[pygame.K_RIGHT] and x < width - 10:
        x += vel_x
    # if userInput[pygame.K_UP] and y > 10:
    #     y -= vel_x
    # if userInput[pygame.K_DOWN] and y < height - 10:
    #     y += vel_x

    # 객체점프
    if jump == False and userInput[pygame.K_SPACE]:
        jump = True
    if jump == True:
        y -= vel_y * 3
        vel_y -= 1
        if vel_y < -10:
            jump = False
            vel_y = 10

    pygame.time.delay(10)
    pygame.display.update() # 중요3. 화면 업데이트(전환)
