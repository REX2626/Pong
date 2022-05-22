import pygame
import pong
import sys

class Menu():
    def __init__(self) -> None:
        self.screen_width = pong.WIDTH
        self.screen_height = pong.HEIGHT
        self.background_colour = pong.DARK_GREY
        self.box_colour = pong.MEDIUM_GREY
        self.setting_chosen = None

        self.singleplayer_button = Button(self.screen_width / 2, self.screen_height / 4,  lambda: pong.main(pong.red_bot_movement, self), "SINGLE PLAYER", pong.WHITE, self.box_colour, "comicsans", 40)
        self.multiplayer_button = Button(self.screen_width / 2, self.screen_height / 2, lambda: pong.main(pong.red_player_movement, self), "MULTIPLAYER", pong.WHITE, self.box_colour, "comicsans", 40)
        
        self.settings_button = Button(self.screen_width / 2, self.screen_height * 3 / 4, self.settings, "SETTINGS", pong.WHITE, self.box_colour, "comicsans", 40)
        self.speed_button = SettingButton(self.screen_width / 2, self.screen_height / 4, lambda: self.chosen_setting(self.speed_button), lambda: f"SPEED: {pong.SPEED}", pong.WHITE, self.box_colour, "comicsans", 40)
        self.ball_size_button = SettingButton(self.screen_width / 2, self.screen_height / 2, lambda: self.chosen_setting(self.ball_size_button), lambda: f"BALL SIZE: {pong.BALL_WIDTH}", pong.WHITE, self.box_colour, "comicsans", 40)
        self.settings_dict = {self.speed_button: self.change_speed, self.ball_size_button: self.change_ball_size}

        self.back_to_menu_button = Button(self.screen_width / 2, self.screen_height / 2, lambda: self.main_menu(), "MAIN MENU", pong.WHITE, self.box_colour, "comicsans", 40)

        self.buttons = [self.singleplayer_button, self.multiplayer_button, self.settings_button]

    def mouse_click(self, mouse):
        for button in self.buttons:
            if button.clicked_on(mouse[0], mouse[1]):
                self.buttons = []
                button.function()

    def draw_menu(self, colour=None):
        if colour:
            pong.WIN.fill(colour)
        for button in self.buttons:
            button.draw()
        pygame.display.update()

    def pause(self):
        self.buttons = [self.back_to_menu_button]
        self.draw_menu()

    def settings(self):
        self.back_to_menu_button.y = self.screen_height * 3 / 4
        self.buttons = [self.back_to_menu_button, self.speed_button, self.ball_size_button]
        self.draw_menu(self.background_colour)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.setting_chosen:
                        self.setting_chosen.outline = self.box_colour
                        self.setting_chosen.draw()
                        self.draw_menu()
                        self.setting_chosen = None
                    self.mouse_click(mouse)

            if self.setting_chosen:
                keys_pressed = pygame.key.get_pressed()

                if keys_pressed[pygame.K_UP]:
                    self.settings_dict[self.setting_chosen](1)
                    self.setting_chosen.update_text()
                    self.draw_menu(self.background_colour)

                if keys_pressed[pygame.K_DOWN]:
                    self.settings_dict[self.setting_chosen](-1)
                    self.setting_chosen.update_text()
                    self.draw_menu(self.background_colour)

    def chosen_setting(self, setting):
        self.buttons = [self.back_to_menu_button, self.speed_button, self.ball_size_button]
        setting.outline = pong.LIGHT_GREY
        setting.draw()
        self.draw_menu()
        self.setting_chosen = setting

    def change_speed(self, change):
        pong.SPEED = max(0, pong.SPEED + change)
        pong.variable_speed = max(0, pong.variable_speed + change)

    def change_ball_size(self, change):
        pong.BALL_HEIGHT = max(0, pong.BALL_HEIGHT + change)
        pong.BALL_WIDTH = max(0, pong.BALL_WIDTH + change)

    def main_menu(self):
        self.buttons = [self.singleplayer_button, self.multiplayer_button, self.settings_button]
        self.draw_menu(self.background_colour)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                self.mouse_click(mouse)



class Button():
    def __init__(self, x, y, function, text, text_colour, colour, font, font_size) -> None:
        self.function = function
        self.text_colour = text_colour
        self.colour = colour
        self.outline = colour
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

    def draw(self):
        pygame.draw.rect(pong.WIN, self.colour, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(pong.WIN, self.outline, (self.x, self.y, self.width, self.height), width=3)
        pong.WIN.blit(self.label, (self.x, self.y))



class SettingButton(Button):
    def __init__(self, x, y, function, text, text_colour, colour, font, font_size) -> None:
        self.get_text = text
        super().__init__(x, y, function, self.get_text(), text_colour, colour, font, font_size)

    def update_text(self):
        self.label = self.font.render(self.get_text(), True, self.text_colour)
        self.width = self.label.get_width()