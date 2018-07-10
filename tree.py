import twentyFortyEight
from copy import deepcopy

class Tree(object):
    def __init__(self, state = twentyFortyEight.TwentyFortyEight()):
        self.children = []
        self.move = 
        self.state = state
        self.dead = False

    def makeChildren(self):
        moves = ['N','E','S','W'] 
        for i in range(4):
            newBoard = deepcopy(self.state)
            newBoard.move(moves[i])
            if newBoard.stuck == False:
                self.children.append(Tree(newBoard))
            
        


def test():
    pass

def main():
    a = Tree()
    a.makeChildren()
    print "test"

if __name__ == '__main__':
    main()


