from mcts.State import State


class Node(object):
    def __init__(self, parent=None, state=None, childs=None):
        # Create the initialized state and initialized node
        self.parent = parent
        self.childs = childs
        self.state = state

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getChild(self):
        return self.childs

    def setChild(self, children):
        self.childs = children

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def getRandomChildNode(self):
        """
        @param
        @return return a random child Node
        """
        # TODO
        pass

    def getChildWithMaxScore(self):
        # TODO return the child having ???
        pass
