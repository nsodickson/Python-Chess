# pos[0]: row, pos[1]: col
# move[0]: position of piece, move[1]: position of target, move[2] whether or not the move is an en passant

letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
switch = {"white": "black", "black": "white"}
scores = {"P": 1, "p": -1, "N": 3, "n": -3, "B": 3, "b": -3, "R": 5, "r": -5, "Q": 9, "q": -9, "K": 100, "k": -100}
one_hot_pieces = {
    'p': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'P': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    'n': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'N': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    'b': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'B': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    'r': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    'R': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    'q': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    'Q': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    'k': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    'K': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    '.': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}


def reconfigure(pos, rowMod, colMod):
    return pos[0] + rowMod, pos[1] + colMod


def posToTuple(string_pos):
    return int(string_pos[1]) - 1, letters.index(string_pos[0])


def moveToTuple(string_move, is_en_passant):
    return posToTuple(string_move[:2]), posToTuple(string_move[3:]), is_en_passant


def posToString(pos):
    return f"{letters[pos[1]].lower()}{pos[0] + 1}"


def moveToString(move):
    return posToString(move[0]) + "x" + posToString(move[1])
    