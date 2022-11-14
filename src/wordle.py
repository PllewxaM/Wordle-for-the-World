import pygame_menu
from typing import Tuple, Any
import pygame
from pygame import mixer
import sys
import random
import words
from words import *
import words2
from words2 import *
from gtts import gTTS
import speech_recognition as sr
import os
from playsound import playsound
import time


# INITIALIZERS AND GLOBAL VARIABLES #

pygame.init()
start_game = 0

# AUDIO INTERFACE
rendered = 0
started = 0
activate = 0
audio_interface_enabled = 0
threshold_initialized = 0

# MUSIC
# DOES NOT WORK WITH WINDOWS CAN UNCOMMENT FOR OTHER OS
mixer.init()
mixer.music.load('sound_effects/background_music.ogg')
mixer.music.set_volume(0.1)

# LANGUAGE
# Text-to-speech languages: English, Spanish, French
languages = ['en', 'es', 'fr']
current_language = 0

# Long sections of text used for instructing hands-free user
startup = "Welcome to wordle for the world, to activate the hands free version of the program, press " \
          "the space bar twice"
activated = "Audio interface activated, if you need help or a refresher on audio commands, say, " \
            "tutorial. To disable audio mode say disable."
wordle_tutorial = "Insert wordle tutorial here"
handsfree_tutorial = "Insert handsfree tutorial here"
stash_tutorial = "Insert stash tutorial/example here"
clear_tutorial = "The command clear will delete all the letters in your current guess stash"
read_tutorial = "Insert read tutorial/example here"
replace_tutorial = "Insert replace tutorial/example here"
submit_tutorial = "Insert submit tutorial/example here"


# select which file to get the word from based on user selection
lang = "en"  # change this to get from user/ui

CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]

# COLORS
RED = "#d90000"
REDORANGE = "#ff6100"
ORANGE = "#ff8600"
ORANGEYELLOW = "#ffc700"
YELLOW = "#c9b458"
YELLOWGREEN = "#a8d800"
GREEN = "#6aaa64"
GREENBLUE = "#00D9C5"
BLUE = "#0085FF"
BLUEPURPLE = "#623CED"
PURPLE = "#9150F3"
PURPLEPINK = "#B912F4"
PINK = "#FB00FF"
REDPINK = "#FF0081"
GREY = "#787c7e"
LT_GREY = "#abadaf"
WHITE = "#ffffff"
BLACK = "#000000"


# CHANGE THESE TO GET FROM USER
CORRECT_COLOR = YELLOWGREEN
SEMI_COLOR = PINK
WRONG_COLOR = BLUEPURPLE

# FONT
FONT = pygame.font.Font("assets/FreeSans.otf", 40)
FONT_MED = pygame.font.Font("assets/FreeSans.otf", 30)
FONT_SM = pygame.font.Font("assets/FreeSans.otf", 20)
FONT_XSM = pygame.font.Font("assets/FreeSans.otf", 15)

# SCREEN
WIDTH, HEIGHT = 850, 750
WINDOW_SIZE = (850, 750)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("World-le")
pygame.display.set_icon(pygame.image.load("assets/Icon.png"))
pygame.display.update()

# KEYBOARD
ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
keys = []
key_pressed = ''

# GAME BOARD
LETTER_X_SPACING = 65
LETTER_Y_SPACING = 70
LETTER_SIZE = 60

BOARD = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]


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
current_letter_bg_x = WIDTH/3.25

game_result = ""


# FUNCTIONS #

# GAME BOARD

def draw():
    for col in range(0, 5):
        for row in range(0, 6):
            # change + values to adjust board positioning
            pygame.draw.rect(SCREEN, BLACK, [col * LETTER_X_SPACING + WIDTH/3.25,
                                             row * LETTER_Y_SPACING + 70, 60, 60], 1, 1)


def draw_color_key():
    key_width, key_height = 155, 225
    pygame.draw.rect(SCREEN, BLACK, [WIDTH - 170, 70, key_width, key_height], 1, 5)
    color_text = FONT_SM.render("Color Key", True, BLACK)
    color_rect = color_text.get_rect(center=(WIDTH - 185/2, 95))
    SCREEN.blit(color_text, color_rect)

    color_x = WIDTH - 155
    color_y = 130
    size = 30
    shape = 100
    text_x = WIDTH - 70

    pygame.draw.rect(SCREEN, CORRECT_COLOR, [color_x, color_y, size, size], shape, shape)
    correct_text = FONT_XSM.render("CORRECT", True, BLACK)
    correct_rect = correct_text.get_rect(center=(text_x, color_y + 15))
    SCREEN.blit(correct_text, correct_rect)

    pygame.draw.rect(SCREEN, SEMI_COLOR, [color_x, color_y + 50, size, size], shape, shape)
    semi_text = FONT_XSM.render("SEMI", True, BLACK)
    semi_rect = semi_text.get_rect(center=(text_x, color_y + 55))
    SCREEN.blit(semi_text, semi_rect)
    semi_text = FONT_XSM.render("CORRECT", True, BLACK)
    semi_rect = semi_text.get_rect(center=(text_x, color_y + 75))
    SCREEN.blit(semi_text, semi_rect)

    pygame.draw.rect(SCREEN, WRONG_COLOR, [color_x, color_y + 105, size, size], shape, shape)
    wrong_text = FONT_XSM.render("WRONG", True, BLACK)
    wrong_rect = wrong_text.get_rect(center=(text_x, color_y + 120))
    SCREEN.blit(wrong_text, wrong_rect)

    pygame.display.update()


def draw_nav_bar():
    pygame.draw.rect(SCREEN, LT_GREY, [0, 0, WIDTH, 50], 100)
    pygame.draw.rect(SCREEN, BLACK, [10, 10, 30, 30], 100)
    header_text = FONT.render("WORLDLE", True, WHITE)
    header_rect = header_text.get_rect(center=(WIDTH/2, 25))
    SCREEN.blit(header_text, header_rect)


# draws letters on the board as user enters them
class Letter:
    # DO NOT CHANGE ANY OF THIS TO ADJUST BOARD POSITIONING
    def __init__(self, text, bg_position):
        # Initializes all the variables, including text, color, position, size, etc.
        self.bg_color = WHITE
        self.text_color = BLACK
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], bg_position[1], LETTER_SIZE, LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x + 30, self.bg_y + 30)
        self.text_surface = FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == WHITE:
            pygame.draw.rect(SCREEN, GREY, self.bg_rect, 3)
        self.text_surface = FONT.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(SCREEN, WHITE, self.bg_rect)
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
        self.bg_color = LT_GREY

    def draw(self):
        # Puts the key and its text on the screen at the desired position.
        pygame.draw.rect(SCREEN, self.bg_color, self.rect, 100, 4)
        self.text_surface = FONT.render(self.text, True, WHITE)
        self.text_rect = self.text_surface.get_rect(center=(self.x + (self.width/2), self.y + (self.height/2)))
        SCREEN.blit(self.text_surface, self.text_rect)
        # pygame.display.update()


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
        self.bg_color = LT_GREY

    def draw(self):
        pygame.draw.rect(SCREEN, self.bg_color, self.rect, 100, 4)
        self.text_surface = FONT_MED.render(self.text, True, WHITE)
        self.text_rect = self.text_surface.get_rect(center=(self.x + (self.width/2), self.y + (self.height/2)))
        SCREEN.blit(self.text_surface, self.text_rect)
        # pygame.display.update()


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
        if lowercase_letter in CORRECT_WORD:
            if lowercase_letter == CORRECT_WORD[i]:
                guess_to_check[i].bg_color = CORRECT_COLOR
                add_correct(lowercase_letter)
                for key in keys:
                    if key.text == lowercase_letter.upper():
                        key.bg_color = CORRECT_COLOR
                        key.draw()
                guess_to_check[i].text_color = WHITE
                if not game_decided:
                    game_result = "W"
            else:
                guess_to_check[i].bg_color = SEMI_COLOR
                add_semi(lowercase_letter)
                for key in keys:
                    if key.text == lowercase_letter.upper():
                        key.bg_color = SEMI_COLOR
                        key.draw()
                guess_to_check[i].text_color = WHITE
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = GREY
            add_incorrect(lowercase_letter)
            for key in keys:
                if key.text == lowercase_letter.upper():
                    key.bg_color = WRONG_COLOR
                    key.draw()
            guess_to_check[i].text_color = WHITE
            game_result = ""
            game_decided = True
        guess_to_check[i].draw()
        pygame.display.update()

    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = WIDTH/3.25

    if guesses_count == 6 and game_result == "":
        game_result = "L"


# display loosing screen and call reset
def lose_play_again():
    # Puts the play again text on the screen.
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, RED, (10, 10, WIDTH - 20, HEIGHT - 20))
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 320))
    word_was_text = play_again_font.render(f"Sorry, the word was {CORRECT_WORD}!", True, WHITE)
    word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 250))
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()


# display winning screen and call reset
def correct_play_again():
    # Puts the play again text on the screen.
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, CORRECT_COLOR, (10, 10, WIDTH - 20, HEIGHT - 20))
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    con_text = play_again_font.render(f"Congratulations!", True, WHITE)
    con_rect = con_text.get_rect(center=(WIDTH/2, 250))
    word_was_text = play_again_font.render(f"The word was {CORRECT_WORD}!", True, WHITE)
    word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 320))
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 390))

    SCREEN.blit(con_text, con_rect)
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()


# reset global variables
def reset():
    # Resets all global variables to their default states.
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result, lang, \
        semi_correct_guesses, correct_guesses, incorrect_guesses
    SCREEN.fill(WHITE)

    guesses_count = 0
    guesses = [[]] * 6
    current_guess = []
    current_guess_string = ""
    game_result = ""
    incorrect_guesses = []
    correct_guesses = []
    semi_correct_guesses = []

    if lang == "en":
        CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
    elif lang == "sp":
        CORRECT_WORD = words2.WORDS2[random.randint(0, len(words2.WORDS2) - 1)]
    elif lang == "ger":
        CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
    elif lang == "fr":
        CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
    elif lang == "kid":
        CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]

    for key in keys:
        key.bg_color = LT_GREY
        key.draw()

    draw_color_key()
    draw_nav_bar()

    # Comment out below for windows (For now!! must fix)
    mixer.music.play(-1)

    pygame.display.update()


# AUDIO CONTROL

# Uses gTTS to say the string 'response' in language 'language'
def say(response, language):
    obj = gTTS(text=response, lang=language, slow=False)
    obj.save("audio.mp3")
    os.system("mpg123 audio.mp3")
    # Windows version comment above, uncomment below
    # os.system("mpg123.exe audio.mp3")


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
        if c == correct[correct_index]:
            playsound('sound_effects/correct_char_trimmed.mp3')
        elif c in correct:
            playsound('sound_effects/semi_correct_char_trimmed.wav')
        else:
            playsound('sound_effects/incorrect_char_trimmed.wav')
        correct_index = correct_index + 1


# Control for common letter misinterpretations. Called if word returned to 'stash' instead of a char
# Returns a character if possible, if none found, returns original word.
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
        return fuzzy_char    # add more if found


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


def replace(response):
    global current_guess_string
    char_to_replace = ''
    replacement = ''

    # find char_to_replace and replacement in response
    response = response.split(' ')
    index = 0
    found = 0
    while not found:
        if response[index] == "replace":
            char_to_replace = response[index + 1]
            replacement = response[index + 3]
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
        say_and_confirm_by_char(guesses_str[guess_number - 1], CORRECT_WORD.upper(), languages[current_language])


def handsfree():
    global current_guess_string, activate, audio_interface_enabled

    waiting_for_command = 1
    while waiting_for_command:
        try:
            time.sleep(0.05)
            command = listen()
            command = command.lower()
            print(command)

            if "tutorial" in command:  # Starts tutorial
                say("say word for wordle tutorial, say free for handsfree tutorial", languages[current_language])
                response = listen()
                if "word" in response:
                    say(wordle_tutorial, languages[current_language])
                elif "free" in response:
                    say(handsfree_tutorial, languages[current_language])
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
            if response_split[index] == "stash":
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
    if len(current_guess_string) == 5 and current_guess_string.lower() in WORDS:
        say_and_confirm_by_char(current_guess_string, CORRECT_WORD.upper(), languages[current_language])
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


def start_the_game() -> None:
    global start_game, audio_interface_enabled, started, game_result, activate, current_guess_string, \
        key_pressed, rendered, activated
    start_game = 1

    SCREEN.fill(WHITE)
    print(CORRECT_WORD)
    print(lang)

    draw_keyboard()
    draw_color_key()
    draw_nav_bar()

    # make keyboard areas - so click on screen activates letter
    q_area = pygame.Rect(125, 500, 57, 70)
    w_area = pygame.Rect(185, 500, 57, 70)
    e_area = pygame.Rect(245, 500, 57, 70)
    r_area = pygame.Rect(305, 500, 57, 70)
    t_area = pygame.Rect(365, 500, 57, 70)
    y_area = pygame.Rect(425, 500, 57, 70)
    u_area = pygame.Rect(485, 500, 57, 70)
    i_area = pygame.Rect(545, 500, 57, 70)
    o_area = pygame.Rect(605, 500, 57, 70)
    p_area = pygame.Rect(665, 500, 57, 70)
    a_area = pygame.Rect(160, 585, 57, 70)
    s_area = pygame.Rect(220, 585, 57, 70)
    d_area = pygame.Rect(280, 585, 57, 70)
    f_area = pygame.Rect(340, 585, 57, 70)
    g_area = pygame.Rect(400, 585, 57, 70)
    h_area = pygame.Rect(460, 585, 57, 70)
    j_area = pygame.Rect(520, 585, 57, 70)
    k_area = pygame.Rect(580, 585, 57, 70)
    l_area = pygame.Rect(640, 585, 57, 70)
    z_area = pygame.Rect(210, 670, 57, 70)
    x_area = pygame.Rect(270, 670, 57, 70)
    c_area = pygame.Rect(330, 670, 57, 70)
    v_area = pygame.Rect(390, 670, 57, 70)
    b_area = pygame.Rect(450, 670, 57, 70)
    n_area = pygame.Rect(510, 670, 57, 70)
    m_area = pygame.Rect(570, 670, 57, 70)
    enter_area = pygame.Rect(635, 670, 125, 70)
    de_area = pygame.Rect(100, 670, 102, 70)

    menu_area = pygame.Rect(10, 10, 30, 30)

    while True:
        # how program should run when audio interface is not enabled
        while not audio_interface_enabled and start_game:
            draw()
            # Comment out below for windows (For now! must fix)
            mixer.music.set_volume(0.1)
            if game_result == "L":
                lose_play_again()
            if game_result == "W":
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
                            if len(current_guess_string) == 5 and current_guess_string.lower() in WORDS:
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
                        if q_area.collidepoint(event.pos):
                            key_pressed = "Q"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if w_area.collidepoint(event.pos):
                            key_pressed = "W"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if e_area.collidepoint(event.pos):
                            key_pressed = "E"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if r_area.collidepoint(event.pos):
                            key_pressed = "R"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if t_area.collidepoint(event.pos):
                            key_pressed = "T"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if y_area.collidepoint(event.pos):
                            key_pressed = "Y"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if u_area.collidepoint(event.pos):
                            key_pressed = "U"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if i_area.collidepoint(event.pos):
                            key_pressed = "I"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if o_area.collidepoint(event.pos):
                            key_pressed = "O"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if p_area.collidepoint(event.pos):
                            key_pressed = "P"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if a_area.collidepoint(event.pos):
                            key_pressed = "A"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if s_area.collidepoint(event.pos):
                            key_pressed = "S"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if d_area.collidepoint(event.pos):
                            key_pressed = "D"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if f_area.collidepoint(event.pos):
                            key_pressed = "F"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if g_area.collidepoint(event.pos):
                            key_pressed = "G"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if h_area.collidepoint(event.pos):
                            key_pressed = "H"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if j_area.collidepoint(event.pos):
                            key_pressed = "J"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if k_area.collidepoint(event.pos):
                            key_pressed = "K"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if l_area.collidepoint(event.pos):
                            key_pressed = "L"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if z_area.collidepoint(event.pos):
                            key_pressed = "Z"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if x_area.collidepoint(event.pos):
                            key_pressed = "X"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if c_area.collidepoint(event.pos):
                            key_pressed = "C"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if v_area.collidepoint(event.pos):
                            key_pressed = "V"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if b_area.collidepoint(event.pos):
                            key_pressed = "B"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if n_area.collidepoint(event.pos):
                            key_pressed = "N"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if m_area.collidepoint(event.pos):
                            key_pressed = "M"
                            if len(current_guess_string) < 5:
                                create_new_letter()
                        if enter_area.collidepoint(event.pos):
                            if len(current_guess_string) == 5 and current_guess_string.lower() in WORDS:
                                check_guess(current_guess)
                        if de_area.collidepoint(event.pos):
                            if len(current_guess_string) > 0:
                                delete_letter()
                        if menu_area.collidepoint(event.pos):
                            start_game = 0
                            menu()

            pygame.display.flip()

            # if not started:
            #     say(startup, languages[current_language])
            #     started = 1

        # how program should run when audio interface is enabled
        while audio_interface_enabled and start_game:
            draw()
            if game_result == "L":
                # Comment out below for windows
                mixer.music.pause()
                playsound('sound_effects/no_more_guesses_trimmed.wav')
                say("You have run out of guesses. The word was " + CORRECT_WORD + " say play again to start over with "
                    "a new word!", languages[current_language])
                lose_play_again()
            if game_result == "W":
                say("correct", languages[current_language])
                playsound('sound_effects/correct_word_trimmed.mp3')
                say("the word was: " + CORRECT_WORD + ". say play again to get "
                                                      "a new word.", languages[current_language])
                correct_play_again()
            if rendered:
                handsfree()
            else:
                # mixer.music.play()
                pygame.display.flip()
                say(activated, languages[current_language])
                time.sleep(0.1)
                mixer.music.set_volume(0.025)
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
                            if len(current_guess_string) == 5 and current_guess_string.lower() in WORDS:
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


def set_language(selected: Tuple[Any, int], value: str) -> None:
    global lang, CORRECT_WORD

    lang = value

    if lang == "sp":
        CORRECT_WORD = words2.WORDS2[random.randint(0, len(words2.WORDS2) - 1)]
    elif lang == "ger":
        CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
    elif lang == "fr":
        CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
    elif lang == "kid":
        CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]


# def set_correct_color(value):

# def set_semi_color(value):

# def set_wrong_color(value):

def background():
    SCREEN.fill(WHITE)


def menu():
    mytheme = pygame_menu.themes.THEME_GREEN.copy()
    mytheme.background_color = pygame_menu.baseimage.BaseImage("assets/Background.png")
    mytheme.title_font = "assets/FreeSans.otf"
    mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    mytheme.title_offset = (WIDTH/2 - 155, 80)
    mytheme.title_font_color = BLACK
    mytheme.title_close_button_background_color = BLACK
    
    mytheme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
    mytheme.widget_font_color = BLACK
    mytheme.widget_font = "assets/FreeSans.otf"
    mytheme.widget_padding = 10
    mytheme.widget_margin = (0, 3)
    
    about_theme = pygame_menu.themes.THEME_GREEN.copy()
    about_theme.title_close_button_background_color = BLACK
    about_theme.title_offset = (20, 10)
    about_theme.background_color = pygame_menu.baseimage.BaseImage("assets/Background.png")
    about_theme.title_font = "assets/FreeSans.otf"
    about_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    about_theme.title_font_color = BLACK
    about_theme.title_close_button_background_color = BLACK

    inst_theme = about_theme

    about_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] - 100,
        theme=about_theme,
        title='About',
        width=WINDOW_SIZE[0] - 100
    )

    inst_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] - 100,
        theme=inst_theme,
        title='Instructions',
        width=WINDOW_SIZE[0] - 100
    )

    menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] - 100,
        theme=mytheme,
        title='WORLD-LE',
        width=WINDOW_SIZE[0] - 100
    )

    menu.add.button('Play', start_the_game)
    menu.add.selector('Language: ', [("English", "en"), ("Spanish", "sp"), ("German", "ger"),
                                     ("French", "fr"), ("Kid Friendly", "kid")], onchange=set_language, default=0)
    menu.add.button('Instructions', inst_menu)
    menu.add.button('About', about_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    
    about_menu.add.button('Quit', pygame_menu.events.EXIT)

    if not start_game:
        menu.mainloop(SCREEN, background)


# Comment out below for windows (for now!! must fix)
mixer.music.play(-1)

menu()
