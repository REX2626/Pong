from time import perf_counter

from objects import Ball, Padel, Powerup, PowerupEffect, BallPowerupEffect, GameEventType, pygame
import _menu
import sys
from win32api import GetSystemMetrics

pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE)
pygame.display.set_caption("GamingX Pong")
FULLSCREEN = False
FULLSCREEN_SIZE = GetSystemMetrics(0), GetSystemMetrics(1)
SIZE_LINK = True

SPEED = 230
variable_speed = SPEED
last_collided = None

WHITE = (255, 255, 255)
LIGHT_GREY = (120, 120, 120)
MEDIUM_GREY = (60, 60, 60)
DARK_GREY = (30, 30, 30)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PADEL_WIDTH, PADEL_HEIGHT = 13, 55
PADEL_INDENT = 10
PADEL_SIDE_INDENT = 80

POWERUP_MIN_X_RATIO = 0.30
POWERUP_MAX_X_RATIO = 1 - POWERUP_MIN_X_RATIO
POWERUP_MIN_Y_RATIO = 0.05
POWERUP_MAX_Y_RATIO = 1 - POWERUP_MIN_Y_RATIO

BALL_WIDTH, BALL_HEIGHT = 8, 8

def update_screen_size():
    global RED_PADEL_X, YELLOW_PADEL_X, PADEL_Y, DASHED_WIDTH, DASHED_X, DASHED_LENGTH, SCORE_FONT, TEXT_BAR_HEIGHT, BALL_WIDTH, BALL_HEIGHT, PADEL_WIDTH, PADEL_HEIGHT, SPEED, variable_speed
    SCORE_FONT = pygame.font.SysFont("comicsans", round(WIDTH / 45))
    TEXT_BAR_HEIGHT = SCORE_FONT.get_height()
    RED_PADEL_X = PADEL_SIDE_INDENT
    YELLOW_PADEL_X = WIDTH - PADEL_SIDE_INDENT - PADEL_WIDTH
    PADEL_Y = TEXT_BAR_HEIGHT + (HEIGHT - TEXT_BAR_HEIGHT) / 2 - PADEL_HEIGHT / 2
    DASHED_WIDTH = WIDTH / 225
    DASHED_X = round(WIDTH / 2 - DASHED_WIDTH / 2)
    DASHED_LENGTH = (HEIGHT - TEXT_BAR_HEIGHT - 2 * PADEL_INDENT) / 9

    if SIZE_LINK:
        BALL_WIDTH = BALL_HEIGHT = round(WIDTH / 112.5)
        PADEL_WIDTH = round(WIDTH / (900 / 13))
        PADEL_HEIGHT = round(HEIGHT / (500 / 55))
        SPEED = round(WIDTH / (900 / 230))
        variable_speed = SPEED

update_screen_size()


def update_playing_screen_size(menu: "_menu.Menu", red: Padel, yellow: Padel, ball: Ball, powerups: "list[Powerup]"):
    global WIDTH, HEIGHT
    red_ratio = (red.y + red.height / 2 - TEXT_BAR_HEIGHT - PADEL_INDENT) / (HEIGHT - TEXT_BAR_HEIGHT - 2 * PADEL_INDENT)
    yellow_ratio = (yellow.y + yellow.height / 2 - TEXT_BAR_HEIGHT - PADEL_INDENT) / (HEIGHT - TEXT_BAR_HEIGHT - 2 * PADEL_INDENT)
    WIDTH, HEIGHT = pygame.display.get_window_size()
    menu.resize()
    red.width = yellow.width = PADEL_WIDTH
    red.height = yellow.height = PADEL_HEIGHT
    red.x = RED_PADEL_X
    yellow.x = YELLOW_PADEL_X
    red.y = red_ratio * (HEIGHT - TEXT_BAR_HEIGHT - 2 * PADEL_INDENT) + TEXT_BAR_HEIGHT + PADEL_INDENT - red.height / 2
    yellow.y = yellow_ratio * (HEIGHT - TEXT_BAR_HEIGHT - 2 * PADEL_INDENT) + TEXT_BAR_HEIGHT + PADEL_INDENT - yellow.height / 2
    for padel in (red, yellow):
        padel.y = max(TEXT_BAR_HEIGHT + PADEL_INDENT, padel.y)
        padel.y = min(HEIGHT - PADEL_INDENT - PADEL_HEIGHT, padel.y)
    ball.screen_width = WIDTH
    ball.screen_height = HEIGHT
    ball.text_bar_height = TEXT_BAR_HEIGHT
    ball.width, ball.height = BALL_WIDTH, BALL_HEIGHT

    for powerup in powerups:
        # TODO: update powerup positions in a correct way
        pass


def get_ball_colour(rally):
    return (255, max(0, 255 - rally * 10), max(0, 255 - rally * 10))


def draw_dashed_line():
    for i in range(0, 10, 2):
        pygame.draw.rect(WIN, WHITE, (DASHED_X, round(TEXT_BAR_HEIGHT + PADEL_INDENT + i*DASHED_LENGTH), round(DASHED_WIDTH), round(DASHED_LENGTH)))
    
def draw_window(yellow: Padel, red: Padel, ball: Ball, powerups: "list[Powerup]", red_score, yellow_score, rally):
    WIN.fill(BLACK)
    draw_dashed_line()

    for powerup in powerups:
        powerup.draw(WIN)

    pygame.draw.rect(WIN, DARK_GREY, (0, 0, WIDTH, TEXT_BAR_HEIGHT)) # the background for the text bar at the top
    red.draw(WIN, RED)
    yellow.draw(WIN, YELLOW)
    ball.draw(WIN, get_ball_colour(rally))

    red_score_label = SCORE_FONT.render(f"RED: {red_score}", True, WHITE)
    yellow_score_label = SCORE_FONT.render(f"YELLOW: {yellow_score}", True, WHITE)
    rally_score_label = SCORE_FONT.render(f"RALLY: {rally}", True, LIGHT_GREY)

    WIN.blit(red_score_label, (PADEL_INDENT, 0))
    WIN.blit(yellow_score_label, (WIDTH - yellow_score_label.get_width() - PADEL_INDENT, 0))
    WIN.blit(rally_score_label, (WIDTH / 2 - rally_score_label.get_width() / 2, 0))

    pygame.display.update()


def red_player_movement(keys_pressed, red: Padel, _, speed):
    red.moving_up = False
    red.moving_down = False
    if keys_pressed[pygame.K_w] and red.y - speed > TEXT_BAR_HEIGHT + PADEL_INDENT:  # UP
        red.y -= speed
        red.moving_up = True
    if keys_pressed[pygame.K_s] and red.y + speed + red.height < HEIGHT - PADEL_INDENT:  # DOWN
        red.y += speed
        red.moving_down = True
    return red


def red_bot_movement(_, red: Padel, ball: Ball, speed):
    red.moving_up = False
    red.moving_down = False
    if ball.y + ball.height / 2 < red.y + red.height / 2 and red.y - speed > TEXT_BAR_HEIGHT + PADEL_INDENT: # If ball higher than padel - move up
        red.y -= speed
        red.moving_up = True
    elif ball.y + ball.height / 2 > red.y + red.height / 2 and red.y + speed + red.height < HEIGHT - PADEL_INDENT: # If ball lower than padel - move down
        red.y += speed
        red.moving_down = True
    return red


def yellow_handle_movement(keys_pressed, yellow: Padel, speed):
    yellow.moving_up = False
    yellow.moving_down = False
    if keys_pressed[pygame.K_UP] and yellow.y - speed > TEXT_BAR_HEIGHT + PADEL_INDENT:  # UP
        yellow.y -= speed
        yellow.moving_up = True
    if keys_pressed[pygame.K_DOWN] and yellow.y + speed + yellow.height < HEIGHT - PADEL_INDENT:  # DOWN
        yellow.y += speed
        yellow.moving_down = True
    return yellow


def handle_ball_movement(ball: Ball, yellow: Padel, red: Padel, powerups: "list[Powerup]", speed):
    global variable_speed
    global last_collided
    game_event = GameEventType.NONE
    ball.move(speed)

    for powerup in powerups:
        ball_hit_powerup = powerup.handle_collisions(ball)
        if not ball_hit_powerup: continue
        
        effect = powerup.powerup_type.powerup_effect
        if isinstance(effect, BallPowerupEffect):
            effect.ball_effect_func(ball)

        powerups.remove(powerup)
        powerups.append(Powerup.create_random(
            min_x=WIDTH * POWERUP_MIN_X_RATIO,
            max_x=WIDTH * POWERUP_MAX_X_RATIO,
            min_y=(HEIGHT - TEXT_BAR_HEIGHT) * POWERUP_MIN_Y_RATIO + TEXT_BAR_HEIGHT,
            max_y=(HEIGHT - TEXT_BAR_HEIGHT) * POWERUP_MAX_Y_RATIO + TEXT_BAR_HEIGHT,
        ))

    for paddle in (red, yellow):
        if ball.collides_with_paddle_check(paddle):
            ball.handle_paddle_collisions(paddle, spin=last_collided != paddle)
            if last_collided != paddle:
                variable_speed *= 1.03
                last_collided = paddle
                game_event = GameEventType.RALLY

    ball.boundary_collision()

    scored = ball.scored()
    if scored:
        ball.restart()
        variable_speed = SPEED
        game_event = scored
        last_collided = None
    
    return game_event


def main(red_handle_movement, menu: "_menu.Menu"):
    delta_time = 0

    red_score = 0
    yellow_score = 0
    rally = 0

    red = Padel(RED_PADEL_X, PADEL_Y, PADEL_WIDTH, PADEL_HEIGHT)
    yellow = Padel(YELLOW_PADEL_X, PADEL_Y, PADEL_WIDTH, PADEL_HEIGHT)

    ball = Ball(WIDTH, HEIGHT, BALL_WIDTH, BALL_HEIGHT, TEXT_BAR_HEIGHT)

    powerups: "list[Powerup]" = []
    for _ in range(3):
        powerups.append(Powerup.create_random(
            min_x=WIDTH * POWERUP_MIN_X_RATIO,
            max_x=WIDTH * POWERUP_MAX_X_RATIO,
            min_y=(HEIGHT - TEXT_BAR_HEIGHT) * POWERUP_MIN_Y_RATIO + TEXT_BAR_HEIGHT,
            max_y=(HEIGHT - TEXT_BAR_HEIGHT) * POWERUP_MAX_Y_RATIO + TEXT_BAR_HEIGHT,
        ))

    running = True
    not_paused = True
    while running:
        while not_paused:
            time1 = perf_counter()
            speed = variable_speed * delta_time

            keys_pressed = pygame.key.get_pressed()
            red = red_handle_movement(keys_pressed, red, ball, speed)
            yellow = yellow_handle_movement(keys_pressed, yellow, speed)

            game_event = handle_ball_movement(ball, yellow, red, powerups, speed)
            if game_event == GameEventType.RED:
                red_score += 1
                rally = 0
            elif game_event == GameEventType.YELLOW:
                yellow_score += 1
                rally = 0
            elif game_event == GameEventType.RALLY:
                rally += 1

            draw_window(yellow, red, ball, powerups, red_score, yellow_score, rally)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    not_paused = False
                    running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.VIDEORESIZE:
                    update_playing_screen_size(menu, red, yellow, ball, powerups)

                elif event.type == pygame.KEYDOWN and event.__dict__["key"] == pygame.K_ESCAPE:
                    not_paused = False
                    menu.pause()


            time2 = perf_counter()
            delta_time = time2 - time1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                not_paused = False
                running = False
                pygame.quit()

            elif event.type == pygame.VIDEORESIZE:
                update_playing_screen_size(menu, red, yellow, ball, powerups)
                draw_window(yellow, red, ball, powerups, red_score, yellow_score, rally)
                menu.pause()

            elif event.type == pygame.KEYDOWN and event.__dict__["key"] == pygame.K_ESCAPE:
                not_paused = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if menu.mouse_click(mouse):
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

            elif event.type == pygame.VIDEORESIZE:
                menu.resize()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                menu.mouse_click(mouse)


if __name__ == "__main__":
    main_menu()