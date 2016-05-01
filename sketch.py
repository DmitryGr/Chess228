def inspect_line(x, y, vector, figures, max_steps=7):
    ''' Start from x, y
    Go step-by-step: x += vector[0], y += vector[1]
    while cell is free. Go no more than max_steps steps.
    Stop if figure is found. Check, if it is in the list.
    
    Return: 
          None            if nothing found or the figure is not in the list
                          or the figure is same color as in the cell (x, y)
          
          (x, y, figure)  otherwise
    '''
    
    for i in range(1, max_steps + 1):
        if data[x + i * dx][y + i * dy]...
           return ...
       
    return None


def inspect_check(position):
    
    x_king, y_king = ...
    for vector in [(0,1), (1,0), (0,-1), (-1,0)]:
        res += [inspect_line(x_king, y_king, vector, [ROOK, QUEEN])]
    for vector in [(0,1), (1,0), (0,-1), (-1,0)]:
        res += [inspect_line(x_king, y_king, vector, [ROOK, QUEEN])]
    for vector in [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]:
        res += [inspect_line(x_king, y_king, vector, [kNIGHT], 1)]
    for vector in [(1,1), (-1,1)]:
        res += [inspect_line(x_king, y_king, vector, [PAWN], 1)]
    
