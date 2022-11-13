import pygame
from pygame.locals import *
from pygame import mixer
import sys
import random
import words
from words import *
from gtts import gTTS
import speech_recognition as sr
import os
from playsound import playsound
import time

# Game initializers
pygame.init()
rendered = 0

# Audio Interface Initializers
audio_interface_enabled = 1
threshold_initialized = 0
mixer.init()
mixer.music.load('sound_effects/background_music.ogg')
mixer.music.set_volume(0.1)

# Text-to-speech languages: English, Spanish, French
languages = ['en', 'es', 'fr']
current_language = 0

# Long sections of text used for instructing hands-free user
startup = "Welcome to wordle for the world, if you need help, say, tutorial"
wordle_tutorial = "Insert wordle tutorial here"
handsfree_tutorial = "Insert handsfree tutorial here"
stash_tutorial = "Insert stash tutorial/example here"
clear_tutorial = "The command clear will delete all the letters in your current guess stash"
read_tutorial = "Insert read tutorial/example here"
replace_tutorial = "Insert replace tutorial/example here"
submit_tutorial = "Insert submit tutorial/example here"

# COLORS
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"

WIDTH, HEIGHT = 700, 750

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill(WHITE)
pygame.display.set_caption("World-le")
pygame.display.set_icon(pygame.image.load("assets/Icon.png"))
pygame.display.update()

lang = "en"

if lang == "en":
    CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
elif lang == "sp":
    CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
elif lang == "ger":
    CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
elif lang == "fr":
    CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
elif lang == "kid":
    CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]

FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
FONT_SM = pygame.font.Font("assets/FreeSansBold.otf", 30)
LETTER_X_SPACING = 65
LETTER_Y_SPACING = 10
LETTER_SIZE = 60

BOARD = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]

ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
keys = []

guesses_count = 0
guesses = [[]] * 6
guesses_str = []    # when each guess is to be checked, the text version will be placed here

correct_guesses = []
incorrect_guesses = []
semicorrect_guesses = []
remaining_guesses = []

current_guess = []
current_guess_string = ""
current_letter_bg_x = 175

game_result = ""


# Uses gTTS to say the string 'response' in language 'language'
def say(response, language):
    obj = gTTS(text=response, lang=language, slow=False)
    obj.save("audio.mp3")
    os.system("mpg123 audio.mp3")


# Uses SpeechRecognition to translate a user response to text. Returns text
def listen():
    global threshold_initialized

    r = sr.Recognizer()
    r.energy_threshold = 750
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
            playsound('sound_effects/semi_correct_char_trimmed.wav')  # choose a knock & trim
        else:
            playsound('sound_effects/incorrect_char_trimmed.wav')
        correct_index = correct_index + 1


# Ask people to say the alphabet after the word stash. Find out
# the most common mishearings and fix them. Called when a word is returned to
# 'stash' function instead of a character. Returns a character if possible, if
# none found, it returns the same thing.
def fix_char(fuzzy_char):
    if fuzzy_char == "see":
        return 'c'
    elif fuzzy_char == "oh":
        return 'o'
    elif fuzzy_char == "ES":
        return 's'
    elif fuzzy_char == "tea":
        return 't'
    elif fuzzy_char == "you":
        return 'u'
    elif fuzzy_char == "too":
        return '2'
    elif fuzzy_char == "four":
        return '4'
    elif fuzzy_char == "for":
        return '4'
    else:
        return fuzzy_char
    # add more as needed


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


def add_semi(char):
    global semicorrect_guesses
    if char not in semicorrect_guesses:
        semicorrect_guesses.append(char)


def add_incorrect(char):
    global incorrect_guesses
    if char not in incorrect_guesses:
        incorrect_guesses.append(char)


def add_correct(char):
    global correct_guesses
    if char not in correct_guesses:
        correct_guesses.append(char)


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
    global current_guess_string

    waiting_for_command = 1
    while waiting_for_command:
        try:
            time.sleep(0.15)
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
                    say_by_char(semicorrect_guesses, languages[current_language])
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


# draw squares
def draw():
    for col in range(0, 5):
        for row in range(0, 6):
            pygame.draw.rect(SCREEN, BLACK, [col * 65 + 175, row * 70 + 10, 60, 60], 1, 1)
            piece_text = FONT.render(BOARD[row][col], True, GREY)
            SCREEN.blit(piece_text, (col * 100 + 10, row * 100 + 15))


# draw and handle keyboard
class KeyButton:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 57, 70)
        self.bg_color = OUTLINE

    def draw(self):
        # Puts the key and its text on the screen at the desired position.
        pygame.draw.rect(SCREEN, self.bg_color, self.rect)
        self.text_surface = FONT.render(self.text, True, "white")
        self.text_rect = self.text_surface.get_rect(center=(self.x+27, self.y+30))
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()


class BigKeyButton:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 102, 70)
        self.bg_color = OUTLINE

    def draw_big(self):
        pygame.draw.rect(SCREEN, self.bg_color, self.rect)
        self.text_surface = FONT_SM.render(self.text, True, "white")
        self.text_rect = self.text_surface.get_rect(center=(self.x+50, self.y+35))
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()


key_x, key_y = 45, 450

for i in range(3):
    for letter in ALPHABET[i]:
        new_key = KeyButton(key_x, key_y, letter)
        keys.append(new_key)
        new_key.draw()
        key_x += 60
    key_y += 85
    if i == 0:
        key_x = 80
    elif i == 1:
        key_x = 130
new_key = BigKeyButton(20, 620, "DEL")
new_key.draw_big()
new_key = BigKeyButton(555, 620, "ENTER")
new_key.draw_big()

q_area = pygame.Rect(45, 450, 57, 70)
w_area = pygame.Rect(105, 450, 57, 70)
e_area = pygame.Rect(165, 450, 57, 70)
r_area = pygame.Rect(225, 450, 57, 70)
t_area = pygame.Rect(285, 450, 57, 70)
y_area = pygame.Rect(345, 450, 57, 70)
u_area = pygame.Rect(405, 450, 57, 70)
i_area = pygame.Rect(465, 450, 57, 70)
o_area = pygame.Rect(525, 450, 57, 70)
p_area = pygame.Rect(585, 450, 57, 70)
a_area = pygame.Rect(80, 535, 57, 70)
s_area = pygame.Rect(140, 535, 57, 70)
d_area = pygame.Rect(200, 535, 57, 70)
f_area = pygame.Rect(260, 535, 57, 70)
g_area = pygame.Rect(320, 535, 57, 70)
h_area = pygame.Rect(380, 535, 57, 70)
j_area = pygame.Rect(440, 535, 57, 70)
k_area = pygame.Rect(500, 535, 57, 70)
l_area = pygame.Rect(560, 535, 57, 70)
z_area = pygame.Rect(130, 620, 57, 70)
x_area = pygame.Rect(190, 620, 57, 70)
c_area = pygame.Rect(250, 620, 57, 70)
v_area = pygame.Rect(310, 620, 57, 70)
b_area = pygame.Rect(370, 620, 57, 70)
n_area = pygame.Rect(430, 620, 57, 70)
m_area = pygame.Rect(490, 620, 57, 70)
enter_area = pygame.Rect(555, 620, 102, 70)
de_area = pygame.Rect(20, 620, 102, 70)


class Letter:
    def __init__(self, text, bg_position):
        # Initializes all the variables, inclinkuding text, color, position, size, etc.
        self.bg_color = "white"
        self.text_color = "black"
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
        if self.bg_color == "white":
            pygame.draw.rect(SCREEN, FILLED_OUTLINE, self.bg_rect, 3)
        self.text_surface = FONT.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(SCREEN, "white", self.bg_rect)
        pygame.draw.rect(SCREEN, OUTLINE, self.bg_rect, 3)
        pygame.display.update()


def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    global current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result
    game_decided = False
    guesses_str.append(current_guess_string)
    for i in range(5):
        lowercase_letter = guess_to_check[i].text.lower()
        if lowercase_letter in CORRECT_WORD:
            if lowercase_letter == CORRECT_WORD[i]:
                guess_to_check[i].bg_color = GREEN
                add_correct(lowercase_letter)
                for key in keys:
                    if key.text == lowercase_letter.upper():
                        key.bg_color = GREEN
                        key.draw()
                guess_to_check[i].text_color = "white"
                if not game_decided:
                    game_result = "W"
            else:
                guess_to_check[i].bg_color = YELLOW
                add_semi(lowercase_letter)
                for key in keys:
                    if key.text == lowercase_letter.upper():
                        key.bg_color = YELLOW
                        key.draw()
                guess_to_check[i].text_color = "white"
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = GREY
            add_incorrect(lowercase_letter)
            for key in keys:
                if key.text == lowercase_letter.upper():
                    key.bg_color = GREY
                    key.draw()
            guess_to_check[i].text_color = "white"
            game_result = ""
            game_decided = True
        guess_to_check[i].draw()
        pygame.display.update()
    
    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = 175

    if guesses_count == 6 and game_result == "":
        game_result = "L"


def lose_play_again():
    # Puts the play again text on the screen.
    pygame.draw.rect(SCREEN, "red", (10, 10, 680, 730))
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "white")
    play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 320))
    word_was_text = play_again_font.render(f"Sorry, the word was {CORRECT_WORD}!", True, "white")
    word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 250))
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()


def correct_play_again():
    # Puts the play again text on the screen.
    pygame.draw.rect(SCREEN, GREEN, (10, 10, 680, 730))
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    con_text = play_again_font.render(f"Congratulations!", True, "white")
    con_rect = con_text.get_rect(center=(WIDTH/2, 250))
    word_was_text = play_again_font.render(f"The word was {CORRECT_WORD}!", True, "white")
    word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 320))
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "white")
    play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 390))
    
    SCREEN.blit(con_text, con_rect)
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()


def reset():
    # Resets all global variables to their default states.
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result, lang
    SCREEN.fill("white")
    guesses_count = 0
    if lang == "en":
        CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
    elif lang == "sp":
        CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
    elif lang == "ger":
        CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
    elif lang == "fr":
        CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
    elif lang == "kid":
        CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
    guesses = [[]] * 6
    current_guess = []
    current_guess_string = ""
    game_result = ""
    pygame.display.update()
    for key in keys:
        key.bg_color = OUTLINE
        key.draw()


def create_new_letter():
    # Creates a new letter and adds it to the guess.
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count * 70 + LETTER_Y_SPACING))
    current_letter_bg_x += LETTER_X_SPACING
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()


def delete_letter():
    # Deletes the last letter from the guess.
    global current_guess_string, current_letter_bg_x
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()
    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_letter_bg_x -= LETTER_X_SPACING


# Identifies whether you are stashing a word or a character, calls the appropriate
# function or tells the user the input is invalid.
def stash(response):
    print("stash called")
    response_split = response.split(' ')

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


def delete():
    global current_guess_string
    if len(current_guess_string) > 0:
        letter_to_delete = current_guess_string[len(current_guess_string) - 1]
        say("Deleting " + letter_to_delete, languages[current_language])
        delete_letter()
    else:
        say("You dont have any letters to delete!", languages[current_language])


def submit():
    global current_guess_string, current_guess
    if len(current_guess_string) == 5 and current_guess_string.lower() in WORDS:
        say_and_confirm_by_char(current_guess_string, CORRECT_WORD.upper(), languages[current_language])
        check_guess(current_guess)
    else:
        say("your stash must contain a real five letter word, try again!", languages[current_language])


while not audio_interface_enabled:
    draw()
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

    pygame.display.flip()

while audio_interface_enabled:
    draw()
    # Game loss event
    if game_result == "L":
        mixer.music.pause()
        playsound('sound_effects/no_more_guesses_trimmed.wav')
        say("You have run out of guesses. say play again to start over with a new word!", languages[current_language])
        lose_play_again()
    # Game win event
    if game_result == "W":
        say("correct", languages[current_language])
        playsound('sound_effects/correct_word_trimmed.mp3')
        say("the word was: " + CORRECT_WORD + ". say play agian to get a new word.", languages[current_language])
        correct_play_again()
    # Allows fully drawn buffer to be shown to the user during startup
    if rendered:
        handsfree()
    else:
        mixer.music.play(-1)
        pygame.display.flip()  # Buffer flip
        say(startup, languages[current_language])
        time.sleep(0.1)
        mixer.music.set_volume(0.025)

    # Handle pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_result != "":
                    reset()
                else:   # Check current guess
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
