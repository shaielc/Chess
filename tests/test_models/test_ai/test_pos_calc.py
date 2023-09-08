from models.AI.greedy import GreedyAI
from models.pieces.rook import Rook

def test_position_diff_y():
    a = GreedyAI(True).position_score(0,0, Rook.TYPE)
    b = GreedyAI(True).position_score(0,1, Rook.TYPE)
    assert( a < b)