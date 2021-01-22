import pygame as p

class Constants:
   
    #these are the basic engine constants 
    WHITE_MOVES = ((-1,-1), (-1,1))
    WHITE_PIECES = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    WHITE_QUEEN = WHITE_PIECES[-1]
    BLACK_MOVES = ((1,-1), (1,1))
    BLACK_PIECES = [14,15,16,17,18,19,20,21,22,23,24,25,26]
    BLACK_QUEEN = BLACK_PIECES[-1]
    QUEEN_MOVES = ((-1,-1), (-1,1), (1,-1), (1,1))
    CAPTURES = ((-2,-2), (-2,2), (2,-2), (2,2))
    PIECES_SIZE_RATIO = {8 : 12, 10 : 20, 12 : 30}

    #these are all the basic constants used by the gui engine
    BORDER = 25
    HEIGHT = WIDTH = 770
    BOARD_HW = HEIGHT - BORDER * 2
    OFFSET = HEIGHT // 144
    MAX_FPS = 15
    AI_MOVE_SPEED = (2000, 1300, 700, 350, 100)
    AI_MOVE_TITLES = ('SLOWEST','SLOW','NORMAL','FAST','FASTEST')
    
    FONT_BOLD = "Damas\\Assets\\OpenSans-SemiBold.ttf"
    FONT_REG = "Damas\\Assets\\OpenSans-Regular.ttf"
    FONT_LIGHT = "Damas\\Assets\\OpenSans-Light.ttf"

    #all the button information about sizes and placement
    BUTTON_WIDTH = WIDTH * 5 // 9
    BUTTON_HEIGHT = HEIGHT * 4 // 63
    BUTTON_ROUND = BUTTON_HEIGHT * 2 // 3
    button_x_start = (WIDTH - BUTTON_WIDTH) // 2 #+ BORDER 
    button_layout = [(button_x_start, HEIGHT * 5 // 13 + OFFSET * 3, BUTTON_WIDTH, BUTTON_HEIGHT),
                        (button_x_start, HEIGHT * 6 // 13 + OFFSET * 3, BUTTON_WIDTH, BUTTON_HEIGHT),
                        (button_x_start, HEIGHT * 7 // 13 + OFFSET * 3, BUTTON_WIDTH, BUTTON_HEIGHT),
                        (button_x_start, HEIGHT * 8 // 13 + OFFSET * 3, BUTTON_WIDTH, BUTTON_HEIGHT),
                        (button_x_start, HEIGHT * 9 // 13 + OFFSET * 3, BUTTON_WIDTH, BUTTON_HEIGHT)]
    set_layout = [(WIDTH * 5 // 6,  HEIGHT * 3 // 10 - OFFSET * 2, BUTTON_WIDTH // 5, BUTTON_HEIGHT),
                  (WIDTH * 5 // 6,  HEIGHT * 4 // 10 - OFFSET * 2, BUTTON_WIDTH // 5, BUTTON_HEIGHT),
                  (WIDTH * 5 // 6 - OFFSET * 5,  HEIGHT * 5 // 10 - OFFSET * 2, BUTTON_WIDTH // 4, BUTTON_HEIGHT),
                  (WIDTH * 9 // 16 + OFFSET,  HEIGHT * 6 // 10 - OFFSET, BUTTON_WIDTH // 8, BUTTON_HEIGHT),
                  (WIDTH * 14 // 16 - OFFSET,  HEIGHT * 6 // 10 - OFFSET, BUTTON_WIDTH // 8, BUTTON_HEIGHT),
                  (WIDTH * 11 // 16 - OFFSET * 6,  HEIGHT * 7 // 10 - OFFSET // 2, BUTTON_WIDTH // 8, BUTTON_HEIGHT),
                  (WIDTH * 14 // 16,  HEIGHT * 7 // 10 - OFFSET // 2, BUTTON_WIDTH // 8, BUTTON_HEIGHT),
                  (button_x_start, HEIGHT * 13 // 16, BUTTON_WIDTH, BUTTON_HEIGHT),
                  (button_x_start, HEIGHT * 7 // 8, BUTTON_WIDTH, BUTTON_HEIGHT)]

    #all the colors used by the game
    BLUE_HOVER = p.Color(139, 188, 205)
    BLACK_HOVER = p.Color(73, 160, 110)
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

    HELP_TEXT = (" Damas is an ancient game that can be played under many different rules ", \
                    " Pieces move one square towards the enemy and only land in empty squares ", \
                    " If a piece can make another capture in the same turn then it must do it. ", \
                    " Captures are made by leaping over enemy pieces onto an empty square ", \
                    " Pìeces that reach the end of the board are promoted to queens ", \
                    " Queens can move backwards and forwards and many squares at a time ", \
                    " If a player has no more pieces or no legal moves then he lost the game. ", \
                    " A game is declared a draw after 40 turns with no captures. ")