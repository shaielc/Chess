from models.board import Board
from models.pieces.pawn import Pawn
from models.pieces.queen import Queen
from models.pieces.piece import PieceTypes

def test_promotion():
    pawn = Pawn(0,1)
    board = Board([pawn])
    board.move(pawn, (0,0)) # NOTE: inidication of bad design
    board.promote(Queen(0,0))
    assert(board.pieces.locations[0,0].TYPE == PieceTypes.QUEEN)

def test_no_promotion():
    pawn = Pawn(0,2)
    board = Board([pawn])
    board.move(pawn, (0,1)) # NOTE: inidication of bad design
    board.promote(Queen(0,0))
    assert(board.pieces.locations.get((0,0)) is None)

def test_no_moves_while_promoting():
    pawn = Pawn(0,1)
    pawn2 = Pawn(0,2)
    pawn3 = Pawn(0,3,white=False)
    board = Board([pawn, pawn2, pawn3])
    board.move(pawn, (0,0)) # NOTE: inidication of bad design
    assert(not board.move(pawn2, (0,1)))
    assert(not board.move(pawn3, (0,4)))
    board.promote(Queen(0,0))
    assert(board.move(pawn2, (0,1)))
    assert(board.move(pawn3, (0,4)))

    