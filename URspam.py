from Sim2048 import Sim2048

def urspam():
    a = Sim2048()
    a.placeRandom()
    while True:
        print(a)
        print(a.score)
        move = "u"
        if a.runValidMove(move) == False:
            if a.runValidMove("r") == False:
                if a.runValidMove("d") == False:
                    if a.runValidMove("l") == False:
                        return a.score
            
        a.placeRandom()
        print(a)
        print(a.score)
        move = "r"
        if a.runValidMove(move) == False:
            if a.runValidMove("u") == False:
                if a.runValidMove("d") == False:
                    if a.runValidMove("l") == False:
                        return a.score
        a.placeRandom()
        
print(urspam())
