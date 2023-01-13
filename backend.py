def valid_moves(board, pos, piece):
    moves = [pos]
    return moves

def get_coups(board, pos, pieces):
    coups = [pos]
    return coups

def is_check(board):
    return True


import copy
array = {}
p = [1, 2, 3]
array['a'] = copy.copy(p)
p[0] = 4
array['b'] = copy.copy(p)
# print(array)

