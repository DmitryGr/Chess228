PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6


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
    def getcolour(self, x, y, figures, colour):
        for i in range(len(figures)):
            if self.data[x][y] == (colour * 6) + figures[i]:
                return True
        return False
    def getfigure(self, x, y):
        if self.data[x][y] != 0:
            return True
        return False    

        
def all_moves_on_line(position, vector, x, y, max_step=7, pawntrue=False):
    line = []
    for i in range(max_step):
        x1, y1 = x + vector[0] * (i + 1), y + vector[1] * (i + 1)
        if min(x1, y1) >= 0 and max(x1, y1) <= 7:
            if pawntrue != True and position.getcolour(x1, y1, [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING], 0) != True:
                line += [[x, y, x1, y1]]
            if position.getfigure(x1, y1) == True:
                return line        
    return line   
    
        
def check_bunch_of_the_line(position, vector, x, y, bunch_tf, figures, max_step=7):
    counter = 0
    for i in range(max_step):
        x1, y1 = x + vector[0] * (i + 1), y + vector[1] * (i + 1)
        if min(x1, y1) >= 0 and max(x1, y1) <= 7:
            if position.getcolour(x1, y1, figures, 1) == True:
                if bunch_tf == False:
                    return 1
                elif counter == 0:
                    counter += 1
                    line_bunch = [x1, y1]
                else:
                    return 1, line_bunch 
    if counter == 0 and bunch_tf == True:
        return 0, []
    else:
        return 0
                    
                
def inspect_check(position):
    x, y = position.white[5][0][0], position.white[5][0][1]
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
        a = check_bunch_of_the_line(position, vector, x, y, False, [KNIGHT], 1)
        number_of_checks += a
    for vector in [(1,1), (-1,1)]:
        a = check_bunch_of_the_line(position, vector, x, y, False, [PAWN], 1)
        number_of_checks += a
    return number_of_checks, list_bunches   


def get_line(number, position, x, y):
    line = []
    if number + 1 == KNIGHT:
        for vector in [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]:
            line += all_moves_on_line(position, vector, x, y, 1)
    elif number + 1 == BISHOP or number + 1 == QUEEN:
        for vector in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            line += all_moves_on_line(position, vector, x, y) 
    elif number + 1 == ROOK or number + 1 == QUEEN:
        for vector in [(1,0), (-1,0), (0,1), (0,-1)]:
            line += all_moves_on_line(position, vector, x, y)
    elif number + 1 == PAWN:
        line += all_moves_on_line(position, (1, 0), x, y, 1)
        for vector in [(1,1), (1,-1)]:
            line += all_moves_on_line(position, vector, x, y, 1, True)
    return line 

def bunch_moves(position, x1, y1, xk, yk, typef):
    line = []
    if typef == KNIGHT:
        return []
    elif x1 == xk and typef in [ROOK, QUEEN]:
        for vector in [(0, 1), (0, -1)]:
            line += all_moves_on_line(position, vector, x1, y1, max_step=7, pawntrue=False)
        return line
    elif y1 == yk:
        if typef in [ROOK, QUEEN]:
            for vector in [(1, 0), (-1, 0)]:
                line += all_moves_on_line(position, vector, x1, y1, max_step=7, pawntrue=False)
            return line
        elif typef == PAWN and yk > y1:
            return all_moves_on_line(position, (1, 0), x1, y1, max_step=1, pawntrue=False)
    elif (x1 - xk - y1 + yk) == 0 and typef in [BISHOP, QUEEN]:
        for vector in [(1, 1), (-1, -1)]:
            line += all_moves_on_line(position, vector, x1, y1, max_step=7, pawntrue=False)
        return line
    else:
        for vector in [(-1, 1), (-1, 1)]:
            line += all_moves_on_line(position, vector, x1, y1, max_step=7, pawntrue=False)
        return line 
    return []
        
                       
def data_legal_moves(position):
    a, line = inspect_check(position)
    list_moves = []
    if a == 0:
        for i in range(0, 5):
            for j in range(len(position.white[i])):
                x, y = position.white[i][j][0], position.white[i][j][1]
                if [x, y] not in line:
                    list_moves += get_line(i, position, x, y)
                else:
                    xking, yking = position.white[5][0][0], position.white[5][0][1]
                    list_moves += bunch_moves(position, x, y, xking, yking, i + 1)            
    print(list_moves)           
    
    
def main():
    data = []
    for i in range(8):
        data += [list(map(int, input().split()))]
    data = data[::-1]    
    start_position = Position(data)
    data_legal_moves(start_position)
    

main()        
            
            
    
    
    

        
      
        