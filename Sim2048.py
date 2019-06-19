import random
from copy import deepcopy


class Sim2048:

    def __init__(self,board=None,score=0):
        if board == None:
            self.board = [[0]*4,[0]*4,[0]*4,[0]*4]
        else:
            self.board = board
        self.score = score

    def __str__(self):
        return str(self.board[0]) + '\n' \
             + str(self.board[1]) + '\n' \
             + str(self.board[2]) + '\n' \
             + str(self.board[3]) 

    #Tests if a move is valid, IF so, perform it and return true.
    def runValidMove(self,move):
        fundict = {'u':self.u,'d':self.d,'l':self.l,'r':self.r}
        newboard = fundict[move]()
        if self.board != newboard:
            self.board = newboard
            return True
        else:
            return False



    '''
    STRATEGY:
    For each direction, Convert it into combinable elements (i.e, an up move would split it into rows)
    Run crush slide crush
    Convert it back
    Assume that farmost side is furthest end of array
    '''
    def u(self):
        board = deepcopy(self.board)
        line = [[x[0] for x in board[::-1]],[x[1] for x in board[::-1]],[x[2] for x in board[::-1]],[x[3] for x in board[::-1]]]
        line = list(map(lambda x: ([0,0,0,0]+x)[len(x):len(x)+4],self.crush(self.slide(line))))
        #Force evaluation using list method
        list(map(lambda x: x.reverse(),line))
        return [[x[0] for x in line],[x[1] for x in line],[x[2] for x in line],[x[3] for x in line]]


    def d(self):
        board = deepcopy(self.board)
        line = [[x[0] for x in board],[x[1] for x in board],[x[2] for x in board],[x[3] for x in board]]
        line = list(map(lambda x: ([0,0,0,0]+x)[len(x):len(x)+4],self.crush(self.slide(line))))
        return [[x[0] for x in line],[x[1] for x in line],[x[2] for x in line],[x[3] for x in line]]

    def l(self):
        board = deepcopy(self.board)
        line = [board[0][::-1],board[1][::-1],board[2][::-1],board[3][::-1]]
        line = list(map(lambda x: ([0,0,0,0]+x)[len(x):len(x)+4],self.crush(self.slide(line))))
        return [line[0][::-1],line[1][::-1],line[2][::-1],line[3][::-1]]

    def r(self):
        board = deepcopy(self.board)
        line = board
        line = list(map(lambda x: ([0,0,0,0]+x)[len(x):len(x)+4],self.crush(self.slide(line))))
        return line

    #Add together adjacent values that are equal 
    def crush(self, line):
        for i in line:
            for j in range(len(i)-2,-1,-1):
                #if i[j] == i[j+1] and (j+2 > 3 or i[j+2] != 0): CRUSH IF AGAINST WALL
                if i[j] == i[j+1]:
                    i[j], i[j+1] = 0, i[j+1]*2
                    self.score+=i[j+1]
        return self.slide(line)

    def placeRandom(self):
        while True:
            i,j = random.randint(0,3),random.randint(0,3)
            if self.board[i][j] == 0:
                self.board[i][j] = 2
                return

    def getEmpty(self):
        out = []
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    out.append((i,j))
        return out
                    
    #Remove zeros, then zero pad
    def slide(self, line):
        return list(map(lambda x: [i for i in x if  i != 0],line))


if __name__ == "__main__":
    print("Testing...")
    a = Sim2048()
    assert len(a.getEmpty()) == 16
    print("Passed Empty length")
    