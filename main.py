import math
import copy
import random
import STcpClient
import math
import copy
import random


COMPUTATION_BUDGET = 30

def uctValue(totalVisit, nodeWinScore, nodeVisit):
    if nodeVisit == 0:
        return float('inf')
    if totalVisit == 0:
        return (nodeWinScore / nodeVisit)
    else:
        return (nodeWinScore / nodeVisit) + 1.41 * math.sqrt(math.log(totalVisit) /  nodeVisit )

def findBestNodeWithUCT(node):
    parentVisit = node.state.visitCount
    valueList   = []
    maxValue    = float('-inf')
    returnNode  = None
    for childNode in node.children:
        value = uctValue(parentVisit, childNode.getState().getWinScore(), childNode.getState().getVisitCount())
        if value > maxValue:
            returnNode = childNode
            maxValue = value
    return returnNode
            
    

def selectPromisingNode(rootNode):
    """
    找到 Expand node
    """
    node = rootNode
    while len(node.children) != 0:
        node = findBestNodeWithUCT(node)
    return node

def backPropogation(nodeToExplore,playoutResult ,playerNo):
    """
    從 Simulation node (注意不是 Expand node! ) 開始往上 backPropogation 
    """
    tempNode = nodeToExplore
    while tempNode != None:
        tempNode.getState().incrementVisit()
        if playoutResult == playerNo :
            tempNode.getState().addScore(1) #WINSCORE
        tempNode = tempNode.getParent()

def checkChess(boardValues, playerNo):
    have = 0
    for row in range(8):
        for col in range(8):
            if boardValues[row][col] == playerNo:
                have = 1
            if have == 1:
                break
        if have == 1:
            break
    if have == 1:
        return True
    return False

def findNextMove(boardValues, playerNo,step):
    if not checkChess(boardValues, playerNo):
        return [[0,0],[1,1]]
    
    tree = Tree()
    rootNode = tree.getRoot()
    rootNode.state.board.boardValues = boardValues
    rootNode.getState().setPlayerNo(playerNo)
    if playerNo == 1:
        rootNode.state.board.blackMovesNum = step
        rootNode.state.board.whiteMovesNum = step
    else:
        rootNode.state.board.blackMovesNum = step + 1
        rootNode.state.board.whiteMovesNum = step
    
    for i in range(400):
        # Run as much as possible under the computation budget
        # Phase 1 - Selection
        promisingNode = selectPromisingNode(rootNode)
        #print(promisingNode.state.board.boardValues)
        # Phase 2 - Expansion
        if promisingNode.getState().getBoard().checkStatus(200) == Board.IN_PROGRESS:
            promisingNode.getRandomChildNode()
        # Phase 3 - Simulation
        nodeToExplore = promisingNode
        if len(promisingNode.getChild()) > 0:
            childIndex = random.randint( 0 , len(promisingNode.children)-1)
            nodeToExplore = promisingNode.children[childIndex]
        playoutResult = nodeToExplore.state.randomPlay()
        
        #Phase 4 - Update
        backPropogation(nodeToExplore, playoutResult, playerNo)
        #print(rootNode.state.winScore,rootNode.state.visitCount)
    maxx = -1
    temp = None
    for childNode in rootNode.children:
        if childNode.state.winScore/ childNode.state.visitCount > maxx:
            temp = childNode
            maxx = childNode.state.winScore / childNode.state.visitCount
        #print(childNode.state.playerNo,childNode.state.winScore,childNode.state.visitCount,childNode.state.moveList)
    #print(maxx)
    #print(temp.state.moveList)
    return temp.state.moveList
class Board(object):
    DEFAULT_BOARD_SIZE = 8
    IN_PROGRESS        = -1
    EMPTY              = 0
    DRAW               = 0
    AVAILABLE_ONE_MOVES    = [[-1,0] , [0,1], [1,0], [0,-1]]
    AVAILABLE_CROSS_MOVES  = [[-2,0] , [0,2], [2,0], [0,-2]]

    def __init__(self):
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
        self.boardValues    = []
        self.blackMovesNum  = 0
        self.whiteMovesNum  = 0

    def moveOneStep(self,playerNo,oneMove):
        """
        @param      playerNo : 1 代表黑色 2 代表白色   oneMove: 一個 list 從 a 移動到 b  [a,b]
        @return     如果是一個合法的移動，會移動該步並回傳True，如果是一個不合法的移動，不移動該步並回傳False
        """
        #oneMove = oneMove.astype(int)
        opponent = 3 - playerNo
        initialRow = oneMove[0][0]
        initialCol = oneMove[0][1]
        finalRow   = oneMove[1][0]
        finalCol   = oneMove[1][1]
        if self.boardValues[initialRow][initialCol] == playerNo and self.boardValues[finalRow][finalCol] == self.EMPTY:
            if [initialRow-finalRow, initialCol-finalCol] in self.AVAILABLE_ONE_MOVES:
                # 上下左右動一步
                self.boardValues[initialRow][initialCol] = self.EMPTY
                self.boardValues[finalRow][finalCol] = playerNo
                return True
            elif [initialRow-finalRow, initialCol-finalCol] in self.AVAILABLE_CROSS_MOVES and \
                self.boardValues[initialRow - int((initialRow-finalRow)/2) ][ initialCol - int((initialCol-finalCol)/2)] == opponent:
                # 跨一步吃掉對手
                self.boardValues[initialRow][initialCol] = self.EMPTY
                self.boardValues[initialRow - int((initialRow-finalRow)/2) ][ initialCol - int((initialCol-finalCol)/2)] = self.EMPTY
                self.boardValues[finalRow][finalCol] = playerNo
                return True
            elif [initialRow-finalRow, initialCol-finalCol] in self.AVAILABLE_CROSS_MOVES and \
                self.boardValues[initialRow - int((initialRow-finalRow)/2) ][ initialCol - int((initialCol-finalCol)/2)] == playerNo:
                # 跨一步自己
                self.boardValues[initialRow][initialCol] = self.EMPTY
                self.boardValues[finalRow][finalCol] = playerNo
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
        #print( moveList)
        tempBoardValues = self.boardValues
        legal = True
        for index in range(len(moveList)-1):
            legal = self.moveOneStep(playerNo,[moveList[index],moveList[index+1]])
            if legal == False:
                break
        
        if legal:
            if playerNo == 1:
                self.blackMovesNum += 1
            else:
                self.whiteMovesNum += 1
            return True
        else:
            # 還原
            self.boardValues = tempBoardValues
            return False

    def getBoardValues(self):
        return self.boardValues
    
    def setBoardValues(self,boardValues):
        self.boardValues = boardValues

    def checkInRegion(self):
        """
        @return 
        黑棋全部都在區域內且白棋都被吃光 1 ， 黑棋全部都在區域內且白棋還有  2 ， 白棋都在區域內且黑棋被吃光 3 ，白棋都在區域內且黑棋還有 4 ， 黑或白棋都沒全到區域內 -1 
        如果黑棋全部都被吃掉，白棋會繼續玩到直到全部白子皆到達目標區域or完成200回合才會結束遊戲 (問助教的)
        """
        # check for black
        blackwin = 0
        whitewin = 0
        for i in range(8):
            for j in range(8):
                if self.boardValues[i][j] == 1 and ( j != 6 and j != 7 ):
                    blackwin = -1
                    break
                elif self.boardValues[i][j] == 1 and ( j == 6 or j == 7 ):
                    blackwin = 1
            if blackwin == -1:
                break
        
        for i in range(8):
            for j in range(8):
                if self.boardValues[i][j] == 2 and ( j != 0 and j != 1):
                    whitewin = -1
                    break
                elif self.boardValues[i][j] == 2 and ( j == 0 or j == 1):
                    whitewin = 1
            if whitewin == -1:
                break
        
        if blackwin == 1 and whitewin == 0:    #黑棋全部都在區域內且白棋都被吃光 
            return 1 
        elif blackwin == 1 and whitewin == -1: #黑棋全部都在區域內且白棋還有
            return 2
        elif whitewin == 1 and blackwin == 0:  #白棋都在區域內且黑棋被吃光
            return 3
        elif whitewin == 1 and blackwin == -1: #白棋都在區域內且黑棋還有
            return 4
        elif whitewin == 0 and blackwin == 0:  #白棋全部沒在區域且黑棋也是
            return 5
        return -1
                    
    def checkStatus(self,step):
        """
        @param
        @return  如果是黑子獲勝 回傳 1 如果是白子獲勝 回傳 2 如果還在進行中 回傳 IN_PROGRESS (-1) 平手 DRAW (0)
        """
        allInRegion = self.checkInRegion()

        if (self.whiteMovesNum >= step and self.blackMovesNum >= step) or (allInRegion != -1 and allInRegion != 2 and allInRegion != 4):
            if allInRegion == 5:
                return self.DRAW
            blackNum = 0
            whiteNum = 0
            for i in range(8):
                for j in range(8):
                    if ( j == 6 or j == 7) and self.boardValues[i][j] == 1:
                        blackNum += 1
                    if ( j == 0 or j == 1) and self.boardValues[i][j] == 2:
                        whiteNum += 1
            
            if blackNum > whiteNum:
                return 1
            elif blackNum < whiteNum:
                return 2
            else:
                return self.DRAW
        return -1

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
                if playerNo == 1:
                    if (index[1] != 6 and index[1]!=7) and (col == 6 or col == 7):
                        newState.winScore   += 30
                elif playerNo == 2:
                    if (index[1] != 0 and index[1]!=1) and (col == 0 or col == 1):
                        newState.winScore   += 30
                
                newState.board.performMove(playerNo,[[index[0],index[1]],[row,col]])
                newState.moveList.extend([[index[0],index[1]],[row,col]])
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
                if playerNo == 1:
                    if (index[1] != 6 and index[1]!=7) and (col == 6 or col == 7):
                        newState.winScore   += 30
                elif playerNo == 2:
                    if (index[1] != 0 and index[1]!=1) and (col == 0 or col == 1):
                        newState.winScore   += 30
                
                if self.board.boardValues[imr][imc] == 3 - playerNo:
                    newState.winScore   += 10
                newState.board.performMove(playerNo,[[index[0],index[1]],[row,col]])
                newState.moveList.extend([[index[0],index[1]],[row,col]])
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
        newMove        = []
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
        step        = board.whiteMovesNum
        addstep     = 50
        if step > 150:
            addstep = 200 - step

        winner      = -1
        # 先選擇一個 playerNo 的棋子
        # 棋子能走的隨機選一個 
        while True:
            winner = board.checkStatus(step+50)
            if winner != -1:
                return
            avaliableChessPos = []
            avaliableMove     = []
            avaliableProp     = []
            boardValues       = board.boardValues
            
            for row in range(8):
                for col in range(8):
                    if boardValues[row][col] == playerNo:
                        if ( col - 2 >= 0 )   and ( boardValues[row][col-1] == 3 - playerNo ) and (boardValues[row][col-2] == 0):
                            return playerNo
                        elif ( col + 2 < 8 )  and ( boardValues[row][col+1] == 3 - playerNo ) and (boardValues[row][col+2] == 0):
                            return playerNo
                        elif ( row - 2 >= 0 ) and ( boardValues[row-1][col] == 3 - playerNo ) and (boardValues[row-2][col] == 0):
                            return playerNo
                        elif ( row + 2 < 8 )  and ( boardValues[row+1][col] == 3 - playerNo ) and (boardValues[row+2][col] == 0):
                            return playerNo
                        avaliableChessPos.append([row,col])

            if len(avaliableChessPos) == 0:
                opponent = 3 - playerNo
                for row in range(8):
                    if opponent == 1:
                        for col in range(6,8):
                            if boardValues[row][col] == opponent:
                                return opponent
                    if opponent == 2:
                        for col in range(0,2):
                            if boardValues[row][col] == opponent:
                                return opponent
            
            delList = []
            for posElement in avaliableChessPos:
                validMove = []
                validProp = []
                for movElement in self.AVAILABLE_ONE_MOVES :
                    row = posElement[0] + movElement[0]
                    col = posElement[1] + movElement[1]
                    if ( row >= 0) and (row < 8) and ( col >= 0) and (col < 8) and (boardValues[row][col] == 0):
                        if movElement[1] > 0 and playerNo == 1:
                            validProp.append(50)
                        elif movElement[1] < 0 and playerNo == 2:
                            validProp.append(50)
                        else:
                            validProp.append(10)
                        validMove.append(movElement)
                
                for movElement in self.AVAILABLE_CROSS_MOVES:
                    row = posElement[0] + movElement[0]
                    col = posElement[1] + movElement[1]
                    mir = posElement[0] + int(movElement[0]/2)
                    mic = posElement[1] + int(movElement[1]/2)
                    if ( row >= 0) and (row < 8) and ( col >= 0) and (col < 8)  and (boardValues[row][col] == 0) and (boardValues[mir][mic] != 0):
                        if movElement[1] > 0 and playerNo == 1:
                            validProp.append(50)
                        elif movElement[1] < 0 and playerNo == 2:
                            validProp.append(50)
                        else:
                            validProp.append(10)
                        validMove.append(movElement)
                
                if len(validMove) == 0:
                    delList.append(avaliableChessPos.index(posElement))
                else:
                    avaliableProp.append(validProp)
                    avaliableMove.append(validMove)


            for i in delList:
                del avaliableChessPos[i]
            
            if len(avaliableChessPos) == 0:
                if playerNo == 1:
                    board.blackMovesNum += 1
                else:
                    board.whiteMovesNum += 1
                playerNo = 3 - playerNo
                continue
            
            round = 0
            while True:
                try:
                    randPos    = random.randint( 0 , len(avaliableChessPos)-1)
                    randMov    = random.choices(list(range(len(avaliableMove[randPos])) ) ,avaliableProp[randPos])
                    position   = avaliableChessPos[randPos]
                    move       = avaliableMove[randPos][randMov[0]]
                    
                    row      = position[0] + move[0]
                    col      = position[1] + move[1]
                    ans      = False
                    if row < 8 and row >= 0 and col < 8 and col >= 0 and board.boardValues[row][col] == 0 :
                        ans  = board.performMove(playerNo,[ [position[0],position[1]] , [row, col] ])
                    round = round + 1
                    if round > 10:
                        playerNo = 3 - playerNo
                        break
                    if ans == True:
                        playerNo = 3 - playerNo
                        break
                except Exception as e:
                    print(e)
                    exit(1)
                    continue
            
        return winner
    
    def togglePlayer(self):
        self.playerNo = 3 - self.playerNo
class Node():
    def __init__(self):
        # Create the initialized state and initialized node
        self.parent   = None
        self.children = []
        self.state    = State()
    def getState(self):
        return self.state
    
    def setState(self,state):
        self.state = state

    def getChild(self):
        return self.children
    
    def setChild(self,children):
        self.children = children
    
    def getParent(self):
        return self.parent

    def setParent(self,parent):
        self.parent = parent
   
    def getRandomChildNode(self):
        """
        @param
        @return return a random child Node
        """ 
        newNodeList = []
        newStateList = self.state.getAllPossibleStates()
        for newState in newStateList:
            newNode = Node()
            newNode.parent = self
            newNode.children = []
            newNode.state = newState
            self.children.append(newNode)
        
    def getChildWithMaxScore():
        #TODO return the child having ???
        pass
class Tree(object):
    def __init__(self):
        # Create the initialized state and initialized node
        self.rootNode = Node()

    def getRoot(self):
        return self.rootNode
    def setRoot(node):
        self.rootNode = node
    def addChild(parent, child):
        #TODO add child for parent
        pass

'''
    輪到此程式移動棋子
    board : 棋盤狀態(list of list), board[i][j] = i row, j column 棋盤狀態(i, j 從 0 開始)
            0 = 空、1 = 黑、2 = 白
    is_black : True 表示本程式是黑子、False 表示為白子

    return step
    step : list of list, step = [(r1, c1), (r2, c2) ...]
            r1, c1 表示要移動的棋子座標 (row, column) (zero-base)
            ri, ci (i>1) 表示該棋子移動路徑
'''
def GetStep(boardValues, is_black, step):
    # fill your program here
    #print(boardValues)
    #print(is_black)
    if is_black == True:
        listStep = findNextMove(boardValues, 1, step)
    else:
        listStep = findNextMove(boardValues, 2, step)
    return listStep

def main():
    # TODO: get state and return actions
    i = 0
    while(True):
        if i == 200:
            i = 0
        
        (stop_program, id_package, board, is_black) = STcpClient.GetBoard()
        if(stop_program):
            break
        listStep = GetStep(board, is_black , i)
        STcpClient.SendStep(id_package, listStep)
        i = i + 1
if __name__ == '__main__':
    main()
