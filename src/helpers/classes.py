from helpers.constants import *

"""Letter Class"""

# draws letters on the board as user enters them
class Letter:
    # DO NOT CHANGE ANY OF THIS TO ADJUST BOARD POSITIONING
    def __init__(self, text, bg_position, main_color, sub_color, my_font):
        # Initializes all the variables, including text, color, position, size, etc.
        self.bg_color = main_color
        self.text_color = sub_color
        self.correct_place = 0
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], bg_position[1], LETTER_SIZE, LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x + 30, self.bg_y + 30)
        self.text_surface = my_font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self, main_color, my_font):
        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == main_color:
            pygame.draw.rect(SCREEN, GREY, self.bg_rect, 3)
        self.text_surface = my_font.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self, main_color):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(SCREEN, main_color, self.bg_rect)
        pygame.display.update()


"""Keyboard Classes"""

# draw and handle keyboard buttons
class KeyButton:
    def __init__(self, x, y, letter, sub_color2):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.width = 57
        self.height = 70
        self.rect = (self.x, self.y, self.width, self.height)
        self.bg_color = sub_color2

    def draw(self, main_color, my_font):
        # Puts the key and its text on the screen at the desired position.
        pygame.draw.rect(SCREEN, self.bg_color, self.rect, 0, 4)
        self.text_surface = my_font.render(self.text, True, main_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x + (self.width / 2), self.y + (self.height / 2)))
        SCREEN.blit(self.text_surface, self.text_rect)


# draw and handle keyboard larger buttons
class BigKeyButton:
    def __init__(self, x, y, letter, width, height, sub_color2):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.width = width
        self.height = height
        self.rect = (self.x, self.y, self.width, self.height)
        self.bg_color = sub_color2

    def draw(self, main_color, my_font_med):
        pygame.draw.rect(SCREEN, self.bg_color, self.rect, 0, 4)
        self.text_surface = my_font_med.render(self.text, True, main_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x + (self.width / 2), self.y + (self.height / 2)))
        SCREEN.blit(self.text_surface, self.text_rect)