import random

class Padel():
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.moving_down = False
        self.moving_up = False



class Ball():
    def __init__(self, width, height, ball_width, ball_height) -> None:
        self.x = width // 2
        self.y = random.randint(30, height - ball_height - 2)
        self.width = ball_width
        self.height = ball_height
        self.spinx = 0
        self.spiny = 0
        vx = random.random() * 0.8 + 0.2
        vy = 1 - vx
        self.vx, self.vy = vx**0.5, vy**0.5
        self.vx *= random.randint(0, 1) * 2 - 1

    def move(self, speed, screen_width):
        self.x += (self.vx + self.spinx) * speed
        self.y += (self.vy + self.spiny) * speed
        if self.spinx != 0:
            if self.spinx > 0:
                self.spinx -= min(self.spinx, speed / screen_width)
            elif self.spinx < 0:
                self.spinx += min(-self.spinx, speed / screen_width)
        if self.spiny != 0:
            if self.spiny > 0:
                self.spiny -= min(self.spiny, speed / screen_width)
            elif self.spiny < 0:
                self.spiny += min(-self.spiny, speed / screen_width)

    def collision_red(self, padel: Padel, spin):
        x, y = self.x, self.y
        if padel.x + padel.width - x > padel.y + padel.height - y: # Top left ball to bottom right padel
            self.vy = abs(self.vy)
        elif padel.x + padel.width - x > y + self.height - padel.y: # Bottom left ball to top right padel
            self.vy = -abs(self.vy)
        else:
            dist_to_centre = (y + self.height / 2) - (padel.y + padel.height / 2) # Distance from center of ball to centre of padel
            self.vy = dist_to_centre / padel.height
            self.vx = (1 - self.vy**2)**0.5
            if spin:
                if padel.moving_up:
                    self.spiny += 1
                    self.spinx += 0.5
                elif padel.moving_down:
                    self.spiny -= 1
                    self.spinx += 0.5

    def collision_yellow(self, padel: Padel, spin):
        x, y = self.x, self.y
        if x + self.width - padel.x > padel.y + padel.height - y: # Top right ball to bottom left padel
            self.vy = abs(self.vy)
        elif x + self.width - padel.x > y + self.height - padel.y: # Bottom right ball to top left padel
            self.vy = -abs(self.vy)
        else:
            dist_to_centre = (y + self.height / 2) - (padel.y + padel.height / 2) # Distance from center of ball to centre of padel
            self.vy = dist_to_centre / padel.height
            self.vx = -(1 - self.vy**2)**0.5
            if spin:
                if padel.moving_up:
                    self.spiny += 1
                    self.spinx -= 0.5
                elif padel.moving_down:
                    self.spiny -= 1
                    self.spinx -= 0.5

    def boundary_collision(self, height):
        if self.y < 30 or self.y + self.height > height - 2:
            self.vy *= -1
            self.spiny *= -1

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
        if self.x < 1:
            return "Yellow"
        elif self.x + self.width > width:
            return "Red"

    def restart(self, width, height):
        self.x = width // 2
        self.y = random.randint(30, height - self.height - 2)
        self.spinx = 0
        self.spiny = 0
        vx = random.random() * 0.8 + 0.2
        vy = 1 - vx
        self.vx, self.vy = vx**0.5, vy**0.5
        self.vx *= random.randint(0, 1) * 2 - 1