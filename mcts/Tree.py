from mcts.Node import Node


class Tree(object):
    def __init__(self, root=Node()):
        # Create the initialized state and initialized node
        self.rootNode = root

    def getRoot(self):
        return self.rootNode

    def setRoot(self, node):
        self.rootNode = node

    def addChild(self, parent, child):
        # TODO add child for parent
        pass
