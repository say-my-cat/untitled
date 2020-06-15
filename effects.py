import pygame
import parameters as p

need_input = False
input_text = '|'
in_tic = 30


def print_text(message, x, y, front_color=(255, 234, 167), front_type='fon/PingPong.ttf', front_size=30):
    front_type = pygame.font.Font(front_type, front_size)
    text = front_type.render(message, True, front_color)
    p.display.blit(text, (x, y))


def get_input():
    global need_input, input_text, in_tic

    in_rect = pygame.Rect(20, 400, 250, 50)  # x, y, w, h

    pygame.draw.rect(p.display, (0, 255, 0), in_rect)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if in_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
        need_input = True

    if need_input:
        for event in pygame.event.get():
            if need_input and event.type == pygame.KEYDOWN:
                input_text = input_text.replace('|', '')
                in_tic = 30

                if event.key == pygame.K_RETURN:
                    need_input = False
                    message = input_text
                    input_text = ''
                    return message
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 10:
                        input_text += event.unicode

                input_text += '|'

    if len(input_text):
        print_text(message=input_text, x=in_rect.x + 10, y=in_rect.y + 10, front_size=35)

    in_tic -= 1

    if in_tic == 0:
        input_text = input_text[:-1]
    if in_tic == -30:
        input_text += '|'
        in_tic = 30
        
    return None
