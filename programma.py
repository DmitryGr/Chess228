import time
from copy import deepcopy
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6
X_COORD = 0
Y_COORD = 1
WHITE = 0
BLACK = 1
KNIGHT_MOVES = (1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)
DIAG_MOVES = (1,1), (1,-1), (-1,1), (-1,-1)
VERT_MOVES = (1,0), (-1,0), (0,1), (0,-1)
KING_MOVES = (1,0), (-1,0), (1,-1), (0,-1), (-1,-1), (0,1), (-1,1), (1,1)




class Position:
    def __init__(self, data):
        line_white = [[], [], [], [], [], []]
        line_black = [[], [], [], [], [], []]
        for i in range(8):
            for j in range(8):
                if data[i][j] > 6:
                    line_black[data[i][j] - 7] += [[i, j]]
                elif data[i][j] != 0:
                    line_white[data[i][j] - 1] += [[i, j]]            
        self.data = data
        self.white = line_white
        self.black = line_black
        
    def get_avail_certain_figure(self, x, y, figures, colour):
        for i in range(len(figures)):
            if self.data[x][y] == (colour * 6) + figures[i]:
                return True
        return False    

    def get_avail_colour_figure(self, x, y, colour):
        return self.data[x][y] > colour * 6

    def get_avail_figure(self, x, y):
        return self.data[x][y] > 0

    
    def return_coords(self, figure, figure_list, colour):
        if colour == WHITE:
            return self.white[figure - 1][figure_list][X_COORD], self.white[figure - 1][figure_list][Y_COORD]
        else:
            return self.black[figure - 1][figure_list][X_COORD], self.black[figure - 1][figure_list][Y_COORD]
        
    def change_coords(self, figure, figure_list, colour, x1, y1):
        if colour == WHITE:
            self.white[figure - 1][figure_list][X_COORD], self.white[figure - 1][figure_list][Y_COORD] = x1, y1
        else:
            self.black[figure - 1][figure_list][X_COORD], self.black[figure - 1][figure_list][Y_COORD] = x1, y1 
            
    def change_position(self, x, y, figure):
        self.data[x][y] = figure
    
    def get_list(self, figure, colour):
        if not colour:
            return self.white[figure - 1]
        else:
            return self.black[figure - 1]
        
        

        
def all_moves_on_line(position, vector, x, y, check, line_legal, colour, max_step=7, pawntrue=False):
    line = []
    for i in range(max_step):
        x1, y1 = x + vector[0] * (i + 1), y + vector[1] * (i + 1)
        if min(x1, y1) >= 0 and max(x1, y1) <= 7:
            if not check:
                    if not pawntrue and not position.get_avail_certain_figure(x1, y1, [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING], colour):
                        line += [[x, y, x1, y1]]    
                    if position.get_avail_figure(x1, y1):
                        return line 
            if check:
                if [x1, y1] in line_legal:
                    return [x, y, x1, y1]
        else:
            break
    return line 


    
        
def check_bunch_of_the_line(position, vector, x, y, bunch_tf, figures, colour, max_step=7):
    counter = 0
    line_bunch = []
    line_legal_moves = []
    for i in range(max_step):
        x1, y1 = x + vector[0] * (i + 1), y + vector[1] * (i + 1)
        if min(x1, y1) >= 0 and max(x1, y1) <= 7:
            if position.get_avail_certain_figure(x1, y1, figures, 1 - colour):
                if not bunch_tf or counter == 0:
                    return 1, [], line_legal_moves
                else:
                    return 0, line_bunch, [] 
            elif position.get_avail_colour_figure(x1, y1, colour):
                if counter:
                    return 0, [], []
                else:
                    counter += 1
                    line_bunch += [x1, y1]
            line_legal_moves += [[x1, y1]]
        else:
            break
    return 0, [], []
                    
                
def inspect_check(position, colour):
    if not colour:
        pawn_vert = 1
    else:
        pawn_vert = -1
    line_legal = []
    x, y = position.return_coords(KING, 0, colour)
    number_of_checks = 0
    list_bunches = []
    for vector in DIAG_MOVES:
        a, b, line_legal_moves = check_bunch_of_the_line(position, vector, x, y, True, [BISHOP, QUEEN], colour)
        number_of_checks += a
        if b:
            list_bunches += [b]
        if line_legal_moves:
            line_legal = line_legal_moves
    for vector in VERT_MOVES:
        a, b, line_legal_moves = check_bunch_of_the_line(position, vector, x, y, True, [ROOK, QUEEN], colour)      
        number_of_checks += a
        if b:
            list_bunches += [b] 
        if line_legal_moves:
            line_legal = line_legal_moves            
    for vector in KNIGHT_MOVES:
        a, b, line_legal_moves = check_bunch_of_the_line(position, vector, x, y, False, [KNIGHT], colour, 1)     
        number_of_checks += a 
        if line_legal_moves:
            line_legal = line_legal_moves        
    for vector in [(pawn_vert,1), (pawn_vert,-1)]:
        a, b, line_legal_moves = check_bunch_of_the_line(position, vector, x, y, False, [PAWN], colour, 1)       
        number_of_checks += a
        if line_legal_moves:
            line_legal = line_legal_moves        
    if number_of_checks == 2:
        line_legal = []
    return number_of_checks, list_bunches, line_legal 


def get_move(figure, position, x, y, line_legal, colour, check=False):
    if colour:
        pawn_vert = 1
    else:
        pawn_vert = -1    
    line = []
    if figure == KNIGHT:
        for vector in KNIGHT_MOVES:
            line += all_moves_on_line(position, vector, x, y, check, line_legal, colour, 1)
    if figure == BISHOP or figure == QUEEN:
        for vector in DIAG_MOVES:
            line += all_moves_on_line(position, vector, x, y, check, line_legal, colour) 
    if figure == ROOK or figure == QUEEN:
        for vector in VERT_MOVES:
            line += all_moves_on_line(position, vector, x, y, check, line_legal, colour)
    if figure == PAWN:
        line += all_moves_on_line(position, (pawn_vert, 0), x, y, check, line_legal, colour, 1)
        for vector in [(pawn_vert,1), (pawn_vert,-1)]:
            line += all_moves_on_line(position, vector, x, y, check, line_legal, colour, 1, True)
    return line 

def bunch_moves(position, x1, y1, xking, yking, typef):
    line = []
    if typef == KNIGHT:
        return []
    elif x1 == xking and typef in [ROOK, QUEEN]:
        for vector in [(0, 1), (0, -1)]:
            line += all_moves_on_line(position, vector, x1, y1, max_step=7, pawntrue=False)
        return line
    elif y1 == yking:
        if typef in [ROOK, QUEEN]:
            for vector in [(1, 0), (-1, 0)]:
                line += all_moves_on_line(position, vector, x1, y1, max_step=7, pawntrue=False)
            return line
        elif typef == PAWN and xking < x1:
            return all_moves_on_line(position, (1, 0), x1, y1, max_step=1, pawntrue=False)
    elif (x1 - xking - y1 + yking) == 0:
        if typef in [BISHOP, QUEEN]:
            for vector in [(1, 1), (-1, -1)]:
                line += all_moves_on_line(position, vector, x1, y1, max_step=7, pawntrue=False)
            return line
        elif typef == PAWN:
            if position.get_avail_colour_figure(x1 + 1, y1 + 1, BLACK):
                return [x1, y1, x1 + 1, y1 + 1]
    else:
        if typef in [BISHOP, QUEEN]:
            for vector in [(-1, 1), (-1, 1)]:
                line += all_moves_on_line(position, vector, x1, y1, max_step=7, pawntrue=False)
            return line 
        elif typef == PAWN:
            if position.get_avail_colour_figure(x1 + 1, y1 - 1, BLACK):
                return [x1, y1, x1 + 1, y1 - 1]        
    return []


def print_data(list):
    print()
    print()
    for i in range(8):
        print(" ".join(map(str, list[7 - i])))
              

def king_moves(position, x, y, colour):
    line = []
    counter = 0
    for vector in KING_MOVES:
        x1, y1 = x + vector[0], y + vector[1]
        if min(x1, y1) >= 0 and max(x1, y1) <= 7 and not position.get_avail_colour_figure(x1, y1, colour):
            number_cell = position.data[x1][y1]
            position.data[x][y] = 0
            position.data[x1][y1] = KING * (colour + 1)
            position.change_coords(KING, 0, colour, x1, y1)
            if inspect_check(position, colour)[0] == 0:
                line += [[x, y, x1, y1]]
            position.data[x][y] = KING * (colour + 1)
            position.data[x1][y1] = number_cell
            position.change_coords(KING, 0, colour, x, y)
            counter += 1
    return line         
                
                               
def legal_moves(position, colour):
    checks, line, line_legal = inspect_check(position, colour)
    xking, yking = position.return_coords(KING, 0, colour)
    list_moves = []
    if checks < 2:
        for figure in [PAWN, KNIGHT, BISHOP, ROOK, QUEEN]:
            if colour == WHITE:
                for coords in position.get_list(figure, colour):
                    x, y = coords[0], coords[1]
                    if checks == 0:
                        if [x, y] not in line:
                            list_moves += get_move(figure, position, x, y, line_legal, colour)
                        else:
                            list_moves += bunch_moves(position, x, y, xking, yking, figure)         
                    else:
                        if [x, y] not in line:
                            list_moves += get_move(figure, position, x, y, line_legal, colour, True)
            else:
                for coords in position.get_list(figure, colour):
                    x, y = coords[0], coords[1]
                    if checks == 0:
                        if [x, y] not in line:
                            list_moves += get_move(figure, position, x, y, line_legal, colour)
                        else:
                            list_moves += bunch_moves(position, x, y, xking, yking, figure)         
                    else:
                        if [x, y] not in line:
                            list_moves += get_move(figure, position, x, y, line_legal, colour, True)                
    list_moves += king_moves(position, xking, yking, colour) 
    return list_moves   

def change_pos(position, x, y, x1, y1, first_figure, second_figure):
    position.change_position(x, y, first_figure)
    position.change_position(x1, y1, second_figure)    
    

   
def make_move(position, colour, length):
    list_moves = legal_moves(position, colour)
    if not length and len(list_moves) > 0:
        return False
    elif not length:
        return True
    for move in list_moves:
        x, y, x1, y1 = move[0], move[1], move[2], move[3]
        number_cell = position.data[x][y]
        number_end = position.data[x1][y1]
        change_pos(position, x, y, x1, y1, 0, number_cell)
        for i in range(len(position.white[number_cell - 1])):
            if position.white[number_cell - 1][i] == [x, y]:
                change_number = i
                position.change_coords(number_cell, i, WHITE, x1, y1)
                delete = False
                if number_end > 0:
                    for figures in position.black:
                        if [x1, y1] in figures:
                            delete 
                            delete_figures = figures
                            figures.remove([x1, y1])           
                break  
        if make_move(position, 1 - colour, length - 1):
            if delete:
                delete_figures += [x1, y1]
            change_pos(position, x, y, x1, y1, number_cell, number_end)
            position.change_coords(number_cell, i, WHITE, x, y)
            if delete:
                delete_figures += [x1, y1]
            return [x, y, x1, y1] 
        change_pos(position, x, y, x1, y1, number_cell, number_end)
        position.change_coords(number_cell, i, WHITE, x, y)
    return [-1, -1, -1, -1]    

    
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
    

def read_position(data):
    data = data[::-1]
    return Position(data)    
    

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
            
            
    
    
    

        
      
        