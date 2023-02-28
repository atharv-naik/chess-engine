import pygame
from typing import ForwardRef
Board = ForwardRef("Board")

class Piece():
    '''A chess piece.'''

    piece_id = 0

    def __init__(self, piece: pygame.Surface=None, piece_name: str=None, Nonetype=False) -> None:
        self.isNone = Nonetype
        if Nonetype:
            self.color = None
            self.type = None
            self.piece = None
            self.piece_name = None
            self.piece_id = None
            return
        self.color = piece_name[0]
        self.type = piece_name[1]
        self.piece = piece
        self.piece_name = piece_name
        self.piece_id = Piece.piece_id
        Piece.piece_id += 1

    def location(self, board: Board) -> tuple:
        '''Get the location of a piece.'''

        for i in range(8):
            for j in range(8):
                if board[j][i].piece_id == self.piece_id:
                    return (i, j)

    # def move(self, board: Board, x: int, y: int) -> None:
    #     '''Move a piece to a location.'''

    #     board[y][x] = self

    def get_moves(self, board: list, x: int, y: int) -> list[tuple]:
        '''Get the possible moves for a piece.'''

        # x, y = self.location(board)
        moves = set()
        if self.type == "K":
            moves = self.get_king_moves(board, x, y)
        elif self.type == "Q":
            moves = self.get_queen_moves(board, x, y)
        elif self.type == "R":
            moves = self.get_rook_moves(board, x, y)
        elif self.type == "B":
            moves = self.get_bishop_moves(board, x, y)
        elif self.type == "N":
            moves = self.get_knight_moves(board, x, y)
        elif self.type == "P":
            moves = self.get_pawn_moves(board, x, y)
        return moves

    def get_pawn_moves(self, board: list, x: int, y: int) -> list[tuple]:
        '''Get the possible moves for a pawn.'''

        moves = set()
        if self.color == "w":
            if board[y - 1][x] is None: # move forward
                moves.add((x, y - 1))
                if y == 6 and board[y - 2][x] is None: # move forward 2
                    moves.add((x, y - 2))
            if x > 0 and board[y - 1][x - 1] is not None and board[y - 1][x - 1].color != self.color: # capture left
                moves.add((x - 1, y - 1))
            if x < 7 and board[y - 1][x + 1] is not None and board[y - 1][x + 1].color != self.color: # capture right
                moves.add((x + 1, y - 1))
        else:
            if board[y + 1][x] is None: # move forward
                moves.add((x, y + 1))
                if y == 1 and board[y + 2][x] is None: # move forward 2
                    moves.add((x, y + 2))
            if x > 0 and board[y + 1][x - 1] is not None and board[y + 1][x - 1].color != self.color: # capture left
                moves.add((x - 1, y + 1))
            if x < 7 and board[y + 1][x + 1] is not None and board[y + 1][x + 1].color != self.color: # capture right
                moves.add((x + 1, y + 1))
        return moves

    def get_knight_moves(self, board: list, x: int, y: int) -> list[tuple]:
        '''Get the possible moves for a knight.'''

        moves = set()
        for i, j in ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)): # check all possible moves
            if 0 <= x + i < 8 and 0 <= y + j < 8: # if on the board
                if board[y + j][x + i] is None or board[y + j][x + i].color != self.color: # if empty or enemy
                    moves.add((x + i, y + j))
        return moves
    
    def get_bishop_moves(self, board: list, x: int, y: int) -> list[tuple]:
        '''Get the possible moves for a bishop.'''

        moves = set()
        for i in range(1, 8): # lower right diagonal
            if 0 <= x + i < 8 and 0 <= y + i < 8: # if on the board
                if board[y + i][x + i] is None: # if empty
                    moves.add((x + i, y + i))
                elif board[y + i][x + i].color != self.color: # if enemy
                    moves.add((x + i, y + i))
                    break
                else: # if friendly
                    break
        for i in range(1, 8): # upper right diagonal
            if 0 <= x + i < 8 and 0 <= y - i < 8: # if on the board
                if board[y - i][x + i] is None: # if empty
                    moves.add((x + i, y - i))
                elif board[y - i][x + i].color != self.color: # if enemy
                    moves.add((x + i, y - i))
                    break
                else: # if friendly
                    break
        for i in range(1, 8): # lower left diagonal
            if 0 <= x - i < 8 and 0 <= y + i < 8: # if on the board
                if board[y + i][x - i] is None: # if empty
                    moves.add((x - i, y + i))
                elif board[y + i][x - i].color != self.color: # if enemy
                    moves.add((x - i, y + i))
                    break
                else: # if friendly
                    break
        for i in range(1, 8): # upper left diagonal
            if 0 <= x - i < 8 and 0 <= y - i < 8: # if on the board
                if board[y - i][x - i] is None: # if empty
                    moves.add((x - i, y - i))
                elif board[y - i][x - i].color != self.color: # if enemy
                    moves.add((x - i, y - i))
                    break
                else: # if friendly
                    break
        return moves
    
    def get_rook_moves(self, board: list, x: int, y: int) -> list[tuple]:
        '''Get the possible moves for a rook.'''

        moves = set()
        for i in range(1, 8): # check right
            if 0 <= x + i < 8: # if on the board
                if board[y][x + i] is None: # if empty
                    moves.add((x + i, y))
                elif board[y][x + i].color != self.color: # if enemy
                    moves.add((x + i, y))
                    break
                else: # if friendly
                    break
        for i in range(1, 8): # check left
            if 0 <= x - i < 8: # if on the board
                if board[y][x - i] is None: # if empty
                    moves.add((x - i, y))
                elif board[y][x - i].color != self.color: # if enemy
                    moves.add((x - i, y))
                    break
                else: # if friendly
                    break
        for i in range(1, 8): # check down
            if 0 <= y + i < 8: # if on the board
                if board[y + i][x] is None: # if empty
                    moves.add((x, y + i))
                elif board[y + i][x].color != self.color: # if enemy
                    moves.add((x, y + i))
                    break
                else: # if friendly
                    break
        for i in range(1, 8): # check up
            if 0 <= y - i < 8: # if on the board
                if board[y - i][x] is None: # if empty
                    moves.add((x, y - i))
                elif board[y - i][x].color != self.color: # if enemy
                    moves.add((x, y - i))
                    break
                else: # if friendly
                    break
        return moves
    
    def get_queen_moves(self, board: list, x: int, y: int) -> list[tuple]:
        '''Get the possible moves for a queen.'''

        moves = set()
        # queen moves are just the combination of rook and bishop moves
        moves.extend(self.get_rook_moves(board, x, y))
        moves.extend(self.get_bishop_moves(board, x, y))
        return moves

    def get_king_moves(self, board: list, x: int, y: int):
        '''Get the possible moves for a king.'''

        moves = set()
        for i, j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)): # check all possible moves
            if 0 <= x + i < 8 and 0 <= y + j < 8: # if on the board
                if board[y + j][x + i] is None or board[y + j][x + i].color != self.color: # if empty or enemy
                    moves.add((x + i, y + j))
        # remove moves that would put the king in check
        
        return moves

p = Piece(Nonetype=True)
print(p.isNone)