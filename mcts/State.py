from Board import Board
class State(object):
    def __init__(self, state=None, board=[], playerNo=0, visitCount=0, winScore=0):
        self.state      = state
        self.board      = board
        self.playerNo   = playerNo
        self.visitCount = visitCount
        self.winScore   = winScore
    
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
        #TODO return all the possible state for current state (type: list)
    
    def incrementVisit(self):
        self.visitCount += 1
    
    def addScore(self,score):
        self.winScore += score
    
    def randomPlay(self):
        #TODO set the self board for random move
    
    def togglePlayer(self):
        self.playerNo = 3 - self.playerNo

    


        
     