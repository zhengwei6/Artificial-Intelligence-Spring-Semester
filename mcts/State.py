from Board import Board
import copy
import random

class State(object):
    AVAILABLE_ONE_MOVES    = [[-1,0] , [0,1], [1,0], [0,-1]]
    AVAILABLE_CROSS_MOVES  = [[-2,0] , [0,2], [2,0], [0,-2]]
    AVAILABLE_MOVES        = [[-1,0] , [0,1], [1,0], [0,-1],[-2,0] , [0,2], [2,0], [0,-2]]
    def __init__(self, playerNo=0, visitCount=0, winScore=0):
        self.board      = Board()
        self.playerNo   = playerNo
        self.visitCount = visitCount
        self.winScore   = winScore  #github UCT 算法 (nodeWinScore / (double) nodeVisit) + 1.41 * Math.sqrt(Math.log(totalVisit) / (double) nodeVisit)
        
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
                newStateList.append(newState)

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
                newStateList.append(newState)
        
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
        for index in avaliableChessPos:
            newStateList.extend(self.posPossibleState(index,self.playerNo)) 
        return  newStateList
    
    def incrementVisit(self):
        self.visitCount += 1
    
    def addScore(self,score):
        self.winScore += score
    
    def randomPlay(self):
        """
        目前這個 object 根據 self.playerNo 去隨機玩遊戲
        """
        playerNo    = self.playerNo
        board       = copy.deepcopy(self.board)
        winner      = -1
        # 先選擇一個 playerNo 的棋子
        # 棋子能走的隨機選一個 
        while True:
            winner = board.checkStatus()
            if winner != -1 :
                break
            avaliableChessPos = []
            avaliableMove     = []
            boardValues       = board.boardValues

            for row in range(8):
                for col in range(8):
                    if boardValues[row][col] == playerNo:
                        avaliableChessPos.append([row,col])

            for posElement in avaliableChessPos:
                validMove = []
                for movElement in self.AVAILABLE_ONE_MOVES :
                    row = posElement[0] + movElement[0]
                    col = posElement[1] + movElement[1]
                    if ( row >= 0) and (row < 8) and ( col >= 0) and (col < 8) and (boardValues[row][col] == 0):
                        validMove.append(movElement)
                
                for movElement in self.AVAILABLE_CROSS_MOVES:
                    row = posElement[0] + movElement[0]
                    col = posElement[1] + movElement[1]
                    mir = posElement[0] + int(movElement[0]/2)
                    mic = posElement[1] + int(movElement[1]/2)
                    if ( row >= 0) and (row < 8) and ( col >= 0) and (col < 8)  and (boardValues[row][col] == 0) and (boardValues[mir][mic] != 0):
                        validMove.append(movElement)
                
                if len(validMove) == 0:
                    avaliableChessPos.remove(posElement)
                else:
                    avaliableMove.append(validMove)
                
            if len(avaliableChessPos) == 0:
                playerNo = 3 - playerNo
                continue
            
            round = 0
            while True:
                try:
                    randPos    = random.randint( 0 , len(avaliableChessPos)-1)
                    randMov    = random.randint( 0 , len(avaliableMove[randPos])-1)
                
                    position   = avaliableChessPos[randPos]
                    move       = avaliableMove[randPos][randMov]
                
                    row      = position[0] + move[0]
                    col      = position[1] + move[1]
                    ans      = False
                    if row < 8 and row >= 0 and col < 8 and col >= 0 and board.boardValues[row][col] == 0 :
                        ans  = board.performMove(playerNo,[ [position[0],position[1]] , [row, col ] ])
                    round = round + 1
                    if round > 10:
                        playerNo = 3 - playerNo
                        break
                    if ans == True:
                        playerNo = 3 - playerNo
                        break
                except:
                    continue
            
        return winner
    
    def togglePlayer(self):
        self.playerNo = 3 - self.playerNo

    


        
     