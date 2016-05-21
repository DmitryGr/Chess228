import unittest
from move import *
from fen import fen_format
from stuff import read_position

class Tests_all_moves_on_line(unittest.TestCase):
    def test_upper(self):
        data = ["4k3/8/8/8/8/5Q2/8/4K3 w"]
        for i in range(len(data)):
            position = read_position(fen_format(data[i]))
            print(position)
            self.assertEqual(all_moves_on_line(position, (1, -1), 2, 5, False, [], 0), [[3, 4], [4, 3], [5, 2], [6, 1], [7, 0]])
        
   
    