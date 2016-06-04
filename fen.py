from constants import *

def fen_format(string):
    colour = BLACK
    data = [[], [], [], [], [], [], [], []]
    counter = 0
    line_figures = ["P", "N", "B", "R", "Q", "K", "p", "n", "b", "r", "q", "k"]
    figures = True
    passant = False
    castling_list = [False, False, False, False]
    all_figures = False
    for i in range(len(string)):
        if figures:
            if string[i] == " ":
                all_figures = True
            if string[i] in line_figures and not all_figures:
                data[counter] += [line_figures.index(string[i]) + 1]
            elif string[i] in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                data[counter] += [0] * int(string[i])
            elif string[i] == "/":
                counter += 1
            elif string[i] == "w":
                colour = WHITE
                figures = False
            elif string[i] == "b":
                figures = False
        else:
            if string[i] in ["K", "Q", "k", "q"]:
                castling_list[["K", "Q", "k", "q"].index(string[i])] = True
            elif string[i] in ["a", "b", "c", "d", "e", "f", "g", "h"]:
                passant = string[i:i + 2]
        if passant != False:
            line_vert = ["a", "b", "c", "d", "e", "f", "g", "h"]
            passant = [int(passant[1]) - 1, line_vert.index(passant[0])]  
    return data, colour, castling_list, passant 
    
