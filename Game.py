import pygame as p
from Damas.Engine.GameState import *
from Damas.Draw import *

clock = p.time.Clock()
#this will start a game from scratch and make a new instance of GameState
def start_new_game(humanPlayers):
    gs = GameState()
    Objects.drawGameState(gs)
    #this just makes the game hold for a second if the first play is from the computer
    if not humanPlayers[0]: 
        p.display.flip()
        p.time.delay(1000)
    call_game(humanPlayers, gs)

#we arrive here from the previous method and also from resuming paused games
def call_game(humanPlayers, gs, delay = 0):
    from Damas.Menu import call_pause_menu, call_end_menu
    isFrozen = False #this is controlled by the SPACE bar to freeze computer play without calling the pause menu
    #this will be a list with the piece number, row and col info and a isDragging flag 
    #(3,1,2,1) - white piece, row 1, col 2, isDragging = True
    draggedPiece = [0,0,0,0] 
    if delay == 0: delay = C.AI_MOVE_SPEED[GameState.delayIndex]
    Objects.drawGameState(gs)
    gs.updateValidMoves()
    while True:
        if not isHumanToPlay(gs, humanPlayers) and not isFrozen:
            p.time.delay(delay)
            gs.makeMove(gs.getComputerMove())
        for e in p.event.get():
            #Mouse handling - left clicks initiates the drag and drop action
            if e.type == p.MOUSEBUTTONDOWN: 
                if e.button == 1 and isHumanToPlay(gs, humanPlayers):
                    draggedPiece = getDraggedPiece(gs, p.mouse.get_pos())
                #right clicking anywhere will bring up the pause menu
                elif e.button == 3 and draggedPiece[3] == 0: call_pause_menu(gs, humanPlayers, delay)
            #here we define what happens when the left button is released
            elif e.type == p.MOUSEBUTTONUP and e.button == 1:
                if draggedPiece[3] == 1: #if a piece is being dragged:  
                    draggedPiece = moveDraggedPiece(gs, draggedPiece, p.mouse.get_pos())
            elif e.type == p.KEYDOWN and draggedPiece[3] == 0: #Keyboard
                if e.key == p.K_ESCAPE: call_pause_menu(gs, humanPlayers, delay) 
                elif e.key == p.K_z: #undo last move when Z is pressed
                    if isFrozen or (all(humanPlayers)): gs.undoMove()
                elif e.key == p.K_x: #get a computer move when X is pressed
                    if isFrozen: gs.makeMove(gs.getComputerMove())
                elif e.key == p.K_SPACE:  isFrozen = not isFrozen
                elif e.key == p.K_KP_PLUS: #increase speed of computer play
                    if delay > 0: delay -= 100
                elif e.key == p.K_KP_MINUS: #decrease speed of computer play
                    if delay <= 3000: delay += 100
        #every loop we check if a move was made, then if so, 
        #we update the validMoves and check for the end of the game
        if gs.moveMade: 
            gs.updateValidMoves() #only check for valid moves once a move has been made
            checkForGameOver(gs, len(gs.validMoves), humanPlayers)
        #and before we start the loop again we update all the drawings on screen
        Objects.drawGameState(gs, humanPlayers, draggedPiece, p.mouse.get_pos())
        clock.tick(C.MAX_FPS)
        p.display.flip()
    call_pause_menu(gs, humanPlayers, delay)

def checkForGameOver(gs, lenValidMoves, humanPlayers):
    from Damas.Menu import call_end_menu
    #here we check to see if the conditions for a draw have been met
    if len(gs.moveLog) - gs.lastCapture == 80: call_end_menu(gs, humanPlayers, True)
    if lenValidMoves == 0: 
        call_end_menu(gs, humanPlayers)
    else: gs.moveMade = False

def getDraggedPiece(gs, mousePos):
    row, col = getMouseRowCol(mousePos)
    if row != -1 and col != -1:
        for move in gs.validMoves:
            if move.startRow == row and move.startCol == col:
                draggedPiece = [gs.board[row][col], row, col, 1]
                gs.board[row][col] = 0
                return draggedPiece
    return [0,0,0,0]

def moveDraggedPiece(gs, draggedPiece, mousePos):
    draggedPiece[3] = 0
    row, col = getMouseRowCol(mousePos)
    if row == -1 and col == -1: returnDraggedPiece(gs, draggedPiece)
    else:
        for move in gs.validMoves:
            if (move.endRow == row and move.endCol == col) and\
                (move.startRow == draggedPiece[1] and move.startCol == draggedPiece[2]):
                gs.makeMove(move)  
                break
        if not gs.moveMade: returnDraggedPiece(gs, draggedPiece) 
    return draggedPiece

def returnDraggedPiece(gs, draggedPiece):
    gs.board[draggedPiece[1]][draggedPiece[2]] = draggedPiece[0]

def isHumanToPlay(gs, humanPlayers):
    if (gs.whiteToMove and humanPlayers[0]) or (not gs.whiteToMove and humanPlayers[1]): return True
    return False

def getMouseRowCol(mousePos):
    sq_size = Screen.measures["sq_size"]
    if (C.BORDER < mousePos[1] < C.BOARD_HW + C.BORDER) and (C.BORDER < mousePos[0] < C.BOARD_HW + C.BORDER):
        col = (mousePos[0] - C.BORDER)//sq_size
        row = (mousePos[1] - C.BORDER)//sq_size
        return row, col
    return -1,-1
