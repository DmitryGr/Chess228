from stuff import read_position, course_record, print_data
from move import make_move
from constants import *
from fen import fen_format


def main():
    while True:
        input_str = input()
        if "/" not in input_str:
            continue
        data, colour, castling_list, passant = fen_format(input_str)    
        position = read_position(data)
        x, y, x1, y1 = make_move(position, colour, 1, castling_list, passant)
        if x != ANSWER_CASTLE_SHORT and x != ANSWER_CASTLE_BIG:
            eat = False
            if x == -1:
                print("NO")
            else:    
                if position.get_avail_colour_figure(x1, y1, BLACK) or (position.data[x][y] == PAWN and passant == [x1, y1]):
                    eat = True   
                print(course_record(x, y, x1, y1, position.data[x][y], eat))
        elif x == ANSWER_CASTLE_BIG:
            print("0-0-0")
        else:
            print("0-0")
        

main()         