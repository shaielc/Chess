import pytest
from models.board import Board
from models.pieces.king import King
from models.pieces.pawn import Pawn

def test_white_pawn_move():
    king = King(8,8)
    piece = Pawn(0,6)
    board = Board([piece])
    board.move(piece,(0,5))