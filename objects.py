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
        self.side_hit = False
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

    def move_out_collision(self, multiplier):
        self.x += self.vx * multiplier
        self.y += self.vy * multiplier

    def move_out_collision_spin(self, multiplier, screen_width):
        self.x += (self.vx + self.spinx) * multiplier
        self.y += (self.vy + self.spiny) * multiplier
        if self.spinx != 0:
            if self.spinx > 0:
                self.spinx -= min(self.spinx, multiplier / screen_width)
            elif self.spinx < 0:
                self.spinx += min(-self.spinx, multiplier / screen_width)
        if self.spiny != 0:
            if self.spiny > 0:
                self.spiny -= min(self.spiny, multiplier / screen_width)
            elif self.spiny < 0:
                self.spiny += min(-self.spiny, multiplier / screen_width)

    def collision_red(self, padel: Padel, spin, speed, screen_width):
        if padel.moving_down:
            self.y += speed
        if padel.moving_up:
            self.y -= speed
        x, y = self.x, self.y

        if padel.x + padel.width - x > padel.y + padel.height - y and y >= padel.y + padel.height / 2: # Top left ball to bottom right padel
            multiplier = (padel.y + padel.height - y) / self.vy
            multiplier = min(1, multiplier)
            self.move_out_collision(-multiplier)
            self.vy = abs(self.vy)
            if not self.side_hit and padel.moving_down:
                self.vy -= 1
                self.side_hit = True
            self.move_out_collision(speed + multiplier)

        if padel.x + padel.width - x > y + self.height - padel.y and y < padel.y + padel.height / 2: # Bottom left ball to top right padel
            multiplier = (y + self.height - padel.y) / self.vy
            multiplier = max(-1, multiplier)
            self.move_out_collision(multiplier)
            self.vy = -abs(self.vy)
            if not self.side_hit and padel.moving_up:
                self.vy += 1
                self.side_hit = True
            self.move_out_collision(speed + multiplier)

        if (x, y) == (self.x, self.y):
            dist_to_centre = (y + self.height / 2) - (padel.y + padel.height / 2) # Distance from center of ball to centre of padel
            multiplier = (padel.x + padel.width - x) / self.vx
            self.move_out_collision(multiplier)
            self.vy = dist_to_centre / padel.height
            self.vx = (1 - self.vy**2)**0.5
            if spin:
                if padel.moving_up:
                    self.spiny += 1
                    self.spinx += 0.5
                elif padel.moving_down:
                    self.spiny -= 1
                    self.spinx += 0.5
            self.move_out_collision_spin(speed + multiplier, screen_width)

    def collision_yellow(self, padel: Padel, spin, speed, screen_width, variable_speed):
        if padel.moving_down:
            self.y += speed
        if padel.moving_up:
            self.y -= speed
        x, y = self.x, self.y

        if x + self.width - padel.x > padel.y + padel.height - y and y >= padel.y + padel.height / 2: # Top right ball to bottom left padel
            multiplier = (padel.y + padel.height - y) / self.vy
            multiplier = min(1, multiplier)
            self.move_out_collision(-multiplier)
            self.vy = abs(self.vy)
            if not self.side_hit and padel.moving_down:
                self.vy -= 1
                self.side_hit = True
            self.move_out_collision(speed + multiplier)

        if x + self.width - padel.x > y + self.height - padel.y and y < padel.y + padel.height / 2: # Bottom right ball to top left padel
            multiplier = (y + self.height - padel.y) / self.vy
            multiplier = max(-1, multiplier)
            self.move_out_collision(-multiplier)
            self.vy = -abs(self.vy)
            if not self.side_hit and padel.moving_up:
                self.vy += 1
                self.side_hit = True
            self.move_out_collision(speed + multiplier)

        if (x, y) == (self.x, self.y):
            dist_to_centre = (y + self.height / 2) - (padel.y + padel.height / 2) # Distance from center of ball to centre of padel
            multiplier = (x + self.width - padel.x) / self.vx
            self.move_out_collision(multiplier)
            self.vy = dist_to_centre / padel.height
            self.vx = -(1 - self.vy**2)**0.5
            if spin:
                if padel.moving_up:
                    self.spiny += 1
                    self.spinx -= 0.5
                elif padel.moving_down:
                    self.spiny -= 1
                    self.spinx -= 0.5
            self.move_out_collision_spin(speed + multiplier, screen_width)

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
        self.side_hit = False
        vx = random.random() * 0.8 + 0.2
        vy = 1 - vx
        self.vx, self.vy = vx**0.5, vy**0.5
        self.vx *= random.randint(0, 1) * 2 - 1