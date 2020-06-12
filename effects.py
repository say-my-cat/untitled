import pygame
import parameters as p
from images import light_img


def print_text(message, x, y, front_color = (0, 0, 0), front_type='fon/PingPong.ttf', front_size=30):
    front_type = pygame.font.Font(front_type, front_size)
    text = front_type.render(message, True, front_color)
    p.display.blit(text, (x, y))
