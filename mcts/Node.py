from State import State
class Node(object):
    def __init__(self, parent=None, children=[]):
        # Create the initialized state and initialized node
        self.parent = parent
        self.children = children
        self.state = State()
    
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