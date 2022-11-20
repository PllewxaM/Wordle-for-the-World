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
from word_files.englishwords import *
from word_files.spanishwords import *
from word_files.frenchwords import *
from word_files.germanwords import *
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
has_warned = 0
current_background_music = 0

try:
    mixer.init()
    mixer.music.load('sound/background_music/the_trail_instruments_trimmed.mp3')
    mixer.music.set_volume(0.1)
except Exception as e:
    print(str(e) + "Something went wrong")

eog_sound_allowed = 1

# LANGUAGE
# Text-to-speech languages: English, Spanish, French
languages = ['en', 'es', 'fr']
current_language = 0

# default
lang = "en"
word_list = EN_WORDS
correct_word = word_list[random.randint(0, len(word_list) - 1)]

# DEFAULT COLORS
correct_color = GREEN
semi_color = YELLOW
wrong_color = GREY

main_color = WHITE
sub_color = BLACK
sub_color2 = LT_GREY

# FONT DEFAULTS
font = "assets/fonts/FreeSans.otf"
font_size = 40
my_font = pygame.font.Font(font, font_size)
my_font_med = pygame.font.Font(font, font_size - 10)
my_font_sm = pygame.font.Font(font, font_size - 20)
my_font_xsm = pygame.font.Font(font, font_size - 25)

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

# Positioning of letter on board
current_letter_bg_x = WIDTH / 3.25

game_result = ""


"""FUNCTIONS"""


"""GAME BOARD"""

# Draws the game board gird on the screen
def draw():
    size = 60
    for col in range(0, 5):
        for row in range(0, 6):
            # change + values to adjust board positioning
            pygame.draw.rect(SCREEN, sub_color, [col * LETTER_X_SPACING + WIDTH / 3.25,
                                                 row * LETTER_Y_SPACING + 70, size, size], 1, 1)


# Template for drawing text on the screen
def draw_text(font_size, text, text_color, position):
    text = font_size.render(text, True, text_color)
    rect = text.get_rect(center=position)
    SCREEN.blit(text, rect)


# Template for drawing icons on the navagation bar
def draw_icon(path, size, position):
    icon_image = pygame.image.load(path)
    icon_image = pygame.transform.scale(icon_image, size)
    rec = icon_image.get_rect()
    rec.center = position
    SCREEN.blit(icon_image, rec)


# draws the color key to show the user what colors are selected and what they mean
def draw_color_key():
    # function variables
    key_width, key_height = 155, 225
    block_x, block_y = WIDTH - 170, 70
    title_x, title_y = WIDTH - 185 / 2, 95
    color_x, color_y = WIDTH - 155, 130
    size, shape = 30, 100
    text_x = WIDTH - 70

    # Draws the color key outline and title of area
    pygame.draw.rect(SCREEN, sub_color, [block_x, block_y, key_width, key_height], 1, ROUND)
    draw_text(my_font_sm, "Color Key", sub_color, (title_x, title_y))

    # draws the correct color circle and lable of color
    pygame.draw.rect(SCREEN, correct_color, [color_x, color_y, size, size], 0, shape)
    draw_text(my_font_xsm, "CORRECT", sub_color, (text_x, color_y + 15))

    # draws the semi correct color circle and lable of color
    pygame.draw.rect(SCREEN, semi_color, [color_x, color_y + 50, size, size], 0, shape)
    draw_text(my_font_xsm, "SEMI", sub_color, (text_x, color_y + 55))
    draw_text(my_font_xsm, "CORRECT", sub_color, (text_x, color_y + 75))

    # draws the wrong color circle and lable of color
    pygame.draw.rect(SCREEN, wrong_color, [color_x, color_y + 105, size, size], 0, shape)
    draw_text(my_font_xsm, "WRONG", sub_color, (text_x, color_y + 120))

    # draw reset colors button
    pygame.draw.rect(SCREEN, LT_GREY, RESET_COLORS, 0, ROUND)
    draw_text(my_font_sm, "Reset Colors", BLACK, (title_x, color_y + 185))

    pygame.draw.rect(SCREEN, LT_GREY, RESET_GAME, 0, ROUND)
    draw_text(my_font_sm, "Reset Game", BLACK, (title_x, color_y + 235))

    pygame.display.update()


# draws the navagation bar at the top of the screen and the contents on the bar
def draw_nav_bar():
    # actual nav bar
    pygame.draw.rect(SCREEN, sub_color2, [0, 0, WIDTH, 50], 0)

    # hamburger menu
    draw_icon('assets/menu.png', (30, 30), ((WIDTH - 825), 25))

    # font selector icon
    draw_icon('assets/font-icon.png', (30, 35), ((WIDTH - 40), 25))

    # color selector icon
    draw_icon('assets/color.png', (30, 30), ((WIDTH - 90), 25))

    # dark mode icon 
    draw_icon('assets/dark.png', (30, 30), ((WIDTH - 140), 25))

    # instructions icon
    draw_icon('assets/instructions.png', (30, 30), ((WIDTH - 190), 25))

    # Draws title of the application
    draw_text(my_font, "WORLD-LE", main_color, (WIDTH / 2, 25))

# FONT MENU

# Draws font options on the font menu
def draw_font_options():
    pygame.draw.rect(SCREEN, LT_BLUE, FONT_ONE_AREA, 0, ROUND)
    draw_text(pygame.font.Font('assets/fonts/FreeSans.otf', 30), "Free Sans Font", BLACK, (WIDTH / 2, HEIGHT - 570))

    pygame.draw.rect(SCREEN, LT_BLUE, FONT_TWO_AREA, 0, ROUND)
    draw_text(pygame.font.Font('assets/fonts/ComicSans.ttf', 30), "Comic Sans", BLACK, (WIDTH / 2, HEIGHT - 510))

    pygame.draw.rect(SCREEN, LT_BLUE, FONT_THREE_AREA, 0, ROUND)
    draw_text(pygame.font.Font('assets/fonts/GFSDidotBold.otf', 30), "GFS Didot Bold", BLACK, (WIDTH / 2, HEIGHT - 450))

    pygame.draw.rect(SCREEN, LT_BLUE, FONT_FOUR_AREA, 0, ROUND)
    draw_text(pygame.font.Font('assets/fonts/LilGrotesk.otf', 30), "Lil Grotesk", BLACK, (WIDTH / 2, HEIGHT - 390))

    pygame.draw.rect(SCREEN, LT_BLUE, FONT_FIVE_AREA, 0, ROUND)
    draw_text(pygame.font.Font('assets/fonts/WignersFriendRoman.ttf', 30), "Wigners Friend", BLACK, (WIDTH / 2, HEIGHT - 330))

    pygame.draw.rect(SCREEN, LT_BLUE, FONT_SIX_AREA, 0, ROUND)
    draw_text(pygame.font.Font('assets/fonts/FirstCoffee.otf', 30), "First Coffee", BLACK, (WIDTH / 2, HEIGHT - 265))

    # draw bold options
    pygame.draw.rect(SCREEN, sub_color2, BOLD_AREA, 0, ROUND)
    draw_text(pygame.font.Font('assets/fonts/FreeSansBold.otf', 30), "BOLD", WHITE, (WIDTH / 2, HEIGHT - 195))


# Draws the increase and decrease buttons on the font menu
def draw_font_size_adjust():
    pygame.draw.rect(SCREEN, GREY, PLUS_AREA, 0, ROUND)
    draw_text(my_font, "+", WHITE, ((WIDTH / 2) - 175, HEIGHT - 195))

    pygame.draw.rect(SCREEN, GREY, SUB_AREA, 0, ROUND)
    draw_text(my_font, "-", WHITE, ((WIDTH / 2) + 175, HEIGHT - 195))


# draws the font menu on the screen when the font change icon is selected
def draw_font_screen(current):
    value = current
    done = 0

    # draw background and front mini menu screens
    pygame.draw.rect(SCREEN, GREY, SM_MENU_AREA_BACK, 0, ROUND)
    pygame.draw.rect(SCREEN, main_color, SM_MENU_AREA_FRONT, 0, ROUND)

    # draw menu title
    draw_text(my_font, "Change Font", sub_color, (WIDTH / 2, (HEIGHT - (HEIGHT * 0.8)) / 2 + 45))

    # draw font options
    draw_font_options()

    # draw size increase / decrease buttons
    draw_font_size_adjust()

    # draw done button
    pygame.draw.rect(SCREEN, sub_color2, DONE_AREA, 0, ROUND)
    draw_text(my_font, "DONE", WHITE, (WIDTH / 2, HEIGHT - 125))

    pygame.display.update()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if FONT_ONE_AREA.collidepoint(event.pos):
                        value = 'assets/fonts/FreeSans.otf'
                        draw_font_options()
                        pygame.draw.rect(SCREEN, BLACK, FONT_ONE_AREA, 3, ROUND)
                    if FONT_TWO_AREA.collidepoint(event.pos):
                        value = 'assets/fonts/ComicSans.ttf'
                        draw_font_options()
                        pygame.draw.rect(SCREEN, BLACK, FONT_TWO_AREA, 3, ROUND)
                    if FONT_THREE_AREA.collidepoint(event.pos):
                        value = 'assets/fonts/GFSDidotBold.otf'
                        draw_font_options()
                        pygame.draw.rect(SCREEN, BLACK, FONT_THREE_AREA, 3, ROUND)
                    if FONT_FOUR_AREA.collidepoint(event.pos):
                        value = 'assets/fonts/LilGrotesk.otf'
                        draw_font_options()
                        pygame.draw.rect(SCREEN, BLACK, FONT_FOUR_AREA, 3, ROUND)
                    if FONT_FIVE_AREA.collidepoint(event.pos):
                        value = 'assets/fonts/WignersFriendRoman.ttf'
                        draw_font_options()
                        pygame.draw.rect(SCREEN, BLACK, FONT_FIVE_AREA, 3, ROUND)
                    if FONT_SIX_AREA.collidepoint(event.pos):
                        value = 'assets/fonts/FirstCoffee.otf'
                        draw_font_options()
                        pygame.draw.rect(SCREEN, BLACK, FONT_SIX_AREA, 3, ROUND)
                    if BOLD_AREA.collidepoint(event.pos):
                        value = 'assets/fonts/FreeSansBold.otf'
                        draw_font_options()
                        pygame.draw.rect(SCREEN, BLACK, BOLD_AREA, 3, ROUND)
                    if PLUS_AREA.collidepoint(event.pos):
                        increase_font_size()
                        draw_font_size_adjust()
                        pygame.draw.rect(SCREEN, BLACK, PLUS_AREA, 3, ROUND)
                    if SUB_AREA.collidepoint(event.pos):
                        decrese_font_size()
                        draw_font_size_adjust()
                        pygame.draw.rect(SCREEN, BLACK, SUB_AREA, 3, ROUND)
                    if DONE_AREA.collidepoint(event.pos):
                        done = 1
        pygame.display.update()

    return value

# COLOR MENU

# draw the color squares on the color menu
def draw_color_squrs():
    size = 75
    c_x = ((WIDTH - WIDTH * 0.6) / 2 + 70)
    c_y = (HEIGHT - HEIGHT * 0.8) / 2 + 125
    shift_amount = 100

    for i in range(4):
        for color in COLORS[i]:
            pygame.draw.rect(SCREEN, color, (c_x, c_y, size, size), 0, ROUND)
            c_x += shift_amount
        c_x = ((WIDTH - WIDTH * 0.6) / 2 + 70)
        c_y += shift_amount

    pygame.display.update()


# draws the color menu and controls the menu functionality, returns selected color
def draw_color_screen(current):
    value = current
    done = 0

    # draw background screen
    pygame.draw.rect(SCREEN, GREY, SM_MENU_AREA_BACK, 0, ROUND)
    # draw front screen
    pygame.draw.rect(SCREEN, main_color, SM_MENU_AREA_FRONT, 0, ROUND)

    # draw menu title
    draw_text(my_font, "Change Color", sub_color, (WIDTH / 2, (HEIGHT - (HEIGHT * 0.8)) / 2 + 45))

    # draw done button
    pygame.draw.rect(SCREEN, sub_color2, DONE_AREA, 0, ROUND)
    draw_text(my_font, "DONE", WHITE, (WIDTH / 2, HEIGHT - 125))

    # draw the color squares
    draw_color_squrs()

    COLOR_AREAS[1][1]

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(4):
                        for area, color in zip(COLOR_AREAS[i], COLORS[i]):
                            if area.collidepoint(event.pos):
                                value = color
                                draw_color_squrs()
                                pygame.draw.rect(SCREEN, sub_color, area, 3, ROUND)
                    if DONE_AREA.collidepoint(event.pos):
                        done = 1
                    pygame.display.update()
    return value


# draw screen where you select which color to change
def draw_select_color():
    done = 0

    # draw background screen and front ground screen
    pygame.draw.rect(SCREEN, GREY, SM_MENU_AREA_BACK, 0, ROUND)
    pygame.draw.rect(SCREEN, main_color, SM_MENU_AREA_FRONT, 0, ROUND)

    # draw menu title
    draw_text(my_font, "SELECT COLOR", sub_color, (WIDTH / 2, (HEIGHT - (HEIGHT * 0.85)) / 2 + 45))
    draw_text(my_font, "TO CHANGE", sub_color, (WIDTH / 2, (HEIGHT - (HEIGHT * 0.85)) / 2 + 90))

    # draw correct select button
    pygame.draw.rect(SCREEN, correct_color, PICK_ONE_AREA, 0, ROUND)
    draw_text(my_font_med, "Change Correct Color", BLACK, (WIDTH / 2, HEIGHT - 510))

    # draw semi correct select button
    pygame.draw.rect(SCREEN, semi_color, PICK_TWO_AREA, 0, ROUND)
    draw_text(my_font_med, "Change Semi Correct Color", BLACK, (WIDTH / 2, HEIGHT - 410))

    # draw wrong select button
    pygame.draw.rect(SCREEN, wrong_color, PICK_THREE_AREA, 0, ROUND)
    draw_text(my_font_med, "Change Wrong Color", BLACK, (WIDTH / 2, HEIGHT - 310))

    pygame.draw.rect(SCREEN, HIGH_CONTRAST_2, PICK_FOUR_AREA, 0, ROUND)
    draw_text(my_font_med, "Activate High Contrast Mode", BLACK, (WIDTH / 2, HEIGHT - 185))

    # draw cancel button
    pygame.draw.rect(SCREEN, sub_color2, CANCEL_AREA, 0, ROUND)
    draw_text(my_font_sm, "CANCEL", WHITE, (WIDTH / 2, HEIGHT - 100))

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


"""KEYBOARD"""

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


"""GENERAL GAME CONTROLS"""

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
    pygame.draw.rect(SCREEN, DK_RED, END_GAME_SCREEN_AREA, 0, ROUND)
    draw_text(my_font, "Press ENTER to Play Again!", WHITE, (WIDTH / 2, 320))
    draw_text(my_font, f"Sorry, the word was {correct_word}!", WHITE, (WIDTH / 2, 250))
    pygame.display.update()


# display winning screen and instructions for play again
def correct_play_again():
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, correct_color, END_GAME_SCREEN_AREA, 0, ROUND)
    draw_text(my_font, "Congratulations!", WHITE, (WIDTH / 2, 250))
    draw_text(my_font, f"The word was {correct_word}!", WHITE, (WIDTH / 2, 320))
    draw_text(my_font, "Press ENTER to Play Again!", WHITE, (WIDTH / 2, 390))
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

    if lang == "sp":
        word_list = SP_WORDS
    elif lang == "ger":
        word_list = GER_WORDS
    elif lang == "fr":
        word_list = FR_WORDS
    elif lang == "kid":
        word_list = KID_WORDS
    else:
        word_list = EN_WORDS

    correct_word = word_list[random.randint(0, len(word_list) - 1)]

    for key in keys:
        key.bg_color = sub_color2
        key.draw()

    draw_color_key()
    draw_nav_bar()

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


"""AUDIO CONTROL"""

# Uses gTTS to say the string 'response' in language 'language'
def say(response, language):
    obj = gTTS(text=response, lang=language, slow=False)
    obj.save("audio.mp3")
    try:
        # mac os version
        os.system("mpg123 audio.mp3")
    except Exception as e:
        # Windows version
        os.system("mpg123.exe audio.mp3")


# Uses SpeechRecognition to translate a user response to text. Returns text
def listen():
    global threshold_initialized

    r = sr.Recognizer()
    r.energy_threshold = 600
    mic = sr.Microphone()

    with mic as source:
        audio = r.listen(source)

    cur_text = r.recognize_google(audio)
    return cur_text


# Says each character in response individually.
def say_by_char(response, language):
    chars = [*response]
    for c in chars:
        say(c, language)
        time.sleep(0.025)


# This function takes in a guess, the correct answer, and a language. It then says each character in the guess
# and compares it to the correct answer. If the guess is correct, it plays a bell sound effect. If the guess is
# incorrect, it plays a buzzer sound effect. If the guess is in the word but at the incorrect index, it plays
# a different sound effect.
def say_and_confirm_by_char(guess, correct, language):
    chars = [*guess]
    correct = [*correct]
    correct_index = 0
    for c in chars:
        say(c, language)
        time.sleep(0.025)
        try:
            if c == correct[correct_index]:
                playsound('sound/effects/correct_char_trimmed.mp3')
            elif c in correct:
                playsound('sound/effects/semi_correct_char_trimmed.wav')
            else:
                playsound('sound/effects/incorrect_char_trimmed.wav')
        except Exception as e:
            print(str(e)+ "Something went wrong")
        correct_index = correct_index + 1


def song_switch_handler(command):
    command_split = command.split()
    keyword_index = return_keyword_index("song", command)
    value_index = keyword_index + 1
    value = word_to_int(command_split[value_index])
    if int(value) <= len(BACKGROUND_MUSIC):
        load_new_background_music(int(value) - 1)
    else:
        say("You must say a song number " + str(len(BACKGROUND_MUSIC)) +
            " or lower", languages[current_language])


def load_new_background_music(music_index):
    global current_background_music
    try:
        current_background_music = music_index
        mixer.music.pause()
        mixer.music.load(BACKGROUND_MUSIC[current_background_music])
        mixer.music.play(-1)
    except Exception as e:
        print(str(e) + "Something went wrong")


def play_background_music():
    try:
        mixer.music.play(-1)
    except Exception as e:
        print(str(e) + "Something went wrong")


def pause_background_music():
    try:
        mixer.music.pause()
    except Exception as e:
        print(str(e) + "Music never started, cannot pause")


def set_background_music_volume(level):
    try:
        mixer.music.set_volume(level)
    except Exception as e:
        print(str(e) + "Music not playing, cannot adjust volume")


def volume_handler(command):
    command_split = command.split()
    value_to_set = 0
    index = 0
    found = 0

    try:
        while not found:
            if command_split[index] == "volume":
                value_to_set = int(word_to_int(command_split[index + 1]))
                found = 1
            index += 1

        if value_to_set <= 10:
            set_background_music_volume(value_to_set / 100)
        else:
            say("You can only set volume between 0 and 10.", languages[current_language])

    except Exception as e:
        print(str(e) + "Something went wrong")


# Prevents sound effect repeat at end of game (eog) through the use of a state variable,
# eog_sound_allowed, which is only reset when game is reset
def eog_sound(current_game_result):
    global eog_sound_allowed
    if eog_sound_allowed:
        if current_game_result == "W":
            pause_background_music()
            try:
                playsound('sound/effects/correct_word_trimmed.mp3')
            except Exception as e:
                print(str(e) + "Something went wrong")
            eog_sound_allowed = 0
        elif current_game_result == "L":
            pause_background_music()
            try:
                playsound('sound/effects/no_more_guesses_trimmed.wav')
            except Exception as e:
                print(str(e) + "Something went wrong")
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
    elif fuzzy_char == "elle" or fuzzy_char == "el":
        return 'l'
    elif fuzzy_char == "oh":
        return 'o'
    elif fuzzy_char == "pea" or fuzzy_char == "pee":
        return 'p'
    elif fuzzy_char == "queue":
        return 'q'
    elif fuzzy_char == "are":
        return 'r'
    elif fuzzy_char == "ES":
        return 's'
    elif fuzzy_char == "tea" or fuzzy_char == "tee":
        return 't'
    elif fuzzy_char == "you":
        return 'u'
    elif fuzzy_char == "double you":
        return 'w'
    elif fuzzy_char == "ex" or fuzzy_char == "axe":
        return 'x'
    elif fuzzy_char == "why":
        return 'y'
    else:
        return fuzzy_char


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
    elif word == 'six':
        return 6
    elif word == 'seven':
        return 7
    elif word == 'eight':
        return 8
    elif word == 'nine':
        return 9
    elif word == 'ten':
        return 10
    else:
        return word


def clear_stash():
    delete_count = len(current_guess_string)
    while delete_count > 0:
        delete_letter()
        delete_count -= 1


# This function replaces a letter in the current guess string with another letter. Replace command handler
# for handsfree().
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


def return_keyword_index(keyword, command):
    index = 0
    found = 0
    command_split = command.split()

    try:
        while not found:
            if command_split[index] == keyword:
                return index
            index += 1
    except Exception as e:
        print(str(e))


# Listens for user command, validates the command, and calls the correct function to execute user command.
def handsfree():
    global current_guess_string, activate, audio_interface_enabled, has_warned

    waiting_for_command = 1
    while waiting_for_command:
        draw()
        try:
            # time.sleep(0.05)
            command = listen()
            # Comment above for debugging, allows typing of command; comment below for handsfree use;
            # command = input("Type a command: ")
            command = command.lower()
            command_split = command.split()
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
                draw()
                pygame.display.flip()
                waiting_for_command = 0
            elif "disable" in command:
                say("Disabling audio, press space bar twice to re-enable.", languages[current_language])
                activate = 0
                audio_interface_enabled = 0
                set_background_music_volume(0.1)
                waiting_for_command = 0
            elif "volume" in command:
                if has_warned or not audio_interface_enabled:
                    say("Adjusting volume.", languages[current_language])
                    volume_handler(command)
                else:
                    say(volume_warning, languages[current_language])
                    has_warned = 1
                waiting_for_command = 0
            elif "song" in command:
                say("Changing background song", languages[current_language])
                song_switch_handler(command)
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

            pygame.display.flip()

        except Exception as e:
            print("Exception: " + str(e))


# Identifies whether you are stashing a word or a character, calls the appropriate
# function or tells the user the input is invalid. Stash command handler for handsfree().
def stash(response):
    print("stash called")
    response_split = response.split(' ')

    guess = ""
    found = 0
    index = 0
    while not found:
        try:
            if response_split[index] == "stash" or response_split[index] == "dash":
                guess = fix_char(response_split[index + 1])
                found = 1
            else:
                index += 1
        except Exception as e:
            say("Remember to say a letter or five letter word after stash command.", languages[current_language])
            print(str(e))
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


# Takes stash command as an input and places new letter on the screen. Stash handler helper function.
def stash_char(char_to_stash):
    global key_pressed
    key_pressed = char_to_stash.upper()
    if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM":
        if len(current_guess_string) < 5:
            create_new_letter()
        else:
            say("your stash is full! submit or delete to guess more letters.", languages[current_language])


# Delete command handler for handsfree().
def delete():
    global current_guess_string
    if len(current_guess_string) > 0:
        letter_to_delete = current_guess_string[len(current_guess_string) - 1]
        say("Deleting " + letter_to_delete, languages[current_language])
        delete_letter()
    else:
        say("You dont have any letters to delete!", languages[current_language])


# Submit command handler for handsfree()
def submit():
    global current_guess_string, current_guess
    if len(current_guess_string) == 5 and current_guess_string.lower() in word_list:
        say_and_confirm_by_char(current_guess_string, correct_word.upper(), languages[current_language])
        check_guess(current_guess)
    else:
        say("your stash must contain a real five letter word, try again!", languages[current_language])


"""TRADITIONAL PLAY CONTROL"""

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


"""APPLICATION CONTROL"""

def start_the_game() -> None:
    global start_game, audio_interface_enabled, started, game_result, activate, current_guess_string, \
        key_pressed, rendered
    start_game = 1

    SCREEN.fill(main_color)
    print(correct_word)

    draw_keyboard()
    draw_color_key()
    draw_nav_bar()

    mixer.music.pause()
    mixer.music.load(BACKGROUND_MUSIC[current_background_music])
    mixer.music.play(-1)

    while True:
        # how program should run when audio interface is not enabled
        while not audio_interface_enabled and start_game:
            draw()
            if game_result == "L":
                lose_play_again()
                eog_sound(game_result)
            if game_result == "W":
                correct_play_again()
                eog_sound(game_result)
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
                        # check if any letter areas are selected
                        for i in range(3):
                            for area, letter in zip(LETTER_AREAS[i], ALPHABET[i]):
                                if area.collidepoint(event.pos):
                                    key_pressed = letter
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
                        if INFO_SEL_AREA.collidepoint(event.pos):
                            start_game = 0
                            instructions()
                        if FONT_SEL_AREA.collidepoint(event.pos):
                            chosen_font = draw_font_screen(font)
                            set_font(chosen_font)
                            reset_screen()
                        if COLOR_SEL_AREA.collidepoint(event.pos):
                            draw_select_color()
                            reset_screen()
                        if DARK_SEL_AREA.collidepoint(event.pos):
                            set_dark_mode()
                            reset_screen()
                        if RESET_COLORS.collidepoint(event.pos):
                            set_correct_color(GREEN)
                            set_semi_color(YELLOW)
                            set_wrong_color(GREY)
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
                        if RESET_GAME.collidepoint(event.pos):
                            reset()

            pygame.display.flip()

            if not started:
                say("STARTUP", languages[current_language])
                started = 1

        # how program should run when audio interface is enabled
        while audio_interface_enabled and start_game:
            draw()
            if game_result == "L":
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
                set_background_music_volume(0.025)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()

            rendered = 1


"""SETTERS"""

def set_background_music(selected: Tuple[Any, int], value: int) -> None:
    global current_background_music

    current_background_music = value


def set_language(selected: Tuple[Any, int], value: str) -> None:
    global lang, correct_word, word_list

    lang = value

    if lang == "sp":
        word_list = SP_WORDS
    elif lang == "ger":
        word_list = GER_WORDS
    elif lang == "fr":
        word_list = FR_WORDS
    elif lang == "kid":
        word_list = KID_WORDS
    else :
        word_list = EN_WORDS

    correct_word = word_list[random.randint(0, len(word_list) - 1)]


def menu_set_font(selected: Tuple[Any, int], value):
    global font, my_font, my_font_med, my_font_sm, my_font_xsm
    font = value
    my_font = pygame.font.Font(font, font_size)
    my_font_med = pygame.font.Font(font, font_size - 10)
    my_font_sm = pygame.font.Font(font, font_size - 20)
    my_font_xsm = pygame.font.Font(font, font_size - 25)


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
    global font, my_font, my_font_med, my_font_sm, my_font_xsm
    font = value
    my_font = pygame.font.Font(font, font_size)
    my_font_med = pygame.font.Font(font, font_size - 10)
    my_font_sm = pygame.font.Font(font, font_size - 20)
    my_font_xsm = pygame.font.Font(font, font_size - 25)


def decrese_font_size():
    global font_size
    if font_size - 25 > 5:
        font_size -= 3


def increase_font_size():
    global font_size
    if font_size < 50:
        font_size += 2


"""MENU"""

def background():
    SCREEN.fill(WHITE)


def menu():
    screen_difference = 50
    padding = 10

    # MENU THEMES
    mytheme = pygame_menu.themes.THEME_DARK.copy()
    # mytheme.background_color = pygame_menu.baseimage.BaseImage("assets/Background.png")
    mytheme.background_color = GREY
    mytheme.title_font = font
    mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    mytheme.title_offset = (WIDTH / 2 - 140, padding * 8)
    mytheme.title_font_color = WHITE
    mytheme.title_close_button_background_color = BLACK

    mytheme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
    mytheme.widget_font_color = WHITE
    mytheme.widget_font = font
    mytheme.widget_padding = padding
    mytheme.widget_margin = (0, 3)

    color_theme = pygame_menu.themes.THEME_GREEN.copy()
    color_theme.background_color = WHITE
    color_theme.title_font_color = WHITE
    color_theme.widget_font_color = BLACK
    color_theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()

    about_theme = color_theme.copy()
    about_theme.background_color = WHITE
    about_theme.title_font = font

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

    inst_menu.add.button("Back", pygame_menu.events.BACK)

    for m in SPACES:
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    # MAIN MENU PAGE
    menu.add.button('Play', start_the_game)
    menu.add.selector('Language: ', [("English", "en"), ("Spanish", "sp"), ("German", "ger"),
                                     ("French", "fr"), ("Kid Friendly", "kid")], onchange=set_language, default=0)
    menu.add.selector('Background Music: ', [("Traditional", 0), ("Happy Beat", 1), ("Bop", 2),
                                     ("Meditation", 3), ("Electric Chill", 4)], onchange=set_background_music, default=0)
    menu.add.selector('Change Font: ', [("Free Sans", 'assets/fonts/FreeSans.otf'), ("Comic Sans", 'assets/fonts/ComicSans.ttf'),
                                        ("Lil Grotesk", 'assets/fonts/LilGrotesk.otf'), ("GFS Didot", 'assets/fonts/GFSDidotBold.oft'),
                                        ("First Coffee", 'assets/fonts/FirstCoffee.otf'), ("Wigners Friend", 'assets/fonts/WignersFriendRoman.ttf')],
                                        onchange=menu_set_font, default=0)
    menu.add.button('Set Colors', color_menu)
    menu.add.button('Instructions', inst_menu)
    menu.add.button('About', about_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    if not start_game:
        menu.mainloop(SCREEN, background)


def instructions():
    global start_game
    start_game = 0
    screen_difference = 50

    mytheme = pygame_menu.themes.THEME_GREEN.copy()
    mytheme.background_color = WHITE
    mytheme.title_font_color = WHITE
    mytheme.title_font = font
    mytheme.widget_font_color = BLACK
    mytheme.widget_selection_effect = pygame_menu.widgets.NoneSelection()

    inst_menu = pygame_menu.Menu(
        height=HEIGHT - screen_difference,
        theme=mytheme,
        title='Game Instructions',
        width=WIDTH - screen_difference
    )

    # INSTRUCTIONS MENU PAGE
    inst_menu.add.button("Back to Game", start_the_game)

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

    inst_menu.add.button("Back to Game", start_the_game)

    for m in SPACES:
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    if not start_game:
        inst_menu.mainloop(SCREEN, background)


def main():
    play_background_music()
    menu()


if __name__ == "__main__":
    main()
