import pygame

pygame.init()
win = pygame.display.set_mode((1000, 500))

bg_img = pygame.image.load('./studyPyGame/Assets/Backgound.png') # 백그라운드에 쓸 이미지
BG = pygame.transform.scale(bg_img, (1000, 500)) # 사이즈업 (본이미지 800x400)
pygame.display.set_caption('게임만들기')
icon = pygame.image.load('./studyPyGame/game.png') # 아이콘 만들기
pygame.display.set_icon(icon)

width = 1000
loop = 0
run = True
while run:
    win.fill((0,0,0)) # 검은색

    # 이벤트 = Python의 시그널
    for event in pygame.event.get(): # 중요2. 이벤트 받기
        if event.type == pygame.QUIT:
            run = False

    # 배경을 그림
    win.blit(BG, (loop, 0)) # 윈도우를 blit로 그림
    win.blit(BG, (width + loop, 0))
    if loop == - width: # 루프가 -1000이랑 같아지면
       # win.blit(BG, (width + loop, 0))
        loop = 0

    loop -= 1

    pygame.display.update()