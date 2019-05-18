from Board import Board
class State(object):
    def __init__(self, state=None, board=[], playerNo=0, visitCount=0, winScore=0):
        self.state      = state
        self.board      = board
        self.playerNo   = playerNo
        self.visitCount = visitCount
        self.winScore   = winScore  #github UCT 算法 (nodeWinScore / (double) nodeVisit) + 1.41 * Math.sqrt(Math.log(totalVisit) / (double) nodeVisit)
        
    def getBoard(self):
        return self.board
    
    def setBoard(self,board):
        self.board = board
    
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
    
    def getAllPossibleStates(self):
        """
        要回傳這個node的所有下一個可能的state object，並且用 list 方式 ， 記得那些回傳的 state 要更新 board、playerNo、visitCount、winScore
        """
        #TODO return all the possible state for current state (type: list of State)
    
    def incrementVisit(self):
        self.visitCount += 1
    
    def addScore(self,score):
        self.winScore += score
    
    def randomPlay(self):
        #TODO set the self board for random move
    
    def togglePlayer(self):
        self.playerNo = 3 - self.playerNo

    


        
     