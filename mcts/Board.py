import numpy as np
class Board(object):
    DEFAULT_BOARD_SIZE = 8
    IN_PROGRESS        = -1
    BLACK              = 1
    WHITE              = 2
    EMPTY              = 0
    AVAILABLE_ONE_MOVES    = [[-1,0] , [0,1], [1,0], [0,-1]]
    AVAILABLE_CROSS_MOVES  = [[-2,0] , [0,2], [2,0], [0,-2]]
    AVAILABLE_CHOICES  = {'TP' : [-1,0] , 'RT' : [0,1] , 'DN' : [1,0] , 'LT' : [0,-1] , 'CT' : [-2,0] , 'CR' : [0,2] , 'CD' : [2,0] , 'CL' : [0,-2]}

    def __init__(self,boardValues=[],totalMoves=0):
        # Create the initialized state and initialized board
        # Example
        # boardValues = [[0,1,1,0,0,0,0,0],
        #                [0,1,1,0,0,2,2,2],
        #                [0,1,1,0,0,2,2,2],
        #                [0,1,1,0,0,2,2,2],
        #                [0,1,1,0,0,2,2,2],
        #                [0,1,1,0,0,2,2,2],
        #                [0,1,1,0,0,2,2,2],
        #                [0,1,1,0,0,2,2,2]]

        self.boardValues = boardValues
        self.totalMoves  = totalMoves

    def moveOneStep(self,playerNo,oneMove):
        """
        @param      playerNo : 1 代表黑色 2 代表白色   oneMove: 一個 list 從 a 移動到 b  [a,b]
        @return     如果是一個合法的移動，會移動該步並回傳True，如果是一個不合法的移動，不移動該步並回傳False
        """
        oneMove = oneMove.astype(int)
        opponent = 3 - playerNo
        initialRow = oneMove[0][0]
        initialCol = oneMove[0][1]
        finalRow   = oneMove[1][0]
        finalCol   = oneMove[1][1]

        if self.boardValues[initialRow][initialCol] == playerNo and self.boardValues[finalRow][finalCol] == EMPTY:
            if [initialRow-finalRow, initialCol-finalCol] in AVAILABLE_ONE_MOVES:
                # 上下左右動一步
                self.boardValues[initialRow][initialCol] = EMPTY
                self.boardValues[finalRow][finalRow] = playerNo
                return True
            elif [initialRow-finalRow, initialCol-finalCol] in AVAILABLE_CROSS_MOVES and \
                self.boardValues[initialRow + int((initialRow-finalRow)/2) ][ initialCol + int((initialCol-finalCol)/2)] == opponent:
                # 跨一步吃掉對手
                self.boardValues[initialRow][initialCol] = EMPTY
                self.boardValues[initialRow + int((initialRow-finalRow)/2) ][ initialCol + int((initialCol-finalCol)/2)] = EMPTY
                self.boardValues[finalRow][finalRow] = playerNo
                return True
            elif [initialRow-finalRow, initialCol-finalCol] in AVAILABLE_CROSS_MOVES and \
                self.boardValues[initialRow + int((initialRow-finalRow)/2) ][ initialCol + int((initialCol-finalCol)/2)] == playerNo:
                # 跨一步自己
                self.boardValues[initialRow][initialCol] = EMPTY
                self.boardValues[finalRow][finalRow] = playerNo
                return True
            return False
        
        return False         

    def performMove(self,playerNo, moveList):
        """
        @param    playerNo : 1 代表黑色 2 代表白色 moveList: 從第一個位置移動到最後一個位置的一連串位置
        @return   如果這一連串的移動是合法的話就成功移動並且return True，如果這是一個不合法的移動，就會return False
        """
        # Example 
        # player     : 1 
        # moveList   : [[3,4] , [3,6] , [3,8]]
        tempBoardValues = self.boardValues
        movePosNumpy = np.reshape(moveList, (-1, 2))
        legal = True
        
        for row in movePosNumpy:
            legal = self.moveOneStep(playerNo,row)
            if legal == False:
                break
        
        if legal:
            return True
        else:
            # 還原
            self.boardValues = tempBoardValues
            return False

    def getBoardValues(self):
        return self.boardValues
    
    def setBoardValues(self,boardValues):
        self.boardValues = boardValues
    
    def checkStatus(self):
        #TODO check for now status and return who win or IN_PROGRESS 
        return IN_PROGRESS 
    
    

    