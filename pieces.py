from extras import *


class Rook:
    def __init__(self, color, starting_pos, board):
        self.color = color
        self.pos = starting_pos
        self.has_moved = False

        if self.color.lower() == "white":
            self.image = "♖"
        elif self.color.lower() == "black":
            self.image = "♜"
        else:
            self.image = "N/A"

        self.board = board

    def move(self, pos2, game_move=True):
        self.board.remove(self.pos)
        self.board.remove(pos2, take=True)
        self.board.add(self, pos2)
        self.pos = pos2

        if game_move:
            self.has_moved = True
            self.board.newMove(self)

    def undoMove(self, piece, pos1):
        self.board.remove(self.pos)
        self.board.add(self, pos1)
        self.board.add(piece, self.pos, new=True)
        self.pos = pos1

    def checkMove(self, pos2):
        if type(self.board.get(pos2)) == str or not self.board.get(pos2).color == self.color:
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

        if self.color.lower() == "white":
            self.image = "♗"
        elif self.color.lower() == "black":
            self.image = "♝"
        else:
            self.image = "N/A"

        self.board = board

    def move(self, pos2, game_move=True):
        self.board.remove(self.pos)
        self.board.remove(pos2, take=True)
        self.board.add(self, pos2)
        self.pos = pos2

        if game_move:
            self.has_moved = True
            self.board.newMove(self)

    def undoMove(self, piece, pos1):
        self.board.remove(self.pos)
        self.board.add(self, pos1)
        self.board.add(piece, self.pos, new=True)
        self.pos = pos1

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

        if self.color.lower() == "white":
            self.image = "♘"
        elif self.color.lower() == "black":
            self.image = "♞"
        else:
            self.image = "N/A"

        self.board = board

    def move(self, pos2, game_move=True):
        self.board.remove(self.pos)
        self.board.remove(pos2, take=True)
        self.board.add(self, pos2)
        self.pos = pos2

        if game_move:
            self.has_moved = True
            self.board.newMove(self)

    def undoMove(self, piece, pos1):
        self.board.remove(self.pos)
        self.board.add(self, pos1)
        self.board.add(piece, self.pos, new=True)
        self.pos = pos1

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

        if self.color.lower() == "white":
            self.image = "♔"
        elif self.color.lower() == "black":
            self.image = "♚"
        else:
            self.image = "N/A"

        self.board = board

    def move(self, pos2, game_move=True):
        self.board.remove(self.pos)
        self.board.remove(pos2, take=True)
        self.board.add(self, pos2)
        self.pos = pos2

        if game_move:
            self.has_moved = True
            self.board.newMove(self)

    def undoMove(self, piece, pos1):
        self.board.remove(self.pos)
        self.board.add(self, pos1)
        self.board.add(piece, self.pos, new=True)
        self.pos = pos1

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

        if self.color.lower() == "white":
            self.image = "♕"
        elif self.color.lower() == "black":
            self.image = "♛"
        else:
            self.image = "N/A"

        self.board = board

    def move(self, pos2, game_move=True):
        self.board.remove(self.pos)
        self.board.remove(pos2, take=True)
        self.board.add(self, pos2)
        self.pos = pos2

        if game_move:
            self.has_moved = True
            self.board.newMove(self)

    def undoMove(self, piece, pos1):
        self.board.remove(self.pos)
        self.board.add(self, pos1)
        self.board.add(piece, self.pos, new=True)
        self.pos = pos1

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

        if self.color.lower() == "white":
            self.image = "♙"
        elif self.color.lower() == "black":
            self.image = "♟"
        else:
            self.image = "N/A"

        self.board = board

    def move(self, pos2, game_move=True):
        self.board.remove(self.pos)
        self.board.remove(pos2, take=True)
        self.board.add(self, pos2)

        # En Passant
        if abs(pos2["row"] - self.pos["row"]) == 1 and abs(pos2["col"] - self.pos["col"]) == 1:
            if type(self.board.get(configure(pos2["row"], self.pos["col"]))) == type(self):
                if self.board.get(configure(pos2["row"], self.pos["col"])).has_moved_two:
                    self.board.remove(configure(pos2["row"], self.pos["col"]), take=True)
                    print("\nEN PASSANT")

        self.pos = pos2

        if game_move:
            if abs(pos2["row"] - self.pos["row"]) == 2:
                self.has_moved_two = True
            else:
                self.has_moved_two = False

            self.has_moved = True
            self.board.newMove(self)

        # Pawn Promoting
        if (self.color == "black" and self.pos["row"] == 0) or (self.color == "white" and self.pos["row"] == 7):
            self.board.remove(pos2, take=True)
            promotion = input("Promote your pawn: ").upper()
            if promotion == "QUEEN":
                self.board.add(Queen(self.color, self.pos, self.board), self.pos, new=True)
            elif promotion == "ROOK":
                self.board.add(Rook(self.color, self.pos, self.board), self.pos, new=True)
            elif promotion == "BISHOP":
                self.board.add(Bishop(self.color, self.pos, self.board), self.pos, new=True)
            elif promotion == "KNIGHT":
                self.board.add(Knight(self.color, self.pos, self.board), self.pos, new=True)

    def undoMove(self, piece, pos1):
        self.board.remove(self.pos)
        self.board.add(self, pos1)
        self.board.add(piece, self.pos, new=True)
        self.pos = pos1

    def checkMove(self, pos2):
        # Black
        if self.color == "black":
            # Moving Forwards
            if self.pos["col"] == pos2["col"] and (self.pos["row"] - 1) == pos2["row"]:
                if type(self.board.get(pos2)) == str:
                    return True
            # Taking Diagonally
            elif (self.pos["row"] - 1) == pos2["row"] and abs(pos2["col"] - self.pos["col"]) == 1:
                if type(self.board.get(pos2)) != str and self.board.get(pos2).color != self.color:
                    return True
                # En Passant
                elif type(self.board.get(pos2)) == str:

                    target_piece = self.board.get(configure(self.pos["row"], pos2["col"]))

                    if isinstance(target_piece, Pawn):
                        if target_piece.color != self.color:
                            if target_piece.has_moved_two:
                                return True
            # Moving Forwards Twice
            elif not self.has_moved:
                if self.board.checkOpenFile(self.pos, configure(pos2["row"] - 1, pos2["col"])):
                    return True
        # White
        elif self.color == "white":
            # Moving Forwards
            if self.pos["col"] == pos2["col"] and (self.pos["row"] + 1) == pos2["row"]:
                if type(self.board.get(pos2)) == str:
                    return True
            # Taking Diagonally
            elif (self.pos["row"] + 1) == pos2["row"] and abs(pos2["col"] - self.pos["col"]) == 1:
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
            elif not self.has_moved:
                if self.board.checkOpenFile(self.pos, configure(pos2["row"] + 1, pos2["col"])):
                    return True
        else:
            print("no color")

        return False
