# File contains all constants used in the program

import pygame
from messages import *
from word_files.englishwords import *
from word_files.spanishwords import *
from word_files.frenchwords import *
from word_files.germanwords import *
from word_files.kidwords import *

#  COLORS
# all colors used in the game
DK_RED = "#c70606"
RED = "#d90000"
REDORANGE = "#ff6100"
ORANGE = "#ff8600"
ORANGEYELLOW = "#ffc700"
YELLOW = "#c9b458"
YELLOWGREEN = "#a8d800"
GREEN = "#6aaa64"
GREENBLUE = "#00d9c5"
BLUE = "#0085ff"
LT_BLUE = "#91dcfa"
BLUEPURPLE = "#623ced"
PURPLE = "#9150f3"
LT_PURPLE = "#b39dfc"
PURPLEPINK = "#b912f4"
PINK = "#fb00ff"
REDPINK = "#ff0081"
GREY = "#787c7e"
LT_GREY = "#abadaf"
WHITE = "#ffffff"
BLACK = "#000000"

# used in menu screen border
MENU_COLOR = "#89a3b0"

# high contract mode colors
HIGH_CONTRAST_1 = "#f803fc"
HIGH_CONTRAST_2 = "#03f0fc"
HIGH_CONTRAST_3 = "#fc4503"

# colors used in color menu
COLORS = [[RED, REDORANGE, ORANGE, ORANGEYELLOW], 
        [YELLOW, YELLOWGREEN, GREEN, GREENBLUE], 
        [BLUE, LT_BLUE, BLUEPURPLE, PURPLE],
        [LT_PURPLE, PURPLEPINK, PINK, REDPINK]]

# GAME BOARD

# game board spacing and square size
LETTER_X_SPACING = 65
LETTER_Y_SPACING = 70
LETTER_SIZE = 60

BOARD = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]

# KEYBOARD
# letters used in game
ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

#LANGUAGE
# Audio language options - only english currently used
LANGUAGES = ['en', 'es', 'fr']
# Used when language is changed by user - contains word lists and menu content in different languages
LANG_SETTINGS = [["en", EN_WORDS, EN_WORDS, ABOUT_ENGLISH, INSTRUCTIONS1_ENGLISH, INSTRUCTIONS2_ENGLISH, INSTRUCTIONS3_ENGLISH, COLOR_INSTRUCTIONS_ENGLISH], 
                ["sp", SP_WORDS, SP_WORDS, ABOUT_SPANISH, INSTRUCTIONS1_SPANISH, INSTRUCTIONS2_SPANISH, INSTRUCTIONS3_SPANISH, COLOR_INSTRUCTIONS_SPANISH], 
                ["ger", GER_WORDS, GER_WORDS, ABOUT_GERMAN, INSTRUCTIONS1_GERMAN, INSTRUCTIONS2_GERMAN, INSTRUCTIONS3_GERMAN, COLOR_INSTRUCTIONS_GERMAN], 
                ["fr", FR_WORDS, FR_WORDS, ABOUT_FRENCH, INSTRUCTIONS1_FRENCH, INSTRUCTIONS2_FRENCH, INSTRUCTIONS3_FRENCH, COLOR_INSTRUCTIONS_FRENCH], 
                ["kid", KID_WORDS, EN_WORDS, ABOUT_ENGLISH, INSTRUCTIONS1_ENGLISH, INSTRUCTIONS2_ENGLISH, INSTRUCTIONS3_ENGLISH, COLOR_INSTRUCTIONS_ENGLISH]]

# GAME WORDS
# used to change different game content language when user changes the language
CHANGE_FONTS = ["Change Font","Cambiar Fuente", "Schriftart Andern," "Changer la Police", "Change Font"]
DONE = ["DONE", "LISTO", "FERTIG", "Terminé", "DONE"]
BOLD = ["BOLD", "BOLD", "BOLD", "GRAS", "BOLD"]
COLOR_KEY = ["Color Key", "Clave de Color", "Farbschlüssel", "Clé de Couleur", "Color Key"]
CORRECT = ["CORRECT", "CORRECTA", "RICHTIG", "CORRECTE", "CORRECT"]
SEMI = ["SEMI", "SEMI", "HALB", "SEMI-", "SEMI"]
WRONG = ["WRONG", "INCORRECTA", "FALSCH", "INCORRECTE", "WRONG"]
RESET_COLOR = ["Reset Colors", "Restablecer Colores", "Farben Zurücksetzen", "Réinitialiser les Couleurs", "Reset Colors"]
RESET_GAMES = ["Reset Game", "Restablecer Juego", "Spiel Zurücksetzen", "Réinitialiser le Jeu", "Reset Game"]
CHANGE_COLOR = ["Change Color", "Cambiar el Color", "Farbe Ändern", "Changer de Couleur", "Change Color"]
SELECT_COLOR = ["SELECT COLOR", "SELECCIONAR COLOR", "WÄHLE SIE DIE ZU", "SÉLECTIONNER LA COULEUR", "SELECT COLOR"]
TO_CHANGE = ["TO CHANGE", "PARA CAMBIAR", "ÄNDERNDE FARBE AUS", "À CHANGER", "TO CHANGE"]
CHANGE_CORRECT_COLOR = ["Change Correct Color", "Cambiar Color Correcto", "Richtige Farbe Ändern", "Modifier la Couleur Correcte", "Change Correct Color"]
CHANGE_SEMI_COLOR = ["Change Semi Correct Color", "Cambiar Color Semicorrecto", "Halbrichtige Farbe Ändern", "Modifier la Couleur Semi-Correcte", \
        "Change Semi Correct Color"]
CHANGE_WRONG_COLOR = ["Change Wrong Color", "Cambiar Color Incorrecto", "Falsche Farbe Ändern", "Modifier la Mauvaise Couleur", "Change Wrong Color"]
HIGH_CONTRAST = ["Activate High Contrast Mode", "Activar Modo de Contraste Alto", "Hochkontrastmodus Aktivieren", "Activer le Mode de Contraste Élevé", \
        "Activate High Contrast Mode"]
CANCEL = ["CANCEL", "CANCELAR", "ABBRECHEN", "ANNULER", "CANCEL"]

# MUSIC

# list of background music options
BACKGROUND_MUSIC = ['sound/background_music/traditional.ogg',
                    'sound/background_music/happy_beat_drop.mp3',
                    'sound/background_music/bops.mp3',  # 2
                    'sound/background_music/guru_meditation.mp3',
                    'sound/background_music/chill_electro_sax.mp3',  # 4
                    'sound/background_music/escaping.mp3',
                    'sound/background_music/Synth.mp3',  # 6
                    'sound/background_music/nature_drizzle.mp3',
                    'sound/background_music/nature_fire.mp3',  # 8
                    'sound/background_music/nature_river.mp3',
                    'sound/background_music/nature_waves.mp3']  # 10

# list of font options
FONTS = ['assets/fonts/FreeSans.otf', 
        'assets/fonts/ComicSans.ttf',
        'assets/fonts/LilGrotesk.otf',
        'assets/fonts/GFSDidotBold.otf',
        'assets/fonts/FirstCoffee.otf',
        'assets/fonts/WignersFriendRoman.ttf',
        'assets/fonts/FreeSansBold.otf']

# SCREEN SIZE
# game screen dimensions
WIDTH, HEIGHT = 850, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# used to reound the corners of different screen features
ROUND = 4

# SCREEN AREAS

# WIN/LOSE SCREEN AREA
END_GAME_SCREEN_AREA = pygame.Rect(10, 10, WIDTH - 20, HEIGHT - 20)

# KEYBOARD KEY AREAS
Q_AREA = pygame.Rect(125, 500, 57, 70)
W_AREA = pygame.Rect(185, 500, 57, 70)
E_AREA = pygame.Rect(245, 500, 57, 70)
R_AREA = pygame.Rect(305, 500, 57, 70)
T_AREA = pygame.Rect(365, 500, 57, 70)
Y_AREA = pygame.Rect(425, 500, 57, 70)
U_AREA = pygame.Rect(485, 500, 57, 70)
I_AREA = pygame.Rect(545, 500, 57, 70)
O_AREA = pygame.Rect(605, 500, 57, 70)
P_AREA = pygame.Rect(665, 500, 57, 70)
A_AREA = pygame.Rect(160, 585, 57, 70)
S_AREA = pygame.Rect(220, 585, 57, 70)
D_AREA = pygame.Rect(280, 585, 57, 70)
F_AREA = pygame.Rect(340, 585, 57, 70)
G_AREA = pygame.Rect(400, 585, 57, 70)
H_AREA = pygame.Rect(460, 585, 57, 70)
J_AREA = pygame.Rect(520, 585, 57, 70)
K_AREA = pygame.Rect(580, 585, 57, 70)
L_AREA = pygame.Rect(640, 585, 57, 70)
Z_AREA = pygame.Rect(210, 670, 57, 70)
X_AREA = pygame.Rect(270, 670, 57, 70)
C_AREA = pygame.Rect(330, 670, 57, 70)
V_AREA = pygame.Rect(390, 670, 57, 70)
B_AREA = pygame.Rect(450, 670, 57, 70)
N_AREA = pygame.Rect(510, 670, 57, 70)
M_AREA = pygame.Rect(570, 670, 57, 70)
LETTER_AREAS = [[Q_AREA, W_AREA, E_AREA, R_AREA, T_AREA, Y_AREA, U_AREA, I_AREA, O_AREA, P_AREA],
                [A_AREA, S_AREA, D_AREA, F_AREA, G_AREA, H_AREA, J_AREA, K_AREA, L_AREA], 
                [Z_AREA, X_AREA, C_AREA, V_AREA, B_AREA, N_AREA, M_AREA]]
ENTER_AREA = pygame.Rect(635, 670, 125, 70)
DEL_AREA = pygame.Rect(100, 670, 102, 70)

# NAVAGATION BAR ICON AREAS
MENU_AREA = pygame.Rect(10, 10, 30, 30)
FONT_SEL_AREA = pygame.Rect(WIDTH - 55, 10, 30, 35)
COLOR_SEL_AREA = pygame.Rect(WIDTH - 105, 10, 30, 30)
DARK_SEL_AREA = pygame.Rect(WIDTH - 155, 10, 30, 30)
INFO_SEL_AREA = pygame.Rect(WIDTH - 205, 10, 30, 30)

# FONT AND COLOR MENU AREAS
SM_MENU_AREA_BACK = pygame.Rect((WIDTH - (WIDTH * 0.6))/ 2, (HEIGHT - (HEIGHT * 0.8)) / 2, WIDTH * 0.6, HEIGHT * 0.8)
SM_MENU_AREA_FRONT = pygame.Rect((WIDTH - (WIDTH * 0.6))/ 2 + 3, (HEIGHT - (HEIGHT * 0.8)) / 2 + 3, WIDTH * 0.6 - 6, HEIGHT * 0.8 - 6)

# COLOR MENU - CHOOSE WHICH COLOR TO CHANGE
PICK_ONE_AREA = pygame.Rect((WIDTH - 400)/ 2, HEIGHT - 550, 400, 75)
PICK_TWO_AREA = pygame.Rect((WIDTH - 400)/ 2, HEIGHT - 450, 400, 75)
PICK_THREE_AREA = pygame.Rect((WIDTH - 400)/ 2, HEIGHT - 350, 400, 75)
PICK_FOUR_AREA = pygame.Rect((WIDTH - 400)/2, HEIGHT - 250, 400, 75)
CANCEL_AREA = pygame.Rect((WIDTH - 200)/ 2, HEIGHT - 140, 200, 50)

# COLOR KEY AREAS
CORRECT_COLOR_AREA = pygame.Rect(WIDTH - 155, 130, 130, 30)
SEMI_COLOR_AREA = pygame.Rect(WIDTH - 155, 180, 130, 30)
WRONG_COLOR_AREA = pygame.Rect(WIDTH - 155, 235, 130, 30)
RESET_COLORS = pygame.Rect(WIDTH - 170, 300, 155, 30)
RESET_GAME = pygame.Rect(WIDTH - 170, 350, 155, 30)

# ADDITIONAL MENU AREAS
DONE_AREA = pygame.Rect((WIDTH - 200) / 2, HEIGHT - 150, 200, 50)
BOLD_AREA = pygame.Rect((WIDTH - 200) / 2, HEIGHT - 220, 200, 50)
PLUS_AREA = pygame.Rect((WIDTH / 2) - 200, HEIGHT - 220, 50, 50)
SUB_AREA = pygame.Rect((WIDTH / 2) + 150, HEIGHT - 220, 50, 50)

# FONT SLEECTION AREAS
FONT_ONE_AREA = pygame.Rect((WIDTH - 400)/ 2, HEIGHT - 595, 400, 50)
FONT_TWO_AREA = pygame.Rect((WIDTH - 400)/ 2, HEIGHT - 535, 400, 50)
FONT_THREE_AREA = pygame.Rect((WIDTH - 400)/ 2, HEIGHT - 475, 400, 50)
FONT_FOUR_AREA = pygame.Rect((WIDTH - 400)/ 2, HEIGHT - 415, 400, 50)
FONT_FIVE_AREA = pygame.Rect((WIDTH - 400)/ 2, HEIGHT - 355, 400, 50)
FONT_SIX_AREA = pygame.Rect((WIDTH - 400)/ 2, HEIGHT - 295, 400, 50)

# COLOR SELECTION AREAS
COLOR1 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 70, (HEIGHT - (HEIGHT * 0.8)) / 2 + 125, 75, 75)
COLOR2 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 170, (HEIGHT - (HEIGHT * 0.8)) / 2 + 125, 75, 75)
COLOR3 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 270, (HEIGHT - (HEIGHT * 0.8)) / 2 + 125, 75, 75)
COLOR4 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 370, (HEIGHT - (HEIGHT * 0.8)) / 2 + 125, 75, 75)
COLOR5 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 70, (HEIGHT - (HEIGHT * 0.8)) / 2 + 225, 75, 75)
COLOR6 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 170, (HEIGHT - (HEIGHT * 0.8)) / 2 + 225, 75, 75)
COLOR7 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 270, (HEIGHT - (HEIGHT * 0.8)) / 2 + 225, 75, 75)
COLOR8 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 370, (HEIGHT - (HEIGHT * 0.8)) / 2 + 225, 75, 75)
COLOR9 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 70, (HEIGHT - (HEIGHT * 0.8)) / 2 + 325, 75, 75)
COLOR10 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 170, (HEIGHT - (HEIGHT * 0.8)) / 2 + 325, 75, 75)
COLOR11 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 270, (HEIGHT - (HEIGHT * 0.8)) / 2 + 325, 75, 75)
COLOR12 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 370, (HEIGHT - (HEIGHT * 0.8)) / 2 + 325, 75, 75)
COLOR13 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 70, (HEIGHT - (HEIGHT * 0.8)) / 2 + 425, 75, 75)
COLOR14 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 170, (HEIGHT - (HEIGHT * 0.8)) / 2 + 425, 75, 75)
COLOR15 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 270, (HEIGHT - (HEIGHT * 0.8)) / 2 + 425, 75, 75)
COLOR16 = pygame.Rect((WIDTH - (WIDTH * 0.6)) / 2 + 370, (HEIGHT - (HEIGHT * 0.8)) / 2 + 425, 75, 75)

# color areas in a list
COLOR_AREAS = [[COLOR1, COLOR2, COLOR3, COLOR4],
                [COLOR5, COLOR6, COLOR7, COLOR8],
                [COLOR9, COLOR10, COLOR11, COLOR12],
                [COLOR13, COLOR14, COLOR15, COLOR16]]

# areas around the mini menus (color and font menus)
EXIT_MENU_AREA1 = pygame.Rect(0, 0, WIDTH, HEIGHT * 0.1)
EXIT_MENU_AREA2 = pygame.Rect(0, HEIGHT - (HEIGHT * 0.1), WIDTH, HEIGHT * 0.1)
EXIT_MENU_AREA3 = pygame.Rect(0, HEIGHT * 0.1, WIDTH * 0.2, HEIGHT * 0.8)
EXIT_MENU_AREA4 = pygame.Rect(WIDTH - (WIDTH * 0.2), HEIGHT * 0.1, WIDTH * 0.2, HEIGHT * 0.8)


FUZZY_CHAR = [["aye", 'a'],["bee", 'b'],["see", 'c'],
              ["gee", 'g'],["ache", 'h'],["eye", 'i'],
              ["jay", 'j'],["kay", 'k'],["elle", 'l'],
              ["el", 'l'],["oh", 'o'],["pea", 'p'],
              ["pee", 'p'],["queue", 'q'],["are", 'r'],
              ["es", 's'],["tea", 't'],["tee", 't'],
              ["you", 'u'],["double you", 'w'],["ex", 'x'],
              ["axe", 'x'],["why", 'y']]

WORD_TO_INT = [['one', 1],['won', 1],
               ['two', 2],['to', 2],['too', 2],
               ['three', 3],
               ['four', 4],['for', 4],
               ['five', 5],['six', 6],
               ['seven', 7], ['eight', 8],
               ['nine', 9], ['ten', 10]]