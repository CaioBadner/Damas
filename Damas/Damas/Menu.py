import pygame as p
import sys
from Damas.Engine.GameState import GameState as GS
from Damas.Draw import *
from Damas.Draw.Screen import Screen as S
from Damas.Game import *

#Here we have all the logic and button config for all the menus of the game

clock = p.time.Clock()

def call_main_menu():
    Objects.drawBoard()
    S.main_menu_setup()
    while True:
        click = False
        for e in p.event.get():
            if e.type == p.MOUSEBUTTONDOWN: click = True
        if S.button("PLAY DAMAS", *C.button_layout[0], click):
            call_play_menu()
        elif S.button("SETTINGS", *C.button_layout[1], click):
            call_settings_menu()
        elif S.button("HELP", *C.button_layout[2], click):
            call_help_menu()
        elif S.button("QUIT GAME", *C.button_layout[3], click): 
            break
        p.display.update(C.button_layout)
        clock.tick(C.MAX_FPS)
    p.quit()
    sys.exit(0)
        
def call_play_menu():
    humanPlayers = [False, False]
    Objects.drawBoard()
    S.main_menu_setup()
    while True:
        click = False
        for e in p.event.get():
            if e.type == p.KEYDOWN and e.key == p.K_ESCAPE: call_main_menu()
            elif e.type == p.MOUSEBUTTONDOWN: click = True
        if S.button("PLAY AS WHITE", *C.button_layout[0], click):
            humanPlayers[0] = True
            start_new_game(humanPlayers)
        elif S.button("PLAY AS BLACK", *C.button_layout[1], click):
            humanPlayers[1] = True
            start_new_game(humanPlayers)
        elif S.button("PLAY AGAINST A FRIEND", *C.button_layout[2], click):
            humanPlayers[0], humanPlayers[0] = True, True
            start_new_game(humanPlayers)
        elif S.button("WATCH THE COMPUTER PLAY", *C.button_layout[3], click):
            start_new_game(humanPlayers)
        elif S.button("BACK", *C.button_layout[4], click): 
            call_main_menu()
        p.display.update(C.button_layout)
        clock.tick(C.MAX_FPS)

def call_help_menu(): 
    Objects.drawBoard()
    S.help_menu_setup()
    while True: 
        click = False
        for e in p.event.get():
            if e.type == p.KEYDOWN and e.key == p.K_ESCAPE: call_main_menu()
            elif e.type == p.MOUSEBUTTONDOWN: click = True
        if S.button("BACK", *C.set_layout[-1], click): 
            call_main_menu()
        p.display.update(C.set_layout)
        clock.tick(C.MAX_FPS)

def call_settings_menu():
    Objects.drawBoard()
    S.settings_menu_setup(GS.boardSize, GS.delayIndex)
    less, more = "<", ">"
    while True:
        click = False
        forcedText, forcedColor, forcedActive = getForcedCaptures()
        oneSquareText, oneSquareColor, oneSquareActive = getOneSquare()
        levelText, levelColor, levelActive = getCompLevel()
        for e in p.event.get():
            if e.type == p.KEYDOWN and e.key == p.K_ESCAPE: call_settings_menu()
            elif e.type == p.MOUSEBUTTONDOWN: click = True
        if S.button(forcedText, *C.set_layout[0], click, forcedColor, forcedActive):
            GS.forcedCaptures = not GS.forcedCaptures
        elif S.button(oneSquareText, *C.set_layout[1], click, oneSquareColor, oneSquareActive):
            GS.queensOneSquare = not GS.queensOneSquare
        elif S.button(levelText, *C.set_layout[2], click, levelColor, levelActive):
            GS.computerLevelHard = not GS.computerLevelHard
        elif S.button(less, *C.set_layout[3], click):
            setDelay(less)
        elif S.button(more, *C.set_layout[4], click):
            setDelay(more)
        elif S.button(less, *C.set_layout[5], click):
            setBoardSize(less)
        elif S.button(more, *C.set_layout[6], click):
            setBoardSize(more)
        elif S.button(" BACK ", *C.set_layout[-2], click):
            call_main_menu()
        p.display.update(C.set_layout)
        clock.tick(C.MAX_FPS)

def call_pause_menu(gs, humanPlayers, delay):
    while True:
        S.pause_menu_setup()
        click = False
        for e in p.event.get():
            if e.type == p.MOUSEBUTTONDOWN and e.button == 1:
                click = True
            elif e.type == p.KEYDOWN and e.key == p.K_ESCAPE:
                call_game(humanPlayers, gs, delay)
        if S.button("RESUME GAME", *C.button_layout[1], click):
            call_game(humanPlayers, gs, delay)
        elif S.button("UNDO LAST MOVE", *C.button_layout[2], click):
            undoMoveWhilePaused(gs, humanPlayers, delay)
        elif S.button("RESTART GAME", *C.button_layout[3], click):
            start_new_game(humanPlayers)
        elif S.button("MAIN MENU", *C.button_layout[4], click): 
            call_main_menu()
        p.display.update(C.button_layout)
        clock.tick(C.MAX_FPS)

def undoMoveWhilePaused(gs, humanPlayers, delay):
    gs.undoMove()
    Objects.drawGameState(gs)
    call_pause_menu(gs, humanPlayers, delay)

    #this is the end screen after we leave the main game loop
def call_end_menu(gs, humanPlayers, isDraw = False):
    Objects.drawGameState(gs)
    winningSide = findResult(isDraw, gs.whiteToMove)
    p.time.delay(1000)
    S.end_screen_setup(winningSide)
    hideMenu = False
    while True:
        click = False
        for e in p.event.get():
            if e.type == p.MOUSEBUTTONDOWN: click = True
            elif e.type == p.KEYDOWN and e.key == p.K_ESCAPE: 
                hideMenu = not hideMenu
                Objects.drawGameState(gs)
                if not hideMenu: S.end_screen_setup(winningSide)
        if not hideMenu:   
            if S.button("PLAY AGAIN", *C.button_layout[2], click):
                start_new_game(humanPlayers)
            elif S.button("MAIN MENU", *C.button_layout[3], click):
                call_main_menu()
            elif S.button("QUIT GAME", *C.button_layout[4], click): break
        p.display.update(C.button_layout)
        clock.tick(C.MAX_FPS)
    p.quit()
    sys.exit(0)

def getForcedCaptures():
    if GS.forcedCaptures: return " YES ", C.DARK_GREEN, C.GREEN
    return " NO ", C.DARK_RED, C.RED

def getOneSquare():
    if GS.queensOneSquare: return " YES ", C.DARK_GREEN, C.GREEN
    return " NO ", C.DARK_RED, C.RED

def getCompLevel():
    if GS.computerLevelHard: return "  HARD  ", C.DARK_RED, C.RED
    return "  EASY  ", C.DARK_GREEN, C.GREEN

def setDelay(dir):
    if dir == "<" and GS.delayIndex > 0: 
        GS.delayIndex -= 1
        S.comp_speed_setup(GS.delayIndex)
    if dir == ">" and GS.delayIndex < len(C.AI_MOVE_SPEED)-1: 
        GS.delayIndex += 1
        S.comp_speed_setup(GS.delayIndex)

def setBoardSize(dir):
    if dir == "<": 
        if GS.boardSize != 8:
            if GS.boardSize == 12: GS.boardSize = 10
            else: GS.boardSize = 8
    else: 
        if GS.boardSize != 12:
            if GS.boardSize == 8: GS.boardSize = 10
            else: GS.boardSize = 12
    S.loadGraphics(GS.boardSize)
    call_settings_menu()   


def findResult(isDraw, whiteToMove):
    if isDraw: return "DRAW"
    if whiteToMove: return "BLACK"
    return "WHITE"
    