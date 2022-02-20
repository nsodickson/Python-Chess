# Extra functions and global variables that are used throughout the project, but didn't fit into a specific file


letters = ["A", "B", "C", "D", "E", "F", "G", "H"]


def configure(row, col):
    return {"row": row, "col": col}


def configureMove(pos1, pos2):
    return {"pos1": pos1, "pos2": pos2}
