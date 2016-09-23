from position import Position
from constants import *

def read_position(data):
    data = data[::-1]
    return Position(data) 

def change_pos(position, x, y, x1, y1, first_figure, second_figure):
    position.change_position(x, y, first_figure)
    position.change_position(x1, y1, second_figure) 
    
def material_count(position):
    material = 0
    for i in range(5):
        material += len(position.white[i]) * VALUES[i] - len(position.black[i]) * VALUES[i]
    return material    
    
def course_record(x, y, x1, y1, figure, eat):
    answer = ""
    line_figures = ["", "N", "B", "R", "Q", "K"]
    figure = figure % 6
    answer += line_figures[figure - 1]
    if eat:
        answer += ":"
    answer += VERTICALES[y1]
    answer += str(x1 + 1)
    if figure == PAWN and eat:
        answer = VERTICALES[y] + answer
    return answer 

def transformation_record(y_start, x, y, figure):
    answer = ""
    line_figures = ["N", "B", "R", "Q"]
    if y_start == y:
        answer += VERTICALES[y]
        answer += str(x + 1)
        for i in range(KNIGHT, QUEEN + 1):
            if i == figure:
                answer += line_figures[i - 2]
    else:
        answer += VERTICALES[y_start]
        answer += VERTICALES[y]
        for i in range(KNIGHT, QUEEN + 1):
            if i == figure:
                answer += line_figures[i - 2]          
    return answer
    
    

def print_data(line):
    print()
    print()
    for i in range(8):
        print(" ".join(map(str, line[7 - i])))
        
      
            
            
        
        
        
              