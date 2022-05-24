import random
from enum import Enum

class GameEventType(Enum):
    NONE = 0
    RALLY = 1
    RED = 2
    YELLOW = 3


class Rect():
    def __init__(self, tlx, tly, brx, bry) -> None: #tlx = top left x etc
        self.tlx = tlx
        self.tly = tly
        self.brx = brx
        self.bry = bry

    def intersects_other_rect(self, other: "Rect") -> "bool":
        if self.tlx > other.brx: return False # to the right
        if self.brx < other.tlx: return False # to the left
        if self.tly > other.bry: return False # below
        if self.bry < other.tly: return False # above
        return True

    def top_l(self) -> "tuple(float, float)":
        return (self.tlx, self.tly)

    def top_r(self) -> "tuple(float, float)":
        return (self.brx, self.tly)

    def bot_l(self) -> "tuple(float, float)":
        return (self.tlx, self.bry)

    def bot_r(self) -> "tuple(float, float)":
        return (self.brx, self.bry)


def add_points(point_a: "tuple(float, float)", point_b: "tuple(float, float)") -> "tuple(float, float)":
    return tuple(point_a[i] + point_b[i] for i in (0, 1))

def sub_points(point_a: "tuple(float, float)", point_b: "tuple(float, float)") -> "tuple(float, float)":
    return tuple(point_a[i] - point_b[i] for i in (0, 1))

def sign(x):
    if x >= 0: return 1
    return -1


class Padel():
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.moving_down = False
        self.moving_up = False

    def rect(self) -> "Rect":
        return Rect(self.x, self.y, self.x + self.width, self.y + self.height)


class Ball():
    def __init__(self, width, height, ball_width, ball_height, text_bar_height) -> None:
        self.screen_width = width
        self.screen_height = height
        self.width = ball_width
        self.height = ball_height
        self.text_bar_height = text_bar_height
        self.restart()

    def move(self, speed):
        self.x += (self.vx + self.spinx) * speed
        self.y += (self.vy + self.spiny) * speed
        if self.spinx != 0:
            if self.spinx > 0:
                self.spinx -= min(self.spinx, speed / self.screen_width / 2)
            elif self.spinx < 0:
                self.spinx += min(-self.spinx, speed / self.screen_width / 2)
        if self.spiny != 0:
            if self.spiny > 0:
                self.spiny -= min(self.spiny, speed / self.screen_width / 2)
            elif self.spiny < 0:
                self.spiny += min(-self.spiny, speed / self.screen_width / 2)

    def handle_paddle_collisions(self, padel: Padel, spin: "bool"):
        sr = self.rect()
        pr = padel.rect()
        collides_with_padel = sr.intersects_other_rect(pr) # check we do have a collision
        if not collides_with_padel: return

        # this is the vector from the corner of the paddle to the corner of the ball at the intersection
        intersection_vector = min(
            sub_points(sr.bot_r(), pr.top_l()),
            sub_points(sr.bot_l(), pr.top_r()),
            sub_points(sr.top_r(), pr.bot_l()),
            sub_points(sr.top_l(), pr.bot_r()),
        key=lambda vector: vector[0]*vector[0] + vector[1]*vector[1]) # (pick vector with smallest magnitude)

        if abs(intersection_vector[0]) < abs(intersection_vector[1]): # horizontal bounce
            dist_to_centre = (self.y + self.height / 2) - (padel.y + padel.height / 2) # Distance from center of ball to centre of padel
            self.vy = dist_to_centre / padel.height # move vertically more quickly when close to edges of paddle
            self.vx = max(1 - self.vy**2, 0.1)**0.5 * -sign(self.vx) # set vx such that the total vel is 1 and so that it is in the right direction
            # shift to the inverse of the intersection vector to escape collision
            self.x -= intersection_vector[0]
            # handle spin
            if spin:
                if padel.moving_up:
                    self.spiny += 1
                    self.spinx += 0.5*sign(self.vx)
                elif padel.moving_down:
                    self.spiny -= 1
                    self.spinx += 0.5*sign(self.vx)

        else: # "side" (vertical) bounce
            self.vy *= -1 # invert y vel
            if not self.ball_has_hit_side: # make sure only increasing vy once, otherwise vy could increase exponentially
                self.vy *= 2 # multiply by 2 to make the effect more visible
                self.ball_has_hit_side = True
            self.spiny = 0 # to avoid bouncing back into the paddle
            # shift to the inverse of the intersection vector to escape collision
            self.y -= intersection_vector[1]

    def boundary_collision(self):
        if self.y < self.text_bar_height + 2:
            self.vy *= -1
            self.spiny *= -1
            delta = self.y - (self.text_bar_height + 2)
            self.y -= delta
        elif self.y + self.height > self.screen_height - 2:
            self.vy *= -1
            self.spiny *= -1
            delta = (self.y + self.height) - (self.screen_height - 2)
            self.y -= delta

    def collides_with_paddle_test(self, padel: Padel):
        return self.rect().intersects_other_rect(padel.rect())        

    def scored(self):
        if self.x + self.width < 1:
            return GameEventType.YELLOW
        elif self.x > self.screen_width:
            return GameEventType.RED
    
    def rect(self) -> "Rect":
        return Rect(self.x, self.y, self.x + self.width, self.y + self.height)

    def restart(self):
        self.x = self.screen_width / 2 - self.width / 2
        self.y = random.randint(self.text_bar_height + 2, self.screen_height - self.height - 2)
        self.spinx = 0
        self.spiny = 0
        vx = random.random() * 0.8 + 0.2
        vy = 1 - vx
        self.vx, self.vy = vx**0.5, vy**0.5
        self.vx *= random.randint(0, 1) * 2 - 1
        self.ball_has_hit_side = False