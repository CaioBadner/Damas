import pygame as p
import pygame.gfxdraw
from Damas.Draw.Constants import Constants as C

#This is the class that controlls most of the User Interface, has the methods that display all the text and
#buttons, keeps the dictionary of images/dragged images. 
#This class stores the measures to be used every time the board size is changed 
#And all the setups for all the screens are also stored here
class Screen():

    display = None
    FONTS = ()
    #this is the dict that stores all the relative sizes according to the 3 different board sizes
    measures = {"dimension" : 0, "sq_size" : 0, "piece_size" : 0, "drag_size" : 0, "diff" : 0}
    #here all the images for the pieces will be loaded and stored for future reference
    images = {}
    dragged_images = {}
    
    def initializeDisplay():
        Screen.display = p.display.set_mode((C.HEIGHT,C.WIDTH))

    def renderFonts():
        #here are the fonts to be used thoughout the game
        #[0] is TITLE, [1] LARGE, [2] MEDIUM, [3] SMALL, [4] TINY
        Screen.FONTS = (p.font.Font(C.FONT_BOLD, int(270 / 1080 * C.HEIGHT)),
                 p.font.Font(C.FONT_REG, int(95 / 1080 * C.HEIGHT)),
                 p.font.Font(C.FONT_REG, int(60 / 1080 * C.HEIGHT)), 
                 p.font.Font(C.FONT_REG, int(40 / 1080 * C.HEIGHT)), 
                 p.font.Font(C.FONT_BOLD, int(28 / 1080 * C.HEIGHT)))

    def getFont(fontPos):
        return Screen.FONTS[fontPos]

    #this method gets called once from main() and then again every time the board size is changed
    def loadGraphics(boardSize):
        #first all the measures all calculated according to the board size
        Screen.measures["dimension"] = boardSize
        Screen.measures["sq_size"] = C.BOARD_HW // Screen.measures["dimension"]
        Screen.measures["piece_size"] = int(Screen.measures["sq_size"] * 0.84)
        Screen.measures["drag_size"] = int(Screen.measures["sq_size"] * 0.88)
        Screen.measures["diff"] = int((Screen.measures["sq_size"] - Screen.measures["piece_size"])/2)
        #then we fill up the global dictionary of images.
        piece_size = Screen.measures["piece_size"]
        drag_size =  Screen.measures["drag_size"]
        for piece in range(1,27):
            Screen.images[piece] = p.transform.scale(p.image.load("Damas\\Assets\\Images\\" + str(piece) + ".png"), (piece_size, piece_size))
            Screen.dragged_images[piece] = p.transform.scale(p.image.load("Damas\\Assets\\Images\\" + str(piece) + ".png"), (drag_size, drag_size))

    #these are the titles and images for the main menu
    def main_menu_setup():
        Screen.writeTextBox("DAMAS", Screen.getFont(0), C.WIDTH // 2, C.HEIGHT // 6 + C.OFFSET * 2, True, 0, C.BLACK)
        Screen.writeTextBox("1.1", Screen.getFont(4), int(C.WIDTH * 0.92), int(C.HEIGHT * 0.92), True, 0, C.BLACK)
        Screen.writeTextBox("Created by Caio Badner", Screen.getFont(3), C.WIDTH // 2, int(C.HEIGHT * 0.92), True, 0, C.BLACK)
        sq_size = Screen.measures["sq_size"]
        Screen.display.blit(Screen.images[20], p.Rect(C.WIDTH * 2 // 16 - C.OFFSET * 5, C.HEIGHT * 3 // 4 + C.OFFSET * 4, sq_size, sq_size))
        Screen.display.blit(Screen.dragged_images[13], p.Rect(C.WIDTH * 2 // 16 - C.OFFSET * 2, C.HEIGHT * 3 // 4 + C.OFFSET * 7, sq_size, sq_size))
        Screen.display.blit(Screen.images[10], p.Rect(C.WIDTH * 13 // 16 + C.OFFSET, C.HEIGHT * 3 // 4 + C.OFFSET * 3, sq_size, sq_size))
        Screen.display.blit(Screen.dragged_images[26], p.Rect(C.WIDTH * 13 // 16 - C.OFFSET * 2, C.HEIGHT * 3 // 4 + C.OFFSET * 6, sq_size, sq_size))
        p.display.update()

    #these are the headers for the settings menu
    def settings_menu_setup(boardSize, delayIndex):
        Screen.writeTextBox(" SETTINGS ", Screen.getFont(1), C.WIDTH // 2, C.HEIGHT // 8)
        Screen.writeTextBox("  FORCED CAPTURES  ", Screen.getFont(3), C.WIDTH // 16, C.HEIGHT * 3 // 10 - C.OFFSET, False)
        Screen.writeTextBox("  QUEENS MOVE ONLY ONE SQUARE  ", Screen.getFont(3), C.WIDTH // 16, C.HEIGHT * 4 // 10 - C.OFFSET, False)
        Screen.writeTextBox("  COMPUTER LEVEL  ", Screen.getFont(3), C.WIDTH // 16, C.HEIGHT * 5 // 10 - C.OFFSET, False)
        Screen.writeTextBox("  COMPUTER MOVE SPEED  ", Screen.getFont(3), C.WIDTH // 16, C.HEIGHT * 6 // 10 - C.OFFSET // 2, False)
        Screen.writeTextBox("  BOARD SIZE  ", Screen.getFont(3), C.WIDTH // 16, C.HEIGHT * 7 // 10, False)
        Screen.board_size_setup(boardSize)
        Screen.comp_speed_setup(delayIndex)
        p.display.update()

    #this method only sets up the computer speed number without reloading the entire page
    def comp_speed_setup(delayIndex):
        x, y = C.WIDTH * 12 // 16, C.HEIGHT * 6 // 10 
        Screen.writeTextBox(C.AI_MOVE_TITLES[delayIndex], Screen.getFont(3), x, y, True, C.BUTTON_WIDTH // 3)

    #this method sets up only the board size number without reloading the entire page
    def board_size_setup(boardSize):
        strBoardSize = "   " + str(boardSize) + "   "
        x, y = C.WIDTH * 13 // 16 - C.OFFSET * 2 , C.HEIGHT * 7 // 10 + C.OFFSET * 2 // 5
        Screen.writeTextBox(strBoardSize, Screen.getFont(3), x, y, True, C.BUTTON_WIDTH // 5)

    #all the text for the help menu      
    def help_menu_setup():
        Screen.writeTextBox(" HELP ", Screen.getFont(1), C.WIDTH // 2, C.HEIGHT // 8 - C.OFFSET * 2)
        Screen.writeHelpText()
        Screen.writeTextBox(" HOTKEYS ", Screen.getFont(2), C.WIDTH // 2, C.HEIGHT * 16 // 30 - C.OFFSET * 4)
        Screen.writeTextBox(" SPACE ", Screen.getFont(3), C.WIDTH // 4, C.HEIGHT * 10 // 17 - C.OFFSET * 2)
        Screen.writeTextBox(" Freeze computer play ", Screen.getFont(3), C.WIDTH * 2// 3, C.HEIGHT * 10 // 17 - C.OFFSET * 2)
        Screen.writeTextBox("  Z  ", Screen.getFont(3), C.WIDTH // 4, C.HEIGHT * 11 // 17 - C.OFFSET * 2)
        Screen.writeTextBox(" Undo last move ", Screen.getFont(3), C.WIDTH * 2// 3, C.HEIGHT * 11 // 17 - C.OFFSET * 2)
        Screen.writeTextBox("  X  ", Screen.getFont(3), C.WIDTH // 4, C.HEIGHT * 12 // 17 - C.OFFSET * 2)
        Screen.writeTextBox(" Call for a computer move ", Screen.getFont(3), C.WIDTH * 2// 3, C.HEIGHT * 12 // 17 - C.OFFSET * 2)
        Screen.writeTextBox(" +/- ", Screen.getFont(3), C.WIDTH // 4, C.HEIGHT * 13 // 17 - C.OFFSET * 2)
        Screen.writeTextBox(" Increase/Decrease speed ", Screen.getFont(3), C.WIDTH * 2// 3, C.HEIGHT * 13 // 17 - C.OFFSET * 2)
        Screen.writeTextBox(" ESC ", Screen.getFont(3), C.WIDTH // 4, C.HEIGHT * 14 // 17 - C.OFFSET * 2)
        Screen.writeTextBox(" Pause Game ", Screen.getFont(3), C.WIDTH * 2// 3, C.HEIGHT * 14 // 17 - C.OFFSET * 2)
        sq_size = Screen.measures["sq_size"]
        Screen.display.blit(Screen.images[15], p.Rect(C.WIDTH * 2 // 16 - C.OFFSET * 7, C.HEIGHT // 16 - C.OFFSET * 2, sq_size, sq_size))
        Screen.display.blit(Screen.images[8], p.Rect(C.WIDTH * 2 // 16 - C.OFFSET * 5, C.HEIGHT // 16, sq_size, sq_size))
        Screen.display.blit(Screen.dragged_images[26], p.Rect(C.WIDTH * 2 // 16 - C.OFFSET * 2, C.HEIGHT // 16 + C.OFFSET * 3, sq_size, sq_size))
        Screen.display.blit(Screen.images[17], p.Rect(C.WIDTH * 13 // 16 , C.HEIGHT * 13 // 16, sq_size, sq_size))
        Screen.display.blit(Screen.dragged_images[13], p.Rect(C.WIDTH * 13 // 16 + C.OFFSET * 2, C.HEIGHT * 13 // 16 + C.OFFSET * 3, sq_size, sq_size))
        p.display.update()

    #the help text gets its own method
    def writeHelpText():
        rect = (C.BORDER + C.OFFSET, C.BORDER * 7 - C.OFFSET * 6, C.WIDTH - C.OFFSET * 12, C.HEIGHT * 3 / 10 - C.BORDER)
        p.draw.rect(Screen.display, C.DARK_GREEN, rect, 0, C.BUTTON_ROUND)
        helpTextY = C.HEIGHT // 30 
        for i in range(8):
            Screen.writeTextBox(C.HELP_TEXT[i], Screen.getFont(4), C.WIDTH // 2,  C.HEIGHT * 7 // 30 - C.OFFSET * 4 + helpTextY * i)
  
    #these are the titles for the end game screen
    def end_screen_setup(winningSide):
        if len(winningSide) == 5: msg = " " + winningSide + " IS THE WINNER! "
        else: msg = " IT'S A DRAW "
        Screen.writeTextBox(msg, Screen.getFont(1), C.WIDTH // 2, C.HEIGHT // 4)
        p.display.update()

    #these are the titles for the paused game screen
    def pause_menu_setup():
        Screen.writeTextBox(" GAME PAUSED ", Screen.getFont(1), C.WIDTH // 2, C.HEIGHT // 4)
        p.display.update()

     #this is what renders the text and gets the rectangle that surrounds the text box
    def text_objects(text, font, color):
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    #this controls the button animation and text       
    def button(text, x, y, w, h, click, inactive_color=C.DARK_GREEN, active_color=C.GREEN, text_color=C.WHITE):
        mouse = p.mouse.get_pos()
        return_value = False
        if x < mouse[0] < x + w and y < mouse[1] < y + h:  # if mouse is hovering the button
            p.draw.rect(Screen.display, active_color, (x, y, w, h), 0, C.BUTTON_ROUND)
            if click and p.time.get_ticks() > 100: return_value = True
        else: p.draw.rect(Screen.display, inactive_color, (x, y, w, h), 0, C.BUTTON_ROUND)
        text_surf, text_rect = Screen.text_objects(text, Screen.getFont(3), color=text_color)
        text_rect.center = (int(x + w / 2), int(y + h / 2))
        Screen.display.blit(text_surf, text_rect)
        return return_value 

    #this is the method that writes all the text in the game
    def writeTextBox(text, font, x, y, isCentered = True, rectWidth = 0, color = C.WHITE):
        text_surf, text_rect = Screen.text_objects(text, font, color)
        if isCentered: text_rect.center = (x,y)
        else: text_rect.x,text_rect.y = (x,y)
        if rectWidth > 0: 
            rect = p.Rect(1,1, rectWidth, C.BUTTON_HEIGHT)
            rect.center = text_rect.center = (x,y + text_rect.height // 2)
            p.draw.rect(Screen.display, C.DARK_GREEN, rect, 0, C.BUTTON_ROUND)
        else:
            if color == C.WHITE: p.draw.rect(Screen.display, C.DARK_GREEN, text_rect, 0, C.BUTTON_ROUND)
        Screen.display.blit(text_surf, text_rect)
