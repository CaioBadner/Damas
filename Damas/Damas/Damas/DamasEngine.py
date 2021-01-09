from random import randint

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


#these are the game rules that can be altered in the settings menu
forcedCaptures = False
queensOneSquare = False
computerLevelHard = True
boardSize = 8
delay_index = 2

class GameState():
    def __init__(self):
        #first off we shuffle the main piece lists to get a unique set of pieces for this game
        whitePieces = self.getUniqueSet(WHITE_PIECES, boardSize)
        blackPieces = self.getUniqueSet(BLACK_PIECES, boardSize)
        #this is the main board of the game
        #pieces are numbered from 1-12 if they are white, 13 is a white queen
        #then 14-25 if they are black and 26 is a black queen
        self.board = self.getNewBoard(boardSize, whitePieces, blackPieces)
        #this controls whose turn is next
        self.whiteToMove = True
        #here all the moves of the game will be stored
        self.moveLog = []
        #this will remember when was the last capture made
        self.lastCapture = 0

    #this method gets a list, erases the last item, shuffles the rest and returns a new list - giving us a unique set for the new game
    def getUniqueSet(self, pieces, boardSize):
        copiedPieces = pieces.copy()
        copiedPieces.pop() #this removes the queen from the list
        pieceSet = []
        for i in range(PIECES_SIZE_RATIO[boardSize]):
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
        if self.board[r][c] in WHITE_PIECES:
            return True
        return False

    def isPieceBlack(self, r, c):
        if self.board[r][c] in BLACK_PIECES:
            return True
        return False

    #this is to help the engine quickly read the moveLog
    def getLastMove(self):
        if len(self.moveLog) > 0:
            lastMove = self.moveLog[-1]
            return lastMove

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
        if r in range(boardSize) and c in range(boardSize):
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
            self.board[move.endRow][move.endCol] = WHITE_QUEEN 
        elif not move.whiteMoved and move.endRow == boardSize -1:
            self.board[move.endRow][move.endCol] = BLACK_QUEEN
        #and finally we can add the move to moveLog
        self.moveLog.append(move)
        self.whiteToMove = self.isWhiteToMove()
    
    #this method will return the future captures list based on any move given
    def findChainCaptures(self, move):
        captures = []
        for m in CAPTURES:
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

    #this is the method that will return all the valid moves from any given position
    def getValidMoves(self):
        #first we check if we are in a chain and we only need to return the possible captures
        if len(self.moveLog) > 0:
            lastMove = self.getLastMove()
            if lastMove.isChain:
                return self.findChainCaptures(lastMove)
        #if we are not then do the normal full valid moves calculation
        moves = []
        captures = []
        #we first determine which side we are on
        if self.whiteToMove: myMoves, myPieces, myQueen = WHITE_MOVES, WHITE_PIECES, WHITE_QUEEN
        else: myMoves, myPieces, myQueen = BLACK_MOVES, BLACK_PIECES, BLACK_QUEEN
        #and we ajust the queen moves according to the rule chosen at the start
        queen_range = 2
        if not queensOneSquare:
            queen_range = boardSize -1
        #then go over the entire board looking for our pieces
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]
                if piece in myPieces:
                    #first we calculate possible queen moves to avoid repetition                    
                    if piece == myQueen:
                        for m in QUEEN_MOVES:
                            for i in range(1,queen_range):    
                                endRow = r + m[0] * i
                                endCol = c + m[1] * i
                                if self.isMoveInRange(endRow, endCol):
                                    if self.board[endRow][endCol] in myPieces:#found an ally piece				
                                        break
                                    elif self.board[endRow][endCol] == 0:#normal move
                                        moves.append(Move((r, c), (endRow, endCol), self.board))
                                    elif self.board[endRow][endCol] not in myPieces:#possible capture
                                        endRow = endRow + m[0]
                                        endCol = endCol + m[1]
                                        if self.isMoveInRange(endRow, endCol) and self.board[endRow][endCol] == 0:
                                            if forcedCaptures: 
                                                captures.append(Move((r, c), (endRow, endCol), self.board))
                                            else: 
                                                moves.append(Move((r, c), (endRow, endCol), self.board))
                                            break #stop searching if found a capture
                                        else:
                                            break #stop if the square after the enemy piece is not free
                                else:
                                    break #stop if out of bounds
                    #now we calculate moves for all the other pieces
                    for m in myMoves: 
                        endRow = r + m[0]
                        endCol = c + m[1]
                        if self.isMoveInRange(endRow, endCol):
                            if self.board[endRow][endCol] == 0: #if the square is empty then it's a valid move
                                moves.append(Move((r, c), (endRow, endCol), self.board))
                            elif self.board[endRow][endCol] not in myPieces: #found an enemy piece
                                endRow = endRow + m[0]
                                endCol = endCol + m[1]
                                #and if the next square is free then its a capture
                                if self.isMoveInRange(endRow, endCol) and self.board[endRow][endCol] == 0:
                                    if forcedCaptures: 
                                        captures.append(Move((r, c), (endRow, endCol), self.board))
                                    else: 
                                        moves.append(Move((r, c), (endRow, endCol), self.board))
        if forcedCaptures and len(captures) > 0:
            return captures
        return moves
    
    #this is the AI part of the game that will look at the valid moves and choose the best one
    def getComputerMove(self, moves):
        
        if not computerLevelHard: 
            return moves.pop(randint(0,len(moves)-1))
        else:
            #this will generate basic information about the current board as a tuple with 6 fields
            #and they will be stored in this list as the analysis deepens
            #[0] - my score, [1] opp score, [2] total my pieces, [3] total opp pieces
            #[4] - total my queens, [5] total opp queens
            #the score is calculated roughly as 1 point per piece, 10 points per queen and 5 per piece 
            #about to promote
            #boardAnalysis = self.analyzeBoard()
            myCaptures = []
            for move in moves: #first we simulate each move available
                if move.pieceCaptured != 0:
                    myCaptures.append(move)
            if len(myCaptures) > 0:
                return myCaptures.pop(randint(0,len(myCaptures)-1))
            else:
                searching = True
                while searching:
                    badMove = False
                    if len(moves) == 1: #when there is only one move left then it stops the search
                        return moves.pop()
                    else:
                        rand = randint(0,len(moves)-1)
                        myMove = moves.pop(rand)
                    self.makeMove(myMove)
                    oppMoves = self.getValidMoves()
                    for move in oppMoves:
                        if move.pieceCaptured != 0:
                            badMove = True
                    if not badMove:
                        searching = False
                    self.undoMove()   
        return myMove

    #TODO this method analyzes the board and help the computer decide what to play
    def analyzeBoard(self):
        myScore = oppScore = myPieces = oppPieces = myQueens = oppQueens = 0
        myQueen = WHITE_QUEEN
        myColor = WHITE_PIECES
        myPromotion = 1
        oppQueen = BLACK_QUEEN
        oppColor = BLACK_PIECES
        oppPromotion = boardSize - 2
        if not self.whiteToMove:
            myQueen = BLACK_QUEEN
            myColor = BLACK_PIECES
            myPromotion = boardSize - 2
            oppQueen = WHITE_QUEEN
            oppColor = WHITE_PIECES
            oppPromotion = 1
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

#This is the class that will generate Move objects, with all the information regarding the move
#These objects will later be stored in the moveLog[] and will be referenced by many different methods in the game
class Move():

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.midRow = -1
        self.midCol = -1
        self.pieceCaptured = 0
        self.pieceMoved = board[self.startRow][self.startCol]
        self.whiteMoved = False
        if board[startSq[0]][startSq[1]] in WHITE_PIECES:
            self.whiteMoved = True
        self.isChain = False
        #this will determine the mid square for a normal capture
        if (self.pieceMoved != WHITE_QUEEN) and (self.pieceMoved != BLACK_QUEEN):
            if ((startSq[0] - endSq[0] == 2) or (startSq[0] - endSq[0] == -2)):
                self.midRow = int((self.startRow + self.endRow)/2)
                self.midCol = int((self.startCol + self.endCol)/2)
        else: #and this will find the capture square for a queen capture
            if (startSq[0] - endSq[0] > 1):
                self.midRow = endSq[0] + 1
            if (startSq[0] - endSq[0] < -1):
                self.midRow = endSq[0] - 1
            if (startSq[1] - endSq[1] > 1):
                self.midCol = endSq[1] + 1
            if (startSq[1] - endSq[1] < -1):
                self.midCol = endSq[1] - 1
        #then if we changed the midSquare we get a value for the piece Captured
        if (self.midRow != -1):    
            self.pieceCaptured = board[self.midRow][self.midCol]
        #here we generate an unique moveID to be compared by the main method
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    #Override the equals method
    def __eq__ (self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False