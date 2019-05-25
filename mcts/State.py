from Board import Board
import copy
import random

class State(object):
    AVAILABLE_ONE_MOVES    = [[-1,0] , [0,1], [1,0], [0,-1]]
    AVAILABLE_CROSS_MOVES  = [[-2,0] , [0,2], [2,0], [0,-2]]
    AVAILABLE_MOVES        = [[-1,0] , [0,1], [1,0], [0,-1],[-2,0] , [0,2], [2,0], [0,-2]]
    def __init__(self):
        self.board      = Board()
        self.playerNo   = 0
        self.visitCount = 0
        self.winScore   = 0   #github UCT 算法 (nodeWinScore / (double) nodeVisit) + 1.41 * Math.sqrt(Math.log(totalVisit) / (double) nodeVisit)
        self.moveList   = []
    def getBoard(self):
        return self.board
    
    def getPlayerNo(self):
        return self.playerNo
    
    def setPlayerNo(self,playerNo):
        self.playerNo = playerNo
    
    def getOpponent(self):
        return 3 - self.playerNo

    def getVisitCount(self):
        return self.visitCount

    def setVisitCount(self,visitCount):
        self.visitCount = visitCount

    def getWinScore(self):
        return  self.winScore
    
    def setWinScore(self,winScore):
        self.winScore = winScore
    
    def posPossibleState(self,index,playerNo):
        newStateList    = []
        for oneMove in self.AVAILABLE_ONE_MOVES:
            row = (index[0] + oneMove[0])
            col = (index[1] + oneMove[1])
            if row < 8 and row >= 0 and col < 8 and col >= 0 and self.board.boardValues[row][col] == 0 :
                newState            = State()
                newState.board      = copy.deepcopy(self.board)
                newState.playerNo   = 3 - playerNo
                newState.visitCount = 0
                newState.winScore   = 0
                newState.board.performMove(playerNo,[[index[0],index[1]],[row,col]])
                newState.moveList.extend([[index[0],index[1]],[row,col]])
                newStateList.append(newState)
        crossQueue = []

        for crsMove in self.AVAILABLE_CROSS_MOVES:
            row = (index[0] + crsMove[0])
            col = (index[1] + crsMove[1])
            imr = (index[0] + int(crsMove[0]/2))
            imc = (index[1] + int(crsMove[1]/2))
            if row < 8 and row >= 0 and col < 8 and col >= 0 and self.board.boardValues[row][col] == 0 and self.board.boardValues[imr][imc] != 0:
                newState            = State()
                newState.board      = copy.deepcopy(self.board)
                newState.playerNo   = 3 - playerNo
                newState.visitCount = 0
                newState.winScore   = 0
                newState.board.performMove(playerNo,[[index[0],index[1]],[row,col]])
                newState.moveList.extend([[index[0],index[1]],[row,col]])
                newStateList.append(newState)
                crossQueue.append(newState)
        
        roun = 0
        while len(crossQueue) != 0:
            roun = roun + 1
            if roun > 10:
                break
            tempState = crossQueue.pop()
            for crsMove in self.AVAILABLE_CROSS_MOVES:
                row = tempState.moveList[-1][0] + crsMove[0]
                col = tempState.moveList[-1][1] + crsMove[1]
                imr = tempState.moveList[-1][0] + int(crsMove[0]/2)
                imc = tempState.moveList[-1][1] + int(crsMove[1]/2)                
                if row < 8 and row >= 0 and col < 8 and col >= 0 and tempState.board.boardValues[row][col] == 0 and tempState.board.boardValues[imr][imc] != 0:
                    newState       =  copy.deepcopy(tempState)
                    newState.board.performMove(playerNo,[[tempState.moveList[-1][0],tempState.moveList[-1][1]],[row,col]])
                    newState.moveList.append([row,col])
                    newStateList.append(newState)
                    crossQueue.append(newState)
        
        random.shuffle(newStateList)
        return newStateList

    def getAllPossibleStates(self):
        """
        要回傳這個node的所有下一個可能的state object，並且用 list 方式 ， 記得那些回傳的 state 要更新 board、playerNo、visitCount、winScore
        """
        avaliableChessPos = []
        tempBoard         = self.board.boardValues
        for row in range(8):
            for col in range(8):
                if tempBoard[row][col] == self.playerNo:
                    avaliableChessPos.append([row,col])
        
        newStateList   = []
        newMove        = []
        for index in avaliableChessPos:
            newStateList.extend(self.posPossibleState(index,self.playerNo)) 
        return  newStateList
    
    def incrementVisit(self):
        self.visitCount += 1
    
    def addScore(self,score):
        self.winScore += score
    
    def evaluatePlay(self):
        """
        evaluate 這個 state
        黑的專門 +
        白的專門 -
        """
        playerscore   = 0
        playerChessNum   = 0
        opponentChessNum = 0
        playerNo    = self.playerNo
        boardValues = self.board.boardValues
        for row in range(8):
            for col in range(8):
                if boardValues[row][col] == 1:
                    playerscore += 10
                if  boardValues[row][col] == 2:
                    playerscore -= 10
                if ( col == 6 or col == 7 ) and boardValues[row][col] == 1:
                    playerscore += 5
                if ( col == 0 or col == 1 ) and boardValues[row][col] == 2:
                    playerscore -= 5
        return  playerscore
    
    def togglePlayer(self):
        self.playerNo = 3 - self.playerNo

    


        
     