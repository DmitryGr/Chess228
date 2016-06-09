import time
from copy import deepcopy
from constants import *
from position import Position
from stuff import change_pos, print_data


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
                        return line    
                    else:
                        if not position.get_avail_figure(x1, y1):
                            line += [[x, y, x1, y1]]                            
                            if max_step == 1:
                                return line 
                            else:
                                max_step = 1 
                        else:
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
                            if max_step == 1:
                                return line 
                            else:
                                max_step = 1
                                
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


def get_move(position, figure, x, y, line_legal, colour, check=False, passant=False):
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
        if x == 1:
            line += all_moves_on_line(position, (pawn_vert, 0), x, y, check, line_legal, colour, 2, True)
        else:
            line += all_moves_on_line(position, (pawn_vert, 0), x, y, check, line_legal, colour, 1, True)
        for vector in [(pawn_vert, 1), (pawn_vert, -1)]:
            line += all_moves_on_line(position, vector, x, y, check, line_legal, colour, 1, True)         
        if passant == [x + pawn_vert, y + 1] or passant == [x + pawn_vert, y - 1]:
            line += [[x, y, passant[0], passant[1]]]
    return line 

def bunch_moves(position, x1, y1, xking, yking, typef, check, line_legal, colour, passant):
    if not check:
        if colour == WHITE:
            change_x_coord = 1
            change_y_coord = 1
        else:
            change_x_coord = -1
            change_y_coord = -1          
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
                if x1 == 1:
                    return all_moves_on_line(position, (change_x_coord, 0), x1, y1, check, line_legal, colour, 1)
                else:
                    return all_moves_on_line(position, (change_x_coord, 0), x1, y1, check, line_legal, colour, 2)
        elif (x1 - xking - y1 + yking) == 0:
            if typef in [BISHOP, QUEEN]:
                for vector in [(1, 1), (-1, -1)]:
                    line += all_moves_on_line(position, vector, x1, y1, check, line_legal, colour)
                return line
            elif typef == PAWN:
                if position.get_avail_colour_figure(x1 + change_x_coord, y1 + change_y_coord, 1 - colour) or [x1 + change_x_coord, y1 + change_y_coord] == passant:
                    return [[x1, y1, x1 + change_x_coord, y1 + change_y_coord]]
        else:
            if typef in [BISHOP, QUEEN]:
                for vector in [(-1, 1), (1, -1)]:
                    line += all_moves_on_line(position, vector, x1, y1, check, line_legal, colour)
                return line 
            elif typef == PAWN:
                if position.get_avail_colour_figure(x1 + change_x_coord, y1 - change_y_coord, 1 - colour) or [x1 + change_x_coord, y1 + change_y_coord] == passant:
                    return [[x1, y1, x1 + change_x_coord, y1 - change_y_coord]]     
    return []


def king_moves(position, x, y, colour, castling_list):
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
    for i in [1, -1]:
        check_castle = False
        castle = SHORT_CASTLE
        if i == 1:
            castle = BIG_CASTLE        
        for vector in [(0, i * 1), (0, i * 2)]:
            if castling_list[colour * 2 + castle]:
                x1, y1 = x + vector[0], y + vector[1]
                if not position.get_avail_figure(x1, y1):
                    position.data[x][y] = 0
                    position.data[x1][y1] = KING * (colour + 1)
                    position.change_coords(KING, 0, colour, x1, y1) 
                    if inspect_check(position, colour)[0] != 0:
                        check_castle = True
                    position.data[x][y] = KING * (colour + 1)
                    position.data[x1][y1] = 0
                    position.change_coords(KING, 0, colour, x, y)                         
        if not check_castle:
            if i == 1 and castling_list[colour * 2]:
                line += [["0-0"]]
                castling_list[colour * 2] = False
                castling_list[colour * 2 + 1] = False
            elif i == -1 and castling_list[colour * 2 + 1]:    
                line += [["0-0-0"]]  
                castling_list[colour * 2] = False
                castling_list[colour * 2 + 1] = False          
    return line         
                
                               
def legal_moves(position, colour, castling_list=[False, False, False, False], passant=False):
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
                            list_moves += get_move(position, figure, x, y, line_legal, colour, False, passant)
                        else:
                            list_moves += bunch_moves(position, x, y, xking, yking, figure, checks, line_legal, colour, passant)         
                    else:
                        if [x, y] not in line:
                            list_moves += get_move(position, figure, x, y, line_legal, colour, True, passant)
            else:
                for coords in position.get_list(figure, colour):
                    x, y = coords[0], coords[1]
                    if checks == 0:
                        if [x, y] not in line:
                            list_moves += get_move(position, figure, x, y, line_legal, colour, False, passant)
                        else:
                            list_moves += bunch_moves(position, x, y, xking, yking, figure, checks, line_legal, colour, passant)         
                    else:
                        if [x, y] not in line:
                            list_moves += get_move(position, figure, x, y, line_legal, colour, True, passant)                
    list_moves += king_moves(position, xking, yking, colour, castling_list) 
    return list_moves, checks      
    
def castle_move(position, length, colour):
    start_vert = colour * 7
    x, y = start_vert, START_KING
    x1, y1 = start_vert, START_KING + length
    if length == 2:
        x_rook_start, y_rook_start = start_vert, START_ROOK_SHORT
        x_rook_end, y_rook_end = start_vert, END_ROOK_SHORT
    else:
        x_rook_start, y_rook_start = start_vert, START_ROOK_BIG
        x_rook_end, y_rook_end = start_vert, END_ROOK_BIG
    change_pos(position, x, y, x1, y1, 0, 6 * (colour + 1)) 
    position.change_coords(KING, 0, colour, x1, y1)
    change_pos(position, x_rook_start, y_rook_start, x_rook_end, y_rook_end, 0, ROOK + 6 * colour)
    if (x_rook_start, y_rook_start == position.return_coords(ROOK, 0, colour)):
        position.change_coords(ROOK, 0, colour, x_rook_end, y_rook_end) 
    else:
        position.change_coords(ROOK, 1, colour, x_rook_end, y_rook_end) 
            
    
def castle_reverse(position, length, colour):
    start_vert = colour * 7
    x, y = start_vert, START_KING
    x1, y1 = start_vert, START_KING - length
    if length == 2:
        x_rook_start, y_rook_start = start_vert, START_ROOK_SHORT
        x_rook_end, y_rook_end = start_vert, END_ROOK_SHORT
    else:
        x_rook_start, y_rook_start = start_vert, START_ROOK_BIG
        x_rook_end, y_rook_end = start_vert, END_ROOK_BIG
    change_pos(position, x, y, x1, y1, 0, 6 * (colour + 1)) 
    position.change_coords(KING, 0 , colour, x, y)
    change_pos(position, x_rook_end, y_rook_end, x_rook_start, y_rook_start, 0, 6 * (colour + 1)) 
    if (x_rook_start, y_rook_start == position.return_coords(ROOK, 0, colour)):
        position.change_coords(ROOK, 0, colour, x_rook_end, y_rook_end) 
    else:
        position.change_coords(ROOK, 1, colour, x_rook_end, y_rook_end)  
        
def move_to_queen(position, x_start, y_start, x, y, colour, length, castling_list):
    for figure in FIGURES:
        delete = False
        change_pos(position, x_start, y_start, x, y, 0, figure)
        position.remove_figure(colour, PAWN - 1, x_start, y_start)
        position.plus_figure(colour, figure - 1, x, y)
        for figures in position.enemy:
            if [x, y] in figures:
                delete = True
                delete_figures = figures
                number_delete = position.enemy.index(figures)
                figures.remove([x, y]) 
        mate = False
        if make_move(position, 1 - colour, length - 1, castling_list):
            mate = True
        change_pos(position, x_start, y_start, x, y, PAWN, 0)
        position.remove_figure(colour, figure - 1, x, y)
        position.current[PAWN - 1] += [[x_start, y_start]]  
        if delete:
            delete_figures += [[x, y]]
            position.enemy[number_delete] = delete_figures         
        if mate:
            return True, figure
    return False, None   
        
def return_position(position, x, y, x1, y1, number_cell, number_end, number_cell_in_list, change_number, colour, delete, delete_figures, number_delete):
    change_pos(position, x, y, x1, y1, number_cell, number_end)
    position.change_coords(number_cell_in_list, change_number, colour, x, y)
    if delete:
        delete_figures += [[x1, y1]]
        position.enemy[number_delete] = delete_figures    
    
    

def make_move(position, colour, length, castling_list=[False, False, False, False], passant=False):
    list_moves, checks = legal_moves(position, colour, castling_list, passant)
    if len(list_moves) == 0 and checks > 0:
        return True
    elif not length:
        return False
    if colour == WHITE:
        position.current = position.white
        position.enemy = position.black
    else:
        position.current = position.black
        position.enemy = position.white    
    for move in list_moves:
        delete_figures = []
        number_delete = 0
        if move != ["0-0"] and move != ["0-0-0"]:
            x, y, x1, y1 = move[0], move[1], move[2], move[3]
            move_pawn_to_queen = False
            if (position.data[x][y] == PAWN and x1 == 7) or (position.data[x][y] == PAWN_BLACK and x1 == 7):
                move_pawn_to_queen = True
        if move != ["0-0"] and move != ["0-0-0"] and move_pawn_to_queen == False:
            passant = False
            if position.data[x][y] == PAWN and x1 - x == 2:
                passant = [x1 - 1, y1]     
            number_cell = position.data[x][y] 
            number_cell_in_list = number_cell % 6
            number_end = position.data[x1][y1]
            change_pos(position, x, y, x1, y1, 0, number_cell)
            for i in range(len(position.current[number_cell_in_list - 1])):
                if position.current[number_cell_in_list - 1][i] == [x, y]:
                    change_number = i
                    position.change_coords(number_cell_in_list, i, colour, x1, y1)
                    delete = False
                    if number_end > 0:
                        for figures in position.enemy:
                            if [x1, y1] in figures:
                                delete = True
                                delete_figures = figures
                                number_delete = position.enemy.index(figures)
                                figures.remove([x1, y1])     
                    break
        elif move_pawn_to_queen:
            mate, figure = move_to_queen(position, x, y, x1, y1, colour, length, castling_list)
            if mate:
                return [figure, y, None, y1]
            continue
        elif move == ["0-0"]:
            castle_move(position, SHORT, colour)
        else:
            castle_move(position, BIG, colour)   
        answer = make_move(position, 1 - colour, length - 1, castling_list, passant)
        if length == 3:
            if answer:
                return_position(position, x, y, x1, y1, number_cell, number_end, number_cell_in_list, change_number, colour, delete, delete_figures, number_delete) 
                if move != ["0-0"] and move != ["0-0-0"]:    
                    return [x, y, x1, y1]
                elif move == ["0-0"]:
                    return [ANSWER_CASTLE_SHORT, ANSWER_CASTLE_SHORT, ANSWER_CASTLE_SHORT, ANSWER_CASTLE_SHORT]
                else:
                    return [ANSWER_CASTLE_BIG, ANSWER_CASTLE_BIG, ANSWER_CASTLE_BIG, ANSWER_CASTLE_BIG]
            if move != ["0-0"] and move != ["0-0-0"]:
                return_position(position, x, y, x1, y1, number_cell, number_end, number_cell_in_list, change_number, colour, delete, delete_figures, number_delete)
            elif move == ["0-0"]:
                castle_reverse(position, SHORT, colour)
            else:
                castle_reverse(position, BIG, colour)
        elif colour == WHITE and answer:
            return_position(position, x, y, x1, y1, number_cell, number_end, number_cell_in_list, change_number, colour, delete, delete_figures, number_delete) 
            return True
        elif colour == WHITE:
            return_position(position, x, y, x1, y1, number_cell, number_end, number_cell_in_list, change_number, colour, delete, delete_figures, number_delete)
        elif colour == BLACK and not answer:
            return_position(position, x, y, x1, y1, number_cell, number_end, number_cell_in_list, change_number, colour, delete, delete_figures, number_delete) 
            return False
        else:
            return_position(position, x, y, x1, y1, number_cell, number_end, number_cell_in_list, change_number, colour, delete, delete_figures, number_delete) 
    if colour == WHITE and length != 3:
        return_position(position, x, y, x1, y1, number_cell, number_end, number_cell_in_list, change_number, colour, delete, delete_figures, number_delete) 
        return False
    elif colour == WHITE:
        return [-1, -1, -1, -1]
    else:
        return_position(position, x, y, x1, y1, number_cell, number_end, number_cell_in_list, change_number, colour, delete, delete_figures, number_delete) 
        return True
       
            
            
    
    
    

        
      
        