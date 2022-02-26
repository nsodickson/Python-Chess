from extras import *


class Rook:
    def __init__(self, color, starting_pos, board):
        self.color = color
        self.pos = starting_pos
        self.has_moved = False

        if self.color.lower() == "black":
            self.image = "♜"
            self.FEN_char = "r"
        else:
            self.image = "♖"
            self.FEN_char = "R"

        self.board = board

    def move(self, pos2):
        self.board.remove(self.pos)
        self.board.take(pos2)
        self.board.add(self, pos2)

        self.pos = pos2
        self.has_moved = True

    def checkMove(self, pos2):
        if type(self.board.get(pos2)) == str or self.board.get(pos2).color != self.color:
            # Rank
            if self.pos["row"] == pos2["row"]:
                if self.board.checkOpenRank(self.pos, pos2):
                    return True
            # File
            elif self.pos["col"] == pos2["col"]:
                if self.board.checkOpenFile(self.pos, pos2):
                    return True
        return False


class Bishop:
    def __init__(self, color, starting_pos, board):
        self.color = color
        self.pos = starting_pos
        self.has_moved = False

        if self.color.lower() == "black":
            self.image = "♝"
            self.FEN_char = "b"
        else:
            self.image = "♗"
            self.FEN_char = "B"

        self.board = board

    def move(self, pos2):
        self.board.remove(self.pos)
        self.board.take(pos2)
        self.board.add(self, pos2)

        self.pos = pos2
        self.has_moved = True

    def checkMove(self, pos2):
        target_piece = self.board.get(pos2)

        if type(target_piece) == str or target_piece.color != self.color:
            # Diagonal
            if abs(pos2["row"] - self.pos["row"]) == abs(pos2["col"] - self.pos["col"]):
                if self.board.checkOpenDiagonal(self.pos, pos2):
                    return True
        return False


class Knight:
    def __init__(self, color, starting_pos, board):
        self.color = color
        self.pos = starting_pos
        self.has_moved = False

        if self.color.lower() == "black":
            self.image = "♞"
            self.FEN_char = "n"
        else:
            self.image = "♘"
            self.FEN_char = "N"

        self.board = board

    def move(self, pos2):
        self.board.remove(self.pos)
        self.board.take(pos2)
        self.board.add(self, pos2)

        self.pos = pos2
        self.has_moved = True

    def checkMove(self, pos2):
        target_piece = self.board.get(pos2)

        if type(target_piece) == str or target_piece.color != self.color:
            if (abs(self.pos["row"]-pos2["row"]) == 2 and abs(self.pos["col"]-pos2["col"]) == 1) or (abs(self.pos["row"]-pos2["row"]) == 1 and abs(self.pos["col"]-pos2["col"]) == 2):
                return True

        return False


class King:
    def __init__(self, color, starting_pos, board):
        self.color = color
        self.pos = starting_pos
        self.has_moved = False

        if self.color.lower() == "black":
            self.image = "♚"
            self.FEN_char = "k"
        else:
            self.image = "♔"
            self.FEN_char = "K"

        self.board = board

    def move(self, pos2):
        self.board.remove(self.pos)
        self.board.take(pos2)
        self.board.add(self, pos2)

        self.pos = pos2
        self.has_moved = True

    def checkMove(self, pos2):
        target_piece = self.board.get(pos2)

        if type(target_piece) == str or target_piece.color != self.color:
            if (abs(self.pos["row"] - pos2["row"]) == 1 or abs(self.pos["row"] - pos2["row"]) == 0) and (abs(self.pos["col"] - pos2["col"]) == 1 or abs(self.pos["col"] - pos2["col"]) == 0):
                return True

        return False


class Queen:
    def __init__(self, color, starting_pos, board):
        self.color = color
        self.pos = starting_pos
        self.has_moved = False

        if self.color.lower() == "black":
            self.image = "♛"
            self.FEN_char = "q"
        else:
            self.image = "♕"
            self.FEN_char = "Q"

        self.board = board

    def move(self, pos2):
        self.board.remove(self.pos)
        self.board.take(pos2)
        self.board.add(self, pos2)

        self.pos = pos2
        self.has_moved = True

    def checkMove(self, pos2):

        target_piece = self.board.get(pos2)

        if type(target_piece) == str or target_piece.color != self.color:
            # Rank
            if self.pos["row"] == pos2["row"]:
                if self.board.checkOpenRank(self.pos, pos2):
                    return True
            # File
            elif self.pos["col"] == pos2["col"]:
                if self.board.checkOpenFile(self.pos, pos2):
                    return True
            # Diagonal
            elif abs(pos2["row"] - self.pos["row"]) == abs(pos2["col"] - self.pos["col"]):
                if self.board.checkOpenDiagonal(self.pos, pos2):
                    return True

        return False


class Pawn:
    def __init__(self, color, starting_pos, board):
        self.color = color
        self.pos = starting_pos
        self.has_moved = False
        self.has_moved_two = False

        if self.color.lower() == "black":
            self.image = "♟"
            self.FEN_char = "p"
        else:
            self.image = "♙"
            self.FEN_char = "P"

        self.board = board

    def move(self, pos2):

        self.board.remove(self.pos)
        if abs(pos2["row"] - self.pos["row"]) == abs(pos2["col"] - self.pos["col"]) and type(self.board.get(pos2)) == str:
            # En Passants
            self.board.take(configure(self.pos["row"], pos2["col"]))
        else:
            self.board.take(pos2)
        self.board.add(self, pos2)

        if abs(pos2["row"] - self.pos["row"]) == 2:
            self.has_moved_two = True
        else:
            self.has_moved_two = False

        self.pos = pos2
        self.has_moved = True

    def checkMove(self, pos2):

        forward = {"white": 1, "black": -1}[self.color]

        # Moving Forwards
        if self.pos["col"] == pos2["col"] and (self.pos["row"] + forward) == pos2["row"]:
            if type(self.board.get(pos2)) == str:
                return True
        # Moving Diagonally
        elif (self.pos["row"] + forward) == pos2["row"] and abs(pos2["col"] - self.pos["col"]) == 1:
            if type(self.board.get(pos2)) != str and self.board.get(pos2).color != self.color:
                return True
            # En Passant
            elif type(self.board.get(pos2)) == str:
                target_piece = self.board.get(configure(self.pos["row"], pos2["col"]))
                if isinstance(target_piece, Pawn):
                    if target_piece.color != self.color:
                        if target_piece.has_moved_two:
                            return True
        # Moving Forward Twice
        elif self.pos["col"] == pos2["col"] and (self.pos["row"] + 2 * forward) == pos2["row"]:
            if not self.has_moved:
                if type(self.board.get(pos2)) == str and type(self.board.get(configure(self.pos["row"] + forward, pos2["col"]))) == str:
                    return True
        return False
