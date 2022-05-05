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


def configureMove(pos1, pos2):
    return {"pos1": pos1, "pos2": pos2}


def transformPos(string_pos):
    return int(string_pos[1]) - 1, letters.index(string_pos[0])


def transformMove(string_move):
    return configureMove(transformPos(string_move[:2]), transformPos(string_move[3:]))


def detransformPos(dict_pos):
    return f"{letters[dict_pos[1]].lower()}{dict_pos[0] + 1}"


def detransformMove(dict_move):
    return detransformPos(dict_move["pos1"]) + "x" + detransformPos(dict_move["pos2"])
    