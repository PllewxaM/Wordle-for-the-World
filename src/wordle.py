import pygame
import pygame_menu
import sys
import random
import speech_recognition as sr
import os
import time

from pygame import mixer
from gtts import gTTS
from playsound import playsound

from word_files.englishwords import *
from word_files.spanishwords import *
from word_files.frenchwords import *
from word_files.germanwords import *
from word_files.kidwords import *

from messages import *
from constants import *
from draw import *
from classes import *

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
    mixer.music.set_volume(0.2)
except Exception as e:
    print(str(e) + "Something went wrong")

eog_sound_allowed = 1

# LANGUAGE
current_language = 0

# default
lang = "en"
word_list = EN_WORDS
check_list = EN_WORDS
correct_word = word_list[random.randint(0, len(word_list) - 1)]
about_display = ABOUT_ENGLISH
instructions1_display = INSTRUCTIONS1_ENGLISH
instructions2_display = INSTRUCTIONS2_ENGLISH
instructions3_display = INSTRUCTIONS3_ENGLISH
color_instructions_display = COLOR_INSTRUCTIONS_ENGLISH
lang_index = 0

# DEFAULT COLORS
correct_color = GREEN
semi_color = YELLOW
wrong_color = GREY

main_color = WHITE
sub_color = BLACK
sub_color2 = LT_GREY

# FONT DEFAULTS
font_size = 40
font_index = 0
my_font = pygame.font.Font(FONTS[font_index], font_size)
my_font_med = pygame.font.Font(FONTS[font_index], font_size - 10)
my_font_sm = pygame.font.Font(FONTS[font_index], font_size - 20)
my_font_xsm = pygame.font.Font(FONTS[font_index], font_size - 25)

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
game_result = ""

current_letter_bg_x = WIDTH / 3.25


""""MENU CONTROLS"""


# draws the font menu on the screen when the font change icon is selected
def font_menu_control(current):
    value = current
    done = 0

    draw_font_menu(main_color, sub_color, sub_color2, my_font)

    pygame.display.update()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if FONT_ONE_AREA.collidepoint(event.pos):
                        value = 0
                        draw_font_options(sub_color2)
                        pygame.draw.rect(SCREEN, BLACK, FONT_ONE_AREA, 3, ROUND)
                    if FONT_TWO_AREA.collidepoint(event.pos):
                        value = 1
                        draw_font_options(sub_color2)
                        pygame.draw.rect(SCREEN, BLACK, FONT_TWO_AREA, 3, ROUND)
                    if FONT_THREE_AREA.collidepoint(event.pos):
                        value = 3
                        draw_font_options(sub_color2)
                        pygame.draw.rect(SCREEN, BLACK, FONT_THREE_AREA, 3, ROUND)
                    if FONT_FOUR_AREA.collidepoint(event.pos):
                        value = 2
                        draw_font_options(sub_color2)
                        pygame.draw.rect(SCREEN, BLACK, FONT_FOUR_AREA, 3, ROUND)
                    if FONT_FIVE_AREA.collidepoint(event.pos):
                        value = 5
                        draw_font_options(sub_color2)
                        pygame.draw.rect(SCREEN, BLACK, FONT_FIVE_AREA, 3, ROUND)
                    if FONT_SIX_AREA.collidepoint(event.pos):
                        value = 4
                        draw_font_options(sub_color2)
                        pygame.draw.rect(SCREEN, BLACK, FONT_SIX_AREA, 3, ROUND)
                    if BOLD_AREA.collidepoint(event.pos):
                        value = 6
                        draw_font_options(sub_color2)
                        pygame.draw.rect(SCREEN, BLACK, BOLD_AREA, 3, ROUND)
                    if PLUS_AREA.collidepoint(event.pos):
                        increase_font_size()
                        draw_font_size_adjust(my_font)
                        pygame.draw.rect(SCREEN, BLACK, PLUS_AREA, 3, ROUND)
                    if SUB_AREA.collidepoint(event.pos):
                        decrese_font_size()
                        draw_font_size_adjust(my_font)
                        pygame.draw.rect(SCREEN, BLACK, SUB_AREA, 3, ROUND)
                    if DONE_AREA.collidepoint(event.pos):
                        done = 1
        pygame.display.update()

    return value


# draw screen where you select which color to change
def color_menu_control():
    done = 0

    draw_color_select_menu(main_color, sub_color, sub_color2, correct_color, semi_color, wrong_color, my_font, my_font_med, my_font_sm)

    pygame.display.update()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if PICK_ONE_AREA.collidepoint(event.pos):
                        reset_screen()
                        chosen_color = draw_color_screen(correct_color, main_color, sub_color, sub_color2, my_font)
                        set_correct_color(chosen_color)
                        done = 1
                    if PICK_TWO_AREA.collidepoint(event.pos):
                        reset_screen()
                        chosen_color = draw_color_screen(semi_color, main_color, sub_color, sub_color2, my_font)
                        set_semi_color(chosen_color)
                        done = 1
                    if PICK_THREE_AREA.collidepoint(event.pos):
                        reset_screen()
                        chosen_color = draw_color_screen(wrong_color, main_color, sub_color, sub_color2, my_font)
                        set_wrong_color(chosen_color)
                        done = 1
                    if PICK_FOUR_AREA.collidepoint(event.pos):
                        set_correct_color(HIGH_CONTRAST_1)
                        set_semi_color(HIGH_CONTRAST_2)
                        set_wrong_color(HIGH_CONTRAST_3)
                        done = 1
                    if CANCEL_AREA.collidepoint(event.pos):
                        done = 1



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


# for traditional version of the game
def create_new_letter():
    # Creates a new letter and adds it to the guess.
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    # do not change this to adjust board positioning
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count * 70 + LETTER_Y_SPACING), main_color, sub_color, my_font)
    current_letter_bg_x += LETTER_X_SPACING
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw(main_color, my_font)


# delete for traditional version of game
def delete_letter():
    # Deletes the last letter from the guess.
    global current_guess_string, current_letter_bg_x
    guesses[guesses_count][-1].delete(main_color)
    guesses[guesses_count].pop()
    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_letter_bg_x -= LETTER_X_SPACING


# check what parts of the user's guess is correct
def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    global current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result, audio_interface_enabled
    game_decided = False
    guesses_str.append(current_guess_string)
    for i in range(5):
        lowercase_letter = guess_to_check[i].text.lower()
        if lowercase_letter in correct_word:
            if lowercase_letter == correct_word[i]:
                guess_to_check[i].bg_color = correct_color
                if not audio_interface_enabled:
                    time.sleep(0.25)
                    playsound("sound/effects/correct_char_trimmed.mp3")
                add_correct(lowercase_letter)
                for key in keys:
                    if key.text == lowercase_letter.upper():
                        key.bg_color = correct_color
                        key.draw(main_color, my_font)
                guess_to_check[i].text_color = main_color
                if not game_decided:
                    game_result = "W"
            else:
                guess_to_check[i].bg_color = semi_color
                if not audio_interface_enabled:
                    time.sleep(0.25)
                    playsound("sound/effects/semi_correct_char_trimmed.wav")
                add_semi(lowercase_letter)
                for key in keys:
                    if key.text == lowercase_letter.upper():
                        key.bg_color = semi_color
                        key.draw(main_color, my_font)
                guess_to_check[i].text_color = main_color
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = wrong_color
            if not audio_interface_enabled:
                time.sleep(0.25)
                playsound("sound/effects/incorrect_char_trimmed.wav")
                time.sleep(0.35)
            add_incorrect(lowercase_letter)
            for key in keys:
                if key.text == lowercase_letter.upper():
                    key.bg_color = wrong_color
                    key.draw(main_color, my_font)
            guess_to_check[i].text_color = main_color
            game_result = ""
            game_decided = True
        guess_to_check[i].draw(main_color, my_font)
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
        semi_correct_guesses, correct_guesses, incorrect_guesses, word_list, check_list, eog_sound_allowed

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
        check_list = word_list
    elif lang == "ger":
        word_list = GER_WORDS
        check_list = word_list
    elif lang == "fr":
        word_list = FR_WORDS
        check_list = word_list
    elif lang == "kid":
        word_list = KID_WORDS
        check_list = EN_WORDS
    else:
        word_list = EN_WORDS
        check_list = word_list

    correct_word = word_list[random.randint(0, len(word_list) - 1)]

    for key in keys:
        key.bg_color = sub_color2
        if key.width < 60 :
            key.draw(main_color, my_font)
        else :
            key.draw(main_color, my_font_med)

    draw_color_key(correct_color, semi_color, wrong_color, sub_color, my_font_sm, my_font_xsm)
    draw_nav_bar(main_color, sub_color2, my_font)

    play_background_music()

    print(correct_word)
    print(lang)
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
        if key.width < 60:
            key.draw(main_color, my_font)
        else:
            key.draw(main_color, my_font_med)

    draw_color_key(correct_color, semi_color, wrong_color, sub_color, my_font_sm, my_font_xsm)
    draw_nav_bar(main_color, sub_color2, my_font)

    for guess in guesses:
        for letter in guess:
            for l in correct_guesses:
                if letter.text == l.upper():
                    letter.bg_color = correct_color
            for l in semi_correct_guesses:
                if letter.text == l.upper():
                    letter.bg_color = semi_color
            for l in incorrect_guesses:
                if letter.text == l.upper():
                    letter.bg_color = wrong_color
            letter.draw(main_color, my_font)

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
            print(str(e) + "Something went wrong")
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
            " or lower", LANGUAGES[current_language])


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
            set_background_music_volume(value_to_set / 50)
        else:
            say("You can only set volume between 0 and 10.", LANGUAGES[current_language])

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
    time.sleep(0.025)
    draw()
    pygame.display.flip()


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
            "Please specify which one by using stash index feature.", LANGUAGES[current_language])
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
        say("You must replace one letter in your stashed guess at a time.", LANGUAGES[current_language])


def read_guess(guess_number):
    if guess_number > guesses_count:
        say("You dont have a guess number " + str(guess_number) + " yet.", LANGUAGES[current_language])
    else:
        say_and_confirm_by_char(guesses_str[guess_number - 1], correct_word.upper(), LANGUAGES[current_language])


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
                say("say word for wordle tutorial, say free for handsfree tutorial", LANGUAGES[current_language])
                response = listen()
                if "word" in response:
                    say(WORDLE_TUTORIAL, LANGUAGES[current_language])
                elif "free" in response:
                    say(HANDSFREE_TUTORIAL, LANGUAGES[current_language])
                waiting_for_command = 0
            elif "replace" in command:
                say("you said: " + command, LANGUAGES[current_language])
                replace(command)
                waiting_for_command = 0
            elif "stash" in command or "dash" in command:  # Places character(s) into current guess
                say("you said: " + command, LANGUAGES[current_language])
                stash(command)
                waiting_for_command = 0
            elif "delete" in command:  # Deletes all characters from stash
                say("You said: delete", LANGUAGES[current_language])
                delete()
                waiting_for_command = 0
            elif "submit" in command:
                say("you said: submit", LANGUAGES[current_language])
                submit()
                waiting_for_command = 0
            elif "clear" in command:
                say("you said: " + command, LANGUAGES[current_language])
                clear_stash()
                waiting_for_command = 0
            elif "disable" in command:
                say("Disabling audio, press space bar twice to re-enable.", LANGUAGES[current_language])
                activate = 0
                audio_interface_enabled = 0
                set_background_music_volume(0.2)
                waiting_for_command = 0
            elif "volume" in command:
                if has_warned or not audio_interface_enabled:
                    say("Adjusting volume.", LANGUAGES[current_language])
                    volume_handler(command)
                else:
                    say(volume_warning, LANGUAGES[current_language])
                    has_warned = 1
                waiting_for_command = 0
            elif "song" in command:
                say("Changing background song", LANGUAGES[current_language])
                song_switch_handler(command)
                waiting_for_command = 0
            elif "play again" in command:
                reset()
            elif "read" in command:
                if "guess" in command or "gas" in command or "guest" in command:
                    if "one" in command or "won" in command or "1" in command:
                        say("read guess one", LANGUAGES[current_language])
                        read_guess(1)
                        waiting_for_command = 0
                    elif "two" in command or "to" in command or "2" in command or "too" in command:
                        say("read guess two", LANGUAGES[current_language])
                        read_guess(2)
                        waiting_for_command = 0
                    elif "three" in command or "3" in command:
                        say("read guess three", LANGUAGES[current_language])
                        read_guess(3)
                        waiting_for_command = 0
                    elif "four" in command or "for" in command or "4" in command:
                        say("read guess four", LANGUAGES[current_language])
                        read_guess(4)
                        waiting_for_command = 0
                    elif "five" in command or "5" in command:
                        say("read guess five", LANGUAGES[current_language])
                        read_guess(5)
                        waiting_for_command = 0
                    else:
                        say("read current guess", LANGUAGES[current_language])
                        say_by_char(current_guess_string, LANGUAGES[current_language])
                        waiting_for_command = 0
                elif "semi" in command:
                    say("read semi correct guesses", LANGUAGES[current_language])
                    say_by_char(semi_correct_guesses, LANGUAGES[current_language])
                    waiting_for_command = 0
                elif "wrong" in command:
                    say("read incorrect guesses", LANGUAGES[current_language])
                    say_by_char(incorrect_guesses, LANGUAGES[current_language])
                    waiting_for_command = 0
                else:
                    say("invalid command", LANGUAGES[current_language])
            else:
                say("invalid command", LANGUAGES[current_language])

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
            say("Remember to say a letter or five letter word after stash command.", LANGUAGES[current_language])
            print(str(e))
            return

    if len(guess) == 1:
        print("single letter")
        stash_char(guess)
    elif len(guess) == 5:
        if len(current_guess_string) != 0:
            say("your stash is full! submit or delete to guess more letters.", LANGUAGES[current_language])
            return
        print("Five letter word")
        for each_letter in guess:
            print(each_letter)
            stash_char(each_letter)
    else:
        say("You can only stash individual letters, or five letter words. Try again!", LANGUAGES[current_language])


# Takes stash command as an input and places new letter on the screen. Stash handler helper function.
def stash_char(char_to_stash):
    global key_pressed
    key_pressed = char_to_stash.upper()
    if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM":
        if len(current_guess_string) < 5:
            create_new_letter()
        else:
            say("your stash is full! submit or delete to guess more letters.", LANGUAGES[current_language])


# Delete command handler for handsfree().
def delete():
    global current_guess_string
    if len(current_guess_string) > 0:
        letter_to_delete = current_guess_string[len(current_guess_string) - 1]
        say("Deleting " + letter_to_delete, LANGUAGES[current_language])
        delete_letter()
    else:
        say("You dont have any letters to delete!", LANGUAGES[current_language])


# Submit command handler for handsfree()
def submit():
    global current_guess_string, current_guess
    if len(current_guess_string) == 5 and current_guess_string.lower() in check_list:
        say_and_confirm_by_char(current_guess_string, correct_word.upper(), LANGUAGES[current_language])
        check_guess(current_guess)
    else:
        say("your stash must contain a real five letter word, try again!", LANGUAGES[current_language])


"""APPLICATION CONTROL"""


def start_the_game():
    global start_game, audio_interface_enabled, started, game_result, activate, current_guess_string, \
        key_pressed, rendered
    start_game = 1

    SCREEN.fill(main_color)
    print(correct_word)
    print(lang)

    draw_keyboard(main_color, sub_color2, my_font, my_font_med, keys)
    draw_color_key(correct_color, semi_color, wrong_color, sub_color, my_font_sm, my_font_xsm)
    draw_nav_bar(main_color, sub_color2, my_font)

    mixer.music.pause()
    mixer.music.load(BACKGROUND_MUSIC[current_background_music])
    mixer.music.play(-1)

    while True:
        # how program should run when audio interface is not enabled
        while not audio_interface_enabled and start_game:
            draw(sub_color)
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
                            if len(current_guess_string) == 5 and current_guess_string.lower() in check_list:
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
                            if len(current_guess_string) == 5 and current_guess_string.lower() in check_list:
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
                            chosen_font = font_menu_control(font_index)
                            set_font(chosen_font)
                            reset_screen()
                        if COLOR_SEL_AREA.collidepoint(event.pos):
                            color_menu_control()
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
                            chosen_color = draw_color_screen(correct_color, main_color, sub_color, sub_color2, my_font)
                            set_correct_color(chosen_color)
                            reset_screen()
                        if SEMI_COLOR_AREA.collidepoint(event.pos):
                            chosen_color = draw_color_screen(semi_color, main_color, sub_color, sub_color2, my_font)
                            set_semi_color(chosen_color)
                            reset_screen()
                        if WRONG_COLOR_AREA.collidepoint(event.pos):
                            chosen_color = draw_color_screen(wrong_color, main_color, sub_color, sub_color2, my_font)
                            set_wrong_color(chosen_color)
                            reset_screen()
                        if RESET_GAME.collidepoint(event.pos):
                            reset()

            pygame.display.flip()

            if not started:
                say("STARTUP", LANGUAGES[current_language])
                started = 1

        # how program should run when audio interface is enabled
        while audio_interface_enabled and start_game:
            draw(sub_color)
            if game_result == "L":
                eog_sound(game_result)
                say("You have run out of guesses. The word was " + correct_word + " say play again to start over with "
                                                                                  "a new word!",
                    LANGUAGES[current_language])
                lose_play_again()
            if game_result == "W":
                eog_sound(game_result)
                say("Correct, the word was: " + correct_word + ". say play again to get "
                                                               "a new word.", LANGUAGES[current_language])
                correct_play_again()
            if rendered:
                handsfree()
            else:
                pygame.display.flip()
                say(ACTIVATED, LANGUAGES[current_language])
                set_background_music_volume(0.025)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()

            rendered = 1


"""SETTERS"""


def set_background_music(selected, value):
    global current_background_music

    current_background_music = value

    mixer.music.pause()
    mixer.music.load(BACKGROUND_MUSIC[current_background_music])
    mixer.music.play(-1)


def set_language(selected, value):
    global lang, correct_word, word_list, check_list, about_display, lang_index, instructions1_display, instructions2_display, \
    instructions3_display, color_instructions_display

    lang = value

    if lang == "sp":
        word_list = SP_WORDS
        check_list = word_list
        about_display = ABOUT_SPANISH
        instructions1_display = INSTRUCTIONS1_SPANISH
        instructions2_display = INSTRUCTIONS2_SPANISH
        instructions3_display = INSTRUCTIONS3_SPANISH
        color_instructions_display = COLOR_INSTRUCTIONS_SPANISH
        lang_index = 1
    elif lang == "ger":
        word_list = GER_WORDS
        check_list = word_list
        about_display = ABOUT_GERMAN
        instructions1_display = INSTRUCTIONS1_GERMAN
        instructions2_display = INSTRUCTIONS2_GERMAN
        instructions3_display = INSTRUCTIONS3_GERMAN
        color_instructions_display = COLOR_INSTRUCTIONS_GERMAN
        lang_index = 2
    elif lang == "fr":
        word_list = FR_WORDS
        check_list = word_list
        about_display = ABOUT_FRENCH
        instructions1_display = INSTRUCTIONS1_FRENCH
        instructions2_display = INSTRUCTIONS2_FRENCH
        instructions3_display = INSTRUCTIONS3_FRENCH
        color_instructions_display = COLOR_INSTRUCTIONS_FRENCH
        lang_index = 3
    elif lang == "kid":
        word_list = KID_WORDS
        check_list = EN_WORDS
        about_display = ABOUT_ENGLISH
        instructions1_display = INSTRUCTIONS1_ENGLISH
        instructions2_display = INSTRUCTIONS2_ENGLISH
        instructions3_display = INSTRUCTIONS3_ENGLISH
        color_instructions_display = COLOR_INSTRUCTIONS_ENGLISH
        lang_index = 4
    else:
        word_list = EN_WORDS
        check_list = word_list
        about_display = ABOUT_ENGLISH
        instructions1_display = INSTRUCTIONS1_ENGLISH
        instructions2_display = INSTRUCTIONS2_ENGLISH
        instructions3_display = INSTRUCTIONS3_ENGLISH
        color_instructions_display = COLOR_INSTRUCTIONS_ENGLISH
        lang_index = 0

    correct_word = word_list[random.randint(0, len(word_list) - 1)]


def menu_set_font(selected, value):
    global font_index, my_font, my_font_med, my_font_sm, my_font_xsm
    font_index = value
    my_font = pygame.font.Font(FONTS[font_index], font_size)
    my_font_med = pygame.font.Font(FONTS[font_index], font_size - 10)
    my_font_sm = pygame.font.Font(FONTS[font_index], font_size - 20)
    my_font_xsm = pygame.font.Font(FONTS[font_index], font_size - 25)


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
    global font_index, my_font, my_font_med, my_font_sm, my_font_xsm
    font_index = value
    my_font = pygame.font.Font(FONTS[font_index], font_size)
    my_font_med = pygame.font.Font(FONTS[font_index], font_size - 10)
    my_font_sm = pygame.font.Font(FONTS[font_index], font_size - 20)
    my_font_xsm = pygame.font.Font(FONTS[font_index], font_size - 25)


def decrese_font_size():
    global font_size
    if font_size - 25 > 5:
        font_size -= 3


def increase_font_size():
    global font_size
    if font_size < 47:
        font_size += 1


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
    mytheme.title_font = FONTS[font_index]
    mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    mytheme.title_offset = (WIDTH / 2 - 140, padding * 8)
    mytheme.title_font_color = WHITE
    mytheme.title_close_button_background_color = BLACK

    mytheme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
    mytheme.widget_font_color = WHITE
    mytheme.widget_font = FONTS[font_index]
    mytheme.widget_padding = padding
    mytheme.widget_margin = (0, 3)

    color_theme = pygame_menu.themes.THEME_GREEN.copy()
    color_theme.background_color = WHITE
    color_theme.title_font_color = WHITE
    color_theme.widget_font_color = BLACK
    color_theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()

    about_theme = color_theme.copy()
    about_theme.background_color = WHITE
    about_theme.title_font = FONTS[font_index]

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
    for m in color_instructions_display:
        color_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    color_menu.add.color_input("Correct Letter Color  ", color_type='hex', onchange=set_correct_color, default=correct_color)
    color_menu.add.color_input("Semi Correct Letter Color  ", color_type='hex', onchange=set_semi_color, default=semi_color)
    color_menu.add.color_input("Wrong Letter Color  ", color_type='hex', onchange=set_wrong_color, default=wrong_color)

    for m in SPACES:
        color_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    color_menu.add.button("Back", pygame_menu.events.BACK)

    for m in SPACES:
        color_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    # ABOUT MENU PAGE
    for m in about_display:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    for m in SPACES:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    about_menu.add.button("Back", pygame_menu.events.BACK)

    for m in SPACES:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    # INSTRUCTIONS MENU PAGE
    for m in instructions1_display: 
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    image_path_correct = pygame_menu.baseimage.BaseImage("assets/correct.jpg")
    inst_menu.add.image(image_path_correct, align=pygame_menu.locals.ALIGN_LEFT)

    for m in instructions2_display: 
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    image_path_semicorrect = pygame_menu.baseimage.BaseImage("assets/semicorrect.jpg")
    inst_menu.add.image(image_path_semicorrect, align=pygame_menu.locals.ALIGN_LEFT)

    for m in instructions3_display:
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    inst_menu.add.button("Back", pygame_menu.events.BACK)

    for m in SPACES:
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    # MAIN MENU PAGE
    menu.add.button('Play', start_the_game)
    menu.add.selector('Language: ', [("English", "en"), ("Spanish", "sp"), ("German", "ger"),
                                     ("French", "fr"), ("Kid Friendly", "kid")], onchange=set_language, default=lang_index)
    menu.add.selector('Background Music: ', [("Traditional", 0),
                                             ("Happy Beat", 1),
                                             ("     Bop      ", 2),
                                             (" Meditation ", 3),
                                             ("Electro Chill", 4),
                                             ("    Escape   ", 5),
                                             ("      Synth     ", 6),
                                             (" Nature 1 ", 7),
                                             (" Nature 2 ", 8),
                                             (" Nature 3 ", 9),
                                             (" Nature 4 ", 10)],
                      onchange=set_background_music, default=current_background_music)
    menu.add.selector('Change Font: ',
                      [("Free Sans", 0), ("Comic Sans", 1),
                       ("Lil Grotesk", 2), ("GFS Didot", 3),
                       ("First Coffee", 4), ("Wigners Friend", 5)],
                      onchange=menu_set_font, default=font_index)
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
    mytheme.title_font = FONTS[font_index]
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

    for m in instructions1_display:
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    image_path_correct = pygame_menu.baseimage.BaseImage("assets/correct.jpg")
    inst_menu.add.image(image_path_correct, align=pygame_menu.locals.ALIGN_LEFT)

    for m in instructions2_display:
        inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    image_path_semicorrect = pygame_menu.baseimage.BaseImage("assets/semicorrect.jpg")
    inst_menu.add.image(image_path_semicorrect, align=pygame_menu.locals.ALIGN_LEFT)

    for m in instructions3_display:
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
