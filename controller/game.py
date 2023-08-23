from controller.board import BoardController
from models.AI.random import RandomAI
from models.events import Event, EventType
from time_func import timeit
from models.player import Player, PlayerType



class GameController:
    def __init__(self, board: BoardController, players: dict[bool, PlayerType]) -> None:
        self.board = board
        self.white = True
        self.players = {k: self.init_player(k, player) for k,player in players.items()}
        self.events = []
    
    def init_player(self, white, player_type: PlayerType):
        if player_type == PlayerType.HUMAN:
            return Player()
        elif player_type == PlayerType.AI:
            return RandomAI(white=white)
    
    @property
    def current_player(self,):
        return self.players[self.white]
    
    @current_player.setter
    def current_player(self, white):
        self.white = white
        if self.current_player.TYPE == PlayerType.AI:
            self.current_player.set_turn()

    @timeit
    def handle_event(self, event):
        if self.current_player.TYPE.value != event.source.value:
            return
        if event.event_type == EventType.BOARD:
            pos = event.payload
            turn = self.board.handle_location_event(pos, self.white)
            
        elif event.event_type == EventType.PROMOTION:
            piece = event.payload
            turn = self.board.promote(piece)
        
        elif event.event_type == EventType.MOVE:
            turn = self.board.handle_move_event(*event.payload, white=self.white)
        
        if turn:
            self.current_player = not self.white

        return turn

    def add_event(self, event: Event):
        self.events.append(event)

    def handle_next(self,):
        if self.board.is_finished()[0]:
            return
        if self.current_player.TYPE == PlayerType.HUMAN:
            if len(self.events) > 0:
                self.handle_event(self.events.pop())
        elif self.current_player.TYPE == PlayerType.AI:
            if self.current_player.is_done():
                if not self.handle_event(self.current_player.get_event()):
                    self.current_player.set_turn()
            elif not self.current_player.started:
                self.current_player.handle_calc_event(self.board.model)
        