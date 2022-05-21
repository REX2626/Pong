from time import perf_counter
import pygame
import os
from objects import Ball, Padel
import _menu
pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GamingX Pong")
ICON = pygame.image.load(
    os.path.join('Assets', 'pong_icon.png'))
pygame.display.set_icon(ICON)

SPEED = 230
variable_speed = SPEED
last_collided = None
score_font = pygame.font.SysFont("comicsans", 20)

WHITE = (255, 255, 255)
LIGHT_GREY = (120, 120, 120)
MEDIUM_GREY = (60, 60, 60)
DARK_GREY = (30, 30, 30)
BLACK = (0, 0, 0)

DASHED_WIDTH = 4
DASHED_X = WIDTH / 2 - DASHED_WIDTH / 2

PADEL_WIDTH, PADEL_HEIGHT = 13, 55
RED_PADEL_X = 80
YELLOW_PADEL_X = 820 - PADEL_WIDTH
PADEL_Y = 250 - PADEL_HEIGHT // 2

YELLOW_PADEL_IMAGE = pygame.image.load(
    os.path.join('Assets', 'padel_yellow.png'))
YELLOW_PADEL = pygame.transform.scale(
    YELLOW_PADEL_IMAGE, (PADEL_WIDTH, PADEL_HEIGHT)).convert()

RED_PADEL_IMAGE = pygame.image.load(
    os.path.join('Assets', 'padel_red.png'))
RED_PADEL = pygame.transform.scale(
    RED_PADEL_IMAGE, (PADEL_WIDTH, PADEL_HEIGHT)).convert()

BACKGROUND_IMAGE = pygame.image.load(
    os.path.join('Assets', 'background.png'))
BACKGROUND = pygame.transform.scale(
    BACKGROUND_IMAGE, (WIDTH, HEIGHT)).convert()

BALL_WIDTH, BALL_HEIGHT = 8, 8


def get_ball_colour(rally):
    return (255, max(0, 255 - rally * 10), max(0, 255 - rally * 10))


def draw_dashed_line():
    pygame.draw.rect(WIN, WHITE, (DASHED_X, 38, DASHED_WIDTH, 50))
    pygame.draw.rect(WIN, WHITE, (DASHED_X, 138, DASHED_WIDTH, 50))
    pygame.draw.rect(WIN, WHITE, (DASHED_X, 238, DASHED_WIDTH, 50))
    pygame.draw.rect(WIN, WHITE, (DASHED_X, 338, DASHED_WIDTH, 50))
    pygame.draw.rect(WIN, WHITE, (DASHED_X, 438, DASHED_WIDTH, 50))


def draw_window(yellow: pygame.Rect, red: pygame.Rect, ball: Ball, red_score, yellow_score, rally):
    WIN.fill(BLACK)
    draw_dashed_line()
    pygame.draw.rect(WIN, DARK_GREY, (0, 0, WIDTH, 28))
    WIN.blit(YELLOW_PADEL, (yellow.x, yellow.y))
    WIN.blit(RED_PADEL, (red.x, red.y))
    pygame.draw.rect(WIN, get_ball_colour(rally), (ball.x, ball.y, ball.width, ball.height))

    red_score_label = score_font.render(f"RED: {red_score}", True, WHITE)
    yellow_score_label = score_font.render(f"YELLOW: {yellow_score}", True, WHITE)
    rally_score_label = score_font.render(f"RALLY: {rally}", True, LIGHT_GREY)

    WIN.blit(red_score_label, (10, 0))
    WIN.blit(yellow_score_label, (WIDTH - yellow_score_label.get_width() - 10, 0))
    WIN.blit(rally_score_label, (WIDTH / 2 - rally_score_label.get_width() / 2, 0))

    pygame.display.update()


def red_player_movement(keys_pressed, red: Padel, _):
    red.moving_up = False
    red.moving_down = False
    if keys_pressed[pygame.K_w] and red.y - speed > 38:  # UP
        red.y -= speed
        red.moving_up = True
    if keys_pressed[pygame.K_s] and red.y + speed + red.height < HEIGHT - 10:  # DOWN
        red.y += speed
        red.moving_down = True
    return red


def red_bot_movement(_, red: Padel, ball: Ball):
    red.moving_up = False
    red.moving_down = False
    if ball.y + ball.height / 2 < red.y + red.height / 2 and red.y - speed > 38: # If ball higher than padel - move up
        red.y -= speed
        red.moving_up = True
    elif ball.y + ball.height / 2 > red.y + red.height / 2 and red.y + speed + red.height < HEIGHT - 10: # If ball lower than padel - move down
        red.y += speed
        red.moving_down = True
    return red


def yellow_handle_movement(keys_pressed, yellow: Padel):
    yellow.moving_up = False
    yellow.moving_down = False
    if keys_pressed[pygame.K_UP] and yellow.y - speed > 38:  # UP
        yellow.y -= speed
        yellow.moving_up = True
    if keys_pressed[pygame.K_DOWN] and yellow.y + speed + yellow.height < HEIGHT - 10:  # DOWN
        yellow.y += speed
        yellow.moving_down = True
    return yellow


def handle_ball_movement(ball: Ball, yellow: Padel, red: Padel):
    global variable_speed
    global last_collided
    event = None
    ball.move(speed, WIDTH // 2)

    if ball.collide_padel(red):
        ball.collision_red(red, spin=last_collided != red, speed=speed, screen_width=WIDTH)
        if last_collided != red:
            variable_speed *= 1.03
            last_collided = red
            event = "Rally"

    elif ball.collide_padel(yellow):
        ball.collision_yellow(yellow, spin=last_collided != yellow, speed=speed, screen_width=WIDTH)
        if last_collided != yellow:
            variable_speed *= 1.03
            last_collided = yellow
            event = "Rally"

    ball.boundary_collision(HEIGHT)

    scored = ball.scored(WIDTH)
    if ball.scored(WIDTH):
        ball.restart(WIDTH, HEIGHT)
        variable_speed = SPEED
        event = scored
        last_collided = None
    
    return event


def main(red_handle_movement, menu):
    global speed
    delta_time = 0

    red_score = 0
    yellow_score = 0
    rally = 0

    red = Padel(RED_PADEL_X, PADEL_Y, PADEL_WIDTH, PADEL_HEIGHT)
    yellow = Padel(YELLOW_PADEL_X, PADEL_Y, PADEL_WIDTH, PADEL_HEIGHT)

    ball = Ball(WIDTH, HEIGHT, BALL_WIDTH, BALL_HEIGHT)

    running = True
    not_paused = True
    while running:
        while not_paused:
            time1 = perf_counter()
            speed = variable_speed * delta_time

            keys_pressed = pygame.key.get_pressed()
            red = red_handle_movement(keys_pressed, red, ball)
            yellow = yellow_handle_movement(keys_pressed, yellow)

            event = handle_ball_movement(ball, yellow, red)
            if event == "Red":
                red_score += 1
                rally = 0
            elif event == "Yellow":
                yellow_score += 1
                rally = 0
            elif event == "Rally":
                rally += 1

            draw_window(yellow, red, ball, red_score, yellow_score, rally)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    not_paused = False
                    running = False
                    pygame.quit()

                elif event.type == pygame.KEYDOWN and event.__dict__["key"] == pygame.K_ESCAPE:
                    not_paused = False
                    menu.pause()


            time2 = perf_counter()
            delta_time = time2 - time1
        
        if not running:
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                not_paused = False
                running = False
                pygame.quit()

            elif event.type == pygame.KEYDOWN and event.__dict__["key"] == pygame.K_ESCAPE:
                not_paused = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                menu.mouse_click(mouse)
                running = False


def main_menu():
    menu = _menu.Menu()
    menu.draw_menu(WIN, DARK_GREY)
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                menu.mouse_click(mouse)


if __name__ == "__main__":
    main_menu()