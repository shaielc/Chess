from models.board import Board
from models.pieces.piece import PiecesContainer
from models.pieces.king import King
from models.pieces.pawn import Pawn

def test_pawn_basic_move():
    piece = Pawn(0,5)
    moves = piece.valid_moves(PiecesContainer([])) # NOTE: indication of a problematic design
    assert(len(moves) == 1)
    assert((0,4) in moves)

    piece = Pawn(0, 4, False)
    moves = piece.valid_moves(PiecesContainer([]))
    assert(len(moves) == 1)
    assert((0,5) in moves)

def test_pawn_double_move():
    piece = Pawn(0,6)
    moves = piece.valid_moves(PiecesContainer([])) # NOTE: indication of a problematic design
    assert(len(moves) == 2)
    assert((0,4) in moves)
    assert((0,5) in moves)

    piece = Pawn(0,1,False)
    moves = piece.valid_moves(PiecesContainer([])) # NOTE: indication of a problematic design
    assert(len(moves) == 2)
    assert((0,2) in moves)
    assert((0,3) in moves)

def test_pawn_blocked_move():
    piece = Pawn(0,6)
    moves = piece.valid_moves(PiecesContainer([Pawn(0,5)])) # NOTE: indication of a problematic design
    assert(len(moves) == 0)

    moves = piece.valid_moves(PiecesContainer([Pawn(0,4)])) # NOTE: indication of a problematic design
    assert(len(moves) == 1)
    assert((0,5) in moves)

def test_pawn_threatning():
    piece = Pawn(0,5)
    moves = piece.threatning(PiecesContainer([]), exclude_empty=True)
    assert(len(moves) == 0)

    moves = piece.threatning(PiecesContainer([]), exclude_empty=False)
    assert(len(moves) == 1)
    assert((1,4) in moves)

    piece = Pawn(1,5)
    moves = piece.threatning(PiecesContainer([]), exclude_empty=False)
    assert(len(moves) == 2)
    assert((2,4) in moves)
    assert((0,4) in moves)

    piece = Pawn(1,5)
    piece_ally = Pawn(2,4)
    piece_enemy = Pawn(0,4, white=False)
    moves = piece.threatning(PiecesContainer([piece_ally, piece_enemy]), exclude_empty=True)
    assert(len(moves) == 1)
    assert((0,4) in moves)

def test_pawn_allow_en_passant():
    piece = Pawn(1,1, white=False)
    piece.move(1,3)
    assert(piece.en_passant == True)
    
    piece = Pawn(1,6)
    piece.move(1,4)
    assert(piece.en_passant == True)

    piece = Pawn(1,6)
    piece.move(1,5)
    piece.move(1,4)
    assert(piece.en_passant == False)

def test_pawn_en_passant():
    piece_enemy = Pawn(1,3, white=False)
    assert(piece_enemy.en_passant == False)
    piece = Pawn(0,3)
    moves = piece.threatning(PiecesContainer([piece_enemy]), exclude_empty=True)
    assert(len(moves) == 0)

    piece_enemy = Pawn(1,1, white=False)
    piece_enemy.move(1,3)
    piece = Pawn(0,3)
    moves = piece.threatning(PiecesContainer([piece_enemy]), exclude_empty=True)
    assert(len(moves) == 1)
    assert((1,2) in moves)

    piece = Pawn(0,4)
    moves = piece.check_en_passant(PiecesContainer([piece_enemy]))
    assert(len(moves) == 0)


def test_pawn_need_promotion():
    piece = Pawn(0,0)
    assert(piece.can_promote() == True)
    
    piece = Pawn(0,1)
    assert(piece.can_promote() == False)

    piece = Pawn(0,7,white=False)
    assert(piece.can_promote() == True)
    
    piece = Pawn(0,6,white=False)
    assert(piece.can_promote() == False)
    