from Damas.Draw.Constants import Constants as C

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
        if board[startSq[0]][startSq[1]] in C.WHITE_PIECES:
            self.whiteMoved = True
        self.isChain = False
        #this will determine the mid square for a normal capture
        if (self.pieceMoved != C.WHITE_QUEEN) and (self.pieceMoved != C.BLACK_QUEEN):
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