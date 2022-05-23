from time import perf_counter
import pygame
from objects import Ball, Padel
import _menu
import sys
pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GamingX Pong")

SPEED = 230
variable_speed = SPEED
last_collided = None
score_font = pygame.font.SysFont("comicsans", 20)
TEXT_BAR_HEIGHT = score_font.get_height()

WHITE = (255, 255, 255)
LIGHT_GREY = (120, 120, 120)
MEDIUM_GREY = (60, 60, 60)
DARK_GREY = (30, 30, 30)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

DASHED_WIDTH = 4
DASHED_X = WIDTH / 2 - DASHED_WIDTH / 2

PADEL_WIDTH, PADEL_HEIGHT = 13, 55
PADEL_INDENT = 10
PADEL_SIDE_INDENT = 80
RED_PADEL_X = PADEL_SIDE_INDENT
YELLOW_PADEL_X = WIDTH - PADEL_SIDE_INDENT - PADEL_WIDTH
PADEL_Y = TEXT_BAR_HEIGHT + (HEIGHT - TEXT_BAR_HEIGHT) / 2 - PADEL_HEIGHT / 2

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
    pygame.draw.rect(WIN, DARK_GREY, (0, 0, WIDTH, TEXT_BAR_HEIGHT))
    pygame.draw.rect(WIN, RED, (red.x, red.y, PADEL_WIDTH, PADEL_HEIGHT))
    pygame.draw.rect(WIN, YELLOW, (yellow.x, yellow.y, PADEL_WIDTH, PADEL_HEIGHT))
    pygame.draw.rect(WIN, get_ball_colour(rally), (ball.x, ball.y, ball.width, ball.height))

    red_score_label = score_font.render(f"RED: {red_score}", True, WHITE)
    yellow_score_label = score_font.render(f"YELLOW: {yellow_score}", True, WHITE)
    rally_score_label = score_font.render(f"RALLY: {rally}", True, LIGHT_GREY)

    WIN.blit(red_score_label, (PADEL_INDENT, 0))
    WIN.blit(yellow_score_label, (WIDTH - yellow_score_label.get_width() - PADEL_INDENT, 0))
    WIN.blit(rally_score_label, (WIDTH / 2 - rally_score_label.get_width() / 2, 0))

    pygame.display.update()


def red_player_movement(keys_pressed, red: Padel, _):
    red.moving_up = False
    red.moving_down = False
    if keys_pressed[pygame.K_w] and red.y - speed > TEXT_BAR_HEIGHT + PADEL_INDENT:  # UP
        red.y -= speed
        red.moving_up = True
    if keys_pressed[pygame.K_s] and red.y + speed + red.height < HEIGHT - PADEL_INDENT:  # DOWN
        red.y += speed
        red.moving_down = True
    return red


def red_bot_movement(_, red: Padel, ball: Ball):
    red.moving_up = False
    red.moving_down = False
    if ball.y + ball.height / 2 < red.y + red.height / 2 and red.y - speed > TEXT_BAR_HEIGHT + PADEL_INDENT: # If ball higher than padel - move up
        red.y -= speed
        red.moving_up = True
    elif ball.y + ball.height / 2 > red.y + red.height / 2 and red.y + speed + red.height < HEIGHT - PADEL_INDENT: # If ball lower than padel - move down
        red.y += speed
        red.moving_down = True
    return red


def yellow_handle_movement(keys_pressed, yellow: Padel):
    yellow.moving_up = False
    yellow.moving_down = False
    if keys_pressed[pygame.K_UP] and yellow.y - speed > TEXT_BAR_HEIGHT + PADEL_INDENT:  # UP
        yellow.y -= speed
        yellow.moving_up = True
    if keys_pressed[pygame.K_DOWN] and yellow.y + speed + yellow.height < HEIGHT - PADEL_INDENT:  # DOWN
        yellow.y += speed
        yellow.moving_down = True
    return yellow


def handle_ball_movement(ball: Ball, yellow: Padel, red: Padel):
    global variable_speed
    global last_collided
    event = None
    ball.move(speed)

    if ball.collide_padel(red):
        ball.collision_red(red, spin=last_collided != red, speed=speed)
        if last_collided != red:
            variable_speed *= 1.03
            last_collided = red
            event = "Rally"

    elif ball.collide_padel(yellow):
        ball.collision_yellow(yellow, spin=last_collided != yellow, speed=speed)
        if last_collided != yellow:
            variable_speed *= 1.03
            last_collided = yellow
            event = "Rally"

    ball.boundary_collision()

    scored = ball.scored()
    if scored:
        ball.restart()
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

    ball = Ball(WIDTH, HEIGHT, BALL_WIDTH, BALL_HEIGHT, TEXT_BAR_HEIGHT)

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
                    sys.exit()

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
    menu.draw_menu(DARK_GREY)
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