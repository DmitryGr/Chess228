from position import Position
from constants import *

def read_position(data):
    data = data[::-1]
    return Position(data) 

def change_pos(position, x, y, x1, y1, first_figure, second_figure):
    position.change_position(x, y, first_figure)
    position.change_position(x1, y1, second_figure) 
    
def course_record(x, y, x1, y1, figure, eat):
    answer = ""
    line_vert = ["a", "b", "c", "d", "e", "f", "g", "h"]
    line_figures = ["", "N", "B", "R", "Q", "K"]
    answer += line_figures[figure - 1]
    if eat:
        answer += ":"
    answer += line_vert[y1]
    answer += str(x1 + 1)
    if figure == PAWN and eat:
        answer = line_vert[y] + answer
    return answer   

def print_data(list):
    print()
    print()
    for i in range(8):
        print(" ".join(map(str, list[7 - i])))
              