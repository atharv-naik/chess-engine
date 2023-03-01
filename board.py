import pygame
import copy
import json
from pieces import Piece


pygame.init()


class Board():
    '''Creates a chess board with a 2D array of squares.'''

    def __init__(self, turn: str ="w") -> None:

        self.DIMENSION = 800
        self.HEIGHT = 800
        self.WIDTH = 800
        self.SQUARE_SIZE = self.DIMENSION // 8

        self.BRAWN_DARK = (170, 139, 86)
        self.BRAWN_LIGHT = (240, 235, 206)

        self.GREEN_DARK = (118, 150, 86)
        self.GREEN_LIGHT = (238, 238, 210)
        self.HIGHLIGHT_COLOR = (186, 202, 68)

        self.HOVER_COLOR = (86, 102, 68)
        self.KING_CHECK_COLOR = (255, 0, 0)
        self.ORDINARY_COUPH_COLOR = (0, 0, 255)
        self.GREEN_BOARD = (self.GREEN_LIGHT, self.GREEN_DARK)  # light, dark

        self.BROWN_BOARD = (self.BRAWN_LIGHT, self.BRAWN_DARK)  # light, dark
        self.BOARD_COLOR = self.GREEN_BOARD

        self.LONG_PRESS_DELAY = 500

        self.boardRep = [
            ["bR1", "bN1", "bB1", "bQ", "bK", "bB2", "bN2", "bR2"],
            ["bP1", "bP2", "bP3", "bP4", "bP5", "bP6", "bP7", "bP8"],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ["wP1", "wP2", "wP3", "wP4", "wP5", "wP6", "wP7", "wP8"],
            ["wR1", "wN1", "wB1", "wQ", "wK", "wB2", "wN2", "wR2"]
        ]
        self.play = True
        self.turn = turn
        self.selected = None

        self.top = 0
        self.progress = {self.top: copy.deepcopy(self.boardRep)}
        self.ceil = len(self.progress)

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(f"Chess- {self.get_color_name(self.turn)}'s turn")

        # initialize pieces
        self.bR1 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bR.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bR")
        self.bR2 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bR.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bR")
        
        self.bN1 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bN.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bN")
        self.bN2 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bN.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bN")
        
        self.bB1 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bB.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bB")
        self.bB2 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bB.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bB")
        
        self.bQ = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bQ.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bQ")
        self.bK = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bK.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bK")
        
        self.bP1 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bP")
        self.bP2 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bP")
        self.bP3 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bP")
        self.bP4 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bP")
        self.bP5 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bP")
        self.bP6 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bP")
        self.bP7 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bP")
        self.bP8 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bP")

        self.wR1 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wR.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wR")
        self.wR2 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wR.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wR")
        
        self.wN1 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wN.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wN")
        self.wN2 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wN.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wN")
        
        self.wB1 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wB.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wB")
        self.wB2 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wB.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wB")
        
        self.wQ = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wQ.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wQ")
        self.wK = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wK.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wK")
        
        self.wP1 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wP")
        self.wP2 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wP")
        self.wP3 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wP")
        self.wP4 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wP")
        self.wP5 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wP")
        self.wP6 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wP")
        self.wP7 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wP")
        self.wP8 = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wP")


        self.board = [
            [self.bR1, self.bN1, self.bB1, self.bQ, self.bK, self.bB2, self.bN2, self.bR2],
            [self.bP1, self.bP2, self.bP3, self.bP4, self.bP5, self.bP6, self.bP7, self.bP8],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [self.wP1, self.wP2, self.wP3, self.wP4, self.wP5, self.wP6, self.wP7, self.wP8],
            [self.wR1, self.wN1, self.wB1, self.wQ, self.wK, self.wB2, self.wN2, self.wR2]
        ]

    def draw(self, screen: pygame.Surface) -> None:
        '''Draw the board and pieces.'''

        # draw board
        for i in range(8):
            for j in range(8):
                color = self.BOARD_COLOR[(i + j) % 2]
                pygame.draw.rect(screen, color, pygame.Rect(
                    i * self.SQUARE_SIZE, j * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

        # highlight hovered square
        x, y = self.get_square(pygame.mouse.get_pos())
        # darken square
        pygame.draw.rect(screen, self.HOVER_COLOR, pygame.Rect(
            x * self.SQUARE_SIZE, y * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
        # highlight selected square
        if self.selected != None and self.get_piece(*self.selected): # if there is a piece selected
            x, y = self.selected
            pygame.draw.rect(screen, self.HIGHLIGHT_COLOR, pygame.Rect(
                x * self.SQUARE_SIZE, y * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE), width=5, border_radius=5)

        # highlight possible moves
        if self.selected and self.get_piece(*self.selected) and self.get_piece(*self.selected).color == self.turn:
            piece = self.get_piece(*self.selected)
            for move in piece.get_moves(self.board, *self.selected): # get all possible moves
                x, y = move
                # highlight circle
                pygame.draw.circle(screen, self.HIGHLIGHT_COLOR, (
                    x * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, y * self.SQUARE_SIZE + self.SQUARE_SIZE // 2), self.SQUARE_SIZE // 10)

        # draw pieces
        for i in range(8):
            for j in range(8):
                if self.board[j][i] is not None:
                    screen.blit(
                        self.board[j][i].piece, (i * self.SQUARE_SIZE, j * self.DIMENSION // 8))
    
    def switch_board_color(self) -> None:
        '''Switch the board color.'''
        self.BOARD_COLOR = self.GREEN_BOARD if self.BOARD_COLOR == self.BROWN_BOARD else self.BROWN_BOARD

    def valid_move(self, board: list, x1: int, y1: int, x2: int, y2: int) -> bool:
        '''Check if a move is valid.'''
        piece = self.get_piece(x1, y1)
        if piece.color != self.turn or (x2, y2) not in piece.get_moves(board, x1, y1):
            print(piece.color, self.turn, (x2, y2), piece.get_moves(board, x1, y1))
            return False
        return True

    def move(self, x1: int, y1: int, x2: int, y2: int) -> None:
        '''Move a piece from (x1, y1) to (x2, y2).'''

        if not self.valid_move(self.board, x1, y1, x2, y2):
            self.selected = None
            print("move invalid")
            return
        print("move valid")
        self.board[y2][x2] = self.board[y1][x1]
        self.board[y1][x1] = None
        self.update_progress(x1, y1, x2, y2)

    def get_square(self, pos: tuple) -> tuple:
        '''Get the square the mouse is on.'''

        x, y = pos
        return (x // self.SQUARE_SIZE, y // self.SQUARE_SIZE)

    def select(self, pos: tuple) -> None:
        '''Select/unselect a square with pygame pos.'''

        x, y = self.get_square(pos)
        self.prev_selected = self.selected
        self.selected = (x, y) if (
            self.selected == None or self.selected != (x, y)) else None
        if self.selected != None and self.prev_selected != None and self.get_piece(*self.prev_selected): # if there is a piece selected
            self.move(*self.prev_selected, *self.selected)
            self.selected = None
            self.prev_selected = None

    def select_square(self, x: int, y: int) -> None:
        '''Select/unselect a square with coordinates.'''

        self.selected = (x, y) if (
            self.selected == None or self.selected != (x, y)) else None

    def get_piece(self, x: int, y: int):
        '''Get the piece at a square.'''

        return self.board[y][x]

    def update_board(self) -> None:
        '''Update the board.'''

        piece_map = {
            "bK": self.bK, "bQ": self.bQ, "bR1": self.bR1, "bR2": self.bR2, "bB1": self.bB1, "bB2": self.bB2, "bN1": self.bN1, "bN2": self.bN2,
            "bP1": self.bP1, "bP2": self.bP2, "bP3": self.bP3, "bP4": self.bP4, "bP5": self.bP5, "bP6": self.bP6, "bP7": self.bP7, "bP8": self.bP8,
            "wK": self.wK, "wQ": self.wQ, "wR1": self.wR1, "wR2": self.wR2, "wB1": self.wB1, "wB2": self.wB2, "wN1": self.wN1, "wN2": self.wN2,
            "wP1": self.wP1, "wP2": self.wP2, "wP3": self.wP3, "wP4": self.wP4, "wP5": self.wP5, "wP6": self.wP6, "wP7": self.wP7, "wP8": self.wP8
        }
        for i in range(8):
            for j in range(8):
                self.board[j][i] = piece_map.get(self.boardRep[j][i])

    def get_color_name(self, color: str) -> str:
        '''Get the name of a color.'''

        return "WHITE" if color == "w" else "BLACK"

    def update_progress(self, x1: int, y1: int, x2: int, y2: int) -> None:
        '''Update game progress.'''

        self.boardRep[y2][x2] = self.boardRep[y1][x1]
        self.boardRep[y1][x1] = None
        self.top += 1
        self.ceil += 1
        self.progress[self.top] = copy.deepcopy(self.boardRep)
        self.update_turn()
    
    def update_turn(self) -> None:
        '''Update the turn.'''

        self.turn = "w" if self.turn == "b" else "b"
        pygame.display.set_caption(f"Chess - {self.get_color_name(self.turn)}'s turn") # update the title

    def undo(self) -> None:
        '''Undo the last move.'''

        if self.top > 0:
            self.top -= 1
            self.boardRep = copy.deepcopy(self.progress[self.top])
            self.update_board()
            self.update_turn()

    def redo(self) -> None:
        '''Redo the last move.'''

        if self.top < self.ceil - 1:
            self.top += 1
            self.boardRep = copy.deepcopy(self.progress[self.top])
            self.update_board()
            self.update_turn()

    def reset(self) -> None:
        '''Reset the board.'''

        if self.top != 0:
            self.top = 0
            self.boardRep = copy.deepcopy(self.progress[self.top])
            self.update_board()
            self.update_turn()

    def save(self) -> None:
        '''Save the game.'''

        game_state = json.dumps({
            "play": self.play,
            "turn": self.turn,
            "top": self.top,
            "progress": self.progress,
        })
        try:
            with open("save.data", "w") as f:
                json.dump(game_state, f)
        except:
            print("Failed to save game.")
        else:
            print("Saved game.")

    def load(self) -> None:
        '''Load the game.'''

        try:
            with open("save.data", "r") as f:
                game_state = json.loads(json.load(f))
            self.play = game_state["play"]
            self.turn = game_state["turn"]
            self.top = game_state["top"]
            self.progress = {
                int(k): v for k, v in game_state["progress"].items()}
            self.boardRep = copy.deepcopy(self.progress[self.top])
            self.ceil = len(self.progress)
            self.update_board()
        except FileNotFoundError:
            print("No save file found.") # add logging in the future
        else:
            print("Loaded save file.")
