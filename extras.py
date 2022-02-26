# Extra functions that are used throughout the project, but didn't fit into a specific file

letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
color_switch = {"white": "black", "black": "white"}


def configure(row, col):
    return {"row": row, "col": col}


def reconfigure(pos, rowMod, colMod):
    return {"row": pos["row"] + rowMod, "col": pos["col"] + colMod}


def configureMove(pos1, pos2):
    return {"pos1": pos1, "pos2": pos2}


def transformMove(string_move):
    pos1 = {"row": int(string_move[1]) - 1, "col": letters.index(string_move[0])}
    pos2 = {"row": int(string_move[4]) - 1, "col": letters.index(string_move[3])}
    return configureMove(pos1, pos2)
