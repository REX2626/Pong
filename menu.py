import pygame

class Menu():
    def __init__(self, height, width, text_colour) -> None:
        self.screen_height = height
        self.screen_width = width
        title_font = pygame.font.SysFont("comicsans", 40)
        self.title_label = title_font.render("START", True, text_colour)
        self.start_x = self.screen_width / 2 - self.title_label.get_width() / 2
        self.start_y = 100
        self.start_width = self.title_label.get_width()
        self.start_height = self.title_label.get_height()

    def draw_menu(self, WIN: pygame.Surface, background_colour, box_colour):
        WIN.fill(background_colour)
        pygame.draw.rect(WIN, box_colour, [self.start_x, self.start_y, self.start_width, self.start_height])
        WIN.blit(self.title_label, (self.start_x, self.start_y))
        pygame.display.update()

    def clicked_on_start(self, mouse):
        return (mouse[0] > self.start_x
        and mouse[0] < self.start_x + self.start_width
        and mouse[1] > self.start_y
        and mouse[1] < self.start_y + self.start_height)