import unittest
from move import *
from fen import fen_format
from stuff import read_position

class TestsAllMovesOnLine(unittest.TestCase):
    def test_upper(self):
        data = ["4k3/8/8/8/8/5Q2/8/4K3 w", "5k2/8/8/8/8/8/8/3K1N2 w", "5k2/8/8/8/6Q1/8/8/3K4 w", "5k2/8/8/8/8/5P2/8/3K4 w", "5k2/8/8/8/4p3/5P2/8/3K4 w", "5k2/8/8/4r3/8/2Q5/8/3K4 w", "5k2/6r1/8/4Q3/8/8/8/4K3 b"]
        data_questions = [[(1, -1), 2, 5, False, [], 0], [(2, -1), 0, 5, False, [], 0, 1], [(0, -1), 3, 5, False, [], 0], [(1, 0), 2, 5, False, [], 0, 1], [(1, -1), 2, 5, False, [], 0, 1, True], [(1, 1), 2, 2, False, [], 0], [(-1, 0), 6, 6, False, [], 1]]
        data_answers = [[[2, 5, 3, 4], [2, 5, 4, 3], [2, 5, 5, 2], [2, 5, 6, 1], [2, 5, 7, 0]], [[0, 5, 2, 4]], [[3, 5, 3, 4], [3, 5, 3, 3], [3, 5, 3, 2], [3, 5, 3, 1], [3, 5, 3, 0]], [[2, 5, 3, 5]], [[2, 5, 3, 4]], [[2, 2, 3, 3], [2, 2, 4, 4]], [[6, 6, 5, 6], [6, 6, 5, 4], [6, 6, 5, 3], [6, 6, 5, 2], [6, 6, 5, 1], [6, 6, 5, 0]]]
        for i in range(len(data)):  
            position = read_position(fen_format(data[i])[0])
            question = all_moves_on_line(position, *data_questions[i])
            self.assertEqual(question, data_answers[i])
            
if __name__ == '__main__':
    unittest.main()            
        
   
    