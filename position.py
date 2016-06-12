from constants import *

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
        if colour == BLACK:
            return self.data[x][y] > colour * 6
        else:
            return (self.data[x][y] > 0 and self.data[x][y] < 7)

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
        
    def remove_figure(self, colour, figure, x, y):
        if colour == WHITE:
            self.white[figure - 1].remove([x, y])
        else:
            self.black[figure - 1].remove([x, y])
            
    def plus_figure(self, colour, figure, x, y):
        if colour == WHITE:
            self.white[figure - 1] += [[x, y]]
        else:
            self.black[figure - 1] += [[x, y]]