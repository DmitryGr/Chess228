class Create_position:
    def __init__(self, data):
        line_white = [[], [], [], [], [], []]
        all_white = []
        all_black = []
        line_black = [[], [], [], [], [], []]
        for i in range(8):
            for j in range(8):
                if data[i][j] > 6:
                    line_black[data[i][j] - 7] += [i * 8 + j]
                    all_black += [i * 8 + j]
                elif data[i][j] != 0:
                    line_white[data[i][j] - 7] += [i * 8 + j]
                    all_white += [i * 8 + j]
        self.data = data
        self.allw = all_white
        self.allb = all_black
        self.white = line_white
        self.black = line_black
        
def inspection_check(position):
    number_of_checks = 0
    list_bunch = []
    candidates = []
    candidates_len = []
    position_king = position.white[5][0]
    if position_king % 8 != 0 and position_king - 9 in position.black[0]:
        number_of_checks += 1
    if position_king % 8 != 7 and position_king - 7 in position.black[0]:
        number_of_checks += 1
    for i in range(len(position.black[1])):
        number = position.black[1][i]
        diff1 = abs(position.black[1][i] % 8 - position_king % 8)
        diff2 = abs(position.black[1][i] // 8 - position_king // 8)
        if abs(diff1 - diff2) == 1 and diff1 + diff2 == 3:
            number_of_checks += 1
    for i in range(len(position.black[2])):
        if abs(position.black[2][i] % 8 - position_king % 8) == abs(position.black[2][i] // 8 - position_king // 8):
            candidates += [position.black[2][i]]
            candidates_len += [abs(position.black[2][i] % 8 - position_king % 8)]
    for i in range(len(position.black[3])):
        if position.black[3][i] % 8 == position_king % 8 or position.black[3][i] // 8 == position_king // 8:
            candidates += [position.black[3][i]]
            candidates_len += [max(abs(position.black[3][i] % 8 - position_king % 8), abs(position.black[3][i] // 8 - position_king // 8))]
    if len(position.black[4]) > 0:        
        if position.black[4][0] % 8 == position_king % 8 or position.black[4][0] // 8 == position_king // 8 or abs(position.black[4][0] % 8 - position_king % 8) == abs(position.black[4][0] // 8 - position_king // 8):
            candidates += [position.black[4][0]]
            candidates_len += [max(abs(position.black[4][0] % 8 - position_king % 8), abs(position.black[4][0] // 8 - position_king // 8))] 
    if candidates_len == 0:
        return number_of_checks, []
    else:
        for i in range(len(candidates)):
            counter = 0
            print(candidates_len)
            number = min(candidates[i], position_king)
            for j in range(candidates_len[i] - 1):
                if number + (j + 1) * (abs(candidates[i] - position_king) // candidates_len[i]) in position.allw:
                    counter += 1
                    cand_bunch = number + (j + 1) * (abs(candidates[i] - position_king) // candidates_len[i])
            if counter == 1:
                list_bunch += [cand_bunch]
            elif counter == 0:
                number_of_checks += 1
        return number_of_checks, list_bunch

            
            
        
        
        
def data_legal_moves(position):
    print(inspection_check(position))
    
    
        
    
        
    
        

def main():
    data = []
    for i in range(8):
        data += [list(map(int, input().split()))]
    data = data[::-1]    
    print(data)
    start_position = Create_position(data)
    data_legal_moves(start_position)
    
    



main()   