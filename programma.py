PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6
X_COORD = 0
Y_COORD = 1


class Position:
    def __init__(self, data):
        line_white = [[], [], [], [], [], []]
        line_black = [[], [], [], [], [], []]
        for i in range(8):
            for j in range(8):
                if data[i][j] > 6:
                    line_black[data[i][j] - 7] += [i, j]
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
        if self.data[x][y] > colour * 6:
            return True
        return False
    
    def get_avail_figure(self, x, y):
        if self.data[x][y] > 0:
            return True
        return False 
    
    def return_coords(self, number_figure, number_figure_list, colour):
        if colour == 0:
            return self.white[number_figure][number_figure_list][X_COORD], self.white[number_figure][number_figure_list][Y_COORD]
        else:
            return self.black[number_figure][number_figure_list][X_COORD], self.white[number_figure][number_figure_list][Y_COORD]

        
def all_moves_on_line(position, vector, x, y, max_step=7, pawntrue=False):
    line = []
    for i in range(max_step):
        x1, y1 = x + vector[0] * (i + 1), y + vector[1] * (i + 1)
        if min(x1, y1) >= 0 and max(x1, y1) <= 7:
            if pawntrue != True and position.get_avail_certain_figure(x1, y1, [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING], 0) != True:
                line += [[x, y, x1, y1]]
            if position.get_avail_figure(x1, y1) == True:
                return line        
    return line   
    
        
def check_bunch_of_the_line(position, vector, x, y, bunch_tf, figures, max_step=7):
    counter = 0
    for i in range(max_step):
        x1, y1 = x + vector[0] * (i + 1), y + vector[1] * (i + 1)
        if min(x1, y1) >= 0 and max(x1, y1) <= 7:
            if position.get_avail_certain_figure(x1, y1, figures, 1) == True:
                if bunch_tf == False:
                    return 1, []
                elif counter == 0:
                    counter += 1
                    line_bunch = [x1, y1]
                else:
                    return 1, line_bunch 
    if counter == 0 and bunch_tf == True:
        return 0, []
    else:
        return 0, []
                    
                
def inspect_check(position):
    x, y = position.return_coords(KING - 1, 0, 0)
    number_of_checks = 0
    list_bunches = []
    for vector in [(1,1), (1,-1), (-1,1), (-1,-1)]:
        a, b = check_bunch_of_the_line(position, vector, x, y, True, [BISHOP, QUEEN])
        number_of_checks += a
        if len(b) != 0:
            list_bunches += b
    for vector in [(0,1), (1,0), (0,-1), (-1,0)]:
        a, b = check_bunch_of_the_line(position, vector, x, y, True, [ROOK, QUEEN])
        number_of_checks += a
        if len(b) != 0:
            list_bunches += b
    for vector in [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]:
        a, b = check_bunch_of_the_line(position, vector, x, y, False, [KNIGHT], 1)
        number_of_checks += a
    for vector in [(1,1), (-1,1)]:
        a, b = check_bunch_of_the_line(position, vector, x, y, False, [PAWN], 1)
        number_of_checks += a
    return number_of_checks, list_bunches   


def get_move(number, position, x, y):
    line = []
    if number == KNIGHT:
        for vector in [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]:
            line += all_moves_on_line(position, vector, x, y, 1)
    elif number == BISHOP or number == QUEEN:
        for vector in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            line += all_moves_on_line(position, vector, x, y) 
    elif number == ROOK or number == QUEEN:
        for vector in [(1,0), (-1,0), (0,1), (0,-1)]:
            line += all_moves_on_line(position, vector, x, y)
    elif number == PAWN:
        line += all_moves_on_line(position, (1, 0), x, y, 1)
        for vector in [(1,1), (1,-1)]:
            line += all_moves_on_line(position, vector, x, y, 1, True)
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
            if position.get_avail_colour_figure(x1 + 1, y1 + 1, 1) == TRUE:
                return [x1, y1, x1 + 1, y1 + 1]
    else:
        if typef in [BISHOP, QUEEN]:
            for vector in [(-1, 1), (-1, 1)]:
                line += all_moves_on_line(position, vector, x1, y1, max_step=7, pawntrue=False)
            return line 
        elif typef == PAWN:
            if position.get_avail_colour_figure(x1 + 1, y1 - 1, 1) == TRUE:
                return [x1, y1, x1 + 1, y1 - 1]        
    return []
        
                       
def data_legal_moves(position):
    checks, line = inspect_check(position)
    list_moves = []
    if not checks:
        for i in range(QUEEN):
            for line in position.white[i]:
                x, y = line[0], line[1]
                if [x, y] not in line:
                    list_moves += get_move(i + 1, position, x, y)
                else:
                    xkinging, ykinging = position.return_coords(KING - 1, 0, 0)
                    list_moves += bunch_moves(position, x, y, xkinging, ykinging, i + 1)
    print(list_moves)           
    
    
def main():
    data = []
    for i in range(8):
        data += [list(map(int, input().split()))]
    data = data[::-1]    
    start_position = Position(data)
    data_legal_moves(start_position)
    

main()        
            
            
    
    
    

        
      
        