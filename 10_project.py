# 오락실 팡 게임
# 캐릭터는 좌우만 이동 가능
# 스페이스 누르면 무기 쏘아올림
# 큰 공 1개 나타나서 바운스
# 무기에 공이 닿으면 2개로 분할, 가장 작은 크기의 공은 사라딤
# 모든 공을 없애면 게임 종료 - 성공
# 케릭터에 공이 닿으면 게임 종료 - 실패
# 시간제한 99초 초과 게임종료 - 실패
# fps 30 고정

# 1. 캐릭터가 공에 맞앗을때
# 2. 모든  공 없앴을 때
# 3. 시간 초과

import pygame
pygame.init()

# 화면 크기
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀
pygame.display.set_caption("Pang Game")

# fps 설정
clock = pygame.time.Clock()

# 사용자화
# background 배경 이미지 
background = pygame.image.load("C:\\Users\\82105\\Desktop\\python workspace\\pygame_basic\\background_play.png")

# stage 만들기
stage = pygame.image.load("C:\\Users\\82105\\Desktop\\python workspace\\pygame_basic\\stage.png")
# stage 사이즈
stage_size = stage.get_rect().size
stage_width = stage_size[0]
stage_height = stage_size[1]

# 캐릭터 이미지
character = pygame.image.load("C:\\Users\\82105\\Desktop\\python workspace\\pygame_basic\\character_play.png")
# 캐릭터 사이즈
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
# 캐릭터 좌표처리
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - stage_height - character_height
# 캐릭터 속도
character_speed = 0.7

# 캐릭터 위치 이동 좌표
character_to_x = 0
character_to_y = 0

# 무기 이미지
weapon = pygame.image.load("C:\\Users\\82105\\Desktop\\python workspace\\pygame_basic\\weapon.png")
# 무기 사이즈
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 한 번에 여러 발 발사 가능
weapons = []
# 무기 이동 속도
weapon_speed = 20
# 무기 위치 이동 좌표

# 공ㅇ 만들기
ball_images = [pygame.image.load("C:\\Users\\82105\\Desktop\\python workspace\\pygame_basic\\ball1.png"), \
                pygame.image.load("C:\\Users\\82105\\Desktop\\python workspace\\pygame_basic\\ball2.png"), \
                pygame.image.load("C:\\Users\\82105\\Desktop\\python workspace\\pygame_basic\\ball3.png"), \
                pygame.image.load("C:\\Users\\82105\\Desktop\\python workspace\\pygame_basic\\ball4.png")
]

# 공의 속도가 다 다름 - 공 크기에 따른 최초의 스피드
ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3

# 공의 정보들
balls = []

# 공의 x좌표, 공의 y좌표, 공의 이미지 인덱스, 공의 x축 이동 방향, 공의 y축 이동방향, y축 최초속도
# 최초 발생하는 큰 공 추가
balls.append({"pos_x" : 50, "pos_y" : 50, "img_idx" : 0, "to_x" : 3, "to_y" : -6, "init_sped_y": ball_speed_y[0]})


# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# font 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()

# 게임종료 메세지
game_result = "Game Over"

# 이벤트 루프
running = True
while running:
    dt = clock.tick(30)

    # 이벤트처리 - 키보드 입력
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            if event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                character_y_pos = screen_height - stage_height - character_height
            if event.key == pygame.K_SPACE: # 무기발사
                # 무기 위치 정의
                weapon_x_pos = character_x_pos + character_width/2 - weapon_width/2
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        if event.type == pygame.KEYUP:
            character_to_x = 0

    # 캐릭터 위치 정의
    character_x_pos += character_to_x * dt

    # 무기 위치 조정 - 무기 올라갔다 내려갔다 ######################################
    # 100, 200 - 180, 160 ...
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]
    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 공에 대한 경게값 처리
        # 가로벽에 닿앗을 때 공 위치 변경
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * (-1)

        # 세로 위치 - stage에 닿앗을때 튕김처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_sped_y"]
        else: # 공이 낙하할 때 - 속도 증가
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 가로, 세로 경계값 ######################################
    if character_x_pos <= 0:
        character_x_pos = 0
    elif character_x_pos >= screen_width - character_width:
        character_x_pos = screen_width - character_width


    # 충돌처리 2가지 - 공, 캐릭터 / 공, 무기
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공, 캐릭터 충돌처리
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공, 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx # 해당 공 없애기 위한 값 설정

                # 가장 작은 공이 아니라면 다음 단게의 공으로 나누기
                if ball_img_idx < 3:
                    # 현재 공 트기 정보 가지고 오기
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕기는 작은 공
                    balls.append({"pos_x" : ball_pos_x + ball_width / 2 - small_ball_width / 2, \
                        "pos_y" : ball_pos_y + ball_height / 2 - small_ball_height / 2, \
                            "img_idx" : ball_img_idx + 1, "to_x" : -3, "to_y" : -6, "init_sped_y": ball_speed_y[ball_img_idx+1]}) 
                    # 오른쪽으로 튕기는 작은 공          
                    balls.append({"pos_x" : ball_pos_x + ball_width / 2 - small_ball_width / 2, \
                        "pos_y" : ball_pos_y + ball_height / 2 - small_ball_height / 2, \
                            "img_idx" : ball_img_idx + 1, "to_x" : 3, "to_y" : -6, "init_sped_y": ball_speed_y[ball_img_idx+1]}) 
                break
        else:
            continue
        break

    # 충돌된 무기 공 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1


    # 모든 공 없애면 게임 종료
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    # 배경이미지 그리기
    screen.blit(background, (0, 0))

    # 무기 그리기
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    # stage 그리기
    screen.blit(stage, (0, screen_height - stage_height))

    # 캐릭터 이미지 그리기
    screen.blit(character, (character_x_pos, character_y_pos))
    
    # 경과 시간
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time: {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 시간 초과했다면
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()

msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center = (int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()
pygame.time.delay(2000)
pygame.quit()