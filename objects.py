import pygame
import random

class Padel():
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height



class Ball():
    def __init__(self, width, height, ball_width, ball_height, speed) -> None:
        self.x = width // 2
        self.y = random.randint(0.01 * height, 0.99 * height)
        self.width = ball_width
        self.height = ball_height
        vx = random.random() * (0.8 * speed**2) + 0.1 * speed**2
        vy = speed**2 - vx
        self.vx, self.vy = vx**0.5, vy**0.5
        self.vx *= random.randint(0, 1) * 2 - 1

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def collision_red(self, padel: Padel):
        x, y = self.x, self.y
        if padel.x + padel.width - x > padel.y + padel.height - y: # Top left ball to bottom right padel
            self.vy = abs(self.vy)
            x, y = self.x, self.y + self.height
        elif padel.x + padel.width - x > y - padel.y: # Bottom left ball to top right padel
            self.vy = -abs(self.vy)
        else:
            self.vx = abs(self.vx)

    def collision_yellow(self, padel: Padel):
        x, y = self.x + self.width, self.y
        if padel.x - x > padel.y + padel.height - y: # Top right ball to bottom left padel
            self.vy = abs(self.vy)
            x, y = self.x + self.width, self.y + self.height
        elif padel.x - x > y - padel.y: # Bottom right ball to top left padel
            self.vy = -abs(self.vy)
        else:
            self.vx = -abs(self.vx)

    def increase_speed(self):
        self.vx *= 1.05
        self.vy *= 1.05

    def boundary_collision(self, height):
        if self.y < 0 or self.y + self.height > height:
            self.vy *= -1

    def collide_padel(self, padel: Padel):
        x, y = self.x, self.y
        if x < padel.x + padel.width and x > padel.x and y < padel.y + padel.height and y > padel.y:
            return True
        x += self.width
        if x < padel.x + padel.width and x > padel.x and y < padel.y + padel.height and y > padel.y:
            return True
        y += self.height
        if x < padel.x + padel.width and x > padel.x and y < padel.y + padel.height and y > padel.y:
            return True
        x = self.x
        if x < padel.x + padel.width and x > padel.x and y < padel.y + padel.height and y > padel.y:
            return True
        return False

    def scored(self, width):
        if self.x < 1 or self.x + self.width > width:
            return True
        return False

    def restart(self, width, height, speed):
        self.x = width // 2
        self.y = random.randint(0.01 * height, 0.99 * height)
        vx = random.random() * (0.8 * speed**2) + 0.1 * speed**2
        vy = speed**2 - vx
        self.vx, self.vy = vx**0.5, vy**0.5
        self.vx *= random.randint(0, 1) * 2 - 1