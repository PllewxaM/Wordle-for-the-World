import pygame

#  COLORS
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

HIGH_CONTRAST_1 = "#f803fc"
HIGH_CONTRAST_2 = "#03f0fc"
HIGH_CONTRAST_3 = "#fc4503"

COLORS = [[RED, REDORANGE, ORANGE, ORANGEYELLOW], 
        [YELLOW, YELLOWGREEN, GREEN, GREENBLUE], 
        [BLUE, LT_BLUE, BLUEPURPLE, PURPLE],
        [LT_PURPLE, PURPLEPINK, PINK, REDPINK]]

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

# KEYBOARD
ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

# SCREEN SIZE
WIDTH, HEIGHT = 850, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# CLICK AREAS

# make keyboard areas - so click on screen activates letter
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
ENTER_AREA = pygame.Rect(635, 670, 125, 70)
DEL_AREA = pygame.Rect(100, 670, 102, 70)

MENU_AREA = pygame.Rect(10, 10, 30, 30)
FONT_SEL_AREA = pygame.Rect(WIDTH - 55, 10, 30, 35)
COLOR_SEL_AREA = pygame.Rect(WIDTH - 105, 10, 30, 30)

# HIGH_CONTRAST_AREA = pygame.Rect()
PICK_ONE_AREA = pygame.Rect((WIDTH - 400)/ 2, HEIGHT - 550, 400, 75)
PICK_TWO_AREA = pygame.Rect((WIDTH - 400)/ 2, HEIGHT - 450, 400, 75)
PICK_THREE_AREA = pygame.Rect((WIDTH - 400)/ 2, HEIGHT - 350, 400, 75)
PICK_FOUR_AREA = pygame.Rect((WIDTH - 400)/2, HEIGHT - 225, 400, 75)
CANCEL_AREA = pygame.Rect((WIDTH - 200)/ 2, HEIGHT - 125, 200, 50)

DARK_SEL_AREA = pygame.Rect(WIDTH - 155, 10, 30, 30)

CORRECT_COLOR_AREA = pygame.Rect(WIDTH - 155, 130, 130, 30)
SEMI_COLOR_AREA = pygame.Rect(WIDTH - 155, 180, 130, 30)
WRONG_COLOR_AREA = pygame.Rect(WIDTH - 155, 235, 130, 30)