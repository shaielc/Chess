from models.AI.greedy import GreedyAI, Threats
from models.pieces.king import King
from models.pieces.knight import Knight
from models.pieces.queen import Queen
from models.pieces.piece import PiecesContainer
from models.pieces.bishop import Bishop
from models.pieces.pawn import Pawn
from models.board import Board
from models.pieces.rook import Rook

def test_cornered_king():
    king = King(7,0,False)
    queen = Queen(6, 2)
    board = PiecesContainer([queen, king])
    threats = queen.threatning(board)
    freedom = GreedyAI.king_freedom(king, threats, board)
    assert(freedom == 1)

def test_position_1():
    king = King(5,2, white=False)
    board = Board([Queen(4,0), Queen(2,1), Bishop(4,4), Pawn(5,4), king])
    ai = GreedyAI(True)
    threats = Threats(ai.get_pressure(board))
    freedom = ai.king_freedom(king, threats, board.pieces)
    assert(freedom == 1)

def test_position_2():
    king = King(6,6, white=False)
    board = Board([Queen(3,1), Bishop(3,2), King(4,7), Rook(5,7), Pawn(7,6), king])
    ai = GreedyAI(True)
    threats = Threats(ai.get_pressure(board))
    freedom = ai.king_freedom(king, threats, board.pieces)
    assert(freedom == 1)

def test_king_blocked_by_own():
    king = King(6,0, white=False)
    board = Board([Queen(5,1), Pawn(4,2), Pawn(7,0, white=False), king])
    ai = GreedyAI(True)
    threats = Threats(ai.get_pressure(board))
    freedom = ai.king_freedom(king, threats, board.pieces)
    assert(freedom == 0)
    assert(board.check_for_endgame(False))

def test_position_3():
    king = King(3,7)
    board = Board([Queen(4,5,), Rook(0,0), Knight(3,5,white=False)])
    ai = GreedyAI(False)
    threats = Threats(ai.get_pressure(board))
    freedom = ai.king_freedom(king, threats, board.pieces)
    assert(freedom == 4)

def test_position_4():
    king = King(3,7)
    board = Board([Queen(4,5,), Rook(0,0), Knight(1,6,white=False)])
    ai = GreedyAI(False)
    threats = Threats(ai.get_pressure(board))
    freedom = ai.king_freedom(king, threats, board.pieces)
    assert(freedom == 5)
