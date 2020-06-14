from sounds import *
from effects import *
from parameters import display


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_clr = (13, 162, 58)
        self.active_clr = (23, 204, 58)
        self.draw_ef = False
        self.clear_ef = False
        self.rect_h = 10
        self.rect_w = width

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
                else:
                    return True

        self.draw_b_rect(mouse[0], mouse[1], x, y)
        print_text(message=message, x=x + 10, y=y + 10, front_size=font_size)

    def draw_b_rect(self, ms_x, ms_y, x, y):
        if x <= ms_x <= x + self.width and y <= ms_y <= y + self.height:
            self.draw_ef = True

        if self.draw_ef:
            if ms_x < x or ms_x > x + self.width or ms_y < y or ms_y > y + self.height:
                self.clear_ef = True
                self.draw_ef = False

            if self.rect_h < self.height:
                self.rect_h += (self.height - 10) / 40

        if self.clear_ef and not self.draw_ef:
            if self.rect_h > 10:
                self.rect_h -= (self.height - 10) / 40
            if self.clear_ef and not self.draw_ef:
                if self.rect_h < 10:
                    self.rect_h -= (self.height - 10) / 40
                else:
                    self.clear_ef = True

        draw_y = y + self.height - self.rect_h
        pygame.draw.rect(display, self.active_clr, (x, draw_y, self.rect_w, self.rect_h))