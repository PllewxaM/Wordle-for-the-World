import pygame
import sys
import random
import words
from words import *
from gtts import gTTS
import speech_recognition as sr
import os
from playsound import playsound
import time

pygame.init()

# Audio Interface Initializers
r = sr.Recognizer()
mic = sr.Microphone()
audio_interface_enabled = 0

# Adjust based on current environment, start high and reduce
# until good results found, good values between 50 and 4000
r.energy_threshold = 4000

# Text-to-speech languages: English, Spanish, French
languages = ['en', 'es', 'fr']
current_language = 0

# Long sections of text used for instructing hands-free user
startup = "Welcome to wordle for the world, if you need help, say, tutorial"
tutorial = "Hello and welcome to wordle for the world. Im here to help you learn the commands to " \
           "play the game in hands free mode. To hold onto a letter you may want to guess later, say " \
           "the keyword, stash, followed by the letter you would like to hold onto. To hear your " \
           "current guess, say the command, read guess. To submit your current guess, say the keyword, " \
           "submit."

# COLORS
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"

WIDTH, HEIGHT = 700, 750

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
SCREEN.fill(WHITE)
pygame.display.set_caption("World-le")
pygame.display.set_icon(pygame.image.load("assets/Icon.png"))
pygame.display.update()


CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]

FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
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
indicators = []

guesses_count = 0
guesses = [[]] * 6

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
    with mic as source:
        audio = r.listen(source)

    cur_text = r.recognize_google(audio)
    return cur_text


def say_by_char(response, language):
    chars = [*response]
    for c in chars:
        say(c, language)
        time.sleep(0.1)


def say_and_confirm_by_char(guess, correct, language):
    chars = [*guess]
    correct = [*correct]
    correct_index = 0
    for c in chars:
        say(c, language)
        time.sleep(0.1)
        if c == correct[correct_index]:
            playsound('sound_effects/CorrectCharacter.wav')
        elif c in correct:
            playsound('sound_effects/SemiCorrectCharacter.wav')
        else:
            playsound('sound_effects/IncorrectCharacter.wav')
        correct_index = correct_index + 1


# draw squares
def draw():
    for col in range(0, 5):
        for row in range(0, 6):
            pygame.draw.rect(SCREEN, BLACK, [col * 65 + 175, row * 70 + 10, 60, 60], 1, 1)
            piece_text = FONT.render(BOARD[row][col], True, GREY)
            SCREEN.blit(piece_text, (col * 100 + 10, row * 100 + 15))


# draw keyboard
class Indicator:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 57, 70)
        self.bg_color = OUTLINE

    def draw(self):
        # Puts the indicator and its text on the screen at the desired position.
        pygame.draw.rect(SCREEN, self.bg_color, self.rect)
        self.text_surface = FONT.render(self.text, True, "white")
        self.text_rect = self.text_surface.get_rect(center=(self.x+27, self.y+30))
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()


# ?
indicator_x, indicator_y = 45, 450

for i in range(3):
    for letter in ALPHABET[i]:
        new_indicator = Indicator(indicator_x, indicator_y, letter)
        indicators.append(new_indicator)
        new_indicator.draw()
        indicator_x += 60
    indicator_y += 85
    if i == 0:
        indicator_x = 80
    elif i == 1:
        indicator_x = 130


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
    for i in range(5):
        lowercase_letter = guess_to_check[i].text.lower()
        if lowercase_letter in CORRECT_WORD:
            if lowercase_letter == CORRECT_WORD[i]:
                guess_to_check[i].bg_color = GREEN
                for indicator in indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = GREEN
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                if not game_decided:
                    game_result = "W"
            else:
                guess_to_check[i].bg_color = YELLOW
                for indicator in indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = YELLOW
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = GREY
            for indicator in indicators:
                if indicator.text == lowercase_letter.upper():
                    indicator.bg_color = GREY
                    indicator.draw()
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
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result
    SCREEN.fill("white")
    guesses_count = 0
    CORRECT_WORD = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
    guesses = [[]] * 6
    current_guess = []
    current_guess_string = ""
    game_result = ""
    pygame.display.update()
    for indicator in indicators:
        indicator.bg_color = OUTLINE
        indicator.draw()


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

    pygame.display.flip()

while audio_interface_enabled:
    draw()
    if game_result == "L":
        lose_play_again()
    if game_result == "W":
        correct_play_again()

    try:
        command = listen()
        print(command)

        if "tutorial" in command:  # Starts tutorial
            say(tutorial, languages[current_language])
        elif "stash" in command:  # Places character(s) into current guess
            say("stash", languages[current_language])
        elif "delete" in command:  # Deletes all characters from stash
            say("delete", languages[current_language])
        elif "read" in command:
            if "guess" in command or "gas" in command or "guest" in command:
                if "one" in command or "won" in command or "1" in command:
                    say("read first guess", languages[current_language])
                elif "two" in command or "to" in command or "2" in command or "too" in command:
                    say("read second guess", languages[current_language])
                elif "three" in command or "3" in command:
                    say("read third guess", languages[current_language])
                elif "four" in command or "for" in command or "4" in command:
                    say("read fourth guess", languages[current_language])
                elif "five" in command or "5" in command:
                    say("read fifth guess", languages[current_language])
                else:
                    say("Read current guess not yet submitted", languages[current_language])
            elif "semi" in command:
                say("read semi correct guesses by character", languages[current_language])
            elif "wrong" in command:
                say("read incorrect guesses by character", languages[current_language])
            else:
                say("invalid command", languages[current_language])
        elif "submit" in command:
            say("submit", languages[current_language])
        else:
            say("invalid command", languages[current_language])

    except Exception as e:
        print("exception: " + repr(e))

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

    pygame.display.flip()
