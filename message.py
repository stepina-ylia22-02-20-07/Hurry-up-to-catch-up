from main import *


def show_message(screen, message):
    font = pygame.font.Font("data/Gantauluauope.ttf", 50)

    text = font.render(message, 1, (50, 70, 0))

    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 - 50 - text.get_height() // 2

    text_w = text.get_width()
    text_h = text.get_height()

    pygame.draw.rect(screen, pygame.Color('paleturquoise'), (text_x - 10, text_y - 10,
                                                             text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def show_message_result_win(screen, message):
    font = pygame.font.Font(None, 40)

    text = font.render(message, 1, (50, 70, 0))

    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 + 40 - text.get_height() // 2

    text_w = text.get_width()
    text_h = text.get_height()

    pygame.draw.rect(screen, pygame.Color('paleturquoise'), (text_x - 10, text_y - 10,
                                                             text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def show_message_result_lose(screen, message):
    font = pygame.font.Font(None, 40)
    text = font.render(message, 1, (50, 70, 0))

    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 + 95 - text.get_height() // 2

    text_w = text.get_width()
    text_h = text.get_height()

    pygame.draw.rect(screen, pygame.Color('paleturquoise'), (text_x - 10, text_y - 10,
                                                             text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def show_message_start(screen, message):
    font = pygame.font.Font(None, 70)

    text = font.render(message, 1, (50, 70, 0))

    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 + 150 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()

    pygame.draw.rect(screen, pygame.Color("cadetblue1"), (text_x - 10, text_y - 10,
                                                          text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))
