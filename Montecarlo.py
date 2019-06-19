from Sim2048 import Sim2048
from randommoves import randomMovesStrategy
from math import log
from copy import deepcopy
import random

class MCT():

    def __init__(self,state=None,player=0,move=None):
        if state is None:
            self.state = Sim2048()
        else:
            self.state = state
        self.reward = self.state.score
        self.descendents = 1 
        self.player = player # 1 For actual player, 0 for board
        self.expanded = False
        self.move = move
        self.children = []


    def selection(self):
        if self.expanded == False:
            reward, descendents = self.expansion()
            self.reward += reward
            self.descendents += descendents
            return reward,descendents
        
        elif (self.children == []):
            return 0,0

        else:
            reward, descendents = self.optimalChild().selection()
            self.reward += reward
            self.descendents += descendents
            return reward,descendents

    def expansion(self):
        children = map(lambda x: self.simulation(x),self.getmoves())
        self.children = [child for child in children if child is not None]
        self.expanded = True
        newreward = sum([x.reward for x in self.children])
        self.reward += newreward
        descendents = len(self.children)
        self.descendents += descendents
        return newreward, descendents+1

    #If a move is given then it is a locaftion of a new 2 piece.
    def simulation(self,move):
        simulation = Sim2048(deepcopy(self.state.board),self.state.score)
        if self.player:
            if not simulation.runValidMove(move):
                return None
            child = MCT(simulation,0,move)
            simulation2 = Sim2048(deepcopy(simulation.board),simulation.score)
            simulation2.placeRandom()

        else:
            simulation.board[move[0]][move[1]] = 2
            child = MCT(simulation,1)
            simulation2 = Sim2048(deepcopy(simulation.board),simulation.score)
        score = randomMovesStrategy(simulation2)
        child.score = score
        return child


    def optimalChild(self):
        try:
            ucbs = list(map(lambda x:x.reward/x.descendents + 1.41 * (self.descendents/x.descendents),self.children))
            return self.children[ucbs.index(max(ucbs))]
        except ValueError:
            print(self.children)

    def getmoves(self):
        if self.player:
            return ["u","d","l","r"]
        else:
            return self.state.getEmpty()


            
            


    def backpropogation(self):
        pass

    def search(self,n=10):
        for i in range(n):
            Flag = self.selection()
            if Flag is None:
                return None
        sims = [x.descendents for x in self.children]
        if sims == []:
            return None, None
        index = sims.index(max(sims))
        return self.children[index].move, self.children[index]

    def getCont(self,simulation):
        for child in self.children:
            if child.state.board == simulation.board:
                print ("CONT") 
                return child
        return MCT(simulation,1)


game = Sim2048()
strategy = MCT(game,1)
while True:
    game.placeRandom()
    strategy = strategy.getCont(game)
    print("\n-------------------\n")
    print(game)
    move, child = strategy.search(100)
    if move is None:
        print (game.score)
        break
    game.runValidMove(move)
    strategy = child