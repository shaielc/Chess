from controller.game import GameController
from models.events import Event, EventSourceType, EventType
from view.board import BoardView
from controller.board import BoardController
from view.history import HistoryView
from view.promotion import PromotionView
from time_func import timeit



class GameView:
    def __init__(self, board: BoardView, promotion: PromotionView, history: HistoryView) -> None:
        self.board = board
        self.promotion = promotion
        self.history_view = history
    
    @timeit
    def update(self, screen, game: GameController):
        self.board.update(screen, game)
        self.promotion.update(screen, game.board.check_promotion())
        self.history_view.update(screen, game)

    def screen_to_board(self, pos):
        x,y = self.board.screen_to_game(pos)
        if x >= 0 and y >=0 and x < 8 and y<8:
            return x, y
        return None
    
    def screen_to_promotion(self, pos):
        return self.promotion.screen_to_game(pos)

    def screen_to_history(self, pos):
        return self.history_view.click_to_game(pos)
    
    def handle_click(self, click_pos):
        pos = self.screen_to_board(click_pos)
        if pos is not None:
            return Event(EventType.BOARD, EventSourceType.UI, pos)
        piece = self.screen_to_promotion(click_pos)
        if piece is not None:
            return Event(EventType.PROMOTION, EventSourceType.UI, piece)
        event_type = self.screen_to_history(click_pos)
        if event_type is not None:
            return Event(event_type, EventSourceType.UI)

