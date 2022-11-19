import pygame_menu
from typing import Tuple, Any
import pygame
from pygame import mixer
import sys
import random
from gtts import gTTS
import speech_recognition as sr
import os
from playsound import playsound
import time
import word_files.englishwords as englishwords
from word_files.englishwords import *
import word_files.spanishwords as spanishwords
from word_files.spanishwords import *
import word_files.frenchwords as frenchwords
from word_files.frenchwords import *
import word_files.germanwords as germanwords
from word_files.germanwords import *
import word_files.kidwords as kidwords
from word_files.kidwords import *
from messages import *
from constants import *

"""INITIALIZERS / GLOBAL VARIABLES"""

pygame.init()
start_game = 0

# AUDIO INTERFACE
rendered = 0
started = 0
activate = 0
audio_interface_enabled = 0
threshold_initialized = 0

# MUSIC
# must debug for windows
try:
    mixer.init()
    mixer.music.load('sound_effects/background_music.ogg')
    mixer.music.set_volume(0.1)
except Exception as e:
    print(str(e) + " Gotta debug this for windows")

eog_sound_allowed = 1

# LANGUAGE
# Text-to-speech languages: English, Spanish, French
languages = ['en', 'es', 'fr']
current_language = 0

# select which file to get the word from based on user selection
lang = "en"
word_list = EN_WORDS

# default
correct_word = EN_WORDS[random.randint(0, len(EN_WORDS) - 1)]

# DEFAULT COLORS
correct_color = GREEN
semi_color = YELLOW
wrong_color = GREY
main_color = WHITE
sub_color = BLACK
sub_color2 = LT_GREY

# FONT DEFAULTS
my_font = pygame.font.Font("assets/FreeSans.otf", 40)
my_font_med = pygame.font.Font("assets/FreeSans.otf", 30)
my_font_sm = pygame.font.Font("assets/FreeSans.otf", 20)
my_font_xsm = pygame.font.Font("assets/FreeSans.otf", 15)

# SCREEN
pygame.display.set_caption("World-le")
pygame.display.set_icon(pygame.image.load("assets/Icon.png"))
pygame.display.update()

# KEYBOARD
keys = []
key_pressed = ''

# WORD/LETTER CONTROL
guesses_count = 0
guesses = [[]] * 6
# when guess checked, full version placed here
guesses_str = []

correct_guesses = []
incorrect_guesses = []
semi_correct_guesses = []
remaining_guesses = []

current_guess = []
current_guess_string = ""

# change this to adjust x coordinate of letter position
current_letter_bg_x = WIDTH / 3.25

game_result = ""


"""FUNCTIONS"""


# GAME BOARD #

# Draws the game board gird on the screen
def draw():
    size = 60
    for col in range(0, 5):
        for row in range(0, 6):
            # change + values to adjust board positioning
            pygame.draw.rect(SCREEN, sub_color, [col * LETTER_X_SPACING + WIDTH / 3.25,
                                                 row * LETTER_Y_SPACING + 70, size, size], 1, 1)


# draws the color key to show the user what colors are selected and what they mean
def draw_color_key():
    # function variables
    key_width, key_height = 155, 225
    block_x, block_y = WIDTH - 170, 70
    title_x, title_y = WIDTH - 185 / 2, 95
    color_x, color_y = WIDTH - 155, 130
    size, shape, round_edge = 30, 100, 5
    text_x = WIDTH - 70

    # Draws the color key outline and title of area
    pygame.draw.rect(SCREEN, sub_color, [block_x, block_y, key_width, key_height], 1, round_edge)
    color_text = my_font_sm.render("Color Key", True, sub_color)
    color_rect = color_text.get_rect(center=(title_x, title_y))
    SCREEN.blit(color_text, color_rect)

    # draws the correct color circle and lable of color
    pygame.draw.rect(SCREEN, correct_color, [color_x, color_y, size, size], 0, shape)
    correct_text = my_font_xsm.render("CORRECT", True, sub_color)
    correct_rect = correct_text.get_rect(center=(text_x, color_y + 15))
    SCREEN.blit(correct_text, correct_rect)

    # draws the semi correct color circle and lable of color
    pygame.draw.rect(SCREEN, semi_color, [color_x, color_y + 50, size, size], 0, shape)
    semi_text = my_font_xsm.render("SEMI", True, sub_color)
    semi_rect = semi_text.get_rect(center=(text_x, color_y + 55))
    SCREEN.blit(semi_text, semi_rect)
    semi_text = my_font_xsm.render("CORRECT", True, sub_color)
    semi_rect = semi_text.get_rect(center=(text_x, color_y + 75))
    SCREEN.blit(semi_text, semi_rect)

    # draws the wrong color circle and lable of color
    pygame.draw.rect(SCREEN, wrong_color, [color_x, color_y + 105, size, size], 0, shape)
    wrong_text = my_font_xsm.render("WRONG", True, sub_color)
    wrong_rect = wrong_text.get_rect(center=(text_x, color_y + 120))
    SCREEN.blit(wrong_text, wrong_rect)

    pygame.display.update()


# draws the navagation bar at the top of the screen and the contents on the bar
def draw_nav_bar():
    size = 30

    # actual nav bar
    pygame.draw.rect(SCREEN, sub_color2, [0, 0, WIDTH, 50], 0)
    # menu placeholder - change to something else
    pygame.draw.rect(SCREEN, BLACK, [10, 10, size, size], 0)

    # font selector icon
    font_image = pygame.image.load('assets/font-icon.png')
    font_image = pygame.transform.scale(font_image, (30, 35))
    rec1 = font_image.get_rect()
    rec1.center = (WIDTH - 40), 25
    SCREEN.blit(font_image, rec1)

    # color selector icon
    color_image = pygame.image.load('assets/color.png')
    color_image = pygame.transform.scale(color_image, (30, 30))
    rec2 = color_image.get_rect()
    rec2.center = (WIDTH - 90), 25
    SCREEN.blit(color_image, rec2)

    # dark mode icon 
    dark_image = pygame.image.load('assets/dark.png')
    dark_image = pygame.transform.scale(dark_image, (30, 30))
    rec3 = dark_image.get_rect()
    rec3.center = (WIDTH - 140), 25
    SCREEN.blit(dark_image, rec3)

    # Draws title of the application
    header_text = my_font.render("WORLDLE", True, main_color)
    header_rect = header_text.get_rect(center=(WIDTH / 2, 25))
    SCREEN.blit(header_text, header_rect)


# draws the font menu on the screen when the font change icon is selected - WORK IN PROGRESS
def draw_font_screen():
    value = ""
    mini_width = WIDTH * 0.6
    mini_height = HEIGHT * 0.8
    round = 4

    # draw background rectangle
    pygame.draw.rect(SCREEN, GREY, ((WIDTH - mini_width) / 2,
                                    (HEIGHT - mini_height) / 2, mini_width, mini_height), 0, round)
    # draw front rectangle
    pygame.draw.rect(SCREEN, main_color, ((WIDTH - mini_width) / 2 + 3,
                                          (HEIGHT - mini_height) / 2 + 3, mini_width - 6, mini_height - 6), 0, round)

    pygame.display.update()

    # while value == "":
    #     x = 1

    return "assets/GFSDidotBold.otf"


# draw the color squares on the color menu
def draw_color_squrs():
    size, round = 75, 4
    c_x = ((WIDTH - WIDTH * 0.6) / 2 + 70)
    c_y = (HEIGHT - HEIGHT * 0.8) / 2 + 125
    shift_amount = 100

    for i in range(4):
        for color in COLORS[i]:
            pygame.draw.rect(SCREEN, color, (c_x, c_y, size, size), 0, round)
            c_x += shift_amount
        c_x = ((WIDTH - WIDTH * 0.6) / 2 + 70)
        c_y += shift_amount

    pygame.display.update()


# draws the color menu and controls the menu functionality, returns selected color
def draw_color_screen(current):
    value = current
    done = 0
    round = 4
    size = 75
    # width and height of the color menu
    mini_width = WIDTH * 0.6
    mini_height = HEIGHT * 0.8

    # draw background screen
    pygame.draw.rect(SCREEN, GREY, ((WIDTH - mini_width) / 2, (HEIGHT - mini_height) / 2,
                                    mini_width, mini_height), 0, round)
    # draw front screen
    pygame.draw.rect(SCREEN, main_color, ((WIDTH - mini_width) / 2 + 3, (HEIGHT - mini_height) / 2 + 3,
                                          mini_width - 6, mini_height - 6), 0, round)
    # draw menu title
    color_text = my_font.render("Change Color", True, sub_color)
    color_rect = color_text.get_rect(center=(WIDTH / 2, (HEIGHT - mini_height) / 2 + 45))
    SCREEN.blit(color_text, color_rect)

    # draw done button
    pygame.draw.rect(SCREEN, sub_color2, ((WIDTH - 200) / 2, HEIGHT - 150, 200, 50), 0, round)
    done_text = my_font.render("DONE", True, WHITE)
    done_rect = done_text.get_rect(center=(WIDTH / 2, HEIGHT - 125))
    SCREEN.blit(done_text, done_rect)

    # draw the color squares
    draw_color_squrs()

    # create areas for each of the color squares
    x_loc_one, y_loc_one = (WIDTH - mini_width) / 2 + 70, (HEIGHT - mini_height) / 2 + 125
    x_loc_two, y_loc_two = (WIDTH - mini_width) / 2 + 170, (HEIGHT - mini_height) / 2 + 225
    x_loc_three, y_loc_three = (WIDTH - mini_width) / 2 + 270, (HEIGHT - mini_height) / 2 + 325
    x_loc_four, y_loc_four = (WIDTH - mini_width) / 2 + 370, (HEIGHT - mini_height) / 2 + 425

    color1 = pygame.Rect(x_loc_one, y_loc_one, size, size)
    color2 = pygame.Rect(x_loc_two, y_loc_one, size, size)
    color3 = pygame.Rect(x_loc_three, y_loc_one, size, size)
    color4 = pygame.Rect(x_loc_four, y_loc_one, size, size)
    color5 = pygame.Rect(x_loc_one, y_loc_two, size, size)
    color6 = pygame.Rect(x_loc_two, y_loc_two, size, size)
    color7 = pygame.Rect(x_loc_three, y_loc_two, size, size)
    color8 = pygame.Rect(x_loc_four, y_loc_two, size, size)
    color9 = pygame.Rect(x_loc_one, y_loc_three, size, size)
    color10 = pygame.Rect(x_loc_two, y_loc_three, size, size)
    color11 = pygame.Rect(x_loc_three, y_loc_three, size, size)
    color12 = pygame.Rect(x_loc_four, y_loc_three, size, size)
    color13 = pygame.Rect(x_loc_one, y_loc_four, size, size)
    color14 = pygame.Rect(x_loc_two, y_loc_four, size, size)
    color15 = pygame.Rect(x_loc_three, y_loc_four, size, size)
    color16 = pygame.Rect(x_loc_four, y_loc_four, size, size)
    done_area = pygame.Rect((WIDTH - 200) / 2, HEIGHT - 150, 200, 50)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if color1.collidepoint(event.pos):
                        value = COLORS[0][0]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color1, 3, round)
                    if color2.collidepoint(event.pos):
                        value = COLORS[0][1]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color2, 3, round)
                    if color3.collidepoint(event.pos):
                        value = COLORS[0][2]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color3, 3, round)
                    if color4.collidepoint(event.pos):
                        value = COLORS[0][3]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color4, 3, round)
                    if color5.collidepoint(event.pos):
                        value = COLORS[1][0]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color5, 3, round)
                    if color6.collidepoint(event.pos):
                        value = COLORS[1][1]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color6, 3, round)
                    if color7.collidepoint(event.pos):
                        value = COLORS[1][2]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color7, 3, round)
                    if color8.collidepoint(event.pos):
                        value = COLORS[1][3]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color8, 3, round)
                    if color9.collidepoint(event.pos):
                        value = COLORS[2][0]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color9, 3, round)
                    if color10.collidepoint(event.pos):
                        value = COLORS[2][1]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color10, 3, round)
                    if color11.collidepoint(event.pos):
                        value = COLORS[2][2]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color11, 3, round)
                    if color12.collidepoint(event.pos):
                        value = COLORS[2][3]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color12, 3, round)
                    if color13.collidepoint(event.pos):
                        value = COLORS[3][0]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color13, 3, round)
                    if color14.collidepoint(event.pos):
                        value = COLORS[3][1]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color14, 3, round)
                    if color15.collidepoint(event.pos):
                        value = COLORS[3][2]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color15, 3, round)
                    if color16.collidepoint(event.pos):
                        value = COLORS[3][3]
                        draw_color_squrs()
                        pygame.draw.rect(SCREEN, sub_color, color16, 3, round)
                    if done_area.collidepoint(event.pos):
                        done = 1
                    pygame.display.update()

    return value


# draw screen where you select which color to change
def draw_select_color():
    round = 4
    done = 0
    # width and height of the color menu
    mini_width = WIDTH * 0.6
    mini_height = HEIGHT * 0.85

    # draw background screen
    pygame.draw.rect(SCREEN, GREY, ((WIDTH - mini_width) / 2, (HEIGHT - mini_height) / 2,
                                    mini_width, mini_height), 0, round)
    # draw front screen
    pygame.draw.rect(SCREEN, main_color, ((WIDTH - mini_width) / 2 + 3, (HEIGHT - mini_height) / 2 + 3,
                                          mini_width - 6, mini_height - 6), 0, round)
    # draw menu title
    color_text = my_font.render("SELECT COLOR", True, sub_color)
    color_rect = color_text.get_rect(center=(WIDTH / 2, (HEIGHT - mini_height) / 2 + 45))
    SCREEN.blit(color_text, color_rect)
    color2_text = my_font.render("TO CHANGE", True, sub_color)
    color2_rect = color2_text.get_rect(center=(WIDTH / 2, (HEIGHT - mini_height) / 2 + 90))
    SCREEN.blit(color2_text, color2_rect)

    # draw correct select button
    pygame.draw.rect(SCREEN, correct_color, PICK_ONE_AREA, 0, round)
    c_text = my_font_med.render("Change Correct Color", True, BLACK)
    c_rect = c_text.get_rect(center=(WIDTH / 2, HEIGHT - 510))
    SCREEN.blit(c_text, c_rect)

    # draw semi correct select button
    pygame.draw.rect(SCREEN, semi_color, PICK_TWO_AREA, 0, round)
    s_text = my_font_med.render("Change Semi Correct Color", True, BLACK)
    s_rect = s_text.get_rect(center=(WIDTH / 2, HEIGHT - 410))
    SCREEN.blit(s_text, s_rect)

    # draw wrong select button
    pygame.draw.rect(SCREEN, wrong_color, PICK_THREE_AREA, 0, round)
    w_text = my_font_med.render("Change Wrong Color", True, BLACK)
    w_rect = w_text.get_rect(center=(WIDTH / 2, HEIGHT - 310))
    SCREEN.blit(w_text, w_rect)

    pygame.draw.rect(SCREEN, HIGH_CONTRAST_2, PICK_FOUR_AREA, 0, round)
    hc_text = my_font_med.render("Activate High Contrast Mode", True, BLACK)
    hc_rect = hc_text.get_rect(center=(WIDTH / 2, HEIGHT - 185))
    SCREEN.blit(hc_text, hc_rect)

    # draw cancel button
    pygame.draw.rect(SCREEN, sub_color2, CANCEL_AREA, 0, round)
    can_text = my_font_sm.render("CANCEL", True, WHITE)
    can_rect = can_text.get_rect(center=(WIDTH / 2, HEIGHT - 100))
    SCREEN.blit(can_text, can_rect)

    pygame.display.update()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if PICK_ONE_AREA.collidepoint(event.pos):
                        reset_screen()
                        chosen_color = draw_color_screen(correct_color)
                        set_correct_color(chosen_color)
                        done = 1
                    if PICK_TWO_AREA.collidepoint(event.pos):
                        reset_screen()
                        chosen_color = draw_color_screen(semi_color)
                        set_semi_color(chosen_color)
                        done = 1
                    if PICK_THREE_AREA.collidepoint(event.pos):
                        reset_screen()
                        chosen_color = draw_color_screen(wrong_color)
                        set_wrong_color(chosen_color)
                        done = 1
                    if PICK_FOUR_AREA.collidepoint(event.pos):
                        set_correct_color(HIGH_CONTRAST_1)
                        set_semi_color(HIGH_CONTRAST_2)
                        set_wrong_color(HIGH_CONTRAST_3)
                        done = 1
                    if CANCEL_AREA.collidepoint(event.pos):
                        done = 1


# draws letters on the board as user enters them
class Letter:
    # DO NOT CHANGE ANY OF THIS TO ADJUST BOARD POSITIONING
    def __init__(self, text, bg_position):
        # Initializes all the variables, including text, color, position, size, etc.
        self.bg_color = main_color
        self.text_color = sub_color
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], bg_position[1], LETTER_SIZE, LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x + 30, self.bg_y + 30)
        self.text_surface = my_font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == main_color:
            pygame.draw.rect(SCREEN, GREY, self.bg_rect, 3)
        self.text_surface = my_font.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(SCREEN, main_color, self.bg_rect)
        pygame.display.update()


# KEYBOARD #

# draw and handle keyboard buttons
class KeyButton:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.width = 57
        self.height = 70
        self.rect = (self.x, self.y, self.width, self.height)
        self.bg_color = sub_color2

    def draw(self):
        # Puts the key and its text on the screen at the desired position.
        pygame.draw.rect(SCREEN, self.bg_color, self.rect, 0, 4)
        self.text_surface = my_font.render(self.text, True, main_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x + (self.width / 2), self.y + (self.height / 2)))
        SCREEN.blit(self.text_surface, self.text_rect)


# draw and handle keyboard larger buttons
class BigKeyButton:
    def __init__(self, x, y, letter, width, height):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.width = width
        self.height = height
        self.rect = (self.x, self.y, self.width, self.height)
        self.bg_color = sub_color2

    def draw(self):
        pygame.draw.rect(SCREEN, self.bg_color, self.rect, 0, 4)
        self.text_surface = my_font_med.render(self.text, True, main_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x + (self.width / 2), self.y + (self.height / 2)))
        SCREEN.blit(self.text_surface, self.text_rect)


def draw_keyboard():
    # starting keyboard location
    key_x, key_y = 125, 500

    # draw letters On top of keyboard buttons
    for i in range(3):
        for letter in ALPHABET[i]:
            new_key = KeyButton(key_x, key_y, letter)
            keys.append(new_key)
            new_key.draw()
            key_x += 60
        key_y += 80
        if i == 0:
            key_x = 160
        elif i == 1:
            key_x = 210
    new_key = BigKeyButton(100, 660, "DEL", 102, 70)
    keys.append(new_key)
    new_key.draw()
    new_key = BigKeyButton(635, 660, "ENTER", 125, 70)
    keys.append(new_key)
    new_key.draw()


# GENERAL GAME CONTROLS

def add_semi(char):
    global semi_correct_guesses
    if char not in semi_correct_guesses:
        semi_correct_guesses.append(char)


def add_incorrect(char):
    global incorrect_guesses
    if char not in incorrect_guesses:
        incorrect_guesses.append(char)


def add_correct(char):
    global correct_guesses
    if char not in correct_guesses:
        correct_guesses.append(char)


# check what parts of the user's guess is correct
def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    global current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result
    game_decided = False
    guesses_str.append(current_guess_string)
    for i in range(5):
        lowercase_letter = guess_to_check[i].text.lower()
        if lowercase_letter in correct_word:
            if lowercase_letter == correct_word[i]:
                guess_to_check[i].bg_color = correct_color
                add_correct(lowercase_letter)
                for key in keys:
                    if key.text == lowercase_letter.upper():
                        key.bg_color = correct_color
                        key.draw()
                guess_to_check[i].text_color = main_color
                if not game_decided:
                    game_result = "W"
            else:
                guess_to_check[i].bg_color = semi_color
                add_semi(lowercase_letter)
                for key in keys:
                    if key.text == lowercase_letter.upper():
                        key.bg_color = semi_color
                        key.draw()
                guess_to_check[i].text_color = main_color
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = GREY
            add_incorrect(lowercase_letter)
            for key in keys:
                if key.text == lowercase_letter.upper():
                    key.bg_color = wrong_color
                    key.draw()
            guess_to_check[i].text_color = main_color
            game_result = ""
            game_decided = True
        guess_to_check[i].draw()
        pygame.display.update()

    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = WIDTH / 3.25

    if guesses_count == 6 and game_result == "":
        game_result = "L"


# display loosing screen and call reset
def lose_play_again():
    # Puts the play again text on the screen.
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, RED, (10, 10, WIDTH - 20, HEIGHT - 20))
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=(WIDTH / 2, 320))
    word_was_text = play_again_font.render(f"Sorry, the word was {correct_word}!", True, WHITE)
    word_was_rect = word_was_text.get_rect(center=(WIDTH / 2, 250))
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()


# display winning screen and call reset
def correct_play_again():
    # Puts the play again text on the screen.
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, correct_color, (10, 10, WIDTH - 20, HEIGHT - 20))
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    con_text = play_again_font.render(f"Congratulations!", True, WHITE)
    con_rect = con_text.get_rect(center=(WIDTH / 2, 250))
    word_was_text = play_again_font.render(f"The word was {correct_word}!", True, WHITE)
    word_was_rect = word_was_text.get_rect(center=(WIDTH / 2, 320))
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=(WIDTH / 2, 390))

    SCREEN.blit(con_text, con_rect)
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()


# reset global variables
def reset():
    # Resets all global variables to their default states.
    global guesses_count, correct_word, guesses, current_guess, current_guess_string, game_result, lang, \
        semi_correct_guesses, correct_guesses, incorrect_guesses, word_list, eog_sound_allowed
    SCREEN.fill(main_color)

    guesses_count = 0
    guesses = [[]] * 6
    current_guess = []
    current_guess_string = ""
    game_result = ""
    incorrect_guesses = []
    correct_guesses = []
    semi_correct_guesses = []
    eog_sound_allowed = 1

    if lang == "en":
        word_list = EN_WORDS
        correct_word = englishwords.EN_WORDS[random.randint(0, len(englishwords.EN_WORDS) - 1)]
    elif lang == "sp":
        word_list = SP_WORDS
        correct_word = spanishwords.SP_WORDS[random.randint(0, len(spanishwords.SP_WORDS) - 1)]
    elif lang == "ger":
        word_list = GER_WORDS
        correct_word = germanwords.GER_WORDS[random.randint(0, len(germanwords.GER_WORDS) - 1)]
    elif lang == "fr":
        word_list = FR_WORDS
        correct_word = frenchwords.FR_WORDS[random.randint(0, len(frenchwords.FR_WORDS) - 1)]
    elif lang == "kid":
        word_list = KID_WORDS
        correct_word = kidwords.KID_WORDS[random.randint(0, len(kidwords.KID_WORDS) - 1)]

    for key in keys:
        key.bg_color = sub_color2
        key.draw()

    draw_color_key()
    draw_nav_bar()

    # no longer need to comment for windows
    play_background_music()

    print(correct_word)
    pygame.display.update()


# reset the screen and redraw with new colors
def reset_screen():
    SCREEN.fill(main_color)

    for key in keys:
        for l in correct_guesses:
            if key.text == l.upper():
                key.bg_color = correct_color
        for l in semi_correct_guesses:
            if key.text == l.upper():
                key.bg_color = semi_color
        for l in incorrect_guesses:
            if key.text == l.upper():
                key.bg_color = wrong_color
        key.draw()

    draw_color_key()
    draw_nav_bar()

    for guess in guesses:
        for letter in guess:
            for l in correct_guesses:
                if letter.text == l.upper():
                    letter.bg_color = correct_color
            for l in semi_correct_guesses:
                if letter.text == l.upper():
                    letter.bg_color = semi_color
            letter.draw()

    pygame.display.update()


# AUDIO CONTROL

# Uses gTTS to say the string 'response' in language 'language'
def say(response, language):
    obj = gTTS(text=response, lang=language, slow=False)
    obj.save("audio.mp3")
    try:
        # mac os version
        os.system("mpg123 audio.mp3")
    except Exception as e:
        # Windows version
        print(e)
        os.system("mpg123.exe audio.mp3")


# Uses SpeechRecognition to translate a user response to text. Returns text
def listen():
    global threshold_initialized

    r = sr.Recognizer()
    r.energy_threshold = 600
    # r.dynamic_energy_threshold = True
    mic = sr.Microphone()
    # Adjust based on current environment, start at 300 and adjust
    # until good results found, good values between 50 and 4000

    with mic as source:
        # if not threshold_initialized:
        #     r.adjust_for_ambient_noise(source, 2)
        #     threshold_initialized = 1
        audio = r.listen(source)
        # audio = r.adjust_for_ambient_noise(source)

    cur_text = r.recognize_google(audio)
    return cur_text


def say_by_char(response, language):
    chars = [*response]
    for c in chars:
        say(c, language)
        time.sleep(0.025)


def say_and_confirm_by_char(guess, correct, language):
    chars = [*guess]
    correct = [*correct]
    correct_index = 0
    for c in chars:
        say(c, language)
        time.sleep(0.025)
        try:
            if c == correct[correct_index]:
                playsound('sound_effects/correct_char_trimmed.mp3')
            elif c in correct:
                playsound('sound_effects/semi_correct_char_trimmed.wav')
            else:
                playsound('sound_effects/incorrect_char_trimmed.wav')
        except Exception as e:
            print(str(e)+ "NOT WORKING :)")
        correct_index = correct_index + 1


def play_background_music():
    try:
        mixer.music.play(-1)
    except Exception as e:
        print(str(e) + "Playing background music only works on mac as of now")


def pause_background_music():
    try:
        mixer.music.pause()
    except Exception as e:
        print(str(e) + "cant pause what never started")


def set_background_music_volume(level):
    try:
        mixer.music.set_volume(level)
    except Exception as e:
        print(str(e) + "Volume controls only work if music is there")


# Prevents sound effect repeat at end of game (eog) through the use of a state variable,
# eog_sound_allowed, which is only reset when game is reset
def eog_sound(current_game_result):
    global eog_sound_allowed
    if eog_sound_allowed:
        if current_game_result == "W":
            pause_background_music()
            try:
                playsound('sound_effects/correct_word_trimmed.mp3')
            except Exception as e:
                print(str(e) + "NOT WORKING :)")
            eog_sound_allowed = 0
        elif current_game_result == "L":
            pause_background_music()
            try:
                playsound('sound_effects/no_more_guesses_trimmed.wav')
            except Exception as e:
                print(str(e) + "NOT WORKING :)")
            eog_sound_allowed = 0


# Control for common letter misinterpretations. Called if word returned to 'stash' instead of a char
# Returns a character if possible, if none found, returns original word. SHOULD IMPLEMENT DIFFERENTLY
def fix_char(fuzzy_char):
    if fuzzy_char == "aye":
        return 'a'
    elif fuzzy_char == "bee":
        return 'b'
    elif fuzzy_char == "see":
        return 'c'
    elif fuzzy_char == "gee":
        return 'g'
    elif fuzzy_char == "ache":
        return 'h'
    elif fuzzy_char == "eye":
        return 'i'
    elif fuzzy_char == "jay":
        return 'j'
    elif fuzzy_char == "kay":
        return 'k'
    elif fuzzy_char == "elle":
        return 'l'
    elif fuzzy_char == "el":
        return 'l'
    elif fuzzy_char == "oh":
        return 'o'
    elif fuzzy_char == "pea":
        return 'p'
    elif fuzzy_char == "pee":
        return 'p'
    elif fuzzy_char == "queue":
        return 'q'
    elif fuzzy_char == "are":
        return 'r'
    elif fuzzy_char == "ES":
        return 's'
    elif fuzzy_char == "tea":
        return 't'
    elif fuzzy_char == "tee":
        return 't'
    elif fuzzy_char == "you":
        return 'u'
    elif fuzzy_char == "double you":
        return 'w'
    elif fuzzy_char == "ex":
        return 'x'
    elif fuzzy_char == "axe":
        return 'x'
    elif fuzzy_char == "why":
        return 'w'
    else:
        return fuzzy_char  # add more if found


def word_to_int(word):
    if word == 'one' or word == 'won':
        return 1
    elif word == 'two' or word == 'to' or word == 'too':
        return 2
    elif word == 'three':
        return 3
    elif word == 'four' or word == 'for':
        return 4
    elif word == 'five':
        return 5
    else:
        return word


def clear_stash():
    delete_count = len(current_guess_string)
    while delete_count > 0:
        delete_letter()
        delete_count -= 1


def replace(command):
    global current_guess_string
    char_to_replace = ''
    replacement = ''

    # find char_to_replace and replacement in response
    command = command.split(' ')
    index = 0
    found = 0
    while not found:
        if command[index] == "replace":
            char_to_replace = command[index + 1]
            replacement = command[index + 3]
            found = 1
        else:
            index += 1

    # check if char_to_replace is an index or a char
    guess_split = [*current_guess_string]
    replacement = fix_char(replacement)
    char_to_replace = fix_char(char_to_replace)

    index_list = ['1', '2', '3', '4', '5', 'one', 'two', 'to', 'too', 'three', 'four', 'for', 'five']
    if char_to_replace in index_list:
        # replace letter at index char_to_replace, with replacement
        guess_split[int(word_to_int(char_to_replace)) - 1] = replacement
        clear_stash()
        new_guess_string = ''.join(guess_split)
        stash("stash " + new_guess_string)
        return

    elif not current_guess_string.count(char_to_replace.upper()) == 1:
        say("there are more than one of the letter to replace in your stash. "
            "Please specify which one by using stash index feature.", languages[current_language])
        return

    elif len(char_to_replace) == 1:
        # find index in current_guess_string that holds char_to_replace
        index_to_replace = 0
        found = 0
        while not found:
            if current_guess_string[index_to_replace] == char_to_replace.upper():
                found = 1
            else:
                index_to_replace += 1

        guess_split[index_to_replace] = replacement.upper()  # Do replacement
        clear_stash()
        new_guess_string = ''.join(guess_split)
        stash("stash " + new_guess_string)

    else:
        say("You must replace one letter in your stashed guess at a time.", languages[current_language])


def read_guess(guess_number):
    if guess_number > guesses_count:
        say("You dont have a guess number " + str(guess_number) + " yet.", languages[current_language])
    else:
        say_and_confirm_by_char(guesses_str[guess_number - 1], correct_word.upper(), languages[current_language])


def handsfree():
    global current_guess_string, activate, audio_interface_enabled

    waiting_for_command = 1
    while waiting_for_command:
        try:
            time.sleep(0.05)
            command = listen()
            # Comment above for debugging, allows typing of command; comment below for handsfree use;
            # command = input("Type a command: ")
            command = command.lower()
            print(command)

            if "tutorial" in command:  # Starts tutorial
                say("say word for wordle tutorial, say free for handsfree tutorial", languages[current_language])
                response = listen()
                if "word" in response:
                    say(WORDLE_TUTORIAL, languages[current_language])
                elif "free" in response:
                    say(HANDSFREE_TUTORIAL, languages[current_language])
                waiting_for_command = 0
            elif "replace" in command:
                say("you said: " + command, languages[current_language])
                replace(command)
                waiting_for_command = 0
            elif "stash" in command or "dash" in command:  # Places character(s) into current guess
                say("you said: " + command, languages[current_language])
                stash(command)
                waiting_for_command = 0
            elif "delete" in command:  # Deletes all characters from stash
                say("You said: delete", languages[current_language])
                delete()
                waiting_for_command = 0
            elif "submit" in command:
                say("you said: submit", languages[current_language])
                submit()
                waiting_for_command = 0
            elif "clear" in command:
                say("you said: " + command, languages[current_language])
                clear_stash()
                waiting_for_command = 0
            elif "disable" in command:
                say("Disabling audio, press space bar twice to re-enable.", languages[current_language])
                activate = 0
                audio_interface_enabled = 0
                waiting_for_command = 0
            elif "play again" in command:
                reset()
            elif "read" in command:
                if "guess" in command or "gas" in command or "guest" in command:
                    if "one" in command or "won" in command or "1" in command:
                        say("read guess one", languages[current_language])
                        read_guess(1)
                        waiting_for_command = 0
                    elif "two" in command or "to" in command or "2" in command or "too" in command:
                        say("read guess two", languages[current_language])
                        read_guess(2)
                        waiting_for_command = 0
                    elif "three" in command or "3" in command:
                        say("read guess three", languages[current_language])
                        read_guess(3)
                        waiting_for_command = 0
                    elif "four" in command or "for" in command or "4" in command:
                        say("read guess four", languages[current_language])
                        read_guess(4)
                        waiting_for_command = 0
                    elif "five" in command or "5" in command:
                        say("read guess five", languages[current_language])
                        read_guess(5)
                        waiting_for_command = 0
                    else:
                        say("read current guess", languages[current_language])
                        say_by_char(current_guess_string, languages[current_language])
                        waiting_for_command = 0
                elif "semi" in command:
                    say("read semi correct guesses", languages[current_language])
                    say_by_char(semi_correct_guesses, languages[current_language])
                    waiting_for_command = 0
                elif "wrong" in command:
                    say("read incorrect guesses", languages[current_language])
                    say_by_char(incorrect_guesses, languages[current_language])
                    waiting_for_command = 0
                else:
                    say("invalid command", languages[current_language])
            else:
                say("invalid command", languages[current_language])

        except Exception as e:
            print("exception: " + repr(e))


# Identifies whether you are stashing a word or a character, calls the appropriate
# function or tells the user the input is invalid.
def stash(response):
    print("stash called")
    response_split = response.split(' ')

    guess = ""
    found = 0
    index = 0
    while not found:
        try:
            if response_split[index] == "stash" or response_split[index] == "dash":
                guess = response_split[index + 1]
                found = 1
            else:
                index += 1
        except Exception as e:
            say("Remember to say a letter or five letter word after stash command.", languages[current_language])
            print(e)
            return

    if len(guess) == 1:
        print("single letter")
        stash_char(guess)
    elif len(guess) == 5:
        if len(current_guess_string) != 0:
            say("your stash is full! submit or delete to guess more letters.", languages[current_language])
            return
        print("Five letter word")
        for each_letter in guess:
            print(each_letter)
            stash_char(each_letter)
    else:
        say("You can only stash individual letters, or five letter words. Try again!", languages[current_language])


# Takes stash command as an input and places new letter on the screen
def stash_char(char_to_stash):
    global key_pressed
    key_pressed = char_to_stash.upper()
    if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM":
        if len(current_guess_string) < 5:
            create_new_letter()
        else:
            say("your stash is full! submit or delete to guess more letters.", languages[current_language])


# delete for handsfree version
def delete():
    global current_guess_string
    if len(current_guess_string) > 0:
        letter_to_delete = current_guess_string[len(current_guess_string) - 1]
        say("Deleting " + letter_to_delete, languages[current_language])
        delete_letter()
    else:
        say("You dont have any letters to delete!", languages[current_language])


# submit for hands-free version
def submit():
    global current_guess_string, current_guess
    if len(current_guess_string) == 5 and current_guess_string.lower() in word_list:
        say_and_confirm_by_char(current_guess_string, correct_word.upper(), languages[current_language])
        check_guess(current_guess)
    else:
        say("your stash must contain a real five letter word, try again!", languages[current_language])


# TRADITIONAL PLAY CONTROL

# for traditional version of the game
def create_new_letter():
    # Creates a new letter and adds it to the guess.
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    # do not change this to adjust board positioning
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count * 70 + LETTER_Y_SPACING))
    current_letter_bg_x += LETTER_X_SPACING
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()


# delete for traditional version of game
def delete_letter():
    # Deletes the last letter from the guess.
    global current_guess_string, current_letter_bg_x
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()
    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_letter_bg_x -= LETTER_X_SPACING


# GAME CONTROL

def start_the_game() -> None:
    global start_game, audio_interface_enabled, started, game_result, activate, current_guess_string, \
        key_pressed, rendered
    start_game = 1
    wait = 0

    SCREEN.fill(main_color)
    print(correct_word)

    draw_keyboard()
    draw_color_key()
    draw_nav_bar()

    while True:
        # how program should run when audio interface is not enabled
        while not audio_interface_enabled and start_game:
            draw()
            if game_result == "L":
                # NO need to comment sound anymore
                # eog_sound(game_result)
                lose_play_again()
            if game_result == "W":
                # eog_sound(game_result)
                correct_play_again()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if game_result != "":
                            reset()
                        else:
                            # THIS NEEDS TO BE ADJUSTED FOR DIFFERENT LANGUAGES
                            if len(current_guess_string) == 5 and current_guess_string.lower() in word_list:
                                check_guess(current_guess)
                    elif event.key == pygame.K_BACKSPACE:
                        if len(current_guess_string) > 0:
                            delete_letter()
                    # have to press space bar twice to activate audio interface
                    elif not activate and event.key == pygame.K_SPACE:
                        activate = 1
                    elif activate and event.key == pygame.K_SPACE:
                        audio_interface_enabled = 1

                    else:
                        key_pressed = event.unicode.upper()
                        if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                            if len(current_guess_string) < 5:
                                create_new_letter()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if Q_AREA.collidepoint(event.pos):
                            key_pressed = "Q"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if W_AREA.collidepoint(event.pos):
                            key_pressed = "W"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if E_AREA.collidepoint(event.pos):
                            key_pressed = "E"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if R_AREA.collidepoint(event.pos):
                            key_pressed = "R"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if T_AREA.collidepoint(event.pos):
                            key_pressed = "T"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if Y_AREA.collidepoint(event.pos):
                            key_pressed = "Y"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if U_AREA.collidepoint(event.pos):
                            key_pressed = "U"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if I_AREA.collidepoint(event.pos):
                            key_pressed = "I"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if O_AREA.collidepoint(event.pos):
                            key_pressed = "O"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if P_AREA.collidepoint(event.pos):
                            key_pressed = "P"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if A_AREA.collidepoint(event.pos):
                            key_pressed = "A"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if S_AREA.collidepoint(event.pos):
                            key_pressed = "S"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if D_AREA.collidepoint(event.pos):
                            key_pressed = "D"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if F_AREA.collidepoint(event.pos):
                            key_pressed = "F"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if G_AREA.collidepoint(event.pos):
                            key_pressed = "G"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if H_AREA.collidepoint(event.pos):
                            key_pressed = "H"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if J_AREA.collidepoint(event.pos):
                            key_pressed = "J"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if K_AREA.collidepoint(event.pos):
                            key_pressed = "K"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if L_AREA.collidepoint(event.pos):
                            key_pressed = "L"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if Z_AREA.collidepoint(event.pos):
                            key_pressed = "Z"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if X_AREA.collidepoint(event.pos):
                            key_pressed = "X"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if C_AREA.collidepoint(event.pos):
                            key_pressed = "C"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if V_AREA.collidepoint(event.pos):
                            key_pressed = "V"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if B_AREA.collidepoint(event.pos):
                            key_pressed = "B"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if N_AREA.collidepoint(event.pos):
                            key_pressed = "N"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if M_AREA.collidepoint(event.pos):
                            key_pressed = "M"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if ENTER_AREA.collidepoint(event.pos):
                            if len(current_guess_string) == 5 and current_guess_string.lower() in word_list:
                                check_guess(current_guess)
                        if DEL_AREA.collidepoint(event.pos):
                            if len(current_guess_string) > 0:
                                delete_letter()
                        if MENU_AREA.collidepoint(event.pos):
                            start_game = 0
                            menu()
                        if FONT_SEL_AREA.collidepoint(event.pos):
                            chosen_font = draw_font_screen()
                            set_font(chosen_font)
                            reset_screen()
                        if COLOR_SEL_AREA.collidepoint(event.pos):
                            draw_select_color()
                            reset_screen()
                        if DARK_SEL_AREA.collidepoint(event.pos):
                            set_dark_mode()
                            reset_screen()
                        if CORRECT_COLOR_AREA.collidepoint(event.pos):
                            chosen_color = draw_color_screen(correct_color)
                            set_correct_color(chosen_color)
                            reset_screen()
                        if SEMI_COLOR_AREA.collidepoint(event.pos):
                            chosen_color = draw_color_screen(semi_color)
                            set_semi_color(chosen_color)
                            reset_screen()
                        if WRONG_COLOR_AREA.collidepoint(event.pos):
                            chosen_color = draw_color_screen(wrong_color)
                            set_wrong_color(chosen_color)
                            reset_screen()

            pygame.display.flip()

            # comment out for testing because it's annoying :)
            # if not started:
            #     say(STARTUP, languages[current_language])
            #     started = 1

        # how program should run when audio interface is enabled
        while audio_interface_enabled and start_game:
            draw()
            if game_result == "L":
                # NO need to comment
                eog_sound(game_result)
                say("You have run out of guesses. The word was " + correct_word + " say play again to start over with "
                                                                                  "a new word!",
                    languages[current_language])
                lose_play_again()
            if game_result == "W":
                eog_sound(game_result)
                say("Correct, the word was: " + correct_word + ". say play again to get "
                                                               "a new word.", languages[current_language])
                correct_play_again()
            if rendered:
                handsfree()
            else:
                pygame.display.flip()
                say(ACTIVATED, languages[current_language])
                time.sleep(0.1)
                # NO NEED TO COMMENT BELOW FOR WINDOWS
                set_background_music_volume(0.025)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if game_result != "":
                            reset()
                        else:
                            # THIS NEEDS TO BE ADJUSTED FOR DIFFERENT LANGUAGES!!!!!
                            if len(current_guess_string) == 5 and current_guess_string.lower() in word_list:
                                check_guess(current_guess)
                    elif event.key == pygame.K_BACKSPACE:
                        if len(current_guess_string) > 0:
                            delete_letter()
                    else:
                        key_pressed = event.unicode.upper()
                        if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                            if len(current_guess_string) < 5:
                                create_new_letter()

            pygame.display.flip()

            rendered = 1


# SETTERS

def set_language(selected: Tuple[Any, int], value: str) -> None:
    global lang, correct_word, word_list

    lang = value

    if lang == "sp":
        word_list = SP_WORDS
        correct_word = spanishwords.SP_WORDS[random.randint(0, len(spanishwords.SP_WORDS) - 1)]
    elif lang == "ger":
        word_list = GER_WORDS
        correct_word = germanwords.GER_WORDS[random.randint(0, len(germanwords.GER_WORDS) - 1)]
    elif lang == "fr":
        word_list = FR_WORDS
        correct_word = frenchwords.FR_WORDS[random.randint(0, len(frenchwords.FR_WORDS) - 1)]
    elif lang == "kid":
        word_list = KID_WORDS
        correct_word = kidwords.KID_WORDS[random.randint(0, len(kidwords.KID_WORDS) - 1)]
    else :
        word_list = EN_WORDS
        correct_word = englishwords.EN_WORDS[random.randint(0, len(englishwords.EN_WORDS) - 1)]


def set_correct_color(value):
    global correct_color
    correct_color = value


def set_semi_color(value):
    global semi_color
    semi_color = value


def set_wrong_color(value):
    global wrong_color
    wrong_color = value


def set_dark_mode():
    global sub_color, main_color, sub_color2
    if main_color == WHITE:
        main_color = BLACK
        sub_color = WHITE
        sub_color2 = GREY
    else:
        main_color = WHITE
        sub_color = BLACK
        sub_color2 = LT_GREY


def set_font(value):
    global my_font, my_font_med, my_font_sm, my_font_xsm
    my_font = pygame.font.Font(value, 40)
    my_font_med = pygame.font.Font(value, 30)
    my_font_sm = pygame.font.Font(value, 20)
    my_font_xsm = pygame.font.Font(value, 15)


# MENU

def background():
    SCREEN.fill(WHITE)


def menu():
    screen_difference = 50
    padding = 10

    # MENU THEMES
    mytheme = pygame_menu.themes.THEME_DARK.copy()
    # mytheme.background_color = pygame_menu.baseimage.BaseImage("assets/Background.png")
    mytheme.background_color = GREY
    mytheme.title_font = "assets/FreeSans.otf"
    mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    mytheme.title_offset = (WIDTH / 2 - 140, padding * 8)
    mytheme.title_font_color = WHITE
    mytheme.title_close_button_background_color = BLACK

    mytheme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
    mytheme.widget_font_color = WHITE
    mytheme.widget_font = "assets/FreeSans.otf"
    mytheme.widget_padding = padding
    mytheme.widget_margin = (0, 3)

    color_theme = pygame_menu.themes.THEME_GREEN.copy()
    color_theme.background_color = WHITE
    color_theme.title_font_color = WHITE
    color_theme.widget_font_color = BLACK
    color_theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()

    about_theme = color_theme.copy()
    # about_theme.background_color = pygame_menu.baseimage.BaseImage("assets/Background.png")
    about_theme.background_color = WHITE
    about_theme.title_font = "assets/FreeSans.otf"

    inst_theme = about_theme

    # MENUS

    menu = pygame_menu.Menu(
        height=HEIGHT - screen_difference,
        theme=mytheme,
        title='WORLD-LE',
        width=WIDTH - screen_difference
    )

    color_menu = pygame_menu.Menu(
        height=HEIGHT - screen_difference,
        theme=color_theme,
        title='Change the Game Colors',
        width=WIDTH - screen_difference
    )

    about_menu = pygame_menu.Menu(
        height=HEIGHT - screen_difference,
        theme=about_theme,
        title='About',
        width=WIDTH - screen_difference
    )

    inst_menu = pygame_menu.Menu(
        height=HEIGHT - screen_difference,
        theme=inst_theme,
        title='Game Instructions',
        width=WIDTH - screen_difference
    )

    # COLOR MENU PAGE   

    for m in COLOR_INSTRUCTIONS:
        color_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    color_menu.add.color_input("Correct Letter Color  ", color_type='hex', onchange=set_correct_color, default=GREEN)
    color_menu.add.color_input("Semi Correct Letter Color  ", color_type='hex', onchange=set_semi_color, default=YELLOW)
    color_menu.add.color_input("Wrong Letter Color  ", color_type='hex', onchange=set_wrong_color, default=GREY)

    for m in SPACES:
        color_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    color_menu.add.button("Back", pygame_menu.events.BACK)

    for m in SPACES:
        color_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    # ABOUT MENU PAGE
    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    for m in SPACES:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    about_menu.add.button("Back", pygame_menu.events.BACK)

    for m in SPACES:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    # INSTRUCTIONS MENU PAGE

    for m in INSTRUCTIONS:
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    image_path_correct = pygame_menu.baseimage.BaseImage("assets/correct.jpg")
    inst_menu.add.image(image_path_correct, align=pygame_menu.locals.ALIGN_LEFT)

    for m in INSTRUCTIONS2:
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    image_path_semicorrect = pygame_menu.baseimage.BaseImage("assets/semicorrect.jpg")
    inst_menu.add.image(image_path_semicorrect, align=pygame_menu.locals.ALIGN_LEFT)

    for m in INSTRUCTIONS3:
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    for m in AUDIO_INSTRUCTIONS:
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    for m in SPACES:
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    inst_menu.add.button("Back", pygame_menu.events.BACK)

    for m in SPACES:
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    # MAIN MENU PAGE
    menu.add.button('Play', start_the_game)
    menu.add.selector('Language: ', [("English", "en"), ("Spanish", "sp"), ("German", "ger"),
                                     ("French", "fr"), ("Kid Friendly", "kid")], onchange=set_language, default=0)
    menu.add.button('Instructions', inst_menu)
    menu.add.button('Set Colors', color_menu)
    menu.add.button('About', about_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    if not start_game:
        menu.mainloop(SCREEN, background)


def main():
    play_background_music()
    menu()


if __name__ == "__main__":
    main()
