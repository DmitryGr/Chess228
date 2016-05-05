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

    
    def return_coords(self, number_figure, number_figure_list, colour):
        if colour == WHITE:
            return self.white[number_figure - 1][number_figure_list][X_COORD], self.white[number_figure - 1][number_figure_list][Y_COORD]
        else:
            return self.black[number_figure - 1][number_figure_list][X_COORD], self.white[number_figure - 1][number_figure_list][Y_COORD]

        
def all_moves_on_line(position, vector, x, y, check, line_legal, max_step=7, pawntrue=False):
    line = []
    for i in range(max_step):
        x1, y1 = x + vector[0] * (i + 1), y + vector[1] * (i + 1)
        if min(x1, y1) >= 0 and max(x1, y1) <= 7:
            if not check:
                if min(x1, y1) >= 0 and max(x1, y1) <= 7:
                    if not pawntrue and not position.get_avail_certain_figure(x1, y1, [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING], 0):
                        line += [[x, y, x1, y1]]
                    if position.get_avail_figure(x1, y1):
                        return line 
            if check:
                if [x1, y1] in line_legal:
                    return [x1, y1]
        else:
            break
    return line 


    
        
def check_bunch_of_the_line(position, vector, x, y, bunch_tf, figures, max_step=7):
    counter = 0
    line_bunch = []
    line_legal_line = []
    for i in range(max_step):
        x1, y1 = x + vector[0] * (i + 1), y + vector[1] * (i + 1)
        if min(x1, y1) >= 0 and max(x1, y1) <= 7:
            if position.get_avail_certain_figure(x1, y1, figures, BLACK):
                if not bunch_tf or counter == 0:
                    print(line_legal_line)
                    return 1, [], line_legal_line
                else:
                    return 1, line_bunch, [] 
            elif position.get_avail_colour_figure(x1, y1, WHITE):
                if counter:
                    return 0, [], []
                else:
                    counter += 1
                    line_bunch += [x1, y1]
            line_legal_line += [[x1, y1]]
        else:
            break
    return 0, [], []
                    
                
def inspect_check(position):
    line_legal = []
    x, y = position.return_coords(KING, 0, 0)
    number_of_checks = 0
    list_bunches = []
    for vector in [(1,1), (1,-1), (-1,1), (-1,-1)]:
        a, b, line_legal_line = check_bunch_of_the_line(position, vector, x, y, True, [BISHOP, QUEEN])
        number_of_checks += a
        if len(b) != 0:
            list_bunches += b
        if line_legal_line != []:
            line_legal = line_legal_line
    for vector in [(0,1), (1,0), (0,-1), (-1,0)]:
        a, b, line_legal_line = check_bunch_of_the_line(position, vector, x, y, True, [ROOK, QUEEN])
        number_of_checks += a
        if len(b) != 0:
            list_bunches += b  
        if line_legal_line != []:
            line_legal = line_legal_line            
    for vector in [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]:
        a, b, line_legal_line = check_bunch_of_the_line(position, vector, x, y, False, [KNIGHT], 1)
        number_of_checks += a 
        if line_legal_line != []:
            line_legal = line_legal_line        
    for vector in [(1,1), (-1,1)]:
        a, b, line_legal_line = check_bunch_of_the_line(position, vector, x, y, False, [PAWN], 1)
        number_of_checks += a
        if line_legal_line != []:
            line_legal = line_legal_line        
    if number_of_checks == 2:
        line_legal = []
    return number_of_checks, list_bunches, line_legal 


def get_move(figure, position, x, y, line_legal, check=False):
    line = []
    if figure == KNIGHT:
        for vector in [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]:
            line += all_moves_on_line(position, vector, x, y, check, line_legal, 1)
    elif figure == BISHOP or figure == QUEEN:
        for vector in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            line += all_moves_on_line(position, vector, x, y, check, line_legal) 
    elif figure == ROOK or figure == QUEEN:
        for vector in [(1,0), (-1,0), (0,1), (0,-1)]:
            line += all_moves_on_line(position, vector, x, y, check, line_legal)
    elif figure == PAWN:
        line += all_moves_on_line(position, (1, 0), x, y, 1, check, line_legal)
        for vector in [(1,1), (1,-1)]:
            line += all_moves_on_line(position, vector, x, y, check, line_legal, 1, True)
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
        
                       
def legal_moves(position):
    checks, line, line_legal = inspect_check(position)
    list_moves = []
    if checks < 2:
        for i in range(QUEEN):
            for line in position.white[i]:
                x, y = line[0], line[1]
                if not checks:
                    if [x, y] not in line:
                        list_moves += get_move(i + 1, position, x, y, line_legal)
                    else:
                        xking, yking = position.return_coords(KING, 0, WHITE)
                        list_moves += bunch_moves(position, x, y, xking, yking, i + 1)         
                else:
                    if [x, y] not in line:
                        list_moves += get_move(i + 1, position, x, y, line_legal, True)             
    return list_moves           
    
    
def main():
    data = []
    for i in range(8):
        data += [list(map(int, input().split()))]
    data = data[::-1]    
    start_position = Position(data)
    legal_moves(start_position)
    

main()        
            
            
    
    
    

        
      
        