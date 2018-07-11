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
            for i in range(len(self.children)):
                self.children[i].makeChildren()
                if len(self.children[i].children) == 0: 
                    self.children[i].dead = True
                    self.children[i].score = -1
                

    def setBestScore(self):
        if (len(self.children) == 0):
            if self.dead:
                self.bestscore = -1
            else:
                self.bestscore = self.score
            return self.bestscore
            
        else:
            bestscore = max(map(lambda x: x.setBestScore(),self.children))
            self.bestscore = bestscore
            return bestscore   

    def setSurvival(self):
        if (len(self.children) == 0):
            if (self.dead):
                pass
            else:
                self.makeChildren()
                if len(self.children) == 0:
                    self.bestscore = -1
                    self.dead = True
                else:
                    self.bestscore = len(self.children)
            return self.bestscore
        else:
            self.bestscore = max(map(lambda x: x.setSurvival(),self.children ))
            return self.bestscore
        

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
    print "SetTitleMatchMode, 2"
    print "SetKeyDelay, 50"
    print ""
    print ""
    print "<^>!r::reload"
    print ""
    print ""
    print "Numpad8::"
    root = Tree()
    root.makeNDeep(10)
    while True:
        #root.make1Deeper()
        #root.setBestScore()
        root.setSurvival()
        for j in range(len(root.children)):
            if (root.bestscore == -1):
                exit(0)
            if (root.children[j].bestscore == root.bestscore):
                print "    ControlSend, , {}, 2048, , ,".format(root.children[j].move)
                root = root.children[j]
                break
    
if __name__ == '__main__':
    main()


