import pygame
import pong

class Menu():
    def __init__(self) -> None:
        self.screen_width = pong.WIDTH
        self.screen_height = pong.HEIGHT
        self.background_colour = pong.DARK_GREY
        self.box_colour = pong.MEDIUM_GREY
        self.setting_chosen = None

        self.singleplayer_button = Button(self.screen_width / 2, self.screen_height / 4,  lambda: pong.main(pong.red_bot_movement, self), "SINGLE PLAYER", pong.WHITE, self.box_colour, "comicsans", 40)
        self.multiplayer_button = Button(self.screen_width / 2, self.screen_height / 2, lambda: pong.main(pong.red_player_movement, self), "MULTIPLAYER", pong.WHITE, self.box_colour, "comicsans", 40)
        
        self.settings_button = Button(self.screen_width / 2, 3 * self.screen_height / 4, self.settings, "SETTINGS", pong.WHITE, self.box_colour, "comicsans", 40)
        self.speed_button = Button(self.screen_width / 2, self.screen_height / 4, lambda: self.chosen_setting(self.speed_button), f"SPEED: {pong.SPEED}", pong.WHITE, self.box_colour, "comicsans", 40)
        self.settings_dict = {self.speed_button: self.changed_speed}

        self.back_to_menu_button = Button(self.screen_width / 2, self.screen_height / 2, lambda: self.main_menu(), "MAIN MENU", pong.WHITE, self.box_colour, "comicsans", 40)

        self.buttons = [self.singleplayer_button, self.multiplayer_button, self.settings_button]

    def mouse_click(self, mouse):
        for button in self.buttons:
            if button.clicked_on(mouse[0], mouse[1]):
                self.buttons = []
                button.function()

    def draw_menu(self, WIN: pygame.Surface, colour=None):
        if colour:
            WIN.fill(colour)
        for button in self.buttons:
            button.draw(WIN, self.box_colour)
        pygame.display.update()

    def pause(self):
        self.buttons = [self.back_to_menu_button]
        self.draw_menu(pong.WIN)

    def settings(self):
        self.buttons = [self.back_to_menu_button, self.speed_button]
        self.draw_menu(pong.WIN, self.background_colour)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    self.setting_chosen = None
                    self.mouse_click(mouse)

            if self.setting_chosen:
                keys_pressed = pygame.key.get_pressed()

                if keys_pressed[pygame.K_UP]:
                    self.settings_dict[self.setting_chosen](1)
                    self.speed_button.update_text(f"SPEED: {pong.SPEED}")
                    self.draw_menu(pong.WIN, self.background_colour)

                if keys_pressed[pygame.K_DOWN]:
                    self.settings_dict[self.setting_chosen](-1)
                    self.speed_button.update_text(f"SPEED: {pong.SPEED}")
                    self.draw_menu(pong.WIN, self.background_colour)

    def chosen_setting(self, setting):
        self.buttons = [self.back_to_menu_button, self.speed_button]
        self.setting_chosen = setting

    def changed_speed(self, change):
        pong.SPEED = max(0, pong.SPEED + change)
        pong.variable_speed = max(0, pong.variable_speed + change)

    def main_menu(self):
        self.buttons = [self.singleplayer_button, self.multiplayer_button, self.settings_button]
        self.draw_menu(pong.WIN, self.background_colour)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                self.mouse_click(mouse)



class Button():
    def __init__(self, x, y, function, text, text_colour, colour, font, font_size) -> None:
        self.function = function
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

    def update_text(self, text):
        self.label = self.font.render(text, True, self.text_colour)
        self.width = self.label.get_width()

    def draw(self, WIN: pygame.Surface, box_colour):
        pygame.draw.rect(WIN, box_colour, (self.x, self.y, self.width, self.height))
        WIN.blit(self.label, (self.x, self.y))