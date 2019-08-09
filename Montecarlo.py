from Sim2048 import Sim2048
from randommoves import randomMovesStrategy
from math import log
from copy import deepcopy
import time
import random

class MCT():

    def __init__(self,state=None,player=0,move=None):
        if state is None:
            self.state = Sim2048()
        else:
            self.state = state
        self.reward = self.getReward()
        self.descendents = 1 
        self.player = player # 1 For actual player, 0 for board
        self.expanded = False
        self.move = move
        self.children = []

    def getReward(self):
        #We want to focus on monotonicity, smoothness and empty space.
        #Lets try, MON COLS + Smooth cols - empty
        #Let's also change which random placements are considered
        return self.getMon() + self.getSmooth() + 3 * self.getEmpty()

    def getMon(self):
        #Shortened form refers to entire row, long form to individual values
        monU,monD,monL,monR = 0,0,0,0
        for i in range(3):
            monotoneU, monotoneD, monotoneL, monotoneR = 0,0,0,0
            for j in range(3):
                if self.state.board[i][j] <= self.state.board[i][j+1]:
                    monotoneL += 1

                if self.state.board[j][i] <= self.state.board[j+1][i]:
                    monotoneD += 1

                if self.state.board[i][j] >= self.state.board[i][j+1]:
                    monotoneR += 1

                if self.state.board[j][i] >= self.state.board[j+1][i]:
                    monotoneU += 1
            monU, monD, monL, monR = monotoneU//3, monotoneD//3, monotoneL//3, monotoneR//3
            

        return max((monotoneL,monotoneR)) + max((monotoneD,monotoneU))

    def getSmooth(self):
        smoothness = 0
        for i in range(3):
            rowS, colS = 0,0
            for j in range(3):
                if self.state.board[i][j] == self.state.board[i][j+1]:
                    rowS += 1

                if self.state.board[j][i] == self.state.board[j+1][i]:
                    colS += 1
            smoothness += rowS//3 + colS//3

        return smoothness

    def getEmpty(self):
        return len(self.state.getEmpty())


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
            #UCB not good with score function, Lets do 0/1 scaling
            meanreward = [x.reward/x.descendents for x in self.children]
            minx = min(meanreward)
            maxx = max(meanreward) 
            if minx == maxx:
                scaled = meanreward
            else:
                scaled = [(x-minx)/(maxx-minx) for x in meanreward]
            ucbs = [scaled[i] + 1.41 * self.descendents/self.children[i].descendents for i in range(len(self.children)) ]
            #ucbs = list(map(lambda x:x.reward/x.descendents + 1.41 * (self.descendents/x.descendents),self.children))
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

    def search(self,n=10,Endtime=None):
        if Endtime is None:
            for i in range(n):
                Flag = self.selection()
                if Flag is None:
                    return None
        else:
            start = time.time()
            while time.time()-start < Endtime:
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
                return child
        return MCT(simulation,1)


game = Sim2048()
strategy = MCT(game,1)
while True:
    game.placeRandom()
    strategy = strategy.getCont(game)
    print("\n-------------------\n")
    print(game)
    move, child = strategy.search(10,1)
    if move is None:
        print (game.score)
        break
    game.runValidMove(move)
    strategy = child