from Sim2048 import Sim2048
import random

def randomMovesStrategy(simulation):
    while True:
        moves = ["u","d","l","r"]
        while(not simulation.runValidMove(moves.pop(random.randrange(0,len(moves))))):
            if len(moves) == 0:
                break
        if len(moves) != 0:
            simulation.placeRandom()
        else:
            return simulation.score

if __name__ == "__main__":
    simulation = Sim2048()
    simulation.placeRandom()
    print(randomMovesStrategy(simulation))
    