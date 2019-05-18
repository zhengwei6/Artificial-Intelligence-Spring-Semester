from Board import Board
from Tree  import Tree
from Node  import Node
import math
import copy

COMPUTATION_BUDGET = 30

def uctValue(totalVisit, nodeWinScore, nodeVisit):
    if nodeVisit == 0:
        return float('inf')
    return (nodeWinScore / float(nodeVisit)) + 1.41 * math.sqrt(math.log(totalVisit) /  float(nodeVisit) )

def findBestNodeWithUCT(node):
    parentVisit = node.getState().getVisitCount()
    valueList   = []
    for childNode in node.getChild():
        value = uctValue(parentVisit, childNode.getState().getWinScore(), childNode.getState().getVisitCount())

def selectPromisingNode(rootNode):
    """
    找到 Expand node
    """
    node = rootNode
    while len(node.getChild()) != 0:
        node = findBestNodeWithUCT(node)
    return node

def backPropogation(nodeToExplore, playerNo):
    """
    從 Simulation node (注意不是 Expand node! ) 開始往上 backPropogation 
    """
    tempNode = nodeToExplore
    while tempNode != None:
        tempNode.getState().incrementVisit()
        if tempNode.getState().getPlayerNo() == playerNo:
            tempNode.getState().addScore(10) #WINSCORE
        tempNode = tempNode.getParent()
    
def simulateRandomPlayout(node,opponent):
    """
    從Simulation node 開始 把遊戲 run 到最後   
    """
    tempNode    = copy.copy(node)
    tempState   = tempNode.getState()
    boardStatus = tempState.getBoard().checkStatus()
    if boardStatus == opponent:
        tempNode.getParent().getState().setWinScore(float('-inf'))
        return boardStatus
    
    while boardStatus == Board.IN_PROGRESS:
        tempState.togglePlayer()
        tempState.randomPlay()
        boardStatus = tempState.getBoard().checkStatus()
    return  boardStatus
    
def expandNode(node):
    """
    把這個node 有可能的 下個 state 都產生出來並且加到 child 中
    """
    possibleStates = node.getState().getAllPossibleStates() 
    for subState in possibleStates:
        newNode = Node(parent=node , state=subState )
        newNode.getState().setPlayerNo(node.getState().getOpponent())
        node.getChild().append(newNode)
    return node

def findNextMove(board, playerNo):
    opponent = 3 - playerNo
    tree = Tree()
    rootNode = tree.getRoot()
    rootNode.getState().setBoard(board)
    rootNode.getState().setPlayerNo(opponent)
    
    # Run as much as possible under the computation budget
    for i in range(COMPUTATION_BUDGET):
        # Phase 1 - Selection
        promisingNode = selectPromisingNode(rootNode)
        
        # Phase 2 - Expansion
        if promisingNode.getState().getBoard().checkStatus() == Board.IN_PROGRESS:
            promisingNode = expandNode(promisingNode)
        
        # Phase 3 - Simulation
        nodeToExplore = promisingNode
        if len(promisingNode.getChild()) > 0:
            nodeToExplore = promisingNode.getRandomChildNode()
        playoutResult = simulateRandomPlayout(nodeToExplore)
        
        #Phase 4 - Update
        backPropogation(nodeToExplore, playoutResult)

    winnerNode = rootNode.getChildWithMaxScore()
    return winnerNode.getState().getBoard()

def main():
    
if __name__ == "__main__":
    main()

