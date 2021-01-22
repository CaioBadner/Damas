import pygame as p
from Damas.Draw import *
from Damas.Engine.GameState import *


#This is the main driver, it will simply initialize basic controls and call the main menu
def main():
    from Damas.Menu import call_main_menu
    p.init()
    p.display.set_caption("Damas 1.0")
    icon = p.image.load("Damas\\damas_icon.bmp")
    p.display.set_icon(icon)
    Screen.initializeDisplay()
    Screen.renderFonts()
    Screen.loadGraphics(GameState.boardSize)
    call_main_menu()

if __name__ == "__main__":
    main()