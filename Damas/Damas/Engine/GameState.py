from random import randint
from Damas.Engine.Move import *
from Damas.Draw.Constants import Constants as C

class GameState():
    #these are the game rules that can be altered in the settings menu
    forcedCaptures = False
    queensOneSquare = False
    computerLevelHard = True
    boardSize = 8
    delayIndex = 2
    
    def __init__(self):
        #first off we shuffle the main piece lists to get a unique set of pieces for this game
        whitePieces = self.getUniqueSet(C.WHITE_PIECES, self.boardSize)
        blackPieces = self.getUniqueSet(C.BLACK_PIECES, self.boardSize)
        #this is the main board of the game
        #pieces are numbered from 1-12 if they are white, 13 is a white queen
        #then 14-25 if they are black and 26 is a black queen
        self.board = self.getNewBoard(self.boardSize, whitePieces, blackPieces)
        #this controls whose turn is next
        self.whiteToMove = True
        #this is where the current validMoves list is saved and this gets updated by the updateValidMoves method
        self.validMoves = []
        #and these are two temporary lists to store the moves as the main list is being put together
        self.tempMoves = []
        self.tempCaptures = []
        #here all the past moves of the game will be stored
        self.moveLog = []
        #this will remember when was the last capture made
        self.lastCapture = 0
        #this is the flag to tell the engine to redo the validMoves list only after a new mode is made
        self.moveMade = False 
    

    #this method gets a list, erases the last item, shuffles the rest and returns a new list - giving us a unique set for the new game
    def getUniqueSet(self, pieces, boardSize):
        copiedPieces = pieces.copy()
        copiedPieces.pop() #this removes the queen from the list
        pieceSet = []
        for i in range(C.PIECES_SIZE_RATIO[boardSize]):
            piece = copiedPieces[randint(0, len(copiedPieces)-1)]
            pieceSet.append(piece)
        return pieceSet

    #this is the method that builds the board according to the size chosen, 
    #the default value is 8, but 10 and 12 are also available
    def getNewBoard(self, boardSize, whitePieces, blackPieces):
        board = [[0 for i in range(boardSize)] for j in range(boardSize)]
        midRows = (boardSize // 2 - 1, boardSize // 2) 
        for r in range(boardSize): 
            for c in range(boardSize):
                if (r+c) % 2 != 0:
                    if r in midRows:
                        board[r][c] = 0
                    elif r < midRows[0]:
                        board[r][c] = blackPieces.pop()
                    else:
                        board[r][c] = whitePieces.pop()
        return board

    #two basic methods to help the engine figure out what color is a piece
    def isPieceWhite(self, r, c):
        if self.board[r][c] in C.WHITE_PIECES:
            return True
        return False

    def isPieceBlack(self, r, c):
        if self.board[r][c] in C.BLACK_PIECES:
            return True
        return False

    def getSide(self):
        if self.whiteToMove: 
            return C.WHITE_MOVES, C.WHITE_PIECES, C.WHITE_QUEEN
        return C.BLACK_MOVES, C.BLACK_PIECES, C.BLACK_QUEEN

    def getQueenRange(self):
        if not self.queensOneSquare:
           return self.boardSize
        return 2

    def clearTemp(self):
        self.tempCaptures.clear()
        self.tempMoves.clear()

    #this is to help the engine quickly read the moveLog
    def getLastMove(self):
        if len(self.moveLog) > 0:
            tempMoveLog = self.moveLog.copy()
            return tempMoveLog.pop()

    #this is the method that decides who plays next
    def isWhiteToMove(self):
        if len(self.moveLog) == 0:
            return True
        else:
            lastMove = self.getLastMove()
            if lastMove.whiteMoved:
                if lastMove.isChain: return True
                else: return False
            else:
                if lastMove.isChain: return False
                else: return True

    #this is a basic method to stop our calculations from going out of bounds
    def isMoveInRange(self, r, c):
        if r in range(self.boardSize) and c in range(self.boardSize):
            return True
        else:
            return False

    #this is the method that will make the actual move and handle promotions and chain captures
    def makeMove(self, move):
        #here we make the actual changes to the board
        self.board[move.startRow][move.startCol] = 0
        self.board[move.endRow][move.endCol] = move.pieceMoved
        #and deleted the captured piece if there was one
        if move.pieceCaptured != 0: 
            self.board[move.midRow][move.midCol] = 0
            self.lastCapture = len(self.moveLog)
            #here we see if there are any more captures from this point and
            #if so, we make one last alteration to the Move object
            if len(self.findChainCaptures(move)) > 0:
                move.isChain = True
        #then we can check if the piece should be promoted
        if move.whiteMoved and move.endRow == 0: 
            self.board[move.endRow][move.endCol] = C.WHITE_QUEEN 
        elif not move.whiteMoved and move.endRow == self.boardSize -1:
            self.board[move.endRow][move.endCol] = C.BLACK_QUEEN
        #and finally we can add the move to moveLog
        self.moveMade = True
        self.moveLog.append(move)
        self.whiteToMove = self.isWhiteToMove()
    
    #this method will return the future captures list based on any move given
    def findChainCaptures(self, move):
        captures = []
        for m in C.CAPTURES:
            endRow = move.endRow + m[0]
            endCol = move.endCol + m[1]
            midRow = int((move.endRow + endRow)/2)
            midCol = int((move.endCol + endCol)/2)
            if self.isMoveInRange(endRow, endCol) and self.board[endRow][endCol] == 0:
                if (move.whiteMoved and self.isPieceBlack(midRow,midCol)) or\
                    (not move.whiteMoved and self.isPieceWhite(midRow,midCol)):
                    captures.append(Move((move.endRow, move.endCol), (endRow, endCol), self.board))
        return captures

    #this method undoes all that the makeMove method can do, 
    def undoMove(self):
        if len(self.moveLog) > 0: #make sure it's not the first move
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = 0
            self.board[move.midRow][move.midCol] = move.pieceCaptured
            self.whiteToMove = self.isWhiteToMove()
            self.moveMade = True

    def updateValidMoves(self):
        self.validMoves = self.getValidMoves()

    #this is the method that will return all the valid moves from any given position
    def getValidMoves(self):
        #first we check if we are in a chain and we only need to return the possible captures
        if len(self.moveLog) > 0:
            lastMove = self.getLastMove()
            if lastMove.isChain:
                return self.findChainCaptures(lastMove)
        #if we are not in a chain then do the normal full valid moves calculation
        self.clearTemp()
        myMoves, myPieces, myQueen = self.getSide()
        queenRange = self.getQueenRange()
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]
                if piece in myPieces:
                    if piece == myQueen: self.findMoves(r, c, myPieces, C.QUEEN_MOVES, queenRange)
                    else: self.findMoves(r, c, myPieces, myMoves, 2)
        if self.forcedCaptures and len(self.tempCaptures) > 0:
            return self.tempCaptures.copy()
        return self.tempMoves.copy()

    def findMoves(self, r, c, myPieces, myMoves, queenRange):
        for m in myMoves:
            for i in range(1,queenRange):    
                endRow = r + m[0] * i
                endCol = c + m[1] * i
                if self.isMoveInRange(endRow, endCol):
                    if self.board[endRow][endCol] in myPieces: break #found an ally piece				
                    elif self.board[endRow][endCol] == 0: #normal move
                        self.tempMoves.append(Move((r, c), (endRow, endCol), self.board))
                    elif self.board[endRow][endCol] not in myPieces:#possible capture
                        endRow = endRow + m[0]
                        endCol = endCol + m[1]
                        if self.isMoveInRange(endRow, endCol) and self.board[endRow][endCol] == 0:
                            if self.forcedCaptures: 
                                self.tempCaptures.append(Move((r, c), (endRow, endCol), self.board))
                            else: self.tempMoves.append(Move((r, c), (endRow, endCol), self.board))
                            break #stop searching if found a capture
                        else: break #stop if the square after the enemy piece is not free
                else: break #stop if out of bounds

    #this is the AI part of the game that will look at the valid moves and choose the best one
    def getComputerMove(self):
        myMoves = self.validMoves.copy()
        if not self.computerLevelHard: 
            return myMoves.pop(randint(0,len(myMoves)-1))
        myCaptures = []
        for move in myMoves: #first he makes a list of captures from the validMoves
            if move.pieceCaptured != 0:
                myCaptures.append(move)
        if len(myCaptures) > 0: #then he will choose a random capture
            return myCaptures.pop(randint(0,len(myCaptures)-1))
        return self.getSafeMove(myMoves)
    
    #if there aren't any captures, he will process all the moves, run the validMoves again from the opponent's
    #perspective and try to find one that doesn't lead to a capture the next round
    def getSafeMove(self, myMoves):
        searching = True
        while searching:
            badMove = False
            if len(myMoves) == 1: return myMoves.pop()
            rand = randint(0,len(myMoves)-1)
            move = myMoves.pop(rand)
            self.makeMove(move) #here he actually makes the move on the board
            oppMoves = self.getValidMoves()
            for m in oppMoves: #checks it against all the opponent's moves 
                if m.pieceCaptured != 0: badMove = True
            if not badMove: searching = False
            self.undoMove()  #can't forget to undo the move before returning
        return move

    """
        #TODO - here there is a lot of work to be done to get a proper working AI
        #so far, the 'hard' level only avoids being captured and doesn't miss capturing the opponent
        #without any long term plans

        #this will generate basic information about the current board as a tuple with 6 fields
        #and they will be stored in a list as the analysis deepens
        #[0] - my score, [1] opp score, [2] total my pieces, [3] total opp pieces
        #[4] - total my queens, [5] total opp queens
        #the score is calculated roughly as 1 point per piece, 10 points per queen and 5 per piece 
    
    def analyzeBoard(self):
        myScore = oppScore = myPieces = oppPieces = myQueens = oppQueens = 0
        if self.whiteToMove:
            myQueen, myColor, myPromotion = C.WHITE_QUEEN, C.WHITE_PIECES, 1
            oppQueen, oppColor, oppPromotion = C.BLACK_QUEEN, C.BLACK_PIECES, self.boardSize - 2
        else: 
            myQueen, myColor, myPromotion = C.BLACK_QUEEN, C.BLACK_PIECES, self.boardSize - 2
            oppQueen, oppColor, oppPromotion = C.WHITE_QUEEN, C.WHITE_PIECES, 1
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] in myColor:
                    if self.board[r][c] == myQueen:
                        myScore += 10
                        myQueens += 1
                    else:
                        if r == myPromotion:
                            myScore +=5
                            myPieces += 1
                        else:
                            myScore +=1
                            myPieces += 1
                elif self.board[r][c] in oppColor:
                    if self.board[r][c] == oppQueen:
                        oppScore += 10
                        oppQueens += 1
                    else:
                        if r == oppPromotion:
                            oppScore +=5
                            oppPieces += 1
                        else:
                            oppScore +=1
                            oppPieces += 1
        #print("The current score is: White " + str(whiteScore) + " x " + str(blackScore) + " Black")
        #print("White has " + str(whitePieces) + " pieces and " + str(whiteQueens) + " queens. And Black has " + str(blackPieces) + " pieces and " + str(blackQueens) + " queens.")
        return myScore, oppScore, myPieces, oppPieces, myQueens, oppQueens
    """