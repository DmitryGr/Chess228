from stuff import read_position, course_record
from move import make_move
from constants import *

def main():
    data = []
    for i in range(8):
        data += [list(map(int, input().split()))]
    position = read_position(data)
    x, y, x1, y1 = make_move(position, 0, 1)
    eat = False
    if x == -1:
        print("NO")
    else:    
        if position.get_avail_colour_figure(x1, y1, BLACK):
            eat = True   
        print(course_record(x, y, x1, y1, position.data[x][y], eat))
        

main()         