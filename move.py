import time
from copy import deepcopy
from constants import *
from position import Position
from stuff import change_pos


def all_moves_on_line(position, vector, x, y, check, line_legal, colour, max_step=7, pawntrue=False):
    line = []
    for i in range(max_step):
        x1, y1 = x + vector[0] * (i + 1), y + vector[1] * (i + 1)
        if min(x1, y1) >= 0 and max(x1, y1) <= 7:
            if not check:
                if pawntrue:
                    if vector[1] != 0:
                        if position.get_avail_certain_figure(x1, y1, [PAWN, KNIGHT, BISHOP, ROOK, QUEEN], 1 - colour):
                            line += [[x, y, x1, y1]]
                    else:
                        if not position.get_avail_figure(x1, y1):
                            line += [[x, y, x1, y1]]
                    return line        
                elif not position.get_avail_colour_figure(x1, y1, colour):
                    line += [[x, y, x1, y1]]  
                if position.get_avail_figure(x1, y1):
                    return line
            else:
                if pawntrue:
                    if [x1, y1] in line_legal:
                        if vector[1] != 0:
                            if position.get_avail_certain_figure(x1, y1, [PAWN, KNIGHT, BISHOP, ROOK, QUEEN], 1 - colour):
                                line += [[x, y, x1, y1]]
                        else:
                            if not position.get_avail_figure(x1, y1):
                                line += [[x, y, x1, y1]]
                        return line                    
                else:    
                    if position.get_avail_colour_figure(x1, y1, colour):
                        return line
                    elif position.get_avail_figure(x1, y1) and [x1, y1]:
                        if [x1, y1] in line_legal:
                            line += [[x, y, x1, y1]]
                        return line
                    elif [x1, y1] in line_legal:
                        line += [[x, y, x1, y1]]
        else:
            break  
    return line 


    
        
def check_bunch_of_the_line(position, vector, x, y, figures, colour, max_step=7):
    counter = 0
    line_bunch = []
    line_legal_moves = []
    for i in range(max_step):
        x1, y1 = x + vector[0] * (i + 1), y + vector[1] * (i + 1)
        if min(x1, y1) >= 0 and max(x1, y1) <= 7:
            if position.get_avail_certain_figure(x1, y1, figures, 1 - colour):
                if counter == 0:
                    line_legal_moves += [[x1, y1]]
                    return 1, [], line_legal_moves
                else:
                    return 0, line_bunch, [] 
            elif position.get_avail_colour_figure(x1, y1, 1 - colour):
                return 0, [], []
            elif position.get_avail_colour_figure(x1, y1, colour):
                if counter:
                    return 0, [], []
                else:
                    counter += 1
                    line_bunch += [[x1, y1]]
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
        a, b, line_legal_moves = check_bunch_of_the_line(position, vector, x, y, [BISHOP, QUEEN], colour)
        number_of_checks += a
        if b:
            list_bunches += b
        if line_legal_moves:
            line_legal = line_legal_moves     
    for vector in VERT_MOVES:
        a, b, line_legal_moves = check_bunch_of_the_line(position, vector, x, y, [ROOK, QUEEN], colour)      
        number_of_checks += a
        if b:
            list_bunches += b 
        if line_legal_moves:
            line_legal = line_legal_moves     
    for vector in KNIGHT_MOVES:
        a, b, line_legal_moves = check_bunch_of_the_line(position, vector, x, y, [KNIGHT], colour, 1)     
        number_of_checks += a 
        if line_legal_moves:
            line_legal = line_legal_moves      
    for vector in [(pawn_vert,1), (pawn_vert,-1)]:
        a, b, line_legal_moves = check_bunch_of_the_line(position, vector, x, y, [PAWN], colour, 1)       
        number_of_checks += a
        if line_legal_moves:
            line_legal = line_legal_moves    
    for vector in KING_MOVES:
        a, b, line_legal_moves = check_bunch_of_the_line(position, vector, x, y, [KING], colour, 1)
        if a > 0:
            return 3, [], []
    if number_of_checks == 2:
        line_legal = []
    return number_of_checks, list_bunches, line_legal 


def get_move(position, figure, x, y, line_legal, colour, check=False):
    if colour:
        pawn_vert = -1
    else:
        pawn_vert = 1    
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
        for vector in [(pawn_vert, 1), (pawn_vert, -1), (pawn_vert, 0)]:
            line += all_moves_on_line(position, vector, x, y, check, line_legal, colour, 1, True)
    return line 

def bunch_moves(position, x1, y1, xking, yking, typef, check, line_legal, colour):
    if not check:
        if colour == WHITE:
            change_x_coord = 1
            change_y_coord = 1
        else:
            change_x_coord = -1
            change_y_coord = -1
#change_y_coord для двух случаев ходов по диагонали            
        line = []
        if typef == KNIGHT:
            return []
        elif x1 == xking and typef in [ROOK, QUEEN]:
            for vector in [(0, 1), (0, -1)]:
                line += all_moves_on_line(position, vector, x1, y1, check, line_legal, colour)
            return line
        elif y1 == yking:
            if typef in [ROOK, QUEEN]:
                for vector in [(1, 0), (-1, 0)]:
                    line += all_moves_on_line(position, vector, x1, y1, check, line_legal, colour)
                return line
            elif typef == PAWN and xking < x1:
                return all_moves_on_line(position, (1, 0), x1, y1, check, line_legal, colour, 1)
        elif (x1 - xking - y1 + yking) == 0:
            if typef in [BISHOP, QUEEN]:
                for vector in [(1, 1), (-1, -1)]:
                    line += all_moves_on_line(position, vector, x1, y1, check, line_legal, colour)
                return line
            elif typef == PAWN:
                if position.get_avail_colour_figure(x1 + change_x_coord, y1 + change_y_coord, 1 - colour):
                    return [[x1, y1, x1 + change_x_coord, y1 + change_y_coord]]
        else:
            if typef in [BISHOP, QUEEN]:
                for vector in [(-1, 1), (1, -1)]:
                    line += all_moves_on_line(position, vector, x1, y1, check, line_legal, colour)
                return line 
            elif typef == PAWN:
                if position.get_avail_colour_figure(x1 + change_x_coord, y1 - change_y_coord, 1 - colour):
                    return [[x1, y1, x1 + change_x_coord, y1 - change_y_coord]]     
    return []


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
                            list_moves += get_move(position, figure, x, y, line_legal, colour)
                        else:
                            list_moves += bunch_moves(position, x, y, xking, yking, figure, checks, line_legal, colour)         
                    else:
                        if [x, y] not in line:
                            list_moves += get_move(position, figure, x, y, line_legal, colour, True)
            else:
                for coords in position.get_list(figure, colour):
                    x, y = coords[0], coords[1]
                    if checks == 0:
                        if [x, y] not in line:
                            list_moves += get_move(position, figure, x, y, line_legal, colour)
                        else:
                            list_moves += bunch_moves(position, x, y, xking, yking, figure, checks, line_legal, colour)         
                    else:
                        if [x, y] not in line:
                            list_moves += get_move(position, figure, x, y, line_legal, colour, True)                
    list_moves += king_moves(position, xking, yking, colour) 
    return list_moves, checks      
    

   
def make_move(position, colour, length):
    list_moves, checks = legal_moves(position, colour)
    if not length and len(list_moves) == 0 and checks > 0:
        return True
    elif not length:
        return False
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
                            delete = True
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
       
            
            
    
    
    

        
      
        