from time import perf_counter
import pygame
import os
from objects import Ball, Padel
from menu import Menu
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GamingX Pong")
ICON = pygame.image.load(
    os.path.join('Assets', 'pong_icon.png'))
pygame.display.set_icon(ICON)

SPEED = 250
variable_speed = SPEED
last_collided = None

WHITE = (255, 255, 255)
LIGHT_GREY = (60, 60, 60)
DARK_GREY = (30, 30, 30)

PADEL_WIDTH, PADEL_HEIGHT = 13, 55
RED_PADEL_X = 100 - PADEL_WIDTH // 2
YELLOW_PADEL_X = 800 - PADEL_WIDTH // 2
PADEL_Y = 250 - PADEL_HEIGHT // 2

YELLOW_PADEL_IMAGE = pygame.image.load(
    os.path.join('Assets', 'padel_yellow.png'))
YELLOW_PADEL = pygame.transform.scale(
    YELLOW_PADEL_IMAGE, (PADEL_WIDTH, PADEL_HEIGHT))

RED_PADEL_IMAGE = pygame.image.load(
    os.path.join('Assets', 'padel_red.png'))
RED_PADEL = pygame.transform.scale(
    RED_PADEL_IMAGE, (PADEL_WIDTH, PADEL_HEIGHT))

BALL_WIDTH, BALL_HEIGHT = 8, 8
BALL_IMAGE = pygame.image.load(
    os.path.join('Assets', 'ball.png'))
BALL = pygame.transform.scale(
    BALL_IMAGE, (BALL_WIDTH, BALL_HEIGHT))

BACKGROUND_IMAGE = pygame.image.load(
    os.path.join('Assets', 'background.png'))
BACKGROUND = pygame.transform.scale(
    BACKGROUND_IMAGE, (WIDTH, HEIGHT))


def draw_window(yellow: pygame.Rect, red: pygame.Rect, ball: Ball):
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(YELLOW_PADEL, (yellow.x, yellow.y))
    WIN.blit(RED_PADEL, (red.x, red.y))
    WIN.blit(BALL, (ball.x, ball.y))
    pygame.display.update()


def red_handle_movement(keys_pressed, red: pygame.Rect):
    if keys_pressed[pygame.K_w] and red.y - speed > 10:  # UP
        red.y -= speed
    if keys_pressed[pygame.K_s] and red.y + speed + red.height < HEIGHT - 10:  # DOWN
        red.y += speed


def yellow_handle_movement(keys_pressed, yellow: pygame.Rect):
    if keys_pressed[pygame.K_UP] and yellow.y - speed > 10:  # UP
        yellow.y -= speed
    if keys_pressed[pygame.K_DOWN] and yellow.y + speed + yellow.height < HEIGHT - 10:  # DOWN
        yellow.y += speed


def handle_ball_movement(ball: Ball, yellow: pygame.Rect, red: pygame.Rect):
    global variable_speed
    global last_collided
    ball.move()

    if ball.collide_padel(red):
        ball.collision_red(red)
        if last_collided != red:
            variable_speed *= 1.05
            ball.increase_speed()
            last_collided = red

    elif ball.collide_padel(yellow):
        ball.collision_yellow(yellow)
        if last_collided != yellow:
            variable_speed *= 1.05
            ball.increase_speed()
            last_collided = yellow

    ball.boundary_collision(HEIGHT)

    if ball.scored(WIDTH):
        ball.restart(WIDTH, HEIGHT)
        variable_speed = SPEED


def main():
    global speed
    delta_time = 0
    red = Padel(RED_PADEL_X, PADEL_Y, PADEL_WIDTH, PADEL_HEIGHT)
    yellow = Padel(YELLOW_PADEL_X, PADEL_Y, PADEL_WIDTH, PADEL_HEIGHT)

    ball = Ball(WIDTH, HEIGHT, BALL_WIDTH, BALL_HEIGHT)

    run = True
    while run:
        time1 = perf_counter()
        speed = variable_speed * delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        yellow_handle_movement(keys_pressed, yellow)

        handle_ball_movement(ball, yellow, red)

        draw_window(yellow, red, ball)
        time2 = perf_counter()
        delta_time = time2 - time1


def main_menu():
    menu = Menu(HEIGHT, WIDTH, text_colour=WHITE)
    menu.draw_menu(WIN, background_colour=DARK_GREY, box_colour=LIGHT_GREY)
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if menu.clicked_on_start(mouse):
                    main()


if __name__ == "__main__":
    main_menu()