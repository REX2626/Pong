import random
from enum import Enum
import pygame
import math


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

    def intersects_other_rect(self, other: "Rect") -> bool:
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

    def corners(self) -> "tuple(tuple(float, float))":
        return (self.top_l(), self.top_r(), self.bot_l(), self.bot_r())

    def width(self) -> "float":
        '''(can return negative numbers)'''
        return self.brx - self.tlx

    def height(self) -> "float":
        '''(can return negative numbers)'''
        return self.bry - self.tly

    def draw(self, window: "pygame.Surface", colour):
        pygame.draw.rect(window, colour, [self.tlx, self.tly, self.width(), self.height()])


def sub_points(point_a: "tuple(float, float)", point_b: "tuple(float, float)") -> "tuple(float, float)":
    return tuple(point_a[i] - point_b[i] for i in (0, 1))

def point_sqrlength(point: "tuple(float, float)"):
    return point[0]*point[0] + point[1]*point[1]

def point_min_abs_component(point: "tuple(float, float)"):
    return min(abs(point[i]) for i in (0, 1))

def sign(x):
    if x >= 0: return 1
    return -1


class Entity():
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class SquareEntity(Entity):
    def __init__(self, x, y, width, height) -> None:
        super().__init__(x, y)
        self.width = width
        self.height = height

    def rect(self) -> Rect:
        return Rect(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self, window, colour):
        self.rect().draw(window, colour)


class Padel(SquareEntity):
    def __init__(self, x, y, width, height) -> None:
        super().__init__(x, y, width, height)
        self.moving_down = False
        self.moving_up = False


class Ball(SquareEntity):
    def __init__(self, screen_width, screen_height, ball_width, ball_height, text_bar_height) -> None:
        super().__init__(0, 0, ball_width, ball_height)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.text_bar_height = text_bar_height
        self.restart()

    def move(self, speed):
        self.x += (self.vx + self.spinx) * speed
        self.y += (self.vy + self.spiny) * speed

        if self.spinx > 0:
            self.spinx -= min(self.spinx, speed / self.screen_width)
        elif self.spinx < 0:
            self.spinx += min(-self.spinx, speed / self.screen_width)

        if self.spiny > 0:
            self.spiny -= min(self.spiny, 2 * speed / self.screen_width)
        elif self.spiny < 0:
            self.spiny += min(-self.spiny, 2 * speed / self.screen_width)

    def handle_paddle_collisions(self, padel: Padel, spin: bool):
        sr = self.rect()
        pr = padel.rect()
        collides_with_padel = sr.intersects_other_rect(pr) # check we do have a collision
        if not collides_with_padel: return

        # this finds the vector from a corner of the paddle to
        # the corner of the ball, with the smallest length of
        # it's minimum component i.e. the one which enforces the
        # smallest change on the ball's position in order to
        # resolve the collision
        intersection_vector = (math.inf, math.inf)
        for self_corner in self.rect().corners():
            for other_corner in padel.rect().corners():
                potential_new_intersection_vector = sub_points(self_corner, other_corner)
                if point_min_abs_component(potential_new_intersection_vector) < point_min_abs_component(intersection_vector):
                    intersection_vector = potential_new_intersection_vector


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
            if not self.ball_has_hit_side and (padel.moving_down or padel.moving_up): # make sure only increasing vy once, otherwise vy could increase exponentially
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

    def collides_with_paddle_check(self, padel: Padel):
        return self.rect().intersects_other_rect(padel.rect())        

    def scored(self):
        if self.x + self.width < 1:
            return GameEventType.YELLOW
        elif self.x > self.screen_width:
            return GameEventType.RED

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


class PowerupEffect:
    pass


class BallPowerupEffect(PowerupEffect):
    def __init__(self, ball_effect_func) -> None:
        self.ball_effect_func = ball_effect_func


class PowerupType:
    def __init__(self, name: str, image_path: str, *, weight: int, powerup_effect: PowerupEffect, width: float=50, height: float=50) -> None:
        self.name = name
        self.image_path = image_path
        self.weight = weight
        self.width = width
        self.height = height
        self.powerup_effect = powerup_effect

class Powerup(SquareEntity):
    POWERUP_TYPES = (
        PowerupType("test",        "./assets/test_powerup.png",   weight= 0, powerup_effect=PowerupEffect()),
        PowerupType("speed_small", "./assets/speed_powerup1.png", weight=50, powerup_effect=BallPowerupEffect(
            lambda ball: (
                setattr(ball, "vx", ball.vx*1.5),
                setattr(ball, "vy", ball.vy*1.5),
                setattr(ball, "spinx", ball.spinx*1.5),
                setattr(ball, "spiny", ball.spiny*1.5)
            )
        )),
        PowerupType("speed_big",   "./assets/speed_powerup2.png", weight=30, powerup_effect=BallPowerupEffect(
            lambda ball: (
                setattr(ball, "vx", ball.vx*2),
                setattr(ball, "vy", ball.vy*2),
                setattr(ball, "spinx", ball.spinx*2),
                setattr(ball, "spiny", ball.spiny*2)
            )
        ))
    )

    def __init__(self, x, y, powerup_type: PowerupType) -> None:
        super().__init__(x, y, powerup_type.width, powerup_type.height)
        self.powerup_type = powerup_type

    @classmethod
    def random_powerup_type(cls) -> PowerupType:
        '''Returns a random `PowerupType` object, where types with a higher `weight` are more likely to be picked'''
        return random.choices(
            population=cls.POWERUP_TYPES,
            weights=tuple(pt.weight for pt in cls.POWERUP_TYPES),
            k=1 # k = the number of things to be chosen
        )[0] # indexed at 0 because this returns a list, but it is only 1 element as k=1

    @classmethod
    def create_random(cls, min_x, max_x, min_y, max_y) -> "Powerup":
        powerup_type = cls.random_powerup_type()

        min_x, max_x, min_y, max_y, width, height = (int(x) for x in (min_x, max_x, min_y, max_y, powerup_type.width, powerup_type.height))
        if max_x - min_x - width  < 0: raise ValueError(f"No area to place powerup of width {width} when min_x is {min_x} and max_x is {max_x}")
        if max_y - min_y - height < 0: raise ValueError(f"No area to place powerup of height {height} when min_y is {min_y} and max_y is {max_y}")

        return Powerup(
            x=random.randrange(min_x, max_x - width),
            y=random.randrange(min_y, max_y - height),
            powerup_type=powerup_type
        )

    def handle_collisions(self, ball: Ball) -> "bool":
        if not self.rect().intersects_other_rect(ball.rect()): return False

        # TODO: do cool stuff e.g. increase ball speed etc

        return True

    def draw(self, window: "pygame.Surface"):
        if not hasattr(self, "image"):
            self.image = pygame.image.load(self.powerup_type.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        window.blit(self.image, [self.x, self.y])
