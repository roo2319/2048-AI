from Sim2048 import Sim2048
from randommoves import randomMovesStrategy
from math import log
from copy import deepcopy
import time
import random

poses = [
    [
        [2**15, 2**14, 2**13, 2**12],
        [2**8 , 2**9 , 2**10, 2**11],
        [2**7 , 2**6 , 2**5 , 2**4 ],
        [2**0 , 2**1 , 2**2 , 2**3 ]
    ],
    [
        [2**0 , 2**1 , 2**2 , 2**3 ],
        [2**7 , 2**6 , 2**5 , 2**4 ],
        [2**8 , 2**9 , 2**10, 2**11],
        [2**15, 2**14, 2**13, 2**12]
    ],
    [
        [2**12, 2**13, 2**14, 2**15],
        [2**11, 2**10, 2**9 , 2**8 ],
        [2**4 , 2**5 , 2**6 , 2**7 ],
        [2**3 , 2**2 , 2**1 , 2**0 ]
    ],
    [
        [2**3 , 2**2 , 2**1 , 2**0 ],
        [2**4 , 2**5 , 2**6 , 2**7 ],
        [2**11, 2**10, 2**9 , 2**8 ],
        [2**12, 2**13, 2**14, 2**15]
    ]
]

class expectimax():

    def __init__(self,state=Sim2048(), nodeType="Player",children=[], move=None):
        self.state = state
        self.nodeType = nodeType
        self.children = children
        #move is u/d/l/r for player and chance for chance 
        self.move = move

    def snake(self):
        score = [0,0,0,0]
        board = self.state.board
        for pose in poses:
            for i in range(4):
                for j in range(4):
                    score[poses.index(pose)] += board[i][j] * pose[i][j]
        return max(score)

    def score(self, depth):
        if len(self.children) == 0 or depth == 0:
            return self.snake()
        
        elif self.nodeType == "Player":
            return max([child.score(depth-1) for child in self.children])
        
        elif self.nodeType == "Chance":
            return sum([(child.move * child.score(depth-1))/len(self.children) for child in self.children])
    
    def expand(self,depth,move=None):
        if depth == 0:
            return

        elif move == None:
            children = map(lambda x: self.expand(depth-1,x),self.getmoves())
            self.children = [child for child in children if child is not None]

        elif len(move) == 1:
            #Player so
            node = expectimax(deepcopy(self.state),nodeType="Chance",move=move)
            if not node.state.runValidMove(move):
                return None
            else:
                node.expand(depth-1)
                return node

        elif len(move) == 2:
            if move[0] == 2:
                chance = 0.9
            else: 
                chance = 0.1
            node = expectimax(deepcopy(self.state),nodeType="Player",move=chance)
            node.state.board[move[1][0]][move[1][1]] = move[0]
            node.expand(depth-1)
            return node


    def getmoves(self):
        if self.nodeType == "Player":
            return ["u","d","l","r"]
        else:
            return [ (value, empty) for empty in self.state.getEmpty() for value in [2,4]]

    def expectimax(self,depth):
        self.expand(depth)
        scoreList = [child.score(depth-1) for child in self.children]
        if len(scoreList) == 0:
            return None
        maxScoreIndex = scoreList.index(max(scoreList))
        return self.children[maxScoreIndex].move
        


game = Sim2048()
while True:
    game.placeRandom()
    strategy = expectimax(game)
    print("\n-------------------\n")
    print(game)
    move = strategy.expectimax(7)
    if move is None:
        print (game.score)
        break
    game.runValidMove(move)

