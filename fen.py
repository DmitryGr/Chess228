from constants import *

def fen_format(string):
    colour = BLACK
    data = [[], [], [], [], [], [], [], []]
    counter = 0
    line_figures = ["P", "N", "B", "R", "Q", "K", "p", "n", "b", "r", "q", "k"]
    for i in range(len(string)):
        if string[i] in line_figures:
            data[counter] += [line_figures.index(string[i]) + 1]
        elif string[i] in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            data[counter] += [0] * int(string[i])
        elif string[i] == "/":
            counter += 1
        elif string[i] == "w":
            colour = WHITE
            break
        elif string[i] == "b":
            break    
    return data, colour 
    
