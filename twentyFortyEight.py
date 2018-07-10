class TwentyFortyEight(object):
    def __init__(self):
        self.board = [[0,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0]] 
        #When two pieces combine then their combined score is added to the score.
        self.score = 0
        self.__addNewPiece()
        self.stuck = False

    #Our movement function is going to consider 2 steps.
    #    1. Move all the pieces in the direction specified, Moving through empty space
    #    2. Combine pieces of equal value in that direction, With the new piece being in
    #    the furthest position.
    #We will also add the new piece deterministically for now.

    def move(self, direction):
        #We will assume that in the case of a NORTH movement that the northmost tiles
        #Combine, In the case of ambiguity in combinations.
        board = map(list,self.board)
        if (direction == 'N'):
            for i in range(len(board)):
                #In line, the earlist element is closest to the side we are pushing it to.
                line = [board[0][i],board[1][i],board[2][i],board[3][i]]
                #Crush, slide, crush.
                line = self.__crush(self.__slide(self.__crush(line)))
                board[0][i],board[1][i],board[2][i],board[3][i] = line[0],line[1],line[2],line[3]
        elif (direction == 'S'):
            for i in range(len(board)):
                line = [board[3][i],board[2][i],board[1][i],board[0][i]]
                line = self.__crush(self.__slide(self.__crush(line)))
                board[3][i],board[2][i],board[1][i],board[0][i] = line[0],line[1],line[2],line[3]
        elif (direction == 'W'):
            for i in range(len(board)):
                line = [board[i][0],board[i][1],board[i][2],board[i][3]]
                line = self.__crush(self.__slide(self.__crush(line)))
                board[i][0],board[i][1],board[i][2],board[i][3] = line[0],line[1],line[2],line[3]
        elif (direction == 'E'):
            for i in range(len(board)):
                line = [board[i][3],board[i][2],board[i][1],board[i][0]]
                line = self.__crush(self.__slide(self.__crush(line)))
                board[i][3],board[i][2],board[i][1],board[i][0] = line[0],line[1],line[2],line[3]

        if (self.board == board):
            self.stuck = True
        else:
            self.board = board
            self.__addNewPiece()

    def __crush(self,line):
        if line[0] == line[1] and line[1] != 0:
            line = [line[0]*2,line[2],line[3],0]
            self.score += line[0]
            line = self.__crush(line)
        elif line[1] == line[2] and line[1] != 0:
            line = [line[0],line[1]*2,line[3],0]
            self.score += line[1]
            line = self.__crush(line)
        elif line[2] == line[3] and line[2] != 0:
            line = [line[0],line[1],line[2]*2,0]
            self.score += line[2]
            line = self.__crush(line)
        return line

    def __slide(self,line):
        line = filter(lambda num: num != 0,line)
        while len(line) != 4:
            line.append(0)
        return line

    def __addNewPiece(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[j][i] == 0:
                    self.board[j][i] = 2
                    return

    def __str__(self):
        string = ""
        for i in range(len(self.board)):
            string += (str(self.board[i]) + "\n")
        return string

def northSouthTest():
    twenty = twentyFortyEight()
    twenty.move('S')
    twenty.move('N')
    assert twenty.score == 4
    assert twenty.board == [[4,0,0,0],[2,0,0,0],[0,0,0,0],[0,0,0,0]]

def eastWestTest():
    twenty = twentyFortyEight()
    twenty.move('E')
    twenty.move('W')
    assert twenty.score == 4
    assert twenty.board == [[4,0,0,0],[2,0,0,0],[0,0,0,0],[0,0,0,0]]    

def longTest():
    twenty = twentyFortyEight()
    twenty.move('E')
    twenty.move('E')
    twenty.move('S')
    twenty.move('S')
    twenty.move('W')
    twenty.move('S')
    twenty.move('S')
    assert twenty.score == 20
    assert twenty.board ==[[2,0,0,0],[2,0,0,0],[4,0,0,0],[8,0,0,0]]

def test():
    # Test NorthSouth movement
    northSouthTest()
    eastWestTest()
    print "All tests passed"
    

def main():
    test()
    

if __name__ == '__main__':
    main()
            
        