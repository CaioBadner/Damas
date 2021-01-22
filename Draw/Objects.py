import pygame as p
from Damas.Draw.Constants import Constants as C
from Damas.Draw.Screen import *
from random import randint

#This module stores all the methods that draw the objects that appear on screen during the game

#this is the main method that gets called every time the game board needs to be updated midgame
#it first paints the border, then collects the last move, calls the drawBoard and then the drawPieces
def drawGameState(gs, humanPlayers = [False,False], draggedPiece = [0,0,0,0], mousePos = (0,0)):
    #from Damas.Draw.Screen import display
    lastMove = None
    if len(gs.moveLog) > 0:
        moveLogCopy = gs.moveLog.copy()
        lastMove = moveLogCopy.pop()
    drawBoard(lastMove) #draw squares on the board
    drawPieces(gs.board) #draw pieces on top of the squares
    if (gs.whiteToMove and humanPlayers[0]) or (not gs.whiteToMove and humanPlayers[1]):
        drawHumanActions(gs, draggedPiece, mousePos)
    p.display.flip()

#Draw the board squares and if there was a move, paint two squares differently
def drawBoard(lastMove = None):
    #from Damas.Draw.Screen import display
    Screen.display.fill(C.BROWN)
    colors = [C.LIGHT_SQ_COLOR, C.DARK_SQ_COLOR]
    startSq = endSq = midSq = (-1,-1)
    sq_size = Screen.measures["sq_size"]
    dimension = Screen.measures["dimension"]
    if lastMove != None:
        startSq = (lastMove.startRow, lastMove.startCol)
        endSq = (lastMove.endRow, lastMove.endCol)
    for r in range(dimension): #here we check to paint differently the two squares involved in the last move
        for c in range(dimension):
            if (r == startSq[0] and c == startSq[1]) or (r == endSq[0] and c == endSq[1]):
                p.draw.rect(Screen.display, C.LIGHT_GREEN, p.Rect(c*sq_size + C.BORDER , r*sq_size + C.BORDER , sq_size, sq_size))
            else:
                color = colors[((r+c) % 2)] #this will draw a board alternating between two colors
                p.draw.rect(Screen.display, color, p.Rect(c*sq_size + C.BORDER , r*sq_size + C.BORDER , sq_size, sq_size))

#Draw the pieces on the squares using the current GameState.board
def drawPieces(board):
    dimension = Screen.measures["dimension"]
    sq_size = Screen.measures["sq_size"]
    diff = Screen.measures["diff"]
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != 0:
                pieceRect = (c*sq_size + diff + C.BORDER , r*sq_size + diff + C.BORDER , sq_size, sq_size)
                Screen.display.blit(Screen.images[piece], p.Rect(pieceRect))

#this gets called every game loop, after the gameState, to draw dragged pieces or circles around available pieces
def drawHumanActions(gs, draggedPiece, mousePos):
    if draggedPiece[3] == 1:
        drawDraggedPiece(draggedPiece[0], mousePos)
    else:
        if (C.BORDER < mousePos[1] < C.BOARD_HW + C.BORDER) and \
            (C.BORDER < mousePos[0] < C.BOARD_HW + C.BORDER):
            drawCircle(gs, mousePos)  

#this is the method to draw the floating piece as it is being dragged by the mouse
def drawDraggedPiece(draggedPiece, mousePos):
    piece = draggedPiece
    sq_size = Screen.measures["sq_size"]
    diff = Screen.measures["diff"]
    Screen.display.blit(Screen.dragged_images[piece], p.Rect(mousePos[0] - diff * 6, mousePos[1] - diff * 6, sq_size, sq_size))
    

#Draw a circle around a piece once its been clicked only if has valid moves this round
def drawCircle(gs, mousePos, color = C.BLUE_HOVER):
    sq_size = Screen.measures["sq_size"]
    col = (mousePos[0] - C.BORDER)//sq_size
    row = (mousePos[1] - C.BORDER)//sq_size
    for move in gs.validMoves:
        if move.startRow == row and move.startCol == col:
            pos = (col * sq_size + (sq_size / 2) + C.BORDER, row * sq_size + (sq_size / 2) + C.BORDER)
            p.draw.circle(Screen.display, color, pos, sq_size / 2 - (sq_size // 20), sq_size // 12)
            

 

