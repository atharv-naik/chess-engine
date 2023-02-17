import pygame
from typing import ForwardRef
Board = ForwardRef("Board")

class Piece():
    '''A chess piece.'''

    def __init__(self, piece: pygame.Surface, piece_id: str) -> None:
        self.color = piece_id[0]
        self.type = piece_id[1]
        self.piece = piece
        self.piece_id = piece_id

    def location(self, board: Board) -> tuple:
        '''Get the location of a piece.'''

        for i in range(8):
            for j in range(8):
                if board.board[j][i].piece_id == self.piece_id:
                    return (i, j)

    def get_moves(self, board: Board) -> list:
        '''Get the possible moves for a piece.'''

        x, y = self.location(board)
        moves = []
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
