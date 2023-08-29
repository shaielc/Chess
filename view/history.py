from controller.board import BoardController
from models.pieces.piece import Piece
from view.piece import PieceView
import pygame

class CapturedPieces:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    
    def update(self, screen, pieces: list[Piece]):
        for i, p in enumerate(sorted(pieces, key=lambda p: p.TYPE.value)):
            pv = PieceView.from_piece( p, self.width//8, self.height//2)
            pv.move(screen, (i % 8)* self.width//8, self.y + i // 8 * self.height//2)

class NotationView:
    FONT = "Ariel"
    def __init__(self, x,y, width, height) -> None:
        self.font = pygame.font.SysFont(self.FONT, 30)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    

    def update(self, screen, history):
        pygame.draw.rect(screen, (25,25,25), (self.x,self.y, self.width, self.height))
        
        lines = 0
        text = "History: "
        for m in history:
            
            line_width = self.font.size(text)[0]
            move = str(m)
            if line_width + self.font.size(move)[0] > self.width:
                text_surf = self.font.render(text, False, (200, 200, 200))
                screen.blit(text_surf, (self.x, self.y + lines * self.font.get_height()))
                text = move
                lines +=1
            else:
                text += move + ","
        
        text_surf = self.font.render(text, False, (200, 200, 200))
        screen.blit(text_surf, (self.x, self.y + lines * self.font.get_height()))

class IconButton:
    buttons = {
        "left": pygame.image.load("resources/arrow_left.png"),
        "right": pygame.image.load("resources/arrow_right.png"),
        "pause": pygame.image.load("resources/pause.png"),
        "play":  pygame.image.load("resources/play.png")
    }
    
    def __init__(self, icon, x, y, width, height, bg) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = self.height
        self.bg = bg
        self.border = 2
        self.image = pygame.transform.scale(self.buttons[icon], (self.size, self.size))
    
    def update(self, screen, active):
        mx,my= pygame.mouse.get_pos()
        ax, ay = screen.get_abs_offset()
        rmx,rmy = mx - ax - self.x - self.border, my - ay - self.y - self.border
        if not active:
            pygame.draw.rect(screen, tuple(c - 20 for c in self.bg), (self.x,self.y, self.width, self.height))
        elif not (0 <= rmx <= self.width - self.border):
            pygame.draw.rect(screen, tuple(c for c in self.bg), (self.x,self.y, self.width, self.height))
        elif not (0 <= rmy <= self.height - self.border):
            pygame.draw.rect(screen, tuple(c for c in self.bg), (self.x,self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, tuple(c + 20 for c in self.bg), (self.x,self.y, self.width, self.height))
        pygame.draw.rect(screen, tuple(c - 40 for c in self.bg), (self.x,self.y, self.width, self.height),self.border)
        screen.blit(self.image, (self.x + self.width//2 -self.size//2 ,self.y, self.width, self.height))


class HistoryControl:    
    def __init__(self, x, y, width, height, bg) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg = bg
        self.back_button = IconButton("left", self.x, self.y, self.width//3, self.height, bg)
        self.next_button = IconButton("right", self.x + 2 * self.width//3, self.y, self.width//3, self.height, bg)
        self.pause_button = IconButton("pause", self.x + self.width//3, self.y, self.width//3, self.height, bg)
        self.play_button = IconButton("play", self.x + self.width//3, self.y, self.width//3, self.height, bg)

    def __contains__(self, pos):
        x,y = pos
        if x < self.x:
            return False
        if x > self.x + self.width:
            return False
        if y < self.y:
            return False
        if y > self.y + self.height:
            return False
        return True
    
    def update(self, screen, paused):
        self.back_button.update(screen, paused)
        self.next_button.update(screen, paused)
        if paused:
            self.play_button.update(screen, True)
        else:
            self.pause_button.update(screen, True)


class HistoryView:
    def __init__(self, x, y, width, height, bg) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg =bg
        self.white_captured = CapturedPieces(0, self.height - self.height//4, self.width, self.height//4)
        self.black_captured = CapturedPieces(0, 0,self.width, self.height//4)
        self.notation_view = NotationView(0, self.height//4, self.width, (self.height*2)//5)
        self.history_control = HistoryControl(0, self.height//4 + (self.height*2)//5, self.width, self.height//10, self.bg)

    def __contains__(self, pos):
        x,y = pos
        if x < self.x:
            return False
        if x > self.x + self.width:
            return False
        if y < self.y:
            return False
        if y > self.y + self.height:
            return False
        return True
    
    def update(self, screen, board: BoardController):
        subsurface = screen.subsurface((self.x, self.y, self.width, self.height))
        subsurface.fill(self.bg)

        eaten_pieces = board.get_eaten_pieces()
        self.black_captured.update(subsurface, [p for p in eaten_pieces if not p.white])
        self.white_captured.update(subsurface, [p for p in eaten_pieces if p.white])
        self.notation_view.update(subsurface, board.get_history())
        self.history_control.update(subsurface, board.is_paused())
    
    def click_to_game(self, pos):
        pos = (pos[0] - self.x, pos[1] - self.y )
        if pos not in self.history_control:
            return None
        return True
