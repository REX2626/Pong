from time import perf_counter
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

        self.singleplayer_button =         Button(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 5    , lambda: pong.main(pong.red_bot_movement, self)        , "SINGLE PLAYER", pong.WHITE, self.box_colour, "comicsans", 40)
        self.multiplayer_button =          Button(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT * 2 / 5, lambda: pong.main(pong.red_player_movement, self)     , "MULTIPLAYER"  , pong.WHITE, self.box_colour, "comicsans", 40)
        self.settings_button =             Button(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT * 3 / 5, self.settings                                         , "SETTINGS"     , pong.WHITE, self.box_colour, "comicsans", 40)
        self.quit_button =                 Button(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT * 4 / 5, self.quit                                             , "QUIT"         , pong.WHITE, self.box_colour, "comicsans", 40)

        self.screen_width_button =  SettingButton(lambda: pong.WIDTH / 4    , lambda: pong.HEIGHT / 6    , lambda: self.chosen_setting(self.screen_width_button) , lambda: f"SCREEN WIDTH: {pong.WIDTH}"       , pong.WHITE, self.box_colour, "comicsans", 40)
        self.screen_height_button = SettingButton(lambda: pong.WIDTH / 4 * 3, lambda: pong.HEIGHT / 6    , lambda: self.chosen_setting(self.screen_height_button), lambda: f"SCREEN HEIGHT: {pong.HEIGHT}"     , pong.WHITE, self.box_colour, "comicsans", 40)
        self.speed_button =         SettingButton(lambda: pong.WIDTH / 4    , lambda: pong.HEIGHT / 6 * 2, lambda: self.chosen_setting(self.speed_button)        , lambda: f"SPEED: {pong.SPEED}"              , pong.WHITE, self.box_colour, "comicsans", 40)
        self.ball_size_button =     SettingButton(lambda: pong.WIDTH / 4 * 3, lambda: pong.HEIGHT / 6 * 2, lambda: self.chosen_setting(self.ball_size_button)    , lambda: f"BALL SIZE: {pong.BALL_WIDTH}"     , pong.WHITE, self.box_colour, "comicsans", 40)
        self.padel_width_button =   SettingButton(lambda: pong.WIDTH / 4    , lambda: pong.HEIGHT / 6 * 3, lambda: self.chosen_setting(self.padel_width_button)  , lambda: f"PADEL WIDTH: {pong.PADEL_WIDTH}"  , pong.WHITE, self.box_colour, "comicsans", 40)
        self.padel_height_button =  SettingButton(lambda: pong.WIDTH / 4 * 3, lambda: pong.HEIGHT / 6 * 3, lambda: self.chosen_setting(self.padel_height_button) , lambda: f"PADEL HEIGHT: {pong.PADEL_HEIGHT}", pong.WHITE, self.box_colour, "comicsans", 40)
        self.fullscreen_button =    SettingButton(lambda: pong.WIDTH / 2,     lambda: pong.HEIGHT / 6 * 4, lambda: self.chosen_setting(self.fullscreen_button)   , lambda: f"FULL SCREEN: {pong.FULLSCREEN}"   , pong.WHITE, self.box_colour, "comicsans", 40)

        self.settings_dict = {
            self.screen_width_button:  self.change_screen_width,
            self.screen_height_button: self.change_screen_height,
            self.speed_button:         self.change_speed,
            self.ball_size_button:     self.change_ball_size,
            self.padel_width_button:   self.change_padel_width,
            self.padel_height_button:  self.change_padel_height,
            self.fullscreen_button:    self.change_fullscreen
        }

        self.back_to_menu_button = Button(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 2, lambda: self.main_menu(), "MAIN MENU", pong.WHITE, self.box_colour, "comicsans", 40)

        self.buttons = [self.singleplayer_button, self.multiplayer_button, self.settings_button, self.quit_button]
        self.all_buttons = [*self.settings_dict.keys()] + self.buttons + [self.back_to_menu_button]

    def mouse_click(self, mouse):
        for button in self.buttons:
            if button.clicked_on(mouse[0], mouse[1]):
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

    def quit(self):
        pygame.quit()
        sys.exit()

    def settings(self):
        self.back_to_menu_button.get_y = lambda: pong.HEIGHT / 6 * 5
        self.back_to_menu_button.update()
        self.buttons = [*self.settings_dict.keys()] + [self.back_to_menu_button]
        self.draw_menu(self.background_colour)
        keys_down = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.setting_chosen:
                        self.setting_chosen.outline = self.box_colour
                        self.setting_chosen.draw()
                        self.draw_menu()
                        self.setting_chosen = None
                    self.mouse_click(mouse)

                elif event.type == pygame.KEYDOWN and event.__dict__["key"] == pygame.K_ESCAPE:
                    if self.setting_chosen:
                        self.setting_chosen.outline = self.box_colour
                        self.setting_chosen = None
                    self.main_menu()

            if self.setting_chosen:
                keys_pressed = pygame.key.get_pressed()

                if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_DOWN]:
                    if not keys_down:
                        keys_down = True
                        key_interval = 0.5
                        next_time = perf_counter() + key_interval
                    else:
                        if perf_counter() < next_time:
                            continue
                        key_interval *= (1 - key_interval)
                        next_time = perf_counter() + key_interval
                else:
                    keys_down = False

                if keys_pressed[pygame.K_UP]:
                    self.settings_dict[self.setting_chosen](+1)
                    self.setting_chosen.update_text()
                    self.draw_menu(self.background_colour)

                if keys_pressed[pygame.K_DOWN]:
                    self.settings_dict[self.setting_chosen](-1)
                    self.setting_chosen.update_text()
                    self.draw_menu(self.background_colour)

    def chosen_setting(self, setting):
        setting.outline = pong.LIGHT_GREY
        setting.draw()
        self.draw_menu()
        self.setting_chosen = setting

    def change_screen_width(self, change):
        pong.WIDTH = max(0, pong.WIDTH + change)
        for button in self.all_buttons:
            button.update()
        pong.update_screen_size()
        pygame.display.set_mode((pong.WIDTH, pong.HEIGHT))
        pong.FULLSCREEN = False
        self.fullscreen_button.update_text()

    def change_screen_height(self, change):
        pong.HEIGHT = max(0, pong.HEIGHT + change)
        for button in self.all_buttons:
            button.update()
        pong.update_screen_size()
        pygame.display.set_mode((pong.WIDTH, pong.HEIGHT))
        pong.FULLSCREEN = False
        self.fullscreen_button.update_text()

    def change_speed(self, change):
        pong.SPEED = max(0, pong.SPEED + change)
        pong.variable_speed = max(0, pong.variable_speed + change)

    def change_ball_size(self, change):
        pong.BALL_HEIGHT = max(0, min(min(pong.WIDTH - 2 * (pong.PADEL_SIDE_INDENT + pong.PADEL_WIDTH), pong.HEIGHT - pong.TEXT_BAR_HEIGHT - 4), pong.BALL_HEIGHT + change))
        pong.BALL_WIDTH = max(0, min(min(pong.WIDTH - 2 * (pong.PADEL_SIDE_INDENT + pong.PADEL_WIDTH), pong.HEIGHT - pong.TEXT_BAR_HEIGHT - 4), pong.BALL_WIDTH + change))

    def change_padel_width(self, change):
        pong.PADEL_WIDTH = max(0, min(pong.WIDTH - pong.PADEL_SIDE_INDENT * 2, pong.PADEL_WIDTH + change))
        pong.YELLOW_PADEL_X = pong.WIDTH - pong.PADEL_SIDE_INDENT - pong.PADEL_WIDTH

    def change_padel_height(self, change):
        pong.PADEL_HEIGHT = max(0, min(pong.HEIGHT - pong.TEXT_BAR_HEIGHT - 2 * pong.PADEL_INDENT, pong.PADEL_HEIGHT + change))

    def change_fullscreen(self, _):
        if pong.FULLSCREEN:
            pong.FULLSCREEN = False
            pygame.display.set_mode((900, 500))
            pong.WIDTH, pong.HEIGHT = 900, 500
            for button in self.all_buttons:
                button.update()
            pong.update_screen_size()
        else:
            pong.FULLSCREEN = True
            pygame.display.set_mode(flags=pygame.FULLSCREEN)
            pong.WIDTH, pong.HEIGHT = pong.WIN.get_size()
            for button in self.all_buttons:
                button.update()
            pong.update_screen_size()
        self.screen_width_button.update_text()
        self.screen_height_button.update_text()

    def main_menu(self):
        self.back_to_menu_button.get_y = lambda: pong.HEIGHT / 2
        self.back_to_menu_button.update()
        self.buttons = [self.singleplayer_button, self.multiplayer_button, self.settings_button, self.quit_button]
        self.draw_menu(self.background_colour)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                self.mouse_click(mouse)



class Button():
    def __init__(self, get_x, get_y, function, text, text_colour, colour, font, font_size) -> None:
        self.function = function
        self.text_colour = text_colour
        self.colour = colour
        self.outline = colour
        self.font = pygame.font.SysFont(font, font_size)
        self.label = self.font.render(text, True, text_colour)
        self.width = self.label.get_width()
        self.height = self.label.get_height()
        self.get_x = get_x
        self.get_y = get_y
        self.x = get_x() - self.width / 2
        self.y = get_y() - self.height / 2

    def clicked_on(self, mouse_x, mouse_y):
        return (mouse_x > self.x
        and mouse_x < self.x + self.width
        and mouse_y > self.y
        and mouse_y < self.y + self.height)

    def update(self):
        self.x = self.get_x() - self.width / 2
        self.y = self.get_y() - self.height / 2

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