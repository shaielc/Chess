from models.AI.greedy import GreedyAI
from models.board import Board
from models.pieces.bishop import Bishop
from models.pieces.knight import Knight
from models.pieces.pawn import Pawn
from models.pieces.king import King


# NOT REALLY A TEST USEFULL FOR DEBUGGING.
def test_pawn_defense():
    board = Board([Bishop(1,4,False), Knight(4,4,False), Pawn(2,6,True), Pawn(1,6,True), King(4,7,True), King(4,0,False)])
    ai = GreedyAI(True)
    ai.calc_move(board)
    event = ai.get_event()