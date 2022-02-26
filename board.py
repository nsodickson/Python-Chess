from pieces import *
from copy import deepcopy

piece_icons = {"P": Pawn, "R": Rook, "N": Knight, "B": Bishop, "Q": Queen, "K": King}


class Board:
    def __init__(self):
        self.board = [["■" if (i+n) % 2 == 0 else "□" for i in range(8)] for n in range(8)]
        self.width = len(self.board[0])
        self.height = len(self.board)

        # 2x2 array that contains the row-column configuration of each location on the board, instead of the piece in that location. Used for a variety of board tests.
        self.board_pos = [[configure(i, n) for n in range(self.width)] for i in range(self.height)]

        self.white_king = King("white", configure(0, 4), self)
        self.black_king = King("black", configure(7, 4), self)
        self.has_castled = {"white": False, "black": False}

        self.moves = []
        self.pieces = [self.white_king, self.black_king]

    def setup(self):
        # Piece Setup
        starting_white_pieces = [
            [Rook("white", configure(0, 0), self), Knight("white", configure(0, 1), self), Bishop("white", configure(0, 2), self), Queen("white", configure(0, 3), self), self.white_king,
             Bishop("white", configure(0, 5), self), Knight("white", configure(0, 6), self), Rook("white", configure(0, 7), self)],
            [Pawn("white", configure(1, i), self) for i in range(8)]]
        starting_black_pieces = [
            [Rook("black", configure(7, 0), self), Knight("black", configure(7, 1), self), Bishop("black", configure(7, 2), self), Queen("black", configure(7, 3), self), self.black_king,
             Bishop("black", configure(7, 5), self), Knight("black", configure(7, 6), self), Rook("black", configure(7, 7), self)],
            [Pawn("black", configure(6, i), self) for i in range(8)]]

        for i in starting_white_pieces:
            for n in i:
                self.addNew(n, n.pos)
        del starting_white_pieces
        for i in starting_black_pieces:
            for n in i:
                self.addNew(n, n.pos)
        del starting_black_pieces

    def reset(self):
        self.__init__()

    def getFEN(self):
        # Returns a FEN string for the current state of the board.
        FEN = []
        for rank in self.board:
            FEN.append("/")
            for square in rank:
                if type(square) == str:
                    if FEN[-1].isdigit():
                        FEN[-1] = str(int(FEN[-1]) + 1)
                    else:
                        FEN.append("1")
                else:
                    FEN.append(square.FEN_char)
        return "".join(FEN[1:])

    def loadFEN(self, FEN):
        # Resets the board to the position of an inputted FEN string.
        FEN_array = [i for i in FEN if i != "/"]
        self.reset()
        FEN_index = 0
        for rank in self.board_pos:
            for pos in rank:
                current = FEN_array[FEN_index]
                if current.isdigit():
                    if current == "1":
                        FEN_index += 1
                    else:
                        FEN_array[FEN_index] = str(int(current) - 1)
                else:
                    FEN_index += 1
                    if current.isupper():
                        if current == "K":
                            self.add(self.white_king, pos)
                        else:
                            self.addNew(piece_icons[current.upper()]("white", pos, self), pos)
                    else:
                        if current == "k":
                            self.add(self.black_king, pos)
                        else:
                            self.addNew(piece_icons[current.upper()]("black", pos, self), pos)

    def deepCopy(self, load_moves=False):
        board_copy = Board()
        board_copy.loadFEN(self.getFEN())
        if load_moves:
            board_copy.moves = [deepcopy(move) for move in self.moves]
        return board_copy

    def transpose(self, board="self.board"):
        if board == "self.board":
            return [[self.board[i][n] for i in range(self.width)] for n in range(self.height)]
        elif board == "self.board_pos":
            return [[self.board_pos[i][n] for i in range(self.width)] for n in range(self.height)]

    def addNew(self, piece, pos):
        # Put a new piece on the board, and add it to the board's internal list of pieces. It is now a new piece in the game.
        if piece not in self.pieces and type(piece) != str:
            self.pieces.append(piece)
        self.board[pos["row"]][pos["col"]] = piece

    def add(self, piece, pos):
        # Put a piece on the board without adding it to the board's internal list of pieces. This is used for moving pieces already in the game.
        self.board[pos["row"]][pos["col"]] = piece

    def remove(self, pos):
        # Replace the piece with the typical black or white square without removing it from the board's internal list of pieces
        if (pos["row"]+pos["col"]) % 2 == 0:
            self.add("■", pos)
        else:
            self.add("□", pos)

    def take(self, pos):
        piece = self.get(pos)
        # Replace the piece with the typical black or white square, and remove it from the board's internal list of pieces. It is now not part of the game.
        if piece in self.pieces:
            self.pieces.remove(piece)

        # Replace the piece with the typical black or white square
        if (pos["row"] + pos["col"]) % 2 == 0:
            self.add("■", pos)
        else:
            self.add("□", pos)

    def get(self, pos):
        return self.board[pos["row"]][pos["col"]]

    def getFilePos(self, pos1, pos2):
        if pos1["row"] > pos2["row"]:
            return self.transpose("self.board_pos")[pos1["col"]][(pos2["row"] + 1):pos1["row"]]
        elif pos2["row"] > pos1["row"]:
            return self.transpose("self.board_pos")[pos1["col"]][(pos1["row"] + 1):pos2["row"]]

    def getRankPos(self, pos1, pos2):
        if pos1["col"] > pos2["col"]:
            return self.board_pos[pos1["row"]][(pos2["col"] + 1):pos1["col"]]
        elif pos2["col"] > pos1["col"]:
            return self.board_pos[pos1["row"]][(pos1["col"] + 1):pos2["col"]]

    def getDiagonalPos(self, pos1, pos2):
        if pos1["row"] > pos2["row"] and pos1["col"] > pos2["col"]:
            return [self.board_pos[pos1["row"] - i][pos1["col"] - i] for i in range(1, abs(pos2["row"] - pos1["row"]))]
        elif pos1["row"] < pos2["row"] and pos1["col"] < pos2["col"]:
            return [self.board_pos[i + pos1["row"]][i + pos1["col"]] for i in range(1, abs(pos2["row"] - pos1["row"]))]
        elif pos1["row"] > pos2["row"] and pos1["col"] < pos2["col"]:
            return [self.board_pos[pos1["row"] - i][i + pos1["col"]] for i in range(1, abs(pos2["row"] - pos1["row"]))]
        elif pos1["row"] < pos2["row"] and pos1["col"] > pos2["col"]:
            return [self.board_pos[i + pos1["row"]][pos1["col"] - i] for i in range(1, abs(pos2["row"] - pos1["row"]))]

    def print(self, color="white"):
        if color.lower() == "white":
            printable_board = list(enumerate(self.board))[::-1]
        else:
            printable_board = list(enumerate(self.board))

        # Prints the board with the correct formatting
        print("\n   ", end='')
        for i in letters:
            print(i, ' ', end='')

        print("")
        for index1, row in printable_board:
            print(index1 + 1, ' ', end='')
            for index2, piece in enumerate(row):
                if piece in self.pieces:
                    print(piece.image, ' ', end='')
                else:
                    print(piece, ' ', end='')
            print(index1 + 1, ' ', end='')
            print("")

        print("   ", end='')
        for i in letters:
            print(i, ' ', end='')
        print("")

    def pressured(self, color, pos, exceptions=None, show=False):
        if exceptions is None:
            exceptions = []

        for piece in self.pieces:
            if piece.color != color and piece not in exceptions:
                if piece.checkMove(pos):
                    if not self.testCheck(piece.pos, pos):
                        if show:
                            print(piece.image, piece.pos)
                        return True
        return False

    def check(self, color):
        # Find the position of the king
        if color == "black":
            king_pos = self.black_king.pos
        else:
            king_pos = self.white_king.pos

        # Check if any piece can move to that position
        if self.pressured(color, king_pos):
            return True
        return False

    def checkMate(self, color):
        if not self.check(color):
            return False
        mate_pieces = []

        enemy_color = color_switch[color]

        # Find the position of the king
        if color == "black":
            king_pos = self.black_king.pos
            king = self.black_king
        else:
            king_pos = self.white_king.pos
            king = self.white_king

        # Find the pieces pressuring the king
        for i in self.pieces:
            if i.color != color:
                if i.checkMove(king_pos):
                    mate_pieces.append(i)

        # Checks if the king can move away
        for i in self.board_pos:
            for n in i:
                if king.checkMove(n):
                    if not self.testCheck(king.pos, n):
                        print(f"King can move to square {n}")
                        return False

        # Checks how many pieces are delivering checkmate (it is only possible to block one piece)
        if len(mate_pieces) <= 1:
            mate_piece = mate_pieces[0]

            # Checks if the piece delivering check can be taken
            if self.pressured(enemy_color, mate_piece.pos, exceptions=[king], show=True):
                print("Piece can be taken")
                return False

            # Checks if a piece can block checkmate
            if "r" or "q" in mate_piece.name:
                if king_pos["row"] == mate_piece.pos["row"]:
                    for i in self.getRankPos(mate_piece.pos, king_pos):
                        for piece in self.pieces:
                            if piece.color == color:
                                if piece.checkMove(i):
                                    if not self.testCheck(piece.pos, i):
                                        return False
                if king_pos["col"] == mate_piece.pos["col"]:
                    for i in self.getFilePos(mate_piece.pos, king_pos):
                        for piece in self.pieces:
                            if piece.color == color:
                                if piece.checkMove(i):
                                    if not self.testCheck(piece.pos, i):
                                        return False
            if "b" or "q" in mate_piece.name:
                if abs(mate_piece.pos["row"] - king_pos["row"]) == abs(mate_piece.pos["col"] - king_pos["col"]):
                    for i in self.getDiagonalPos(mate_piece.pos, king_pos):
                        for piece in self.pieces:
                            if piece.color == color:
                                if piece.checkMove(i):
                                    if not self.testCheck(piece.pos, i):
                                        return False
        return True

    def stalemateNoMoves(self, color):
        if self.check(color):
            return False
        for i in self.pieces:
            if i.color == color:
                for x in self.board_pos:
                    for y in x:
                        if i.checkMove(y):
                            if not self.testCheck(i.pos, y):
                                return False
        return True

    def stalemateNoPieces(self):
        blackPieces = set()
        whitePieces = set()
        for i in self.pieces:
            if i.color == "black":
                blackPieces.add(type(i).__name__)
        for i in self.pieces:
            if i.color == "white":
                whitePieces.add(type(i).__name__)
        blackPieces = set(blackPieces)
        whitePieces = set(whitePieces)
        if blackPieces == {"King"} or blackPieces == {"Bishop", "King"} or blackPieces == {"King", "Knight"} or blackPieces == {"King", "Knight", "Knight"}:
            if whitePieces == {"King"} or whitePieces == {"Bishop", "King"} or whitePieces == {"King", "Knight"} or whitePieces == {"King", "Knight", "Knight"}:
                return True
        return False

    def stalemateDraw(self):
        if len(self.moves) >= 12:
            if self.moves[-4:] == self.moves[-8:-4] and self.moves[-8:-4] == self.moves[-12:-8]:
                return True
        return False

    def checkOpenFile(self, pos1, pos2):
        for i in self.getFilePos(pos1, pos2):
            if type(self.get(i)) != str:
                return False
        return True

    def checkOpenRank(self, pos1, pos2):
        for i in self.getRankPos(pos1, pos2):
            if type(self.get(i)) != str:
                return False
        return True

    def checkOpenDiagonal(self, pos1, pos2):
        for i in self.getDiagonalPos(pos1, pos2):
            if type(self.get(i)) != str:
                return False
        return True

    def testCheck(self, pos1, pos2):
        # Creates a copy of the board, and moves the piece on that copy to test if it results in check.
        copy = self.deepCopy()
        piece = copy.get(pos1)
        try:
            piece.move(pos2)
            if copy.check(piece.color):

                return True
        except TypeError:
            return False
        return False

    def newMove(self):
        # Used exclusively for making sure pawns that moved two spaces in one move are only vulnerable to en passants the turn they were moved.
        for i in self.pieces:
            if isinstance(i, Pawn):
                i.has_moved_two = False

    def castle(self, castle_type, color):
        rank = {"white": 0, "black": 7}[color]

        if castle_type.upper() == "SHORT":
            self.board[rank][4].move(configure(rank, 6))
            self.board[rank][7].move(configure(rank, 5))
            print(f"\n{color} has {castle_type.lower()} castled")
            self.has_castled[color] = True
            self.moves.append("SHORT_CASTLE")
        elif castle_type.upper() == "LONG":
            self.board[rank][4].move(configure(rank, 1))
            self.board[rank][0].move(configure(rank, 2))
            print(f"\n{color} has {castle_type.lower()} castled")
            self.has_castled[color] = True
            self.moves.append("LONG_CASTLE")

    def canCastle(self, castle_type, color):
        rook_case = {"LONG": 0, "SHORT": 7}[castle_type]
        rank_case = {"white": 0, "black": 7}[color]
        rook = self.board[rank_case][rook_case]
        king = self.board[rank_case][4]

        if self.has_castled[color]:
            print(f"Invalid Move: {color} has already castled")
            return False
        elif not (isinstance(rook, Rook) and isinstance(king, King)):
            print("Invalid Move: Pieces have moved away from their original positions")
            return False
        elif rook.has_moved or king.has_moved:
            print("Invalid Move: Pieces have moved away from their original positions")
            return False
        elif self.check(color):
            print("Invalid Move: Can't castle out of check")
            return False
        else:
            for square in self.getRankPos((configure(0, 4)), configure(0, rook)):
                if type(self.get(square)) != str:
                    print("Invalid Move: Pieces in the way of castle")
                    return False
                elif self.pressured(color, square):
                    print("Invalid Move: Can't castle through or into check")
                    return False
                else:
                    return True



