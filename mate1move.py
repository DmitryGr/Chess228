from stuff import read_position, course_record
from move import make_move
from constants import *
from fen import fen_format


def main():
    while True:
        input_str = input()
        if "/" not in input_str:
            continue
        data, colour = fen_format(input_str)
        position = read_position(data)
        x, y, x1, y1 = make_move(position, colour, 1)
        eat = False
        if x == -1:
            print("NO")
        else:    
            if position.get_avail_colour_figure(x1, y1, BLACK):
                eat = True   
            print(course_record(x, y, x1, y1, position.data[x][y], eat))
        

main()         