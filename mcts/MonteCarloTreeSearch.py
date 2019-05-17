from Board import Board
from Tree  import Tree
from Node  import Node
COMPUTATION_BUDGET = 30

def findBestNodeWithUCT(node):
    #TODO return the best node base on UCT

def selectPromisingNode(rootNode):
    """
    找到 Expand node
    """
    node = rootNode
    while (len(node.getChild()) != 0) {
            node = UCT.findBestNodeWithUCT(node);
    }
    return node

def backPropogation(nodeToExplore, playerNo):
    """
    從 Simulation node (注意不是 Expand node! ) 開始往上 backPropogation 
    """
    #TODO backPropogation 

def simulateRandomPlayout(node):
    """
    從Simulation node 開始 把遊戲 run 到最後   
    """
    #TODO simulate to terminal and return win or loss

def expandNode(node):
    """
    把這個node 有可能的 下個 state 都產生出來並且加到 child 中
    """
    possibleStates = node.getState().getAllPossibleStates()
    #TODO Set child Node

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
        expandNode(promisingNode)
        
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

