from controller.game import GameController
from controller.board import BoardController
from models.board import Board
from models.pieces.pawn import Pawn


def test_human_player_select():
    board = Board([Pawn(0,5)])
    GameController(BoardController(board), )