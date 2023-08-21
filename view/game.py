from models.events import Event, EventSourceType, EventType
from view.board import BoardView
from controller.board import BoardController
from view.histoty import HistoryView
from view.promotion import PromotionView



class GameView:
    def __init__(self, board: BoardView, promotion: PromotionView, history: HistoryView) -> None:
        self.board = board
        self.promotion = promotion
        self.history_view = history
    
    def update(self, screen, board: BoardController):
        self.board.update(screen,board)
        self.promotion.update(screen, board.check_promotion())
        self.history_view.update(screen, board)

    def screen_to_board(self, pos):
        x,y = self.board.screen_to_game(pos)
        if x >= 0 and y >=0 and x < 8 and y<8:
            return x, y
        return None
    
    def screen_to_promotion(self, pos):
        if pos not in self.promotion:
            return None
        return self.promotion.screen_to_game(pos)
    
    def handle_click(self, click_pos):
        pos = self.screen_to_board(click_pos)
        if pos is not None:
            return Event(EventType.BOARD, EventSourceType.UI, pos)
        piece = self.screen_to_promotion(click_pos)
        if piece is not None:
            return Event(EventType.PROMOTION, EventSourceType.UI, piece)
