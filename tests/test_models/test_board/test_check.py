from models.board import Board
from models.pieces.bishop import Bishop
from models.pieces.king import King
from models.pieces.knight import Knight
from models.pieces.pawn import Pawn
from models.pieces.queen import Queen
from models.pieces.rook import Rook

def test_check():
    k = King(7,4,white=False)
    board = Board([King(0,4,white=True), Queen(1,4,white=True), k])
    checks = board.check_for_check()
    assert(len(checks) == 1)
    assert(k in checks)
    assert(board.check_for_endgame(False) == False)
    assert(board.check_for_endgame(True) == False)


def test_checkmate_queen():
    k = King(7,7,white=False)
    board = Board([King(5,5,white=True), Queen(6,6,white=True), k])
    checks = board.check_for_check()
    assert(len(checks) == 1)
    assert(k in checks)
    assert(board.check_for_endgame(False) == True)

def test_checkmate_queen_def():
    k = King(7,7,white=False)
    board = Board([Queen(5,5,white=True), Queen(6,6,white=True), k])
    checks = board.check_for_check()
    assert(len(checks) == 1)
    assert(k in checks)
    assert(board.check_for_endgame(False) == True)

def test_checkmate_pawn_def():
    k = King(0,0,white=False)
    board = Board([Pawn(2,2,white=True), Queen(1,1,white=True), k])
    checks = board.check_for_check()
    assert(len(checks) == 1)
    assert(k in checks)
    assert(board.check_for_endgame(False) == True)

def test_checkmate_pawn_threat():
    k = King(0,0,white=False)
    board = Board([Pawn(1,1,white=True), Queen(2,1,white=True), King(1,2,white=True), k])
    checks = board.check_for_check()
    assert(len(checks) == 1)
    assert(k in checks)
    assert(board.check_for_endgame(False) == True)

def test_checkmate_bishop_def():
    k = King(0,0,white=False)
    board = Board([Bishop(2,2,white=True), Queen(1,1,white=True), k])
    checks = board.check_for_check()
    assert(len(checks) == 1)
    assert(k in checks)
    assert(board.check_for_endgame(False) == True)


def test_checkmate_bishop_threat():
    k = King(0,0,white=False)
    board = Board([Bishop(2,2,white=True), Queen(2,1,white=True), k])
    checks = board.check_for_check()
    assert(len(checks) == 1)
    assert(k in checks)
    assert(board.check_for_endgame(False) == True)


def test_checkmate_rook_def():
    k = King(0,0,white=False)
    board = Board([Rook(1,2,white=True), Queen(1,1,white=True), k])
    checks = board.check_for_check()
    assert(len(checks) == 1)
    assert(k in checks)
    assert(board.check_for_endgame(False) == True)

def test_checkmate_rook_threat():
    k = King(0,0,white=False)
    board = Board([Rook(0,2,white=True), Queen(2,1,white=True), k])
    checks = board.check_for_check()
    assert(len(checks) == 1)
    assert(k in checks)
    assert(board.check_for_endgame(False) == True)

def test_checkmate_knight_def():
    k = King(0,0,white=False)
    board = Board([Knight(2,3,white=True), Queen(1,1,white=True), k])
    checks = board.check_for_check()
    assert(len(checks) == 1)
    assert(k in checks)
    assert(board.check_for_endgame(False) == True)

def test_checkmate_knight_threat():
    k = King(0,0,white=False)
    board = Board([Knight(1,2,white=True), Queen(2,1,white=True), k])
    checks = board.check_for_check()
    assert(len(checks) == 1)
    assert(k in checks)
    assert(board.check_for_endgame(False) == True)

def test_stalemate():
    k = King(7,7,white=False)
    board = Board([King(5,5,white=True), Queen(5,6,white=True), k])
    checks = board.check_for_check()
    assert(len(checks) == 0)
    assert(board.check_for_endgame(False) == True)

def test_two_kings_stalemate():
    board = Board([King(5,5,white=True), King(7,7,white=False)])
    checks = board.check_for_check()
    assert(len(checks) == 0)
    assert(board.check_for_endgame(False) == True)