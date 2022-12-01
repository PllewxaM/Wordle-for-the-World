import pygame_menu
from pygame_menu import Theme
from constants import *

pygame.init()

screen_difference = 50
padding = 8
font_index = 0

# MENU THEMES
mytheme = Theme(background_color = WHITE, 
                title_font = 'assets/fonts/Retronoid.ttf',
                title_font_size = 100,
                title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE,
                title_offset = (WIDTH / 2 - 275, padding * 5),
                title_font_color = BLACK,
                title_close_button_background_color = BLACK,
                selection_color = BLACK,
                widget_selection_effect = pygame_menu.widgets.NoneSelection(),
                widget_font_color = BLACK,
                widget_font = FONTS[font_index],
                widget_padding = padding)

color_theme = pygame_menu.themes.THEME_GREEN.copy()
color_theme.background_color = WHITE
color_theme.font_color = BLACK
color_theme.title_font = FONTS[font_index]
color_theme.title_font_color = WHITE
color_theme.title_fixed = True
color_theme.widget_font_color = BLACK
color_theme.widget_font_size = 25
color_theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()

about_theme = color_theme
inst_theme = color_theme


# MENUS

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

# DRAW MENUS

def draw_instructions(instructions1_display, instructions2_display, instructions3_display):

    inst_menu.add.label(" ", align=pygame_menu.locals.ALIGN_LEFT, font_size=18)
    
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


def append_instructions(instructions1_display, instructions2_display, instructions3_display):
    inst_menu.add.label(SPACER, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

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


def draw_about_page(about_display):
    for m in about_display:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    for m in SPACES:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    about_menu.add.button("Back", pygame_menu.events.BACK)

    for m in SPACES:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)


def append_about_instructions(about_display):
    about_menu.add.label(SPACER, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    for m in about_display:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)


# COLOR MENU

def draw_color_menu():
    for m in SPACES:
        color_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    color_menu.add.button("Back", pygame_menu.events.BACK)

    for m in SPACES:
        color_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)


def draw_color_instructions(color_instructions_display):
    color_menu.add.label(" ", align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    for m in color_instructions_display: 
            color_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)
    
    for m in SPACES:
        color_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)


def append_color_instructions(color_instructions_display):
    color_menu.add.label(SPACER, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)
    draw_color_instructions(color_instructions_display)
    for m in SPACES:
        color_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=18)

    