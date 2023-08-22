from controller.game import GameController
from models.player import PlayerType
from controller.board import BoardController
from models.board import Board
from models.pieces.pawn import Pawn
from models.events import Event, EventSourceType, EventType


def test_human_player_move():
    board = Board([Pawn(0,5)])
    controller = GameController(BoardController(board), {True: PlayerType.HUMAN, False: PlayerType.AI})
    assert(controller.white)
    out = controller.handle_event(Event(EventType.BOARD, EventSourceType.UI, (0,5)))
    out = controller.handle_event(Event(EventType.BOARD, EventSourceType.UI, (0,4)))
    assert(not controller.white)

def test_human_player_move():
    board = Board([Pawn(0,5)])
    controller = GameController(BoardController(board), {False: PlayerType.HUMAN, True: PlayerType.AI})
    assert(controller.white)
    out = controller.handle_event(Event(EventType.BOARD, EventSourceType.UI, (0,5)))
    assert(out is None)
    out = controller.handle_event(Event(EventType.BOARD, EventSourceType.UI, (0,4)))
    assert(out is None)