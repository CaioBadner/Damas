'''
This is the main driver file
It will be responsible for handling user input and displaying current GameState through the GUI
'''

import pygame as p
import sys
from Damas import DamasEngine

#these are all the basic constants used by the gui engine
BORDER = 25
HEIGHT = WIDTH = 770
BOARD_HW = HEIGHT - BORDER * 2
OFFSET = HEIGHT // 144
MAX_FPS = 15
AI_MOVE_SPEED = (2000, 1300, 700, 350, 100)
AI_MOVE_TITLES = ('SLOWEST','SLOW','NORMAL','FAST','FASTEST')
IMAGES = {}
DRAGGED_IMAGES = {}
MEASURES = {"dimension" : 0, "sq_size" : 0, "piece_size" : 0, "drag_size" : 0, "diff" : 0}
FONT_BOLD = 'assets/OpenSans-SemiBold.ttf'
FONT_REG = 'assets/OpenSans-Regular.ttf'
FONT_LIGHT = 'assets/OpenSans-Light.ttf'

#all the button information about sizes and placement
BUTTON_WIDTH = WIDTH * 5 // 9
BUTTON_HEIGHT = HEIGHT * 4 // 63
BUTTON_ROUND = BUTTON_HEIGHT * 2 // 3
button_x_start = (WIDTH - BUTTON_WIDTH) // 2 #+ BORDER 
button_layout = [(button_x_start, HEIGHT * 5 // 13 + OFFSET, BUTTON_WIDTH, BUTTON_HEIGHT),
                    (button_x_start, HEIGHT * 6 // 13 + OFFSET, BUTTON_WIDTH, BUTTON_HEIGHT),
                    (button_x_start, HEIGHT * 7 // 13 + OFFSET, BUTTON_WIDTH, BUTTON_HEIGHT),
                    (button_x_start, HEIGHT * 8 // 13 + OFFSET, BUTTON_WIDTH, BUTTON_HEIGHT),
                    (button_x_start, HEIGHT * 9 // 13 + OFFSET, BUTTON_WIDTH, BUTTON_HEIGHT)]
set_layout = [(WIDTH * 5 // 6,  HEIGHT * 3 // 10 - OFFSET * 2, BUTTON_WIDTH // 5, BUTTON_HEIGHT),
              (WIDTH * 5 // 6,  HEIGHT * 4 // 10 - OFFSET * 2, BUTTON_WIDTH // 5, BUTTON_HEIGHT),
              (WIDTH * 5 // 6 - OFFSET * 5,  HEIGHT * 5 // 10 - OFFSET * 2, BUTTON_WIDTH // 4, BUTTON_HEIGHT),
              (WIDTH * 9 // 16 + OFFSET,  HEIGHT * 6 // 10 - OFFSET, BUTTON_WIDTH // 8, BUTTON_HEIGHT),
              (WIDTH * 14 // 16 - OFFSET,  HEIGHT * 6 // 10 - OFFSET, BUTTON_WIDTH // 8, BUTTON_HEIGHT),
              (WIDTH * 11 // 16 - OFFSET * 6,  HEIGHT * 7 // 10 - OFFSET // 2, BUTTON_WIDTH // 8, BUTTON_HEIGHT),
              (WIDTH * 14 // 16,  HEIGHT * 7 // 10 - OFFSET // 2, BUTTON_WIDTH // 8, BUTTON_HEIGHT),
              (button_x_start, HEIGHT * 14 // 16 - OFFSET * 4, BUTTON_WIDTH, BUTTON_HEIGHT)]

#all the colors used by the game
BLUE_HOVER = p.Color(139, 188, 205)
LIGHT_SQ_COLOR = p.Color(225,235,218)
DARK_SQ_COLOR = p.Color(119,168,185)
WHITE = p.Color(255,255,255)
BLACK = p.Color(0,0,0)
DARK_GREEN = p.Color(33, 120, 80)
GREEN = p.Color(53, 140, 100)
DARK_RED = p.Color(150,50,60)
RED = p.Color(170,70,80)
LIGHT_GREEN = p.Color(129,178,125)
BROWN = p.Color(83, 35, 0)

def getMeasures():
    #dimension = sq_size = piece_size = drag_size = diff = 0
    MEASURES["dimension"] = DamasEngine.boardSize
    MEASURES["sq_size"] = BOARD_HW // MEASURES["dimension"]
    MEASURES["piece_size"] = int(MEASURES["sq_size"] * 0.84)
    MEASURES["drag_size"] = int(MEASURES["sq_size"] * 0.88)
    MEASURES["diff"] = int((MEASURES["sq_size"] - MEASURES["piece_size"])/2)
    loadImages()
    
#initializing the global dictionary of images. This will be done only once in the main 
def loadImages():
    piece_size = MEASURES["piece_size"]
    drag_size =  MEASURES["drag_size"]
    
    for piece in range(1,27):
        IMAGES[piece] = p.transform.scale(p.image.load("Assets/Images/" + str(piece) + ".png"), (piece_size, piece_size))
        DRAGGED_IMAGES[piece] = p.transform.scale(p.image.load("Assets/Images/" + str(piece) + ".png"), (drag_size, drag_size))
 
#this controls the button animation        
def button(SCREEN, font, text, x, y, w, h, click, inactive_color=DARK_GREEN, active_color=GREEN, text_color=WHITE):
    mouse = p.mouse.get_pos()
    return_value = False
    if x < mouse[0] < x + w and y < mouse[1] < y + h:  # if mouse is hovering the button
        #p.draw.circle(SCREEN, active_color, (x, y + h/2), h/2)
        #p.draw.circle(SCREEN, active_color, (x + w, y + h/2), h/2)
        p.draw.rect(SCREEN, active_color, (x, y, w, h), 0, BUTTON_ROUND)
        if click and p.time.get_ticks() > 100: return_value = True
    else:
        #p.draw.circle(SCREEN, inactive_color, (x, y + h/2), h/2)
        #p.draw.circle(SCREEN, inactive_color, (x + w, y + h/2), h/2)
        p.draw.rect(SCREEN, inactive_color, (x, y, w, h), 0, BUTTON_ROUND)

    text_surf, text_rect = text_objects(text, font, color=text_color)
    text_rect.center = (int(x + w / 2), int(y + h / 2))
    SCREEN.blit(text_surf, text_rect)
    return return_value

#these are the titles and images for the main menu
def main_menu_setup(SCREEN, FONTS):
    sq_size = MEASURES["sq_size"]
    text_surf, text_rect = text_objects('DAMAS', FONTS[0], BLACK)
    text_rect.center = (int(WIDTH / 2), int(HEIGHT / 6) + OFFSET * 2)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects('1.0', FONTS[3], BLACK)
    text_rect.center = (int(WIDTH * 0.92), int(HEIGHT * 0.92))
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects('Created by Caio Badner', FONTS[3], BLACK)
    text_rect.center = (int(WIDTH / 2), int(HEIGHT * 0.92))
    SCREEN.blit(text_surf, text_rect)
    SCREEN.blit(IMAGES[20], p.Rect(WIDTH * 2 // 16 - OFFSET * 5, HEIGHT * 3 // 4 + OFFSET * 4, sq_size, sq_size))
    SCREEN.blit(DRAGGED_IMAGES[13], p.Rect(WIDTH * 2 // 16 - OFFSET * 2, HEIGHT * 3 // 4 + OFFSET * 7, sq_size, sq_size))
    SCREEN.blit(IMAGES[10], p.Rect(WIDTH * 13 // 16 + OFFSET, HEIGHT * 3 // 4 + OFFSET * 3, sq_size, sq_size))
    SCREEN.blit(DRAGGED_IMAGES[26], p.Rect(WIDTH * 13 // 16 - OFFSET * 2, HEIGHT * 3 // 4 + OFFSET * 6, sq_size, sq_size))
    p.display.update()

#this is what renders the text and gets the rectangle that surrounds the text box
def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

#these are the titles for the end game screen
def end_screen_setup(SCREEN, FONTS, winningSide):
    if len(winningSide) == 5:
        msg = " " + winningSide + " IS THE WINNER! "
    else:
        msg = " IT'S A DRAW "
    text_surf, text_rect = text_objects(msg, FONTS[1], WHITE)
    text_rect.center = (int(WIDTH / 2), int(HEIGHT / 4))
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    p.display.update()

#these are the titles for the paused game screen
def pause_menu_setup(SCREEN, FONTS):
    text_surf, text_rect = text_objects(" GAME PAUSED ", FONTS[1], WHITE)
    text_rect.center = (int(WIDTH / 2), int(HEIGHT / 4))
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    p.display.update()

#this will display everything on the HELP screen
def help_setup(SCREEN, FONTS):
    drawBoard(SCREEN)
    text_surf, text_rect = text_objects(" HELP ", FONTS[1], WHITE)
    text_rect.center = (WIDTH // 2, HEIGHT // 8)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    sq_size = MEASURES["sq_size"]
    text_surf, text_rect = text_objects(" Damas is an ancient game that can be played under many different rules ", FONTS[4], WHITE)
    text_rect.center = (WIDTH // 2, HEIGHT * 7 // 30)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" Pieces move one square towards the enemy and only land in empty squares ", FONTS[4], WHITE)
    text_rect.center = (WIDTH // 2, HEIGHT * 8 // 30)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" If a piece can make another capture in the same turn then it must do it. ", FONTS[4], WHITE)
    text_rect.center = (WIDTH // 2, HEIGHT * 10 // 30)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" Captures are made by leaping over enemy pieces onto an empty square ", FONTS[4], WHITE)
    text_rect.center = (WIDTH // 2, HEIGHT * 9 // 30)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" Pìeces that reach the end of the board are promoted to queens ", FONTS[4], WHITE)
    text_rect.center = (WIDTH // 2, HEIGHT * 11 // 30)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" Queens can move backwards and forwards and many squares at a time ", FONTS[4], WHITE)
    text_rect.center = (WIDTH // 2, HEIGHT * 12 // 30)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" If a player has no more pieces or no legal moves then he lost the game. ", FONTS[4], WHITE)
    text_rect.center = (WIDTH // 2, HEIGHT * 13 // 30)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" A game is declared a draw after 40 turns with no captures. ", FONTS[4], WHITE)
    text_rect.center = (WIDTH // 2, HEIGHT * 14 // 30)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" HOTKEYS ", FONTS[2], WHITE)
    text_rect.center = (WIDTH // 2, HEIGHT * 16 // 30 + OFFSET // 2)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" SPACE ", FONTS[3], WHITE)
    text_rect.center = (WIDTH // 5, HEIGHT * 21 // 34)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" Freeze computer play ", FONTS[3], WHITE)
    text_rect.center = (WIDTH * 2// 3, HEIGHT * 21 // 34)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" Z ", FONTS[3], WHITE)
    text_rect.center = (WIDTH // 5, HEIGHT * 23 // 34)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" Undo last move ", FONTS[3], WHITE)
    text_rect.center = (WIDTH * 2// 3, HEIGHT * 23 // 34)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" X ", FONTS[3], WHITE)
    text_rect.center = (WIDTH // 5, HEIGHT * 25 // 34)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" Call for a computer move ", FONTS[3], WHITE)
    text_rect.center = (WIDTH * 2// 3, HEIGHT * 25 // 34)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" +/- ", FONTS[3], WHITE)
    text_rect.center = (WIDTH // 5, HEIGHT * 27 // 34)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects(" Increase/Decrease speed ", FONTS[3], WHITE)
    text_rect.center = (WIDTH * 2// 3, HEIGHT * 27 // 34)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    SCREEN.blit(IMAGES[15], p.Rect(WIDTH * 2 // 16 - OFFSET * 7, HEIGHT // 16 - OFFSET * 2, sq_size, sq_size))
    SCREEN.blit(IMAGES[8], p.Rect(WIDTH * 2 // 16 - OFFSET * 5, HEIGHT // 16, sq_size, sq_size))
    SCREEN.blit(DRAGGED_IMAGES[26], p.Rect(WIDTH * 2 // 16 - OFFSET * 2, HEIGHT // 16 + OFFSET * 3, sq_size, sq_size))
    SCREEN.blit(IMAGES[17], p.Rect(WIDTH * 13 // 16 , HEIGHT * 13 // 16, sq_size, sq_size))
    SCREEN.blit(DRAGGED_IMAGES[13], p.Rect(WIDTH * 13 // 16 + OFFSET * 2, HEIGHT * 13 // 16 + OFFSET * 3, sq_size, sq_size))
    p.display.update()

#these are the headers for the settings menu
def set_setup(SCREEN, FONTS):
    drawBoard(SCREEN)
    text_surf, text_rect = text_objects(" SETTINGS ", FONTS[1], WHITE)
    text_rect.center = (WIDTH // 2, HEIGHT // 8)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects("  FORCED CAPTURES  ", FONTS[3], WHITE)
    text_rect.x,text_rect.y = (WIDTH // 16, HEIGHT * 3 // 10 - OFFSET)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects("  QUEENS MOVE ONLY ONE SQUARE  ", FONTS[3], WHITE)
    text_rect.x,text_rect.y = (WIDTH // 16, HEIGHT * 4 // 10 - OFFSET)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects("  COMPUTER LEVEL  ", FONTS[3], WHITE)
    text_rect.x,text_rect.y = (WIDTH // 16, HEIGHT * 5 // 10 - OFFSET)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects("  COMPUTER MOVE SPEED  ", FONTS[3], WHITE)
    text_rect.x,text_rect.y = (WIDTH // 16, HEIGHT * 6 // 10 - OFFSET // 2)
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    comp_speed_setup(SCREEN, FONTS)
    text_surf, text_rect = text_objects("  BOARD SIZE  ", FONTS[3], WHITE)
    text_rect.x,text_rect.y = (WIDTH // 16, HEIGHT * 7 // 10 )
    p.draw.rect(SCREEN, DARK_GREEN, text_rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    board_size_setup(SCREEN, FONTS)
    p.display.update()

#this is just controls the game speed label (slowest/slow/normal/fast/fastest)
def comp_speed_setup(SCREEN, FONTS):
    rect = p.Rect(1,1, BUTTON_WIDTH // 3, BUTTON_HEIGHT)
    text_surf, text_rect = text_objects(AI_MOVE_TITLES[DamasEngine.delay_index], FONTS[3], WHITE)
    box_h = text_rect.height
    center = (WIDTH * 12 // 16, HEIGHT * 6 // 10 + box_h // 2)
    rect.center = text_rect.center = center
    p.draw.rect(SCREEN, DARK_GREEN, rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)
    p.display.update()

#and this is the board size label (8/10/12)
def board_size_setup(SCREEN, FONTS):
    strBoardSize = "   " + str(DamasEngine.boardSize) + "   "
    rect = p.Rect(1,1, BUTTON_WIDTH // 5, BUTTON_HEIGHT)
    text_surf, text_rect = text_objects(strBoardSize, FONTS[3], WHITE)
    box_h = text_rect.height
    center = (WIDTH * 13 // 16 - OFFSET * 2 , HEIGHT * 7 // 10 + OFFSET * 2 // 5 + (box_h // 2))
    rect.center = text_rect.center = center
    p.draw.rect(SCREEN, DARK_GREEN, rect, 0, BUTTON_ROUND)
    SCREEN.blit(text_surf, text_rect)

#this is the controller for the main menu, here are all the buttons except the settings screen    
def main_menu(SCREEN, FONTS, settings_menu = False, clock = p.time.Clock()):
    #these are all the menu variables
    SCREEN.fill(BROWN)
    play_menu = False
    help_menu = False
    start_game = False
    whiteIsHuman = False
    blackIsHuman = False
    drawBoard(SCREEN)
    if settings_menu:
        call_settings_menu(SCREEN, FONTS)
    else:
        main_menu_setup(SCREEN, FONTS)
        while True:
            click = False
            for e in p.event.get():
                if e.type == p.MOUSEBUTTONDOWN: click = True
            if button(SCREEN, FONTS[3], 'PLAY DAMAS', *button_layout[0], click):
                play_menu = True
                break
            elif button(SCREEN, FONTS[3], 'SETTINGS', *button_layout[1], click):
                settings_menu = True
                break
            elif button(SCREEN, FONTS[3], 'HELP', *button_layout[2], click):
                help_menu = True
                break
            elif button(SCREEN, FONTS[3], 'QUIT GAME', *button_layout[3], click): 
                break
            p.display.update(button_layout)
            clock.tick(MAX_FPS)
        drawBoard(SCREEN)
        main_menu_setup(SCREEN, FONTS)
        while play_menu:
            click = False
            for e in p.event.get():
                if e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        main_menu(SCREEN, FONTS)
                elif e.type == p.MOUSEBUTTONDOWN: click = True
            if button(SCREEN, FONTS[3], 'PLAY AS WHITE', *button_layout[0], click):
                whiteIsHuman = True
                start_game = True
            elif button(SCREEN, FONTS[3], 'PLAY AS BLACK', *button_layout[1], click):
                blackIsHuman = True
                start_game = True
            elif button(SCREEN, FONTS[3], 'PLAY AGAINST A FRIEND', *button_layout[2], click):
                whiteIsHuman = True
                blackIsHuman = True
                start_game = True
            elif button(SCREEN, FONTS[3], 'WATCH THE COMPUTER PLAY', *button_layout[3], click):
                start_game = True
            elif button(SCREEN, FONTS[3], 'BACK', *button_layout[4], click): 
                main_menu(SCREEN, FONTS)
            if start_game:
                game(SCREEN, FONTS, whiteIsHuman, blackIsHuman)
            p.display.update(button_layout)
            clock.tick(MAX_FPS)
        if settings_menu:
            call_settings_menu(SCREEN, FONTS)
        while help_menu: #TODO
            help_setup(SCREEN, FONTS)
            click = False
            for e in p.event.get():
                if e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        main_menu(SCREEN, FONTS)
                elif e.type == p.MOUSEBUTTONDOWN: click = True
            if button(SCREEN, FONTS[3], 'BACK', *set_layout[-1], click): 
                main_menu(SCREEN, FONTS)
            p.display.update(set_layout)
            clock.tick(MAX_FPS)
    #if nothing was chosen that means that the user clicked on quit
    p.quit()
    sys.exit(0)

#this is all the information needed for the settings menu, it is loaded separately because when we change the board size
#the board reloads and we are sent directly to this page
def call_settings_menu(SCREEN, FONTS, boardSize = DamasEngine.boardSize, clock = p.time.Clock()):
    drawBoard(SCREEN)
    set_setup(SCREEN, FONTS)
    while True:
        click = False
        if DamasEngine.forcedCaptures: forcedText, forcedColor, forcedActive = ' YES ', DARK_GREEN, GREEN
        else: forcedText, forcedColor, forcedActive = ' NO ', DARK_RED, RED
        if DamasEngine.queensOneSquare: oneSquareText, oneSquareColor, oneSquareActive = ' YES ', DARK_GREEN, GREEN
        else: oneSquareText, oneSquareColor, oneSquareActive = ' NO ', DARK_RED, RED
        if DamasEngine.computerLevelHard: levelText, levelColor, levelActive = '  HARD  ', DARK_RED, RED
        else: levelText, levelColor, levelActive = '  EASY  ', DARK_GREEN, GREEN
        if DamasEngine.computerLevelHard: levelText, levelColor, levelActive = '  HARD  ', DARK_RED, RED
        else: levelText, levelColor, levelActive = '  EASY  ', DARK_GREEN, GREEN
        for e in p.event.get():
            if e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        main_menu(SCREEN, FONTS)
            elif e.type == p.MOUSEBUTTONDOWN: click = True
        if button(SCREEN, FONTS[3], forcedText, *set_layout[0], click, forcedColor, forcedActive):
            DamasEngine.forcedCaptures = not DamasEngine.forcedCaptures
        elif button(SCREEN, FONTS[3], oneSquareText, *set_layout[1], click, oneSquareColor, oneSquareActive):
            DamasEngine.queensOneSquare = not DamasEngine.queensOneSquare
        elif button(SCREEN, FONTS[3], levelText, *set_layout[2], click, levelColor, levelActive):
            DamasEngine.computerLevelHard = not DamasEngine.computerLevelHard
        elif button(SCREEN, FONTS[3], '<', *set_layout[3], click):
            if DamasEngine.delay_index > 0: 
                DamasEngine.delay_index -= 1
                comp_speed_setup(SCREEN, FONTS)
        elif button(SCREEN, FONTS[3], '>', *set_layout[4], click):
            if DamasEngine.delay_index < len(AI_MOVE_SPEED)-1: 
                DamasEngine.delay_index += 1
                comp_speed_setup(SCREEN, FONTS)
        elif button(SCREEN, FONTS[3], '<', *set_layout[5], click):
            if DamasEngine.boardSize != 8:
                if DamasEngine.boardSize == 12: 
                    DamasEngine.boardSize = 10
                else: DamasEngine.boardSize = 8
                getMeasures()
                main_menu(SCREEN, FONTS, True)   
        elif button(SCREEN, FONTS[3], '>', *set_layout[6], click):
            if DamasEngine.boardSize != 12:
                if DamasEngine.boardSize == 8: 
                    DamasEngine.boardSize = 10
                else: DamasEngine.boardSize = 12
                getMeasures()
                main_menu(SCREEN, FONTS, True)    
        elif button(SCREEN, FONTS[3], ' BACK ', *set_layout[-1], click):
            main_menu(SCREEN, FONTS)
        clock.tick(90)
        p.display.update(set_layout)

# This is the method that runs the game itself. It inherits the SCREEN and FONTS objects from the main_menu() method
# whiteIsHuman and blackIsHuman will be determined in the main menu and tells the engine who is who
# isPaused is the flag that tells the engine to show the pause_menu and pause the game
# it's pre-defined as an argument because we will reload this class everytime a move is undone in the pause menu 
# and we want the board to be updated in the background, so we will call game() with this flag as True
# gs is the GameState object from the engine class that will store all the information regarding the game itself
# and clock is the clock
def game(SCREEN, FONTS, whiteIsHuman, blackIsHuman, isPaused = False, gs = None, clock = p.time.Clock()):
    delay = AI_MOVE_SPEED[DamasEngine.delay_index]
    if gs == None:
        gs = DamasEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #this is the flag to tell the engine to redo the validMoves list only after a new mode is made
    isDragging = False #this is to keep track of whether there is a piece being dragged right now
    isFrozen = False #this is a flag controlled by the SPACE bar to freeze computer play without calling the pause menu
    draggedPiece = () #this will be a tuple with the piece number, row and col info  (3,1,2) - white piece, row 1, col 2
    mistakes = 0
    #this just makes the game hold for a second if the first play is from the computer
    if not whiteIsHuman and not isPaused:
        drawGameState(SCREEN, gs)
        p.display.flip()
        p.time.delay(delay)
    running = True
    while running:
        if isPaused: 
            #if we are paused then we just re-draw the board and call the pause menu again
            #used only when undoing moves in the pause menu
            drawGameState(SCREEN, gs)
            call_pause_menu(SCREEN, FONTS, gs, whiteIsHuman, blackIsHuman)
        else:
            
            #first we check to see if we need the computer to move
            if (gs.whiteToMove and not whiteIsHuman) or\
                (not gs.whiteToMove and not blackIsHuman):
                if not isFrozen:
                    p.time.delay(delay)
                    gs.makeMove(gs.getComputerMove(validMoves))
                    moveMade = True
            for e in p.event.get():
                #Mouse handling - left clicks control the drag and drop action
                if e.type == p.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        if (gs.whiteToMove and whiteIsHuman) or (not gs.whiteToMove and blackIsHuman) or isPaused:
                            row, col = getMouseRowCol()
                            if row != -1 and col != -1:
                                for move in validMoves:
                                    if move.startRow == row and move.startCol == col:
                                        isDragging = True
                                        draggedPiece = (gs.board[row][col], row, col)
                                        gs.board[row][col] = 0
                                        break
                    elif e.button == 3: #right clicking anywhere will bring up the pause menu
                        call_pause_menu(SCREEN, FONTS, gs, whiteIsHuman, blackIsHuman)
                elif e.type == p.MOUSEBUTTONUP:
                    if e.button == 1: #here we define what happens when the left button is released
                        if isDragging:    
                            isDragging = False
                            row, col = getMouseRowCol()
                            if row != -1 and col != -1:
                                for move in validMoves:
                                    if (move.endRow == row and move.endCol == col) and\
                                       (move.startRow == draggedPiece[1] and move.startCol == draggedPiece[2]):
                                        gs.makeMove(move)  
                                        moveMade = True
                                        break
                                if not moveMade: #this returns the dragged piece to the original location
                                    gs.board[draggedPiece[1]][draggedPiece[2]] = draggedPiece[0]
                            else:
                                gs.board[draggedPiece[1]][draggedPiece[2]] = draggedPiece[0]        
                #Keyboard
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE: #call the in-game pause menu
                        call_pause_menu(SCREEN, FONTS, gs, whiteIsHuman, blackIsHuman)
                    elif e.key == p.K_z: #undo last move when Z is pressed
                        if isFrozen or (whiteIsHuman and blackIsHuman):
                            gs.undoMove()
                            moveMade = True
                    elif e.key == p.K_x: #get a computer move when X is pressed
                        if isFrozen:
                            gs.makeMove(gs.getComputerMove(validMoves))
                            moveMade = True
                    elif e.key == p.K_SPACE: #freezes the computer game without bringing the menu
                        isFrozen = not isFrozen
                    #elif e.key == p.K_a: #prints the computer analysis
                    #    gs.analyzeBoard()
                    elif e.key == p.K_KP_PLUS: #increase speed of computer play
                        if delay > 0:
                            delay -= 50
                        #print("Current delay is " + str(delay))
                    elif e.key == p.K_KP_MINUS: #decrease speed of computer play
                        if delay <= 5000:
                            delay += 50
                        #print("Current delay is " + str(delay))
                    
            if moveMade:
                validMoves = gs.getValidMoves() #only check for valid moves once a move has been made
                if len(validMoves) == 0: #checking for the end of the game
                    if gs.whiteToMove:
                        winningSide = "BLACK"
                    else:
                        winningSide = "WHITE"
                    running = False
                    end_screen_setup(SCREEN, FONTS, winningSide)
                else:
                    moveMade = False
            #here we check to see if the conditions for a draw have been met
            if len(gs.moveLog) - gs.lastCapture == 80:
                    running = False
                    winningSide = "DRAW"
                    end_screen_setup(SCREEN, FONTS, winningSide)

        #and before we start the loop again we update all the drawings on screen
        drawGameState(SCREEN, gs)
        
        if isDragging:
            drawDraggedPiece(SCREEN, draggedPiece[0], p.mouse.get_pos())
        else:
            if (gs.whiteToMove and whiteIsHuman) or (not gs.whiteToMove and blackIsHuman) or isPaused:
                drawCircle(SCREEN, p.mouse.get_pos(), validMoves)
        clock.tick(MAX_FPS)
        p.display.flip()
    
    #this is the end screen after we leave the main game loop
    drawGameState(SCREEN, gs)
    end_screen_setup(SCREEN, FONTS, winningSide)
    hideMenu = False
    while True:
        click = False
        for e in p.event.get():
            if e.type == p.MOUSEBUTTONDOWN: click = True
            elif e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE: #pressing ESC here will hide the end menu and show the full board
                    hideMenu = not hideMenu
                    drawGameState(SCREEN, gs)
                    if not hideMenu:
                        end_screen_setup(SCREEN, FONTS, winningSide)
        if not hideMenu:   
            if button(SCREEN, FONTS[3], 'PLAY AGAIN', *button_layout[2], click):
                game(SCREEN, FONTS, whiteIsHuman, blackIsHuman)
            elif button(SCREEN, FONTS[3], 'MAIN MENU', *button_layout[3], click):
                main_menu(SCREEN, FONTS)
            elif button(SCREEN, FONTS[3], 'QUIT GAME', *button_layout[4], click): break
        p.display.update(button_layout)
        clock.tick(MAX_FPS)
    p.quit()
    sys.exit(0)

#this is the pause menu screen, it will 
def call_pause_menu(SCREEN, FONTS, gs, whiteIsHuman, blackIsHuman, clock = p.time.Clock()):
    pauseMenu = True
    while pauseMenu:
        pause_menu_setup(SCREEN, FONTS)
        click = False
        for e in p.event.get():
            if e.type == p.MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True
            elif e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    game(SCREEN, FONTS, whiteIsHuman, blackIsHuman, False, gs)
        if button(SCREEN, FONTS[3], 'RESUME GAME', *button_layout[1], click):
            game(SCREEN, FONTS, whiteIsHuman, blackIsHuman, False, gs)
        elif button(SCREEN, FONTS[3], 'UNDO LAST MOVE', *button_layout[2], click):
            gs.undoMove()
            game(SCREEN, FONTS, whiteIsHuman, blackIsHuman, True, gs)
        elif button(SCREEN, FONTS[3], 'RESTART GAME', *button_layout[3], click):
            game(SCREEN, FONTS, whiteIsHuman, blackIsHuman, False)
        elif button(SCREEN, FONTS[3], 'MAIN MENU', *button_layout[4], click): 
            main_menu(SCREEN, FONTS)
        p.display.update(button_layout)
        clock.tick(MAX_FPS)

#This method will be responsible for drawing the board and the pieces within a current game state
def drawGameState(SCREEN, gs):
    SCREEN.fill(BROWN)
    lastMove = None
    if len(gs.moveLog) > 0:
        moveLog = gs.moveLog.copy()
        lastMove = moveLog.pop()
    drawBoard(SCREEN, lastMove) #draw squares on the board
    drawPieces(SCREEN, gs.board) #draw pieces on top of the squares
    

#Draw the board squares and if there was a move, paint two squares differently
def drawBoard(SCREEN, lastMove = None):
    colors = [LIGHT_SQ_COLOR, DARK_SQ_COLOR]
    startSq = (-1,-1)
    endSq = (-1,-1)
    sq_size = MEASURES["sq_size"]
    dimension = MEASURES["dimension"]
    if lastMove != None:
        startSq = (lastMove.startRow, lastMove.startCol)
        endSq = (lastMove.endRow, lastMove.endCol)
    for r in range(dimension): #here we check to paint differently the two squares involved in the last move
        for c in range(dimension):
            if (r == startSq[0] and c == startSq[1]) or (r == endSq[0] and c == endSq[1]):
                p.draw.rect(SCREEN, LIGHT_GREEN, p.Rect(c*sq_size + BORDER , r*sq_size + BORDER , sq_size, sq_size))
            else:
                color = colors[((r+c) % 2)] #this will draw a board alternating between two colors
                p.draw.rect(SCREEN, color, p.Rect(c*sq_size + BORDER , r*sq_size + BORDER , sq_size, sq_size))

#Draw the pieces on the squares using the current GameState.board
def drawPieces(SCREEN, board):
    dimension = MEASURES["dimension"]
    sq_size = MEASURES["sq_size"]
    diff = MEASURES["diff"]
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != 0:
                SCREEN.blit(IMAGES[piece], p.Rect(c*sq_size + diff + BORDER , r*sq_size + diff + BORDER , sq_size, sq_size))

#Draw the piece being dragged, using the DRAGGED PIECES dict which have the pieces loaded a bit larger
def drawDraggedPiece(SCREEN, draggedPiece, mouse_pos):
    piece = draggedPiece
    sq_size = MEASURES["sq_size"]
    diff = MEASURES["diff"]
    SCREEN.blit(DRAGGED_IMAGES[piece], p.Rect(mouse_pos[0] - diff * 6, mouse_pos[1] - diff * 6, sq_size, sq_size))

#Draw a circle around a piece once its been clicked only if has valid moves this round
def drawCircle(SCREEN, mouse_pos, validMoves, color = BLUE_HOVER):
    if isMouseInBoard(mouse_pos):
        sq_size = MEASURES["sq_size"]
        col = (mouse_pos[0] - BORDER)//sq_size
        row = (mouse_pos[1] - BORDER)//sq_size
        for move in validMoves:
            if move.startRow == row and move.startCol == col:
                pos = (col * sq_size + (sq_size / 2) + BORDER, row * sq_size + (sq_size / 2) + BORDER)
                p.draw.circle(SCREEN, color, pos, sq_size / 2 - (sq_size // 20), sq_size // 12)

#two simple methods to help the program understand what is going on
def getMouseRowCol():
    sq_size = MEASURES["sq_size"]
    location = p.mouse.get_pos()
    if isMouseInBoard(location):
        col = (location[0] - BORDER)//sq_size
        row = (location[1] - BORDER)//sq_size
        return row, col
    else:
        return -1,-1

def isMouseInBoard(mouse_pos):
    x = mouse_pos[1]
    y = mouse_pos[0]
    if (BORDER < x < BOARD_HW + BORDER) and (BORDER < y < BOARD_HW + BORDER):
            return True

#This is the main driver, it will simply initialize basic controls and call the main menu
def main():
    p.init()
    p.display.set_caption("Damas 1.0")
    SCREEN = p.display.set_mode((HEIGHT,WIDTH))
    #this will calculate all the measures related to the board and also call the loadImages()
    #all information will be stored in the MEASURES dict 
    #and this will be recalled every time board sizes are changed 
    getMeasures()
    #here are the fonts to be used thoughout the game
    # [0] is TITLE, [1] LARGE, [2] MEDIUM, [3] SMALL, [4] TINY
    FONTS = (p.font.Font(FONT_BOLD, int(270 / 1080 * HEIGHT)),
             p.font.Font(FONT_REG, int(95 / 1080 * HEIGHT)),
             p.font.Font(FONT_REG, int(60 / 1080 * HEIGHT)), 
             p.font.Font(FONT_REG, int(40 / 1080 * HEIGHT)), 
             p.font.Font(FONT_BOLD, int(28 / 1080 * HEIGHT)))
    main_menu(SCREEN, FONTS)

if __name__ == "__main__":
    main()
