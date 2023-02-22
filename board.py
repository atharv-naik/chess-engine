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
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.play = True
        self.turn = turn
        self.selected = None

        self.top = 0
        self.progress = {self.top: copy.deepcopy(self.boardRep)}
        self.ceil = len(self.progress)

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(f"Chess- {self.get_color_name(self.turn)}'s turn")

        # load assets
        self.bR = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bR.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bR")
        self.bN = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bN.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bN")
        self.bB = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bB.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bB")
        self.bQ = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bQ.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bQ")
        self.bK = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bK.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bK")
        self.bP = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/bP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "bP")

        self.wR = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wR.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wR")
        self.wN = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wN.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wN")
        self.wB = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wB.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wB")
        self.wQ = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wQ.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wQ")
        self.wK = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wK.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wK")
        self.wP = Piece(pygame.transform.scale(pygame.image.load(
            "assets/images/wP.png"), (self.SQUARE_SIZE, self.SQUARE_SIZE)), "wP")

        self.board = [
            [self.bR, self.bN, self.bB, self.bQ, self.bK, self.bB, self.bN, self.bR],
            [self.bP, self.bP, self.bP, self.bP, self.bP, self.bP, self.bP, self.bP],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [self.wP, self.wP, self.wP, self.wP, self.wP, self.wP, self.wP, self.wP],
            [self.wR, self.wN, self.wB, self.wQ, self.wK, self.wB, self.wN, self.wR]
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
            "bK": self.bK, "bQ": self.bQ, "bR": self.bR, "bB": self.bB, "bN": self.bN, "bP": self.bP,
            "wK": self.wK, "wQ": self.wQ, "wR": self.wR, "wB": self.wB, "wN": self.wN, "wP": self.wP
        }
        for i in range(8):
            for j in range(8):
                self.board[j][i] = piece_map.get(self.boardRep[j][i])

    def get_color_name(self, color: str) -> str:
        '''Get the name of a color.'''

        return "white" if color == "w" else "black"

    def update_progress(self, x1: int, y1: int, x2: int, y2: int) -> None:
        '''Update the progress of the game.'''

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
