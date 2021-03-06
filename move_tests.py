import unittest
from move import *
from fen import fen_format
from stuff import read_position

class TestsAllMovesOnLine(unittest.TestCase):
    def test(self):
        data = ["4k3/8/8/8/8/5Q2/8/4K3 w", "5k2/8/8/8/8/8/8/3K1N2 w", "5k2/8/8/8/6Q1/8/8/3K4 w", "5k2/8/8/8/8/5P2/8/3K4 w", "5k2/8/8/8/4p3/5P2/8/3K4 w", "5k2/8/8/4r3/8/2Q5/8/3K4 w", "5k2/6r1/8/4Q3/8/8/8/4K3 b", "4k3/4r3/4Q3/8/8/8/8/4K3 b", "5k2/8/8/8/7n/7P/8/2K5 w", "4k3/8/8/8/6bn/7P/8/4K3 w", "2R5/5pkp/6p1/6PN/8/8/6K1/8", "r3r3/4bN1k/2pqp3/pp1n3p/3P3P/2PQ1N2/1n1B1P2/2K3R1 w", "rnb2bkr/pppp3p/3P3B/4p3/2BP4/4KP2/PPP3q1/RN6 b"]
        data_questions = [[(1, -1), 2, 5, False, [], 0], [(2, -1), 0, 5, False, [], 0, 1], [(0, -1), 3, 5, False, [], 0], [(1, 0), 2, 5, False, [], 0, 1], [(1, -1), 2, 5, False, [], 0, 1, True], [(1, 1), 2, 2, False, [], 0], [(-1, 0), 6, 6, False, [], 1], [(-1, 0), 6, 4, False, [], 1], [(1, 0), 2, 7, False, [], 0, 1, True], [(1, -1), 2, 7, False, [], 0, 1, True], [(-1, 1), 5, 6, True, [[4, 7]], 1, 1, True], [(-1, 1), 5, 4, True, [[2, 3], [3, 4], [4, 5], [5, 6]], 1, 1, True], [(1, -1), 1, 6, True, [[3, 2], [4, 3], [5, 4], [6, 5]], 1]]
        data_answers = [[[2, 5, 3, 4], [2, 5, 4, 3], [2, 5, 5, 2], [2, 5, 6, 1], [2, 5, 7, 0]], [[0, 5, 2, 4]], [[3, 5, 3, 4], [3, 5, 3, 3], [3, 5, 3, 2], [3, 5, 3, 1], [3, 5, 3, 0]], [[2, 5, 3, 5]], [[2, 5, 3, 4]], [[2, 2, 3, 3], [2, 2, 4, 4]], [[6, 6, 5, 6], [6, 6, 4, 6], [6, 6, 3, 6], [6, 6, 2, 6], [6, 6, 1, 6], [6, 6, 0, 6]], [[6, 4, 5, 4]], [], [[2, 7, 3, 6]], [[5, 6, 4, 7]], [], []]
        for i in range(len(data)):  
            position = read_position(fen_format(data[i])[0])
            question = all_moves_on_line(position, *data_questions[i])
            self.assertEqual(question, data_answers[i])
            
class TestsCheckBunchLine(unittest.TestCase):
    def test(self):
        data = ["5k2/8/6q1/8/8/8/6N1/2K5 w", "5k2/8/7q/8/8/8/6N1/2K5 w", "5k2/8/7q/6N1/8/8/8/2K5 w", "5k2/8/8/8/3N4/3n4/8/2K5 w", "5k2/4q3/8/2B5/8/8/8/2K5 b", "8/8/5k2/4P3/8/8/8/2K5 b", "1r6/kP5Q/8/8/8/8/8/K7 b", "1R4k1/5pn1/8/8/2B5/6R1/8/4K3 b"]
        data_questions = [[(1, 1), 0, 2, [BISHOP, QUEEN], 0], [(1, 1), 0, 2, [BISHOP, QUEEN], 0], [(1, 1), 0, 2, [BISHOP, QUEEN], 0], [(2, 1), 0, 2, [KNIGHT], 0, 1], [(-1, -1), 7, 5, [BISHOP, QUEEN], 1], [(-1, -1), 5, 5, [PAWN], 1, 1], [(0, 1), 6, 0, [ROOK, QUEEN], 1], [(-1, -1), 7, 6, [BISHOP, QUEEN], 1]]
        data_answers = [(0, [], []), (1, [], [[1, 3], [2, 4], [3, 5], [4, 6], [5, 7]]), (0, [[4, 6]], []), (1, [], [[2, 3]]), (0, [[6, 4]], []), (1, [], [[4, 4]]), (0, [], []), (0, [[6, 5]], [])]
        for i in range(len(data)):  
            position = read_position(fen_format(data[i])[0])
            question = check_bunch_of_the_line(position, *data_questions[i])
            self.assertEqual(question, data_answers[i])    
    
class TestInspectCheck(unittest.TestCase):
    def test(self):
        data = ["8/5q2/8/8/8/8/8/4K3 w", "8/8/3q1r2/8/6n1/4p3/2b3r1/4K3 w", "8/8/5r2/4q3/6n1/8/2b3r1/4K3 w", "8/8/5r2/8/6n1/8/2b2pr1/4K3 w", "8/8/5r2/8/4r3/8/5b2/4K3 w", "8/8/8/8/4q3/8/8/4K3 w", "8/8/8/8/4q3/8/4N3/4K3 w", "6k1/8/8/8/1b2q3/8/3PN3/4KB1r w", "6k1/8/8/8/1b2q3/8/3PN3/r3KB1r w", "6k1/8/8/8/8/3n4/8/4K3 w", "6k1/8/8/b7/8/3n4/8/4K3 w", "6k1/8/5N2/8/8/8/8/4K3 b", "6k1/8/5N2/8/8/8/B7/4K3 b", "6k1/8/8/8/8/8/B7/4K3 b", "1R4k1/5pn1/8/8/2B5/6R1/8/4K3 b", "1r6/kP5Q/8/8/8/8/8/K7 b", "2R5/5pkp/6p1/6PN/8/8/6K1/8 b", "r3r3/4bN1k/2pqp3/pp1n3p/3P3P/2PQ1N2/1n1B1P2/2K3R1 w"]
        data_questions = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1], [1], [1], [1], [1], [1], [1]]
        data_answers = [(0, [], []), (0, [], []), (1, [], [[1, 4], [2, 4], [3, 4], [4, 4]]), (1, [], [[1, 5]]), (2, [], []), (1, [], [[1, 4], [2, 4], [3, 4]]), (0, [[1, 4]], []), (0, [[1, 3], [1, 4], [0, 5]], []), (1, [[1, 3], [1, 4], [0, 5]], [[0, 3], [0, 2], [0, 1], [0, 0]]), (1, [], [[2, 3]]), (2, [], []), (1, [], [[5, 5]]), (2, [], []), (1, [], [[6, 5], [5, 4], [4, 3], [3, 2], [2, 1], [1, 0]]), (1, [[6, 5], [6, 6]], [[7, 5], [7, 4], [7, 3], [7, 2], [7, 1]]), (0, [], []), (1, [], [[4, 7]]), (1, [], [[5, 6], [4, 5], [3, 4], [2, 3]])]
        for i in range(len(data)):  
            position = read_position(fen_format(data[i])[0])
            question = inspect_check(position, *data_questions[i])
            self.assertEqual(question, data_answers[i])         
    
class TestGetMove(unittest.TestCase): 
    def test(self):
        data = ["6k1/8/8/8/8/4P3/8/4K3 w", "6k1/8/8/8/8/4N3/8/4K3 w", "6k1/8/8/8/8/4Q3/8/4K3 w", "6k1/8/8/8/8/4Q3/8/4K2r w", "6k1/8/8/8/6n1/5P2/8/4K3 w", "7K/8/8/8/8/4q3/8/4k3 b", "7K/8/8/8/2R5/8/8/4k3 w", "7K/8/8/8/2r1n3/3P4/8/4k3 w", "8/8/5K2/8/4n3/3P4/8/4k3 w", "8/8/5K2/8/7n/7P/8/4k3 w", "4k3/8/8/8/6bn/7P/8/4K3 w", "4k3/8/4K3/8/8/8/R7/8 w", "r1bqr3/pppnbk1p/2p2ppB/3Q4/3P4/8/PPP1NPPP/R3K2R w", "kr6/8/1P6/8/2K1Q3/8/8/8 w", "2R5/5pkp/6p1/6PN/8/8/6K1/8 b", "r3r3/4bN1k/2pqp3/pp1n3p/3P3P/2PQ1N2/1n1B1P2/2K3R1 b", "r3r3/4bN1k/2pqp3/pp1n3p/3P3P/2PQ1N2/1n1B1P2/2K3R1 b", "rnb2bkr/pppp3p/7B/3Pp3/2BP4/4KP2/PPP3q1/RN6 w", "6k1/2q5/8/5Pp1/4K3/8/8/5K2 w"]
        data_questions = [[PAWN, 2, 4, [], 0], [KNIGHT, 2, 4, [], 0], [QUEEN, 2, 4, [], 0], [QUEEN, 2, 4, [[0, 5], [0, 6]], 0, True], [PAWN, 2, 5, [], 0], [QUEEN, 2, 4, [], 1], [ROOK, 3, 2, [], 0], [PAWN, 2, 3, [], 0], [PAWN, 2, 3, [[3, 4]], 0, True], [PAWN, 2, 7, [], 0], [PAWN, 2, 7, [], 0], [ROOK, 1, 0, [], 0], [PAWN, 5, 2, [[4, 3], [5, 4]], 1, True], [ROOK, 7, 1, [[6, 1], [5, 2], [4, 3], [3, 4]], 1, True], [PAWN, 5, 6, [[4, 7]], 1, True], [KNIGHT, 1, 1, [[2, 3], [3, 4], [4, 5], [5, 6]], 1, True], [ROOK, 7, 4, [[2, 3], [3, 4], [4, 5], [5, 6]], 1, True], [QUEEN, 1, 6, [[3, 2], [4, 3], [5, 4], [6, 5]], 1, True], [PAWN, 5, 4, [], 0, False, [6, 5]]]
        data_answers = [[[2, 4, 3, 4]], [[2, 4, 3, 2], [2, 4, 3, 6], [2, 4, 1, 6], [2, 4, 1, 2], [2, 4, 4, 5], [2, 4, 4, 3], [2, 4, 0, 5], [2, 4, 0, 3]], [[2, 4, 1, 4], [2, 4, 3, 4], [2, 4, 4, 4], [2, 4, 5, 4], [2, 4, 6, 4], [2, 4, 7, 4], [2, 4, 2, 3], [2, 4, 2, 2], [2, 4, 2, 1], [2, 4, 2, 0], [2, 4, 2, 5], [2, 4, 2, 6], [2, 4, 2, 7], [2, 4, 1, 3], [2, 4, 0, 2], [2, 4, 3, 5], [2, 4, 4, 6], [2, 4, 5, 7], [2, 4, 1, 5], [2, 4, 0, 6], [2, 4, 3, 3], [2, 4, 4, 2], [2, 4, 5, 1], [2, 4, 6, 0]], [[2, 4, 0, 6]], [[2, 5, 3, 5], [2, 5, 3, 6]], [[2, 4, 1, 4], [2, 4, 3, 4], [2, 4, 4, 4], [2, 4, 5, 4], [2, 4, 6, 4], [2, 4, 7, 4], [2, 4, 2, 3], [2, 4, 2, 2], [2, 4, 2, 1], [2, 4, 2, 0], [2, 4, 2, 5], [2, 4, 2, 6], [2, 4, 2, 7], [2, 4, 1, 3], [2, 4, 0, 2], [2, 4, 3, 5], [2, 4, 4, 6], [2, 4, 5, 7], [2, 4, 1, 5], [2, 4, 0, 6], [2, 4, 3, 3], [2, 4, 4, 2], [2, 4, 5, 1], [2, 4, 6, 0]], [[3, 2, 3, 1], [3, 2, 3, 0], [3, 2, 3, 3], [3, 2, 3, 4], [3, 2, 3, 5], [3, 2, 3, 6], [3, 2, 3, 7], [3, 2, 4, 2], [3, 2, 5, 2], [3, 2, 6, 2], [3, 2, 7, 2], [3, 2, 0, 2], [3, 2, 1, 2], [3, 2, 2, 2]], [[2, 3, 3, 2], [2, 3, 3, 4], [2, 3, 3, 3]], [[2, 3, 3, 4]], [], [[2, 7, 3, 6]], [[1, 0, 0, 0], [1, 0, 2, 0], [1, 0, 3, 0], [1, 0, 4, 0], [1, 0, 5, 0], [1, 0, 6, 0], [1, 0, 7, 0], [1, 0, 1, 1], [1, 0, 1, 2], [1, 0, 1, 3], [1, 0, 1, 4], [1, 0, 1, 5], [1, 0, 1, 6], [1, 0, 1, 7]], [[5, 2, 4, 3]], [[7, 1, 6, 1]], [[5, 6, 4, 7]], [[1, 1, 2, 3]], [], [], [[5, 4, 6, 4], [5, 4, 6, 5]]]
        for i in range(len(data)):  
            position = read_position(fen_format(data[i])[0])
            question = get_move(position, *data_questions[i])
            self.assertEqual(sorted(question), sorted(data_answers[i]))
            
class TestBunchMove(unittest.TestCase): 
    def test(self):
        data = ["5k2/8/7q/8/8/8/3P4/2K5 w", "5k2/8/7q/8/8/2r5/2RP4/2K5 w", "5k2/8/7q/8/8/2r5/2RP4/2K5 w", "5k2/8/7q/8/8/8/3B4/2K5 w", "5k2/8/2r4q/8/8/8/3B4/2K5 w", "5k2/8/8/8/8/4q3/3P4/2K5 w", "5k2/6p1/7B/5K2/8/8/7q/8 b", "7k/6p1/5B2/5K2/8/8/7q/8 b", "7k/7n/8/5K2/8/8/7Q/8 b", "7k/7r/8/5K2/8/8/7Q/8 b", "7k/8/8/5K2/3q4/8/1B6/8 b", "8/8/8/2k2K2/3q4/4B3/8/8 b", "8/8/1k6/5K2/3q4/4B3/8/8 b", "8/8/1k6/8/3q4/2B5/8/K7 w", "6k1/7q/8/5Pp1/4K3/8/8/5K2 w"]
        data_questions = [[1, 3, 0, 2, PAWN, False, [], 0, False], [1, 2, 0, 2, ROOK, False, [], 0, False], [1, 3, 0, 2, PAWN, False, [], 0, False], [1, 3, 0, 2, BISHOP, False, [], 0, False], [1, 3, 0, 2, BISHOP, True, [], 0, False], [1, 3, 0, 2, PAWN, False, [], 0, False], [6, 6, 7, 5, PAWN, False, [], 1, False], [6, 6, 7, 7, PAWN, False, [], 1, False], [6, 6, 7, 7, KNIGHT, False, [], 1, False], [6, 7, 7, 7, ROOK, False, [], 1, False], [3, 3, 7, 7, QUEEN, False, [], 1, False], [3, 3, 4, 2, QUEEN, False, [], 1, False], [3, 3, 5, 1, QUEEN, False, [], 1, False], [2, 2, 0, 0, BISHOP, False, [], 0, False], [5, 4, 4, 3, PAWN, False, [], 0, [6, 5]]]
        data_answers = [[], [[1, 2, 2, 2]], [], [[1, 3, 2, 4], [1, 3, 3, 5], [1, 3, 4, 6], [1, 3, 5, 7]], [], [[1, 3, 2, 4]], [[6, 6, 5, 7]], [[6, 6, 5, 5]], [], [[6, 7, 5, 7], [6, 7, 4, 7], [6, 7, 3, 7], [6, 7, 2, 7], [6, 7, 1, 7]], [[3, 3, 2, 2], [3, 3, 1, 1], [3, 3, 4, 4], [3, 3, 5, 5], [3, 3, 6, 6]], [[3, 3, 2, 4]], [[3, 3, 2, 4], [3, 3, 4, 2]], [[2, 2, 1, 1], [2, 2, 3, 3]], [[5, 4, 6, 5]]]
        for i in range(len(data)):  
            position = read_position(fen_format(data[i])[0])
            question = bunch_moves(position, *data_questions[i])
            self.assertEqual(sorted(question), sorted(data_answers[i]))
            
class TestKingMoves(unittest.TestCase): 
    def test(self):
        data = ["2r5/2p5/kpB5/8/R7/1K6/8/8 b", "kr6/1P5Q/8/8/8/8/8/K7 b", "kr6/8/1P6/8/2K1Q3/8/8/8 b", "2R5/5pkp/6p1/6PN/8/8/6K1/8 w"]
        data_questions = [[5, 0, 1], [7, 0, 1], [7, 0, 1], [6, 6, 1]]
        data_answers = [[], [[7, 0, 6, 0]], [], []]
        for i in range(len(data)):  
            position = read_position(fen_format(data[i])[0])
            question = king_moves(position, *data_questions[i])
            self.assertEqual(sorted(question), sorted(data_answers[i]))
            
class TestLegalMoves(unittest.TestCase): 
    def test(self):
        data = ["r3r3/4bN1k/2pqp3/pp1n3p/3P3P/2PQ1N2/1n1B1P2/2K3R1 b", "rnb2bkr/pppp3p/3P3B/4p3/2BP4/4KP2/PPP3q1/RN6 b", "8/8/7p/5K1k/6Pr/7R/8/8 b"]
        data_questions = [[1], [1], [1]]
        data_answers = [([[1, 1, 2, 3]], 1), ([], 1), ([], 1)]
        for i in range(len(data)):  
            position = read_position(fen_format(data[i])[0])
            question = legal_moves(position, *data_questions[i])
            self.assertEqual(question, data_answers[i])   
            
class TestMakeMove(unittest.TestCase): 
    def test(self):
        data = ["8/8/8/5Q2/8/4K3/8/5k2 b", "7Q/8/8/8/8/4K3/8/5k2 b"]
        data_questions = [[1, 2], [1, 2]]
        data_answers = [False, False]
        for i in range(len(data)):  
            position = read_position(fen_format(data[i])[0])
            question = make_move(position, *data_questions[i])
            self.assertEqual(question, data_answers[i])              

                        
            
if __name__ == '__main__':
    unittest.main()            
        
   
    