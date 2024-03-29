from time import perf_counter
import pygame
import pong

class Menu():
    def __init__(self) -> None:
        self.screen_width = pong.WIDTH
        self.screen_height = pong.HEIGHT
        self.background_colour = pong.DARK_GREY
        self.box_colour = pong.MEDIUM_GREY
        self.setting_chosen = None

        self.title_text =                  Widget(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 7    , "Gaming X Pong", pong.WHITE, "comicsans", 40)
        self.singleplayer_button =         Button(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 7 * 2, lambda: pong.main(pong.red_bot_movement, self)        , "SINGLE PLAYER", pong.WHITE, self.box_colour, "comicsans", 40)
        self.multiplayer_button =          Button(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 7 * 3, lambda: pong.main(pong.red_player_movement, self)     , "MULTIPLAYER"  , pong.WHITE, self.box_colour, "comicsans", 40)
        self.settings_button =             Button(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 7 * 4, self.settings                                         , "SETTINGS"     , pong.WHITE, self.box_colour, "comicsans", 40)
        self.info_button =                 Button(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 7 * 5, self.info                                             , "INFO"         , pong.WHITE, self.box_colour, "comicsans", 40)
        self.quit_button =                 Button(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 7 * 6, pong.quit                                             , "QUIT"         , pong.WHITE, self.box_colour, "comicsans", 40)

        self.screen_width_button =  SettingButton(lambda: pong.WIDTH / 4    , lambda: pong.HEIGHT / 6    , lambda: self.chosen_setting(self.screen_width_button) , lambda: f"SCREEN WIDTH: {pong.WIDTH}"       , pong.WHITE, self.box_colour, "comicsans", 40)
        self.screen_height_button = SettingButton(lambda: pong.WIDTH / 4 * 3, lambda: pong.HEIGHT / 6    , lambda: self.chosen_setting(self.screen_height_button), lambda: f"SCREEN HEIGHT: {pong.HEIGHT}"     , pong.WHITE, self.box_colour, "comicsans", 40)
        self.speed_button =         SettingButton(lambda: pong.WIDTH / 4    , lambda: pong.HEIGHT / 6 * 2, lambda: self.chosen_setting(self.speed_button)        , lambda: f"SPEED: {pong.SPEED}"              , pong.WHITE, self.box_colour, "comicsans", 40)
        self.ball_size_button =     SettingButton(lambda: pong.WIDTH / 4 * 3, lambda: pong.HEIGHT / 6 * 2, lambda: self.chosen_setting(self.ball_size_button)    , lambda: f"BALL SIZE: {pong.BALL_WIDTH}"     , pong.WHITE, self.box_colour, "comicsans", 40)
        self.padel_width_button =   SettingButton(lambda: pong.WIDTH / 4    , lambda: pong.HEIGHT / 6 * 3, lambda: self.chosen_setting(self.padel_width_button)  , lambda: f"PADEL WIDTH: {pong.PADEL_WIDTH}"  , pong.WHITE, self.box_colour, "comicsans", 40)
        self.padel_height_button =  SettingButton(lambda: pong.WIDTH / 4 * 3, lambda: pong.HEIGHT / 6 * 3, lambda: self.chosen_setting(self.padel_height_button) , lambda: f"PADEL HEIGHT: {pong.PADEL_HEIGHT}", pong.WHITE, self.box_colour, "comicsans", 40)
        self.fullscreen_button =    SettingButton(lambda: pong.WIDTH / 4    , lambda: pong.HEIGHT / 6 * 4, self.change_fullscreen                                , lambda: f"FULL SCREEN: {pong.FULLSCREEN}"   , pong.WHITE, self.box_colour, "comicsans", 40)
        self.size_link_button =     SettingButton(lambda: pong.WIDTH / 4 * 3, lambda: pong.HEIGHT / 6 * 4, self.change_size_link                                 , lambda: f"SIZE LINK: {pong.SIZE_LINK}"      , pong.WHITE, self.box_colour, "comicsans", 40)
        self.num_powerups_button =  SettingButton(lambda: pong.WIDTH / 4    , lambda: pong.HEIGHT / 20   , lambda: self.chosen_setting(self.num_powerups_button)     , lambda: f"NUM POWERUPS: {pong.NUM_POWERUPS}", pong.WHITE, self.box_colour, "comicsans", 10)
        
        self.settings_dict = {
            self.screen_width_button:  self.change_screen_width,
            self.screen_height_button: self.change_screen_height,
            self.speed_button:         self.change_speed,
            self.ball_size_button:     self.change_ball_size,
            self.padel_width_button:   self.change_padel_width,
            self.padel_height_button:  self.change_padel_height,
            self.fullscreen_button:    self.change_fullscreen,
            self.size_link_button:     self.change_size_link,
            self.num_powerups_button:  self.change_num_powerups
        }

        for button in self.settings_dict:
            button.uniform_size(self.settings_dict)

        self.credit_title =   Widget(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 8    , "CREDITS"     , pong.WHITE, "comicsans", 40)
        self.credit_text =      Text(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 8 * 2, """
                                                                                          Rex Attwood
                                                                                          Freddie Weir
                                                                                          """ , pong.WHITE, "comicsans", 20)
        self.controls_title = Widget(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 8 * 3, "CONTROLS"     , pong.WHITE, "comicsans", 40)
        self.controls_text =    Text(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 8 * 4.7, """
                                                                                          RED PADDLE UP: W
                                                                                          RED PADDLE DOWN:S
                                                                                          YELLOW PADDLE UP: UP ARROW
                                                                                          YELLOW PADDLE DOWN: DOWN ARROW
                                                                                          CHANGE SETTINGS: UP AND DOWN ARROWS
                                                                                          PAUSE: ESC
                                                                                          """ , pong.WHITE, "comicsans", 20)

        self.info_widgets = [
            self.credit_title,
            self.credit_text,
            self.controls_title,
            self.controls_text
        ]

        self.back_to_menu_button = Button(lambda: pong.WIDTH / 2, lambda: pong.HEIGHT / 2, lambda: self.main_menu(), "MAIN MENU", pong.WHITE, self.box_colour, "comicsans", 40)

        self.text_widgets = [self.title_text]
        self.buttons = [self.singleplayer_button, self.multiplayer_button, self.settings_button, self.info_button, self.quit_button, self.num_powerups_button]
        self.all_widgets: list[Widget, Button, SettingButton] = self.text_widgets + self.info_widgets + self.buttons + [*self.settings_dict.keys()] + [self.back_to_menu_button]

    def mouse_click(self, mouse):
        for button in self.buttons:
            if button.clicked_on(mouse[0], mouse[1]):
                button.function()
                return True

    def draw_menu(self, colour=None):
        if colour:
            pong.WIN.fill(colour)
        for text_widget in self.text_widgets:
            text_widget.draw()
        for button in self.buttons:
            button.draw()
        pygame.display.update()

    def pause(self):
        self.buttons = [self.back_to_menu_button]
        self.draw_menu()

    def resize(self):
        pong.WIDTH, pong.HEIGHT = pygame.display.get_window_size()
        pong.update_screen_size()
        for widget in self.all_widgets:
            widget.resize_text()
            widget.update()
        for setting_button in self.settings_dict:
            setting_button.uniform_size(self.settings_dict)
        self.draw_menu(self.background_colour)

    def settings(self):
        self.back_to_menu_button.get_y = lambda: pong.HEIGHT / 6 * 5
        self.back_to_menu_button.update()
        self.text_widgets = []
        self.buttons = [*self.settings_dict.keys()] + [self.back_to_menu_button]
        self.draw_menu(self.background_colour)
        keys_down = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pong.quit()

                elif event.type == pygame.WINDOWSIZECHANGED:
                    self.resize()

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
                    for button in self.settings_dict:
                        button.uniform_size(self.settings_dict)
                    self.draw_menu(self.background_colour)

                if keys_pressed[pygame.K_DOWN]:
                    self.settings_dict[self.setting_chosen](-1)
                    self.setting_chosen.update_text()
                    for button in self.settings_dict:
                        button.uniform_size(self.settings_dict)
                    self.draw_menu(self.background_colour)

    def chosen_setting(self, setting: "SettingButton"):
        setting.outline = pong.LIGHT_GREY
        setting.draw()
        self.draw_menu()
        self.setting_chosen = setting

    def info(self):
        self.back_to_menu_button.get_y = lambda: pong.HEIGHT / 6 * 5
        self.back_to_menu_button.update()
        self.text_widgets = self.info_widgets
        self.buttons = [self.back_to_menu_button]
        self.draw_menu(self.background_colour)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pong.quit()

                elif event.type == pygame.WINDOWSIZECHANGED:
                    self.resize()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    self.mouse_click(mouse)

    def change_screen_width(self, change):
        pong.WIDTH = max(0, pong.WIDTH + change)
        for widget in self.all_widgets:
            widget.update()
        pong.update_screen_size()
        pygame.display.set_mode((pong.WIDTH, pong.HEIGHT), flags=pygame.RESIZABLE)
        pong.FULLSCREEN = False
        self.fullscreen_button.update_text()

    def change_screen_height(self, change):
        pong.HEIGHT = max(0, pong.HEIGHT + change)
        for widget in self.all_widgets:
            widget.update()
        pong.update_screen_size()
        pygame.display.set_mode((pong.WIDTH, pong.HEIGHT), flags=pygame.RESIZABLE)
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

    def change_num_powerups(self, change):
        pong.NUM_POWERUPS = max(0, pong.NUM_POWERUPS + change)

    def change_fullscreen(self, _=None):
        if pong.FULLSCREEN:
            pong.FULLSCREEN = False
            # Mouse moves when resizing, this keeps mouse in same relative position
            mouse_ratio = [i / j for i, j in list(zip(pygame.mouse.get_pos(), pygame.display.get_window_size()))]
            pygame.mouse.set_pos([i * j for i, j in list(zip(mouse_ratio, pong.WINDOW_SIZE))])
            pygame.display.set_mode(pong.WINDOW_SIZE, flags=pygame.RESIZABLE)
        else:
            pong.FULLSCREEN = True
            # Mouse moves when resizing, this keeps mouse in same relative position
            mouse_ratio = [i / j for i, j in list(zip(pygame.mouse.get_pos(), pygame.display.get_window_size()))]
            pygame.display.set_mode(flags=pygame.FULLSCREEN+pygame.RESIZABLE)
            pygame.mouse.set_pos([i * j for i, j in list(zip(mouse_ratio, pong.FULLSCREEN_SIZE))])
        self.fullscreen_button.outline = pong.LIGHT_GREY
        self.setting_chosen = self.fullscreen_button

    def change_size_link(self):
        if pong.SIZE_LINK:
            pong.SIZE_LINK = False
        else:
            pong.SIZE_LINK = True
        self.size_link_button.outline = pong.LIGHT_GREY
        self.setting_chosen = self.size_link_button
        self.size_link_button.update_text()
        for setting_button in self.settings_dict:
            setting_button.uniform_size(self.settings_dict)
        self.draw_menu(self.background_colour)

    def main_menu(self):
        self.back_to_menu_button.get_y = lambda: pong.HEIGHT / 2
        self.back_to_menu_button.update()
        self.text_widgets = [self.title_text]
        self.buttons = [self.singleplayer_button, self.multiplayer_button, self.settings_button, self.info_button, self.quit_button]
        self.draw_menu(self.background_colour)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pong.quit()

            elif event.type == pygame.VIDEORESIZE:
                self.resize()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                self.mouse_click(mouse)



class Widget():
    def __init__(self, get_x, get_y, text, text_colour, font, font_size) -> None:
        self.text = text
        self.text_colour = text_colour
        self.font = pygame.font.SysFont(font, font_size)
        self.font_type = font
        self.font_size = 900 / font_size
        self.label = self.font.render(text, True, text_colour)
        self.width = self.label.get_width()
        self.height = self.label.get_height()
        self.get_x = get_x
        self.get_y = get_y
        self.x = get_x() - self.width / 2
        self.y = get_y() - self.height / 2

    def update(self):
        self.x = self.get_x() - self.width / 2
        self.y = self.get_y() - self.height / 2

    def resize_text(self):
        self.font = pygame.font.SysFont(self.font_type, round(pong.WIDTH / self.font_size))
        self.label = self.font.render(self.text, True, self.text_colour)
        self.width = self.label.get_width()
        self.height = self.label.get_height()

    def draw(self):
        pong.WIN.blit(self.label, (round(self.x + (self.width - self.label.get_width()) / 2), round(self.y)))



class Text(Widget):
    def __init__(self, get_x, get_y, text: str, text_colour, font, font_size) -> None:
        super().__init__(get_x, get_y, text, text_colour, font, font_size)
        self.text = [sentence.lstrip() for sentence in text.split("\n")]
        self.labels = [self.font.render(sentence, True, text_colour) for sentence in self.text]

    def resize_text(self):
        self.font = pygame.font.SysFont(self.font_type, round(pong.WIDTH / self.font_size))
        self.labels = [self.font.render(sentence, True, self.text_colour) for sentence in self.text]
        self.width = max([label.get_width() for label in self.labels])
        self.height = sum([label.get_height() for label in self.labels])

    def draw(self):
        for idx, label in enumerate(self.labels):
            pong.WIN.blit(label, (round(self.x + (self.width - label.get_width()) / 2), round(self.y + idx * label.get_height())))



class Button(Widget):
    def __init__(self, get_x, get_y, function, text, text_colour, colour, font, font_size) -> None:
        self.function = function
        self.colour = colour
        self.outline = colour
        super().__init__(get_x, get_y, text, text_colour, font, font_size)

    def clicked_on(self, mouse_x, mouse_y):
        return (mouse_x > self.x
        and mouse_x < self.x + self.width
        and mouse_y > self.y
        and mouse_y < self.y + self.height)

    def draw(self):
        pygame.draw.rect(pong.WIN, self.colour, (round(self.x), round(self.y), self.width, self.height))
        pygame.draw.rect(pong.WIN, self.outline, (round(self.x), round(self.y), self.width, self.height), width=round(pong.WIDTH/300))
        pong.WIN.blit(self.label, (round(self.x + (self.width - self.label.get_width()) / 2), round(self.y)))



class SettingButton(Button):
    def __init__(self, x, y, function, text, text_colour, colour, font, font_size) -> None:
        self.get_text = text
        super().__init__(x, y, function, self.get_text(), text_colour, colour, font, font_size)

    def update_text(self):
        self.label = self.font.render(self.get_text(), True, self.text_colour)
        self.width = self.label.get_width()

    def resize_text(self):
        self.font = pygame.font.SysFont(self.font_type, round(pong.WIDTH / self.font_size))
        self.update_text()
        self.height = self.label.get_height()

    def uniform_size(self, settings_dict: dict["SettingButton"]):
        self.width = max(settings_dict, key=lambda button: button.width).width
        self.update()