from controller.board import BoardController
from controller.history import HistoryController
from models.AI.greedy import GreedyAI
from models.AI.random import RandomAI
from models.events import Event, EventType, EventSourceType
from time_func import timeit
from models.player import Player, PlayerType



class GameController:
    def __init__(self, board: BoardController, players: dict[bool, PlayerType]) -> None:
        self.board = board
        self.white = True
        self.players = {k: self.init_player(k, player) for k,player in players.items()}
        self.events = []
        self.history = HistoryController(board.model)
        self.paused = False
    
    def init_player(self, white, player_type: PlayerType):
        if player_type == PlayerType.HUMAN:
            return Player()
        elif player_type == PlayerType.AI:
            return GreedyAI(white=white) if white else GreedyAI(white=white)
    
    @property
    def current_player(self,):
        return self.players[self.white]
    
    @current_player.setter
    def current_player(self, white):
        self.white = white
        if self.current_player.TYPE == PlayerType.AI:
            self.current_player.set_turn()
    
    def toggle_pause(self,):
        self.paused = not self.paused
    
    def is_paused(self,):
        return self.paused

    # @timeit
    def handle_event(self, event):
        if event.event_type == EventType.PAUSE:
            self.toggle_pause()
            if not self.paused:
                self.history.resume()
            return
        
        if self.is_paused():
            return self.history.handle_event(event,)

        if self.current_player.TYPE.value != event.source.value:
            return
        
        turn = self.board.handle_event(event, white=self.white)
        
        if turn:
            self.current_player = not self.white

        return turn

    def add_event(self, event: Event):
        self.events.append(event)

    def handle_next(self,):
        event = None
        if len(self.events) > 0:
            event = self.events.pop()
        if event is None and self.current_player.TYPE == PlayerType.AI:
            if self.current_player.is_done():
                event = self.current_player.get_event()
        turn = False
        if event is not None:
            turn = self.handle_event(event)
        if self.paused:
            return
        if self.board.is_finished():
            return
        if self.current_player.TYPE == PlayerType.AI:
            if not self.current_player.started:
                self.current_player.handle_calc_event(self.board.model)
            elif not self.current_player.is_done():
                return
            elif event is not None and event.source == EventSourceType.AI and not turn:
                self.current_player.set_turn()
        