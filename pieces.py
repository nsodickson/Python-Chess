# pos[0]: row, pos[1]: col
# move[0]: position of piece, move[1]: position of target, move[2] whether or not the move is an en passant

class Piece:
    def __init__(self, color, starting_pos, board):
        # To-Do, make a piece class that all pieces subclass, use isinstance(piece, Piece) in board.py
        self.color = color
        self.pos = starting_pos
        self.has_moved = False
        self.board = board
        self.image = "?"
        self.FEN_char = "?"

    def setPos(self, pos):
        self.pos = pos

    def getPos(self):
        return self.pos


class Rook(Piece):
    def __init__(self, color, starting_pos, board):
        super().__init__(color, starting_pos, board)

        if self.color == "black":
            self.image = "♜"
            self.FEN_char = "r"
        else:
            self.image = "♖"
            self.FEN_char = "R"

    def move(self, pos2, game_move=True):
        self.board.take(pos2)
        self.board.remove(self.getPos())
        self.board.add(self, pos2)
        self.setPos(pos2)

        if game_move:
            self.has_moved = True

    def checkMove(self, pos2):
        if not isinstance(self.board.get(pos2), Piece) or self.board.get(pos2).color != self.color:
            # Rank
            if self.pos[0] == pos2[0]:
                if self.board.checkOpenRank(self.getPos(), pos2):
                    return True
            # File
            elif self.pos[1] == pos2[1]:
                if self.board.checkOpenFile(self.getPos(), pos2):
                    return True
        return False


class Bishop(Piece):
    def __init__(self, color, starting_pos, board):
        super().__init__(color, starting_pos, board)

        if self.color == "black":
            self.image = "♝"
            self.FEN_char = "b"
        else:
            self.image = "♗"
            self.FEN_char = "B"

    def move(self, pos2, game_move=True):
        self.board.take(pos2)
        self.board.remove(self.getPos())
        self.board.add(self, pos2)
        self.setPos(pos2)

        if game_move:
            self.has_moved = True

    def checkMove(self, pos2):
        target = self.board.get(pos2)

        if not isinstance(target, Piece) or target.color != self.color:
            # Diagonal
            if abs(pos2[0] - self.pos[0]) == abs(pos2[1] - self.pos[1]):
                if self.board.checkOpenDiagonal(self.getPos(), pos2):
                    return True
        return False


class Knight(Piece):
    def __init__(self, color, starting_pos, board):
        super().__init__(color, starting_pos, board)

        if self.color == "black":
            self.image = "♞"
            self.FEN_char = "n"
        else:
            self.image = "♘"
            self.FEN_char = "N"

        self.board = board

    def move(self, pos2, game_move):
        self.board.take(pos2)
        self.board.remove(self.getPos())
        self.board.add(self, pos2)
        self.setPos(pos2)

        if game_move:
            self.has_moved = True

    def checkMove(self, pos2):
        target = self.board.get(pos2)

        if not isinstance(target, Piece) or target.color != self.color:
            if (abs(self.pos[0]-pos2[0]) == 2 and abs(self.pos[1]-pos2[1]) == 1) or (abs(self.pos[0]-pos2[0]) == 1 and abs(self.pos[1]-pos2[1]) == 2):
                return True

        return False


class King(Piece):
    def __init__(self, color, starting_pos, board):
        super().__init__(color, starting_pos, board)

        if self.color == "black":
            self.image = "♚"
            self.FEN_char = "k"
        else:
            self.image = "♔"
            self.FEN_char = "K"

    def move(self, pos2, game_move):
        self.board.take(pos2)
        self.board.remove(self.getPos())
        self.board.add(self, pos2)
        self.setPos(pos2)

        if game_move:
            self.has_moved = True

    def checkMove(self, pos2):
        target = self.board.get(pos2)

        if not isinstance(target, Piece) or target.color != self.color:
            if (abs(self.pos[0] - pos2[0]) == 1 or abs(self.pos[0] - pos2[0]) == 0) and (abs(self.pos[1] - pos2[1]) == 1 or abs(self.pos[1] - pos2[1]) == 0):
                return True

        return False


class Queen(Piece):
    def __init__(self, color, starting_pos, board):
        super().__init__(color, starting_pos, board)

        if self.color == "black":
            self.image = "♛"
            self.FEN_char = "q"
        else:
            self.image = "♕"
            self.FEN_char = "Q"

    def move(self, pos2, game_move=True):
        self.board.take(pos2)
        self.board.remove(self.getPos())
        self.board.add(self, pos2)
        self.setPos(pos2)

        if game_move:
            self.has_moved = True

    def checkMove(self, pos2):
        target = self.board.get(pos2)

        if not isinstance(target, Piece) or target.color != self.color:
            # Rank
            if self.pos[0] == pos2[0]:
                if self.board.checkOpenRank(self.getPos(), pos2):
                    return True
            # File
            elif self.pos[1] == pos2[1]:
                if self.board.checkOpenFile(self.getPos(), pos2):
                    return True
            # Diagonal
            elif abs(pos2[0] - self.pos[0]) == abs(pos2[1] - self.pos[1]):
                if self.board.checkOpenDiagonal(self.getPos(), pos2):
                    return True

        return False


class Pawn(Piece):
    def __init__(self, color, starting_pos, board):
        super().__init__(color, starting_pos, board)
        self.has_moved_two = False
        if self.color == "black":
            self.image = "♟"
            self.FEN_char = "p"
            self.forward = -1
        else:
            self.image = "♙"
            self.FEN_char = "P"
            self.forward = 1

    def move(self, pos2, is_en_passant, game_move=True):
        if game_move:
            if abs(pos2[0] - self.pos[0]) == 2:
                self.has_moved_two = True
            else:
                self.has_moved_two = False

            self.has_moved = True

        if is_en_passant:
            self.board.take((self.getPos()[0], pos2[1]))
        else:
            self.board.take(pos2)

        self.board.remove(self.getPos())
        self.board.add(self, pos2)
        self.setPos(pos2)

    def checkMove(self, pos2):
        target = self.board.get(pos2)

        # Moving Forwards (checks are done differently than for other pieces because during en passants, the pawn's target isn't where it is moving).
        if self.pos[1] == pos2[1] and (self.pos[0] + self.forward) == pos2[0]:
            if not isinstance(target, Piece):  # Pawns can only move forwards into empty spaces
                return True
        # Moving Diagonally
        elif self.pos[0] + self.forward == pos2[0] and abs(pos2[1] - self.pos[1]) == 1:
            if isinstance(target, Piece) and target.color != self.color:  # Pawns can only move diagonally to take
                return True
            # En Passant
            elif not isinstance(self.board.get(pos2), Piece):
                target = self.board.get((self.pos[0], pos2[1]))
                if isinstance(target, Pawn):
                    if target.color != self.color:
                        if target.has_moved_two:
                            return True
        # Moving Forward Twice
        elif self.pos[1] == pos2[1] and self.pos[0] + 2 * self.forward == pos2[0]:
            if not self.has_moved:
                if not isinstance(target, Piece) and not isinstance(self.board.get((self.pos[0] + self.forward, pos2[1])), Piece):
                    return True
        return False
