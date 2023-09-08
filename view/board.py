import pygame
from controller.game import GameController
from models.pieces.piece import Piece
from view.piece import PieceView
from pygame.rect import Rect

class WinnerView:
    FONT = "Ariel"
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_alpha(200)
        self.surface.fill((0,0,0))
        self.font = pygame.font.SysFont(self.FONT, 120)
        

    def draw(self, screen, white):
        screen.blit(self.surface,(0,0))
        text = "draw!"
        if white is not None:
            text = "%s wins" % ("white" if white != True else "black")
        
        rendered = self.font.render(text, False, (255,255,255))
        
        
        screen.blit(rendered, (self.width//2 - rendered.get_width()//2, self.height//2 - rendered.get_height()//2))
    
    def update(self, screen, game: GameController):
        if game.is_paused():
            return
        board = game.board
        finished, checked = board.is_finished(), board.checked()
        if finished:
            self.draw(screen, checked)

class BoardView:
    WHITE = (200, 200, 200)
    BLACK = (50, 50, 50)
    
    def __init__(self, width, height) -> None:
        self.square_size = min(width,height)//8
        self.highlighted = []
        self.pvs = {}
        self.winner_view = WinnerView(width, height)

    def draw_background(self, screen,):
        for row in range(8):
            for col in range(8):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                pygame.draw.rect(screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))
    
    def add_piece(self, piece: Piece):
        return PieceView.from_piece(piece, self.square_size)
    
    def screen_to_game(self, pos):
        return pos[0]//self.square_size, pos[1]//self.square_size
    
    def highlight(self, screen, squares):
        for square in squares:
            row, col = square
            pygame.draw.rect(screen, (0,200,0), (row * self.square_size, col * self.square_size, self.square_size, self.square_size), 4)
    
    def move_pieces(self, screen, pieces: list[Piece]):
        for p in pieces:
            if p not in self.pvs:
                self.pvs[p] = self.add_piece(p)
            pv = self.pvs[p]
            pv.move(screen, p.x * self.square_size, p.y * self.square_size)
    
    def update(self, screen, game: GameController):
        board = game.board
        self.draw_background(screen)
        self.move_pieces(screen, board.get_pieces())
        self.highlight(screen, board.get_valid_moves())
        self.winner_view.update(screen, game)
    