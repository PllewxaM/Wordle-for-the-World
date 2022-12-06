from helpers.classes import *
import sys

# DRAW GAME BOARD #


# Draws the game board gird on the screen - the squares where the letters go
def draw(sub_color):
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


# draws the mute button on the nav bar depending on the state of sound
def draw_muted(muted, sub_color2):
    if not muted:
        pygame.draw.rect(SCREEN, sub_color2, MUTE_AREA, 0)
        draw_icon('assets/Speaker_Icon.png', (30, 30), ((WIDTH - 190), 25))
    else:
        pygame.draw.rect(SCREEN, sub_color2, MUTE_AREA, 0)
        draw_icon('assets/Mute_Icon.png', (30, 30), ((WIDTH - 190), 25))


# Draws the navagation bar at the top of the screen and the contents on the bar
def draw_nav_bar(main_color, sub_color2, my_font, muted):
    # actual nav bar
    pygame.draw.rect(SCREEN, sub_color2, [0, 0, WIDTH, 50], 0)

    # hamburger menu
    draw_icon('assets/menu.png', (30, 30), ((WIDTH - 825), 25))

    # instructions icon
    draw_icon('assets/instructions.png', (30, 30), ((WIDTH - 775), 25))
    
    # font selector icon
    draw_icon('assets/font-icon.png', (30, 35), ((WIDTH - 40), 25))

    # color selector icon
    draw_icon('assets/color.png', (30, 30), ((WIDTH - 90), 25))

    # dark mode icon 
    draw_icon('assets/dark.png', (30, 30), ((WIDTH - 140), 25))

    # mute icon
    draw_muted(muted, sub_color2)

    # Draws title of the application
    draw_text(my_font, "WORLD-LE", main_color, (WIDTH / 2, 25))


# DRAW FONT MENU #

# draw the font menu and call functions to draw other font menu elements
def draw_font_menu(main_color, sub_color, sub_color2, my_font, font_size, lang_index) :
    # draw background and front mini menu screens
    pygame.draw.rect(SCREEN, GREY, SM_MENU_AREA_BACK, 0, ROUND)
    pygame.draw.rect(SCREEN, main_color, SM_MENU_AREA_FRONT, 0, ROUND)

    # draw menu title
    draw_text(my_font, CHANGE_FONTS[lang_index], sub_color, (WIDTH / 2, (HEIGHT - (HEIGHT * 0.8)) / 2 + 45))

    # draw font options
    draw_font_options(sub_color2, font_size, lang_index)

    # draw size increase / decrease buttons
    draw_font_size_adjust(my_font)

    # draw done button
    pygame.draw.rect(SCREEN, sub_color2, DONE_AREA, 0, ROUND)
    draw_text(my_font, DONE[lang_index], WHITE, (WIDTH / 2, HEIGHT - 125))


# Draws font options on the font menu
def draw_font_options(sub_color2, font_size, lang_index):
    size = font_size - 10
    # draw font options
    pygame.draw.rect(SCREEN, LT_GREY, FONT_ONE_AREA, 0, ROUND)
    draw_text(pygame.font.Font(FONTS[0], size), "Free Sans Font", BLACK, (WIDTH / 2, HEIGHT - 570))

    pygame.draw.rect(SCREEN, LT_GREY, FONT_TWO_AREA, 0, ROUND)
    draw_text(pygame.font.Font(FONTS[1], size), "Comic Sans", BLACK, (WIDTH / 2, HEIGHT - 510))

    pygame.draw.rect(SCREEN, LT_GREY, FONT_THREE_AREA, 0, ROUND)
    draw_text(pygame.font.Font(FONTS[3], size), "GFS Didot Bold", BLACK, (WIDTH / 2, HEIGHT - 450))

    pygame.draw.rect(SCREEN, LT_GREY, FONT_FOUR_AREA, 0, ROUND)
    draw_text(pygame.font.Font(FONTS[2], size), "Lil Grotesk", BLACK, (WIDTH / 2, HEIGHT - 390))

    pygame.draw.rect(SCREEN, LT_GREY, FONT_FIVE_AREA, 0, ROUND)
    draw_text(pygame.font.Font(FONTS[5], size), "Wigners Friend", BLACK, (WIDTH /2, HEIGHT - 330))

    pygame.draw.rect(SCREEN, LT_GREY, FONT_SIX_AREA, 0, ROUND)
    draw_text(pygame.font.Font(FONTS[4], size), "First Coffee", BLACK, (WIDTH / 2, HEIGHT - 265))

    # draw bold option
    pygame.draw.rect(SCREEN, sub_color2, BOLD_AREA, 0, ROUND)
    draw_text(pygame.font.Font(FONTS[6], size), BOLD[lang_index], WHITE, (WIDTH / 2, HEIGHT - 195))


# Draws the increase and decrease buttons on the font menu
def draw_font_size_adjust(my_font):
    pygame.draw.rect(SCREEN, GREY, PLUS_AREA, 0, ROUND)
    draw_text(my_font, "+", WHITE, ((WIDTH / 2) - 175, HEIGHT - 195))

    pygame.draw.rect(SCREEN, GREY, SUB_AREA, 0, ROUND)
    draw_text(my_font, "-", WHITE, ((WIDTH / 2) + 175, HEIGHT - 195))
    


# DRAW COLOR MENU #


# Draws the color key to show the user what colors are selected and what they mean
def draw_color_key(correct_color, semi_color, wrong_color, sub_color, my_font_sm, my_font_xsm, lang_index):
    # function variables
    key_width, key_height = 155, 225
    block_x, block_y = WIDTH - 170, 70
    title_x, title_y = WIDTH - 185 / 2, 95
    color_x, color_y = WIDTH - 155, 130
    size, shape = 30, 100
    text_x = WIDTH - 70

    # Draws the color key outline and title of area
    pygame.draw.rect(SCREEN, sub_color, [block_x, block_y, key_width, key_height], 1, ROUND)
    draw_text(my_font_sm, COLOR_KEY[lang_index], sub_color, (title_x, title_y))

    # draws the correct color circle and lable of color
    pygame.draw.rect(SCREEN, correct_color, [color_x, color_y, size, size], 0, shape)
    draw_text(my_font_xsm, CORRECT[lang_index], sub_color, (text_x, color_y + 15))

    # draws the semi correct color circle and lable of color
    pygame.draw.rect(SCREEN, semi_color, [color_x, color_y + 50, size, size], 0, shape)
    draw_text(my_font_xsm, SEMI[lang_index], sub_color, (text_x, color_y + 55))
    draw_text(my_font_xsm, CORRECT[lang_index], sub_color, (text_x, color_y + 75))

    # draws the wrong color circle and lable of color
    pygame.draw.rect(SCREEN, wrong_color, [color_x, color_y + 105, size, size], 0, shape)
    draw_text(my_font_xsm, WRONG[lang_index], sub_color, (text_x, color_y + 120))

    # draw reset colors button
    pygame.draw.rect(SCREEN, LT_GREY, RESET_COLORS, 0, ROUND)
    draw_text(my_font_sm, RESET_COLOR[lang_index], BLACK, (title_x, color_y + 185))

    pygame.draw.rect(SCREEN, LT_GREY, RESET_GAME, 0, ROUND)
    draw_text(my_font_sm, RESET_GAMES[lang_index], BLACK, (title_x, color_y + 235))

    pygame.display.update()


# Draw the color squares on the color menu
def draw_color_squrs():
    # size of the color squares
    size = 75
    # starting position of the first color square
    c_x = ((WIDTH - WIDTH * 0.6) / 2 + 70)
    c_y = (HEIGHT - HEIGHT * 0.8) / 2 + 125
    # spacing between each square
    shift_amount = 100

    # draw four rows of color squares, colors are the colors in the color list
    for i in range(4):
        for color in COLORS[i]:
            # draw square
            pygame.draw.rect(SCREEN, color, (c_x, c_y, size, size), 0, ROUND)
            # next square starting x position
            c_x += shift_amount
        # next row starting x and y position
        c_x = ((WIDTH - WIDTH * 0.6) / 2 + 70)
        c_y += shift_amount

    pygame.display.update()


# Draws the color menu and controls the menu functionality, returns selected color
def draw_color_screen(current, main_color, sub_color, sub_color2, my_font, lang_index):
    value = current
    done = 0

    # draw background screen
    pygame.draw.rect(SCREEN, GREY, SM_MENU_AREA_BACK, 0, ROUND)
    # draw front screen
    pygame.draw.rect(SCREEN, main_color, SM_MENU_AREA_FRONT, 0, ROUND)

    # draw menu title
    draw_text(my_font, CHANGE_COLOR[lang_index], sub_color, (WIDTH / 2, (HEIGHT - (HEIGHT * 0.8)) / 2 + 45))

    # draw done button
    pygame.draw.rect(SCREEN, sub_color2, DONE_AREA, 0, ROUND)
    draw_text(my_font, DONE[lang_index], WHITE, (WIDTH / 2, HEIGHT - 125))

    # draw the color squares
    draw_color_squrs()

    # while on the menu listen for click event on one of the color squares
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(4):
                        for area, color in zip(COLOR_AREAS[i], COLORS[i]):
                            if area.collidepoint(event.pos):
                                value = color
                                draw_color_squrs()
                                pygame.draw.rect(SCREEN, sub_color, area, 3, ROUND)
                    # listen for click on done button - exit menu
                    if DONE_AREA.collidepoint(event.pos) or EXIT_MENU_AREA1.collidepoint(event.pos) or EXIT_MENU_AREA2.collidepoint(event.pos):
                        done = 1
                    if EXIT_MENU_AREA3.collidepoint(event.pos) or EXIT_MENU_AREA4.collidepoint(event.pos):
                        done = 1
                    pygame.display.update()
    return value


# draw the menu where the user can choose which color they want to change - called when user clicks color icon in nav bar
def draw_color_select_menu(main_color, sub_color, sub_color2, correct_color, semi_color, wrong_color, my_font, my_font_med, my_font_sm, lang_index) :
    
    # draw background screen and front ground screen
    pygame.draw.rect(SCREEN, GREY, SM_MENU_AREA_BACK, 0, ROUND)
    pygame.draw.rect(SCREEN, main_color, SM_MENU_AREA_FRONT, 0, ROUND)

    # draw menu title
    draw_text(my_font, SELECT_COLOR[lang_index], sub_color, (WIDTH / 2, (HEIGHT - (HEIGHT * 0.85)) / 2 + 45))
    draw_text(my_font, TO_CHANGE[lang_index], sub_color, (WIDTH / 2, (HEIGHT - (HEIGHT * 0.85)) / 2 + 90))

    # draw correct select button
    pygame.draw.rect(SCREEN, correct_color, PICK_ONE_AREA, 0, ROUND)
    draw_text(my_font_med, CHANGE_CORRECT_COLOR[lang_index], BLACK, (WIDTH / 2, HEIGHT - 510))

    # draw semi correct select button
    pygame.draw.rect(SCREEN, semi_color, PICK_TWO_AREA, 0, ROUND)
    draw_text(my_font_med, CHANGE_SEMI_COLOR[lang_index], BLACK, (WIDTH / 2, HEIGHT - 410))

    # draw wrong select button
    pygame.draw.rect(SCREEN, wrong_color, PICK_THREE_AREA, 0, ROUND)
    draw_text(my_font_med, CHANGE_WRONG_COLOR[lang_index], BLACK, (WIDTH / 2, HEIGHT - 310))

    # draw high contrast button
    pygame.draw.rect(SCREEN, HIGH_CONTRAST_1, PICK_FOUR_AREA, 0, ROUND)
    draw_text(my_font_med, HIGH_CONTRAST[lang_index], BLACK, (WIDTH / 2, HEIGHT - 210))

    # draw cancel button
    pygame.draw.rect(SCREEN, sub_color2, CANCEL_AREA, 0, ROUND)
    draw_text(my_font_sm, CANCEL[lang_index], WHITE, (WIDTH / 2, HEIGHT - 115))


# DRAW KEYBOARD #

# draw the on screen keyboard
def draw_keyboard(main_color, sub_color2, my_font, my_font_med, keys):
    # starting keyboard location
    key_x, key_y = 125, 500

    # draw buttons and letters on top of keyboard buttons
    for i in range(3):
        # make key object and draw key for every letter in the alphabet
        for letter in ALPHABET[i]:
            new_key = KeyButton(key_x, key_y, letter, sub_color2)
            keys.append(new_key)
            new_key.draw(main_color, my_font)
            # shift x position
            key_x += 60
        # shift y position
        key_y += 80
        # depending on keyboard row, shift x position
        if i == 0:
            key_x = 160
        elif i == 1:
            key_x = 210
    # draw enter and delete buttons
    new_key = BigKeyButton(100, 660, "DEL", 102, 70, sub_color2)
    keys.append(new_key)
    new_key.draw(main_color, my_font_med)
    new_key = BigKeyButton(635, 660, "ENTER", 125, 70, sub_color2)
    keys.append(new_key)
    new_key.draw(main_color, my_font_med)