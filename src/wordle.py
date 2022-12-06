import sys
import random

import pygame
import speech_recognition as sr
import os
import time

from pygame import mixer
from gtts import gTTS
from playsound import playsound

from helpers.draw import *
from helpers.menu import *
from helpers.constants import *
from helpers.messages import *
from helpers.classes import *
from word_files.englishwords import *


"""INITIALIZERS / GLOBAL VARIABLES"""

pygame.init()
start_game = 0

# AUDIO INTERFACE FLAGS
hands_free_rendered = 0
game_started = 0
activate_audio = 0
audio_interface_enabled = 0

# MUSIC FLAGS
has_warned = 0
current_background_music = 0
muted = 0
eog_sound_allowed = 1

# LANGUAGE DEFAULT = ENGLISH - FOR GRAPHICS
lang_index = 0
word_list = EN_WORDS
check_list = CHECK_WORDS
correct_word = word_list[random.randint(0, len(word_list) - 1)]
about_display = ABOUT_ENGLISH
instructions1_display = INSTRUCTIONS1_ENGLISH
instructions2_display = INSTRUCTIONS2_ENGLISH
instructions3_display = INSTRUCTIONS3_ENGLISH
color_instructions_display = COLOR_INSTRUCTIONS_ENGLISH


# DEFAULT COLORS - FOR GRAPHICS
correct_color = GREEN
semi_color = YELLOW
wrong_color = GREY

main_color = WHITE
sub_color = BLACK
sub_color2 = LT_GREY

# FONT DEFAULTS - FOR GRAPHICS
font_size = 40
font_index = 0
my_font = pygame.font.Font(FONTS[font_index], font_size)
my_font_med = pygame.font.Font(FONTS[font_index], font_size - 10)
my_font_sm = pygame.font.Font(FONTS[font_index], font_size - 20)
my_font_xsm = pygame.font.Font(FONTS[font_index], font_size - 25)

# SCREEN - FOR GRAPHICS
pygame.display.set_caption("World-le")
pygame.display.set_icon(pygame.image.load("assets/Icon.png"))
pygame.display.update()

# KEYBOARD - FOR GRAPHICS
# list is all key objects used to draw the on screen keyboard
keys = []
key_pressed = ''

# WORD/LETTER CONTROL
guesses_count = 0
# holds all guesses as lists of letter objects
guesses = [[], [], [], [], [], []]
# when guess checked, full version in string format placed here
guesses_str = []
# contains letter objects of current/ most recent guess
current_guess = []
current_guess_string = ""
game_result = ""

# all letter objects that have been guessed and are respectively 
# correct, incorrect and semi correct
correct_guesses = []
incorrect_guesses = []
semi_correct_guesses = []

current_letter_bg_x = WIDTH / 3.25

# MENU FLAGS FOR MENU PAGES
about_index = 0
inst_index = 0
color_index = 0
about_loaded = [1, 0, 0, 0, 1]
inst_loaded = [1, 0, 0, 0, 1]
color_loaded = [1, 0, 0, 0, 1]

""""MENU CONTROLS"""


# calls draw functions to draws the font menu on the screen when the font change icon is selected
# controls what happens when user clicks on different areas of the screen while the font menu is up
def font_menu_control(current):
    # what is the current font
    value = current
    done = 0

    draw_font_menu(main_color, sub_color, sub_color2, my_font, font_size, lang_index)

    pygame.display.update()

    # listens for screen click and handles program actions accordingly
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # if user clicks a font area, the font is changes to the respective font
                    if FONT_ONE_AREA.collidepoint(event.pos):
                        value = 0
                        draw_font_options(sub_color2, font_size, lang_index)
                        pygame.draw.rect(SCREEN, sub_color, FONT_ONE_AREA, 3, ROUND)
                    if FONT_TWO_AREA.collidepoint(event.pos):
                        value = 1
                        draw_font_options(sub_color2, font_size, lang_index)
                        pygame.draw.rect(SCREEN, sub_color, FONT_TWO_AREA, 3, ROUND)
                    if FONT_THREE_AREA.collidepoint(event.pos):
                        value = 3
                        draw_font_options(sub_color2, font_size, lang_index)
                        pygame.draw.rect(SCREEN, sub_color, FONT_THREE_AREA, 3, ROUND)
                    if FONT_FOUR_AREA.collidepoint(event.pos):
                        value = 2
                        draw_font_options(sub_color2, font_size, lang_index)
                        pygame.draw.rect(SCREEN, sub_color, FONT_FOUR_AREA, 3, ROUND)
                    if FONT_FIVE_AREA.collidepoint(event.pos):
                        value = 5
                        draw_font_options(sub_color2, font_size, lang_index)
                        pygame.draw.rect(SCREEN, sub_color, FONT_FIVE_AREA, 3, ROUND)
                    if FONT_SIX_AREA.collidepoint(event.pos):
                        value = 4
                        draw_font_options(sub_color2, font_size, lang_index)
                        pygame.draw.rect(SCREEN, sub_color, FONT_SIX_AREA, 3, ROUND)
                    if BOLD_AREA.collidepoint(event.pos):
                        value = 6
                        draw_font_options(sub_color2, font_size, lang_index)
                        pygame.draw.rect(SCREEN, sub_color, BOLD_AREA, 3, ROUND)
                    # increase and decrease font depending on which area is clicked
                    if PLUS_AREA.collidepoint(event.pos):
                        increase_font_size()
                        draw_font_size_adjust(my_font)
                        draw_font_options(sub_color2, font_size, lang_index)
                        pygame.draw.rect(SCREEN, sub_color, PLUS_AREA, 3, ROUND)
                    if SUB_AREA.collidepoint(event.pos):
                        decrese_font_size()
                        draw_font_size_adjust(my_font)
                        draw_font_options(sub_color2, font_size, lang_index)
                        pygame.draw.rect(SCREEN, sub_color, SUB_AREA, 3, ROUND)
                    # if the done buttons or any areas around the mini menu is clicked, exit the menu
                    if DONE_AREA.collidepoint(event.pos) or EXIT_MENU_AREA1.collidepoint(
                            event.pos) or EXIT_MENU_AREA2.collidepoint(event.pos):
                        done = 1
                    if EXIT_MENU_AREA3.collidepoint(event.pos) or EXIT_MENU_AREA4.collidepoint(event.pos):
                        done = 1

        pygame.display.update()
    # return the chosen font - same as current if not changed
    return value


# calls draw functions to draws the color menu on the screen when the color change icon is selected
# controls what happens when user clicks on different areas of the screen while the color menu is up
def color_menu_control():
    done = 0

    # draw the menu to select which color to change
    draw_color_select_menu(main_color, sub_color, sub_color2, correct_color, semi_color, wrong_color, my_font,
                           my_font_med, my_font_sm, lang_index)

    pygame.display.update()

    # listens for which color the user wants to change - area click corresponds to different colors
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # pick change correct color - will reset screen and call function to select a color
                    if PICK_ONE_AREA.collidepoint(event.pos):
                        reset_screen()
                        chosen_color = draw_color_screen(correct_color, main_color, sub_color, sub_color2, my_font,
                                                         lang_index)
                        set_correct_color(chosen_color)
                        done = 1
                    # pick change semi correct color - will reset screen and call function to select a color
                    if PICK_TWO_AREA.collidepoint(event.pos):
                        reset_screen()
                        chosen_color = draw_color_screen(semi_color, main_color, sub_color, sub_color2, my_font,
                                                         lang_index)
                        set_semi_color(chosen_color)
                        done = 1
                    # pick change wrong color - will reset screen and call function to select a color
                    if PICK_THREE_AREA.collidepoint(event.pos):
                        reset_screen()
                        chosen_color = draw_color_screen(wrong_color, main_color, sub_color, sub_color2, my_font,
                                                         lang_index)
                        set_wrong_color(chosen_color)
                        done = 1
                    # activate high contrast colors - changes all colors
                    if PICK_FOUR_AREA.collidepoint(event.pos):
                        set_correct_color(HIGH_CONTRAST_1)
                        set_semi_color(HIGH_CONTRAST_2)
                        set_wrong_color(HIGH_CONTRAST_3)
                        done = 1
                    # if the done buttons or any areas around the mini menu is clicked, exit the menu
                    if CANCEL_AREA.collidepoint(event.pos) or EXIT_MENU_AREA1.collidepoint(
                            event.pos) or EXIT_MENU_AREA2.collidepoint(event.pos):
                        done = 1
                    if EXIT_MENU_AREA3.collidepoint(event.pos) or EXIT_MENU_AREA4.collidepoint(event.pos):
                        done = 1


"""GENERAL GAME CONTROLS"""


# parameter is a character that was semi correct/ in word, wrong position
# if it was not already in the list, append it to the semi correct guess list
def add_semi(char):
    global semi_correct_guesses
    if char not in semi_correct_guesses:
        semi_correct_guesses.append(char)


# parameter is a character that was incorrect/ not in the word
# if it was not already in the list, append it to the incorrect guess list
def add_incorrect(char):
    global incorrect_guesses
    if char not in incorrect_guesses:
        incorrect_guesses.append(char)


# parameter is a character that was correct/ ni word and right position
# if it was not already in the list, append it to the correct guess list
def add_correct(char):
    global correct_guesses
    if char not in correct_guesses:
        correct_guesses.append(char)


# adds a new letter when letter is entered by a user
def create_new_letter():
    # Creates a new letter and adds it to the guess.
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    # create new letter object 
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count * 70 + LETTER_Y_SPACING), main_color,
                        sub_color, my_font)
    current_letter_bg_x += LETTER_X_SPACING
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    # draw letter at correct position
    for guess in guesses:
        for letter in guess:
            letter.draw(main_color, my_font)


# delete letter when user presses backspace
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
                guess_to_check[i].correct_place = 1
                if not audio_interface_enabled:
                    time.sleep(0.25)
                    play_sound("sound/effects/correct_char_trimmed.mp3")                    
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
                guess_to_check[i].correct_place = 0
                if not audio_interface_enabled:
                    time.sleep(0.25)
                    play_sound("sound/effects/semi_correct_char_trimmed.wav")
                add_semi(lowercase_letter)
                for key in keys:
                    if key.text == lowercase_letter.upper():
                        if key.bg_color != correct_color:
                            key.bg_color = semi_color
                            key.draw(main_color, my_font)
                guess_to_check[i].text_color = main_color
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = wrong_color
            guess_to_check[i].correct_place = 0
            if not audio_interface_enabled:
                time.sleep(0.25)
                play_sound("sound/effects/incorrect_char_trimmed.wav")
                time.sleep(0.25)
            add_incorrect(lowercase_letter)
            for key in keys:
                if key.text == lowercase_letter.upper():
                    key.bg_color = wrong_color
                    key.draw(main_color, my_font)
            guess_to_check[i].text_color = main_color
            game_result = ""
            game_decided = True
        guess_to_check[i].draw(main_color, my_font)
        time.sleep(0.2)
        pygame.display.update()

    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = WIDTH / 3.25

    if guesses_count == 6 and game_result == "":
        game_result = "L"


# display lost game screen and instructions to play again
def lose_play_again(stats, game_result):
    eog_sound(game_result)
    reset_game = 0
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, DK_RED, END_GAME_SCREEN_AREA, 0, ROUND)
    # draw end game message
    draw_text(my_font, f"Sorry, the word was {correct_word}!", WHITE, (WIDTH / 2, 100))
    draw_text(my_font, "Press ENTER to Play Again!", WHITE, (WIDTH / 2, 170))
    # Draw game and player statistics
    won_percent = "         {:.1f}%         ".format(int(stats[1]) / int(stats[0]) * 100)
    draw_text(my_font, str(stats[0]) + won_percent + str(stats[2]) + "            " + str(stats[3]), WHITE, (WIDTH / 2, 280))
    draw_text(my_font_sm, "Games Played           Won %            Current Streak       Max Streak", WHITE, (WIDTH/2, 335))
    draw_text(my_font_med, "Guess Distribution", WHITE, (WIDTH/2, 435))

    draw_histogram(WIDTH / 20, HEIGHT - (HEIGHT / 3), WIDTH - WIDTH / 10, HEIGHT - (3 * (HEIGHT / 4)), "l")

    pygame.display.update()
    # while on end game screen listen for enter key to restart game
    while not reset_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # if user pressed enter key
                if event.key == pygame.K_RETURN:
                    # restart game
                    reset_game = 1
                    reset()


# display won game screen and instructions for play again
def correct_play_again(stats, game_result):
    eog_sound(game_result)
    reset_game = 0
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, correct_color, END_GAME_SCREEN_AREA, 0, ROUND)
    # draw end game message
    draw_text(my_font, "Congratulations!", WHITE, (WIDTH / 2, 100))
    draw_text(my_font, f"The word was {correct_word}!", WHITE, (WIDTH / 2, 160))
    draw_text(my_font, "Press ENTER to Play Again!", WHITE, (WIDTH / 2, 220))
    # Calculate and draw game and player statistics
    won_percent = "         {:.1f}%         ".format(int(stats[1]) / int(stats[0]) * 100)
    draw_text(my_font, str(stats[0]) + won_percent + str(stats[2]) + "            " + str(stats[3]), WHITE, (WIDTH / 2, 315))
    draw_text(my_font_sm, "Games Played           Won %            Current Streak       Max Streak", WHITE, (WIDTH/2, 365))
    draw_text(my_font_med, "Guess Distribution", WHITE, (WIDTH/2, 455))

    # left, top, width, height
    draw_histogram(WIDTH / 20, HEIGHT - (HEIGHT / 3), WIDTH - WIDTH / 10, HEIGHT - (3 * (HEIGHT / 4)), "w")

    pygame.display.update()
    # while on end game screen listen for enter key to restart game
    while not reset_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # if user pressed enter key
                if event.key == pygame.K_RETURN:
                    # restart game
                    reset_game = 1
                    reset()


# function handles reading from and writing to stats.txt and hist.txt file
# takes in if user won the game or not and returns the updated stats.
def handle_stats(stat):
    if not os.path.exists("stats.txt"):
        # create new file if none exsists
        f = open("stats.txt", "w+")
        # write stats to file :games played, games won, current streak, max streak
        f.write("%d\n%d\n%d\n%d" % (1, stat, stat, stat))
        # return current stats
        data = [1, stat, stat, stat]
    else:
        # open file and read stats
        f = open("stats.txt", "r")
        data = f.readlines()
        f.close()
        # increment games played
        data[0] = int(data[0]) + 1
        # increament games won
        data[1] = int(data[1]) + stat
        # set current streak value
        if stat == 0:
            data[2] = 0
        else:
            data[2] = int(data[2]) + stat
        # chekc if max streak should be changed
        if data[2] > int(data[3]):
            data[3] = data[2]
        # write new data to file
        f = open("stats.txt", "w")
        # write to file: games played, games won, current streak, max streak
        f.write("%d\n%d\n%d\n%d" % (data[0], data[1], data[2], int(data[3])))

    f.close()

    if stat == 1:
        if not os.path.exists("hist.txt"):
            f = open("hist.txt", "w+")
            f.write("%d\n%d\n%d\n%d\n%d\n%d" % (0, 0, 0, 0, 0, 0))
            f.close()

        f = open("hist.txt", "r")
        hist_data = f.readlines()
        str_entry_to_inc = hist_data[guesses_count - 1]
        int_entry_to_inc = int(str_entry_to_inc)
        int_entry_to_inc += 1
        hist_data[guesses_count - 1] = int_entry_to_inc

        f.close()

        f = open("hist.txt", "w")
        f.write("%d\n%d\n%d\n%d\n%d\n%d" % (int(hist_data[0]), int(hist_data[1]), int(hist_data[2]), int(hist_data[3]),
                                            int(hist_data[4]), int(hist_data[5])))
        f.close()

    return data


# Draws histogram at location (x_position, y_position), and size x_width x y_height, based on the data in "hist.txt".
# if "w" -> highlight the current number of guesses it took to win in the histogram.
# if "l" -> dont highlight anything.
def draw_histogram(x_position, y_position, x_width, y_height, w_or_l):
    f = open("hist.txt", "r")
    hist_data = f.readlines()

    aesthetic_offset = y_height / 6 * 0.1

    bar_height = y_height / 6

    # Draw individual histogram bar based on the proportion of width and y offset.
    def draw_hist_bar(bar_number, proportion_of_width):

        bar_offset = bar_height * bar_number

        current_bar_height = y_position + bar_offset

        # Draw current proportion bar
        pygame.draw.rect(SCREEN, WHITE, pygame.Rect(x_position + (WIDTH / 20),
                                                    current_bar_height + aesthetic_offset,
                                                    (x_width - (WIDTH / 20)) * proportion_of_width,
                                                    y_height / 6 - (2 * aesthetic_offset)))

        # Draw white background square for current guess number identifier
        pygame.draw.rect(SCREEN, WHITE, pygame.Rect(x_position,
                                                    current_bar_height + aesthetic_offset,
                                                    y_height / 6 - (2 * aesthetic_offset),
                                                    y_height / 6 - (2 * aesthetic_offset)))

        # Draw guess number identifier 1-6
        draw_text(my_font_sm, str(bar_number + 1), BLACK, (x_position + (WIDTH / 80),
                                                           current_bar_height + (y_height / 12)))

        # Draw histogram data onto respective proportions
        draw_text(my_font_xsm, str(hist_data[x]).strip(), BLACK, (x_position + (WIDTH / 15),
                                                                  current_bar_height + (y_height / 12)))

    # Find largest value in hist.txt to use for proportion.
    largest_value = 0
    for x in range(6):
        if int(hist_data[x]) > largest_value:
            largest_value = int(hist_data[x])

    for x in range(6):
        draw_hist_bar(x, int(hist_data[x]) / largest_value)

    # If being called from a win, draw highlight square on top of the current guess count.
    if w_or_l == "w":
        pygame.draw.rect(SCREEN, DK_RED, pygame.Rect(x_position,
                                                     y_position + (bar_height * (guesses_count - 1)) + aesthetic_offset,
                                                     y_height / 6 - (2 * aesthetic_offset),
                                                     y_height / 6 - (2 * aesthetic_offset)), 2)

    pygame.display.flip()


# reset global variables and game screen after previous game ends
def reset():
    # Resets all global variables to their default states.
    global guesses_count, correct_word, guesses, current_guess, current_guess_string, game_result, \
        semi_correct_guesses, correct_guesses, incorrect_guesses, eog_sound_allowed

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

    correct_word = word_list[random.randint(0, len(word_list) - 1)]

    # redraw game screen items
    for key in keys:
        key.bg_color = sub_color2
        if key.width < 60:
            key.draw(main_color, my_font)
        else:
            key.draw(main_color, my_font_med)

    draw_color_key(correct_color, semi_color, wrong_color, sub_color, my_font_sm, my_font_xsm, lang_index)
    draw_nav_bar(main_color, sub_color2, my_font, muted)

    # restart background music
    if not muted:
        play_background_music()

    # For testing purposes
    print(correct_word)

    pygame.display.update()


# reset the screen and redraw with new colors/font/any changes user has made
def reset_screen():
    SCREEN.fill(main_color)

    # redraw keys
    for key in keys:
        for l in correct_guesses:
            if key.text == l.upper():
                key.bg_color = correct_color
        for l in semi_correct_guesses:
            if key.text == l.upper():
                if key.bg_color != correct_color:
                    key.bg_color = semi_color
        for l in incorrect_guesses:
            if key.text == l.upper():
                key.bg_color = wrong_color
        if key.width < 60:
            key.draw(main_color, my_font)
        else:
            key.draw(main_color, my_font_med)

    draw_color_key(correct_color, semi_color, wrong_color, sub_color, my_font_sm, my_font_xsm, lang_index)
    draw_nav_bar(main_color, sub_color2, my_font, muted)

    # redraw current game board state
    for guess in guesses:
        for letter in guess:
            for l in correct_guesses:
                if letter.text == l.upper():
                    if letter.correct_place != 0:
                        letter.bg_color = correct_color
            for l in semi_correct_guesses:
                if letter.text == l.upper():
                    if letter.correct_place != 1:
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


# Wraps playsound in try-catch for windows integration
def play_sound(sound):
    try:
        playsound(sound)
    except Exception as e:
        print(str(e) + "Something went wrong")


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
                play_sound('sound/effects/correct_char_trimmed.mp3')
            elif c in correct:
                play_sound('sound/effects/semi_correct_char_trimmed.wav')
            else:
                play_sound('sound/effects/incorrect_char_trimmed.wav')
        except Exception as e:
            print(str(e) + "Something went wrong")
        correct_index = correct_index + 1


# Finds keyword "song" in command, then takes the next value in the command string as an argument.
# Calls load_new_background_music with the value found above passed as an argument
def song_switch_handler(command):
    command_split = command.split()
    keyword_index = return_keyword_index("song", command)
    value_index = keyword_index + 1
    value = word_to_int(command_split[value_index])
    if int(value) <= len(BACKGROUND_MUSIC):
        load_new_background_music(int(value) - 1)
    else:
        say("You must say a song number " + str(len(BACKGROUND_MUSIC)) +
            " or lower", LANGUAGES[0])


# Loads a song based on an index argument passed in. Pauses current music, plays new song on infinite loop.
def load_new_background_music(music_index):
    global current_background_music
    try:
        current_background_music = music_index
        mixer.music.pause()
        mixer.music.load(BACKGROUND_MUSIC[current_background_music])
        mixer.music.play(-1)
    except Exception as e:
        print(str(e) + "Something went wrong")


# Mixer call wrapped in try-catch for windows.
def play_background_music():
    try:
        mixer.music.play(-1)
    except Exception as e:
        print(str(e) + "Something went wrong")


# Pause call wrapped in try-catch for windows.
def pause_background_music():
    try:
        mixer.music.pause()
    except Exception as e:
        print(str(e) + "Music never started, cannot pause")


# Set volume call wrapped in try-catch for windows.
def set_background_music_volume(level):
    try:
        mixer.music.set_volume(level)
    except Exception as e:
        print(str(e) + "Music not playing, cannot adjust volume")


# Finds keyword "volume" and passes the next value in the command string to set_background_music_volume.
# Wrapped in try-catch for windows.
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
            say("You can only set volume between 0 and 10.", LANGUAGES[0])

    except Exception as e:
        print(str(e) + "Something went wrong")


# Prevents sound effect repeat at end of game (eog) through the use of a state variable,
# eog_sound_allowed, which is only reset when game is reset
def eog_sound(current_game_result):
    global eog_sound_allowed
    if eog_sound_allowed:
        if current_game_result == "W":
            pause_background_music()
            play_sound('sound/effects/correct_word_trimmed.mp3')
            eog_sound_allowed = 0
        elif current_game_result == "L":
            pause_background_music()
            play_sound('sound/effects/no_more_guesses_trimmed.wav')
            eog_sound_allowed = 0


# Control for common letter misinterpretations. Called if word returned to 'stash' instead of a char
# Returns a character if possible, if none found, returns original word.
def fix_char(fuzzy_char):
    for i in range(len(FUZZY_CHAR)):
        if fuzzy_char == FUZZY_CHAR[i][0]:
            return FUZZY_CHAR[i][1]
    return fuzzy_char


# Converts strings that represent integers into their respective integer.
def word_to_int(word):
    print(word)
    for i in range(len(WORD_TO_INT)):
        if word == WORD_TO_INT[i][0]:
            return WORD_TO_INT[i][1]
    return word


# For all letters in stash, call delete_letter()
def clear_stash():
    delete_count = len(current_guess_string)
    while delete_count > 0:
        delete_letter()
        delete_count -= 1
    time.sleep(0.025)
    draw(sub_color)
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

    # If char_to_replace is an index
    index_list = ['1', '2', '3', '4', '5', 'one', 'two', 'to', 'too', 'three', 'four', 'for', 'five']
    if char_to_replace in index_list:
        # replace letter at index char_to_replace, with replacement
        guess_split[int(word_to_int(char_to_replace)) - 1] = replacement
        clear_stash()
        new_guess_string = ''.join(guess_split)
        stash("stash " + new_guess_string)
        return

    # If char_to_replace is a char that is in the stash multiple times
    elif not current_guess_string.count(char_to_replace.upper()) == 1:
        say("there are more than one of the letter to replace in your stash. "
            "Please specify which one by using stash index feature.", LANGUAGES[0])
        return

    # If char_to_replace is a char that is in the stash only once.
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
        say("You must replace one letter in your stashed guess at a time.", LANGUAGES[0])


# Reads a previous guess to the user character by character. Confirmed by character.
def read_guess(guess_number):
    if guess_number > guesses_count:
        say("You dont have a guess number " + str(guess_number) + " yet.", LANGUAGES[0])
    else:
        say_and_confirm_by_char(guesses_str[guess_number - 1], correct_word.upper(), LANGUAGES[0])


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
            say("Remember to say a letter or five letter word after stash command.", LANGUAGES[0])
            print(str(e))
            return

    if len(guess) == 1:
        print("single letter")
        stash_char(guess)
    elif len(guess) == 5:
        if len(current_guess_string) != 0:
            say("your stash is full! submit or delete to guess more letters.", LANGUAGES[0])
            return
        print("Five letter word")
        for each_letter in guess:
            print(each_letter)
            stash_char(each_letter)
    else:
        say("You can only stash individual letters, or five letter words. Try again!", LANGUAGES[0])


# Takes stash command as an input and places new letter on the screen. Stash handler helper function.
def stash_char(char_to_stash):
    global key_pressed
    key_pressed = char_to_stash.upper()
    if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM":
        if len(current_guess_string) < 5:
            create_new_letter()
        else:
            say("your stash is full! submit or delete to guess more letters.", LANGUAGES[0])


# Delete command handler for handsfree().
def delete():
    if len(current_guess_string) > 0:
        letter_to_delete = current_guess_string[len(current_guess_string) - 1]
        say("Deleting " + letter_to_delete, LANGUAGES[0])
        delete_letter()
    else:
        say("You dont have any letters to delete!", LANGUAGES[0])


# Submit command handler for handsfree()
def submit():
    if len(current_guess_string) == 5 and current_guess_string.lower() in check_list:
        say_and_confirm_by_char(current_guess_string, correct_word.upper(), LANGUAGES[0])
        check_guess(current_guess)
    else:
        say("your stash must contain a real five letter word, try again!", LANGUAGES[0])


# Generic function to return index of keyword in command. Wrapped in try/catch to avoid program crashing
# if command.split() only has one element
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


# Tutorial for submit function.
def submit_tutorial():
    say("When you press submit, I will read each letter in your stash, and after each letter you will hear a sound."
        "if you hear", "en")

    play_sound('sound/effects/incorrect_char_trimmed.wav')

    say("Then the letter you guessed was not in the word. If you hear", "en")

    play_sound('sound/effects/semi_correct_char_trimmed.wav')

    say("That means the letter you entered was in the word, but not in the right place. If you hear", "en")

    play_sound('sound/effects/correct_char_trimmed.mp3')

    say("Then the letter you guessed was in the letter and in the correct place. Here is an example of what "
        "would happen if the correct word was apple, and you stashed and then submitted the word pines", "en")

    say_and_confirm_by_char("pines", "apple", "en")


# Tutorial command handler for handsfree(). Reads correct tutorial based on command.
def tutorial(command):
    found = 0
    index = 0

    command_split = command.split()

    if len(command_split) == 1:
        say(TUTORIAL_RESPONSE, "en")
        return

    try:
        while not found:
            if command_split[index] == "tutorial":
                key = command_split[index - 1]
                found = 1

            index += 1

    except Exception as e:
        print("value before tutorial was not a valid key")

    if key == "submit":
        submit_tutorial()
    else:
        say(command_tutorial_dict[key], "en")


# Listens for user command, validates the command, and calls the correct function to execute user command.
def handsfree():
    global current_guess_string, activate_audio, audio_interface_enabled, has_warned

    waiting_for_command = 1
    while waiting_for_command:
        draw(sub_color)
        try:
            time.sleep(0.05)
            command = listen()
            # Comment above for debugging, allows typing of command; comment below for handsfree use;
            # command = input("Type a command: ")
            command = command.lower()
            command_split = command.split()
            print(command)

            if "tutorial" in command:  # Starts tutorial
                tutorial(command)
                waiting_for_command = 0
            elif "replace" in command:
                say("you said: " + command, LANGUAGES[0])
                replace(command)
                waiting_for_command = 0
            elif "stash" in command or "dash" in command:  # Places character(s) into current guess
                say("you said: " + command, LANGUAGES[0])
                stash(command)
                waiting_for_command = 0
            elif "delete" in command:  # Deletes all characters from stash
                say("You said: delete", LANGUAGES[0])
                delete()
                waiting_for_command = 0
            elif "submit" in command:
                say("you said: submit", LANGUAGES[0])
                submit()
                waiting_for_command = 0
            elif "clear" in command:
                say("you said: " + command, LANGUAGES[0])
                clear_stash()
                waiting_for_command = 0
            elif "disable" in command:
                say("Disabling audio, press space bar twice to re-enable.", LANGUAGES[0])
                activate_audio = 0
                audio_interface_enabled = 0
                set_background_music_volume(0.2)
                waiting_for_command = 0
            elif "volume" in command:
                if has_warned or not audio_interface_enabled:
                    say("Adjusting volume.", LANGUAGES[0])
                    volume_handler(command)
                else:
                    say(VOLUME_WARNING, LANGUAGES[0])
                    has_warned = 1
                waiting_for_command = 0
            elif "song" in command:
                say("Changing background song", LANGUAGES[0])
                song_switch_handler(command)
                waiting_for_command = 0
            elif "play again" in command:
                reset()
            elif "read" in command:
                if "guess" in command or "gas" in command or "guest" in command:
                    if "one" in command or "won" in command or "1" in command:
                        say("read guess one", LANGUAGES[0])
                        read_guess(1)
                        waiting_for_command = 0
                    elif "two" in command or "to" in command or "2" in command or "too" in command:
                        say("read guess two", LANGUAGES[0])
                        read_guess(2)
                        waiting_for_command = 0
                    elif "three" in command or "3" in command:
                        say("read guess three", LANGUAGES[0])
                        read_guess(3)
                        waiting_for_command = 0
                    elif "four" in command or "for" in command or "4" in command:
                        say("read guess four", LANGUAGES[0])
                        read_guess(4)
                        waiting_for_command = 0
                    elif "five" in command or "5" in command:
                        say("read guess five", LANGUAGES[0])
                        read_guess(5)
                        waiting_for_command = 0
                    else:
                        say("read current guess", LANGUAGES[0])
                        say_by_char(current_guess_string, LANGUAGES[0])
                        waiting_for_command = 0
                elif "semi" in command:
                    say("read semi correct guesses", LANGUAGES[0])
                    say_by_char(semi_correct_guesses, LANGUAGES[0])
                    waiting_for_command = 0
                elif "wrong" in command:
                    say("read incorrect guesses", LANGUAGES[0])
                    say_by_char(incorrect_guesses, LANGUAGES[0])
                    waiting_for_command = 0
                else:
                    say("invalid command", LANGUAGES[0])
            else:
                say("invalid command", LANGUAGES[0])

            pygame.display.flip()

        except Exception as e:
            print("Exception: " + str(e))


"""APPLICATION CONTROL"""


# This function is the main control loop for the game and is called once the user presses play in the menu
# This function draws the screen components and loops continuously until the user quits the game
# The program tracks the current game status, keyboard clicks, mousebutton clicks and 
def start_the_game():
    global start_game, audio_interface_enabled, game_started, game_result, activate_audio, current_guess_string, \
        key_pressed, hands_free_rendered, muted
    start_game = 1
    SCREEN.fill(main_color)
    # for testing purposes
    print(correct_word)

    # draw screen elements - keyboard, nav bar and color key
    draw_keyboard(main_color, sub_color2, my_font, my_font_med, keys)
    draw_color_key(correct_color, semi_color, wrong_color, sub_color, my_font_sm, my_font_xsm, lang_index)
    draw_nav_bar(main_color, sub_color2, my_font, muted)
    reset_screen()

    # load background music
    if not muted:
        mixer.music.pause()
        mixer.music.load(BACKGROUND_MUSIC[current_background_music])
        mixer.music.play(-1)

    while True:
        # how program should run when audio interface is not enabled
        while not audio_interface_enabled and start_game:
            draw(sub_color)
            # load end of game screens depending on result
            if game_result == "L":
                stats = handle_stats(0)
                time.sleep(0.2)
                lose_play_again(stats, game_result)
            if game_result == "W":
                stats = handle_stats(1)
                time.sleep(0.2)
                correct_play_again(stats, game_result)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # if user pressed enter key
                    if event.key == pygame.K_RETURN:
                        # try to submit and check guess
                        if len(current_guess_string) == 5 and current_guess_string.lower() in check_list:
                            check_guess(current_guess)
                    # if user presses backspace key, delete letter from guess
                    elif event.key == pygame.K_BACKSPACE:
                        if len(current_guess_string) > 0:
                            delete_letter()
                    # have to press space bar twice to activate audio interface
                    elif not activate_audio and event.key == pygame.K_SPACE:
                        activate_audio = 1
                    # if user pressed space bar already and presses again, enable audio interface
                    elif activate_audio and event.key == pygame.K_SPACE:
                        audio_interface_enabled = 1
                    # if user presses any letter key, add letter to guess
                    else:
                        key_pressed = event.unicode.upper()
                        if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                            if len(current_guess_string) < 5:
                                create_new_letter()
                # if user clicks on screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # check if any letter areas are selected
                        for i in range(3):
                            for area, letter in zip(LETTER_AREAS[i], ALPHABET[i]):
                                if area.collidepoint(event.pos):
                                    key_pressed = letter
                                    if len(current_guess_string) < 5:
                                        create_new_letter()
                        # check if on-screen enter key is clicked, submit and check guess
                        if ENTER_AREA.collidepoint(event.pos):
                            if len(current_guess_string) == 5 and current_guess_string.lower() in check_list:
                                check_guess(current_guess)
                        # check if on-screen delete key is clicked, delete letter from guess
                        if DEL_AREA.collidepoint(event.pos):
                            if len(current_guess_string) > 0:
                                delete_letter()
                        # if menu icon in nav bar is clicked
                        if MENU_AREA.collidepoint(event.pos):
                            start_game = 0
                            game_menu(0)
                        # if info icon in nav bar is clicked load instructions page
                        if INFO_SEL_AREA.collidepoint(event.pos):
                            start_game = 0
                            instructions()
                        # if font icon in nav bar is clicked, open font menu
                        if FONT_SEL_AREA.collidepoint(event.pos):
                            chosen_font = font_menu_control(font_index)
                            menu_set_font(1, chosen_font)
                            reset_screen()
                        if MUTE_AREA.collidepoint(event.pos):
                            if not muted:
                                pause_background_music()
                                muted = 1
                                draw_muted(muted, sub_color2)
                            else:
                                play_background_music()
                                muted = 0
                                draw_muted(muted, sub_color2)

                        # if color icon in nav bar is clicked, open color menu
                        if COLOR_SEL_AREA.collidepoint(event.pos):
                            color_menu_control()
                            reset_screen()
                        # if dark mode icon is clicked, activate dark mode
                        if DARK_SEL_AREA.collidepoint(event.pos):
                            set_dark_mode()
                            reset_screen()
                        # if reset color button is clicked, reset colors to default wordle colors
                        if RESET_COLORS.collidepoint(event.pos):
                            set_correct_color(GREEN)
                            set_semi_color(YELLOW)
                            set_wrong_color(GREY)
                            reset_screen()
                        # if the correct color in color key is clicked, open color selector page
                        if CORRECT_COLOR_AREA.collidepoint(event.pos):
                            chosen_color = draw_color_screen(correct_color, main_color, sub_color, sub_color2, my_font,
                                                             lang_index)
                            set_correct_color(chosen_color)
                            reset_screen()
                        # if the semi correct color in color key is clicked, open color selector page
                        if SEMI_COLOR_AREA.collidepoint(event.pos):
                            chosen_color = draw_color_screen(semi_color, main_color, sub_color, sub_color2, my_font,
                                                             lang_index)
                            set_semi_color(chosen_color)
                            reset_screen()
                        # if the wrong color in color key is clicked, open color selector page
                        if WRONG_COLOR_AREA.collidepoint(event.pos):
                            chosen_color = draw_color_screen(wrong_color, main_color, sub_color, sub_color2, my_font,
                                                             lang_index)
                            set_wrong_color(chosen_color)
                            reset_screen()
                        # if reset game button is clicked, reset entire game
                        if RESET_GAME.collidepoint(event.pos):
                            reset()

            pygame.display.flip()

            # audio reads startup instructions to user when game is loaded
            if not game_started:
                say(STARTUP, LANGUAGES[0])
                game_started = 1

        # how program should run when audio interface is enabled
        while audio_interface_enabled and start_game:
            draw(sub_color)
            # if user loses game
            if game_result == "L":
                eog_sound(game_result)
                say("You have run out of guesses. The word was " + correct_word + " say play again to start over with "
                                                                                  "a new word!",
                    LANGUAGES[0])
                stats = handle_stats(0)
                lose_play_again(stats)
            # if user wins game
            if game_result == "W":
                eog_sound(game_result)
                say("Correct, the word was: " + correct_word + ". say play again to get "
                                                               "a new word.", LANGUAGES[0])
                stats = handle_stats(1)
                correct_play_again(stats)
            # go to hands free control function
            if hands_free_rendered:
                handsfree()
            # when audio mode is first activated read breif instructions to user
            else:
                pygame.display.flip()
                say(ACTIVATED, LANGUAGES[0])
                set_background_music_volume(0.025)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()

            hands_free_rendered = 1


"""SETTERS"""


# sets the background music value 
def set_background_music(selected, value):
    global current_background_music

    current_background_music = value

    mixer.music.pause()
    mixer.music.load(BACKGROUND_MUSIC[current_background_music])
    mixer.music.play(-1)


# sets the language and word list that the program uses to get the word and check guesses
def set_language(selected, value):
    global correct_word, word_list, check_list, lang_index

    lang = LANG_SETTINGS[value][0]
    word_list = LANG_SETTINGS[value][1]
    check_list = LANG_SETTINGS[value][2]
    lang_index = value

    # reset game - current word and game screen
    reset()


# set the language that the about page content should be drawn in
def set_about_lang(selected, value):
    global about_display, about_index
    about_index = value
    about_display = LANG_SETTINGS[value][3]


# send the about page content to the menu drawing functions in the new language
def send_about():
    global about_loaded, about_index
    if about_loaded[about_index] == 0:
        append_about_instructions(about_display)
        about_loaded[about_index] = 1
    about_index = 0


# set the language that the instructions menu should be drawn in
def set_instructions_lang(selected, value):
    global instructions1_display, instructions2_display, instructions3_display, inst_index
    inst_index = value
    instructions1_display = LANG_SETTINGS[value][4]
    instructions2_display = LANG_SETTINGS[value][5]
    instructions3_display = LANG_SETTINGS[value][6]


# send the instructions page content to the menu drawing functions in the new language
def send_instructions():
    global inst_loaded, inst_index
    if inst_loaded[inst_index] == 0:
        append_instructions(instructions1_display, instructions2_display, instructions3_display)
        inst_loaded[inst_index] = 1
    inst_index = 0


# set the langage that the color menu instructions should be drawn in
def set_color_lang(selected, value):
    global color_instructions_display, color_index
    color_index = value
    color_instructions_display = LANG_SETTINGS[value][7]


# send the color menu instructions to the menu drawing functions in the new language
def send_color_instructions():
    global color_index, color_loaded
    if color_loaded[color_index] == 0:
        append_color_instructions(color_instructions_display)
    color_loaded[color_index] = 1
    color_index = 0


# used by the game to set the font of the game for each font size
def menu_set_font(selected, value):
    global font_index, my_font, my_font_med, my_font_sm, my_font_xsm
    font_index = value
    my_font = pygame.font.Font(FONTS[font_index], font_size)
    my_font_med = pygame.font.Font(FONTS[font_index], font_size - 10)
    my_font_sm = pygame.font.Font(FONTS[font_index], font_size - 20)
    my_font_xsm = pygame.font.Font(FONTS[font_index], font_size - 25)


# sets the color used for the correct letters in the game
def set_correct_color(value):
    global correct_color
    try:
        if value[1] < 0:
            correct_color = GREEN
        else:
            correct_color = value
    except Exception as e:
        correct_color = value


# sets the color used for the semi correct letters in the game
def set_semi_color(value):
    global semi_color
    try:
        if value[1] < 0:
            semi_color = YELLOW
        else:
            semi_color = value
    except Exception as e:
        semi_color = value


# sets the color used for the wrong letters in the game
def set_wrong_color(value):
    global wrong_color
    try:
        if value[1] < 0:
            wrong_color = GREY
        else:
            wrong_color = value
    except Exception as e:
        wrong_color = value


# sets the colors of the background and game screen features to dark mode
# if already in dark mode, set back to light mode
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


# decrease the font size of game elements- limited so smallest font cannot be < 8
def decrese_font_size():
    global font_size
    if font_size - 25 > 8:
        font_size -= 2


# increase font size of game elements- limited so larget font cannot exceed 47
def increase_font_size():
    global font_size
    if font_size < 47:
        font_size += 1


"""MENUS"""


# generates the instruction menu when the user clicks the instruction icon in the nav bar
def instructions():
    global start_game
    start_game = 0

    # MENU LOOP
    if not start_game:
        inst_menu.mainloop(SCREEN, background)


# the general applicaition background - menu is drawn on top of this
def background():
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, MENU_COLOR, END_GAME_SCREEN_AREA, 0)


# draws and controls the opening game menu - is also called when user selects menu icon in nav bar
def game_menu(enter_time):
    # main menu object details
    menu = pygame_menu.Menu(
        height=HEIGHT - screen_difference,
        theme=mytheme,
        title='WORLD-LE',
        width=WIDTH - screen_difference
    )

    # draw sub menu items only on first generation of menu on application load
    if enter_time == 1:

        # DRAW COLOR MENU PAGE
        color_menu.add.label(" ", align=pygame_menu.locals.ALIGN_CENTER, font_size=18)
        color_menu.add.selector('Language: ', [("English", 0), ("Spanish", 1), ("German", 2), ("French", 3)],
                                onchange=set_color_lang, default=lang_index)
        color_menu.add.button("Click to Add Instructions in New Language", send_color_instructions)
        color_menu.add.label("Scroll down to see new instructions", align=pygame_menu.locals.ALIGN_CENTER, font_size=22)
        draw_color_instructions(color_instructions_display)
        color_menu.add.color_input("Correct Letter Color  ", color_type='hex', onchange=set_correct_color,
                                   default=correct_color)
        color_menu.add.color_input("Semi Correct Letter Color  ", color_type='hex', onchange=set_semi_color,
                                   default=semi_color)
        color_menu.add.color_input("Wrong Letter Color  ", color_type='hex', onchange=set_wrong_color,
                                   default=wrong_color)
        draw_color_menu()

        # DRAW ABOUT MENU PAGE
        about_menu.add.selector('Language: ', [("English", 0), ("Spanish", 1), ("German", 2), ("French", 3)],
                                onchange=set_about_lang, default=lang_index)
        about_menu.add.button("Click to Add Content in New Language", send_about)
        about_menu.add.label("Scroll down to see new information", align=pygame_menu.locals.ALIGN_CENTER, font_size=22)
        draw_about_page(about_display)

        # DRAW INSTRUCTIONS MENU PAGE
        inst_menu.add.selector('Language: ', [("English", 0), ("Spanish", 1), ("German", 2), ("French", 3)],
                               onchange=set_instructions_lang, default=0)
        inst_menu.add.button("Click to Add Instructions in New Language", send_instructions)
        inst_menu.add.label("Scroll down to see new instructions", align=pygame_menu.locals.ALIGN_CENTER, font_size=22)
        draw_instructions(instructions1_display, instructions2_display, instructions3_display)
        inst_menu.add.button("Play Game", start_the_game)
        for m in SPACES: inst_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=18)

    # DRAW MAIN MENU PAGE
    menu.add.button('Play', start_the_game)
    menu.add.selector('Language: ', [("English", 0), ("Spanish", 1), ("German", 2),
                                     ("French", 3), ("Kid Friendly", 4)],
                      onchange=set_language, default=lang_index)
    menu.add.selector('Background Music: ', [("     Synth    ", 0), ("Happy Beat", 1),
                                             ("     Bop      ", 2), (" Meditation ", 3),
                                             ("Electro Chill", 4), ("    Escape   ", 5),
                                             (" Traditional ", 6), (" Nature 1 ", 7),
                                             (" Nature 2 ", 8), (" Nature 3 ", 9),
                                             (" Jeopardy ", 10)],
                      onchange=set_background_music,
                      default=current_background_music)
    menu.add.selector('Change Font: ', [("Free Sans", 0), ("Comic Sans", 1), ("Lil Grotesk", 2),
                                        ("GFS Didot Bold", 3), ("First Coffee", 4), ("Wigners Friend", 5)],
                      onchange=menu_set_font, default=font_index)
    menu.add.button('Set Colors', color_menu)
    menu.add.button('Instructions', inst_menu)
    menu.add.button('About', about_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    # loop the menu until the user starts the game
    if not start_game:
        menu.mainloop(SCREEN, background)


# main function calls the menu on startup and starts the backgrouns music
def main():
    try:
        mixer.init()
        mixer.music.load('sound/background_music/the_trail_instruments_trimmed.mp3')
        mixer.music.set_volume(0.2)
    except Exception as e:
        print(str(e) + "Something went wrong")

    play_background_music()
    game_menu(1)


if __name__ == "__main__":
    main()
