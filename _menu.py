import pygame
import pong

class Menu():
    def __init__(self) -> None:
        self.screen_width = pong.WIDTH
        self.screen_height = pong.HEIGHT
        self.background_colour = pong.DARK_GREY
        self.box_colour = pong.MEDIUM_GREY
        self.singleplayer_button = Button(self.screen_width / 2, 100, "SINGLE PLAYER", pong.WHITE, self.box_colour, "comicsans", 40)
        self.multiplayer_button = Button(self.screen_width / 2, 200, "MULTIPLAYER", pong.WHITE, self.box_colour, "comicsans", 40)

    def mouse_click(self, mouse):
        if self.singleplayer_button.clicked_on(mouse[0], mouse[1]):
            pong.main(pong.red_bot_movement)
        elif self.multiplayer_button.clicked_on(mouse[0], mouse[1]):
            pong.main(pong.red_player_movement)

    def draw_menu(self, WIN: pygame.Surface):
        WIN.fill(self.background_colour)
        self.singleplayer_button.draw(WIN, self.box_colour)
        self.multiplayer_button.draw(WIN, self.box_colour)
        pygame.display.update()



class Button():
    def __init__(self, x, y, text, text_colour, colour, font, font_size) -> None:
        self.text = text
        self.text_colour = text_colour
        self.colour = colour
        self.font = pygame.font.SysFont(font, font_size)
        self.label = self.font.render(text, True, text_colour)
        self.width = self.label.get_width()
        self.height = self.label.get_height()
        self.x = x - self.width / 2
        self.y = y - self.height / 2

    def clicked_on(self, mouse_x, mouse_y):
        return (mouse_x > self.x
        and mouse_x < self.x + self.width
        and mouse_y > self.y
        and mouse_y < self.y + self.height)

    def draw(self, WIN: pygame.Surface, box_colour):
        pygame.draw.rect(WIN, box_colour, (self.x, self.y, self.width, self.height))
        WIN.blit(self.label, (self.x, self.y))