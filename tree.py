import twentyFortyEight
from copy import deepcopy

class Tree(object):
    def __init__(self, state = twentyFortyEight.TwentyFortyEight(), move = 'V'):
        self.children = []
        #NESW or V for void
        self.move = move
        self.state = state
        self.score = self.state.score
        self.bestscore = 0
        self.dead = False

    def makeChildren(self):
        moves = ['W','A','S','D'] 
        for i in range(4):
            newBoard = deepcopy(self.state)
            newBoard.move(moves[i])
            if newBoard.stuck == False:
                self.children.append(Tree(newBoard,moves[i]))

    def makeNDeep(self, N):
        if N == 0:
            return
        #Creates a 1 deep.
        self.makeChildren()
        if len(self.children) == 0: 
            self.dead = True
            self.score = -1
            return
        else:
            map(lambda x: x.makeNDeep(N-1),self.children)

    def make1Deeper(self):
        if len(self.children) == 0 and not self.dead:
            self.makeChildren()
            return
        else:
            map(lambda x: x.make1Deeper(),self.children)

    def setBestScore(self):
        if (len(self.children) == 0):
            self.bestscore = self.score
            return self.score
            
        else:
            bestscore = max(map(lambda x: x.setBestScore(),self.children))
            self.bestscore = bestscore
            return bestscore   
        

def makeChildrenTest():
    a = Tree()
    a.makeChildren()
    assert a.children[0].state.board == [[2,0,0,0],[0,0,0,0],[0,0,0,0],[2,0,0,0]]

def make1DeeperTest():
    root = Tree()
    root.makeNDeep(5)
    root2 = Tree()
    root2.makeNDeep(4)
    root2.make1Deeper()
    root.setBestScore()
    root2.setBestScore()
    assert root2.bestscore == root.bestscore

def test():
    makeChildrenTest()
    make1DeeperTest()
    print "All tests pass!"

def main():
    root = Tree()
    root.makeNDeep(5)
    for i in range(100):
        root.make1Deeper()
        root.setBestScore()
        for i in range(len(root.children)):
            if (root.children[i].bestscore == root.bestscore):
                print "ControlSend, , {}, 2048, , ,".format(root.children[i].move)
                root = root.children[i]
                break
    print root.state
if __name__ == '__main__':
    main()


