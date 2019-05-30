from Board import Board
from Tree import Tree
from Node import Node
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
        if playerNo == 1:
            tempNode.state.winScore += playoutResult
        else:
            tempNode.state.winScore -= playoutResult
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

def displayChildInfo(rootNode):
    for child in rootNode.children:
        print("playerNo",child.state.playerNo,"winscore",child.state.winScore)
        print(child.state.moveList)
    print("----------------------------")

def findNextMove(boardValues, playerNo,tree,step):
    if not checkChess(boardValues, playerNo):
        return [[0,0],[1,1]]

    rootNode = tree.rootNode
    rootNode.state.board.boardValues = boardValues
    rootNode.getState().setPlayerNo(playerNo)
    

    if playerNo == 1:
        rootNode.state.board.blackMovesNum = step
        rootNode.state.board.whiteMovesNum = step
    else:
        rootNode.state.board.blackMovesNum = step + 1
        rootNode.state.board.whiteMovesNum = step
    
    for i in range(1000):
        # Run as much as possible under the computation budget
        # Phase 1 - Selection
        promisingNode = selectPromisingNode(rootNode)
        # Phase 2 - Expansion
        if promisingNode.getState().getBoard().checkStatus(200) == Board.IN_PROGRESS:
            promisingNode.getRandomChildNode()
        # Phase 3 - Simulation
        nodeToExplore = promisingNode
        if len(promisingNode.getChild()) > 0:
            childIndex = random.randint( 0 , len(promisingNode.children)-1)
            nodeToExplore = promisingNode.children[childIndex]
        playoutResult = nodeToExplore.state.evaluatePlay()
        
        #Phase 4 - Update
        backPropogation(nodeToExplore, playoutResult, playerNo)
    
    maxx   = float('-inf')
    temp   = None
    displayChildInfo(rootNode)
    for childNode in rootNode.children:
        if childNode.state.winScore/ childNode.state.visitCount > maxx:
            temp   = childNode
            maxx   = childNode.state.winScore / childNode.state.visitCount

    tree.rootNode = temp
    tree.rootNode.parent = None
    return temp.state.moveList,tree

def oppoentMove(boardValues,tree):
    find = 0
    for childNode in tree.rootNode.children:
        if boardValues == childNode.state.board.boardValues :
            tree.rootNode = childNode
            find          = 1
            return tree
    if find == 0:  
        return None
    
def main():
    tree        = Tree()
    playerNo    = 1
    step        = 180
    boardValues = [ [1,0,0,0,0,0,2,0],
                    [0,0,0,0,0,0,2,0],
                    [0,0,0,0,0,0,2,0],
                    [0,0,0,1,2,0,0,0],
                    [0,0,0,0,0,2,0,0],
                    [0,0,0,0,0,0,2,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]]

    moveList,tree = findNextMove(boardValues,playerNo,tree,step)
    print(moveList)
    playerNo    = 1
    step        = 181
    boardValues = [ [1,0,0,0,0,0,2,0],
                    [0,0,0,0,0,0,2,0],
                    [0,0,0,0,0,2,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,1],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]]
    tree = oppoentMove(boardValues,tree)
    moveList,tree = findNextMove(boardValues,playerNo,tree,step)
    
if __name__ == "__main__":
    main()
