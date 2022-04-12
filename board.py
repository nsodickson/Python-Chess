from pieces import *
from extras import *

piece_icons = {"P": Pawn, "R": Rook, "N": Knight, "B": Bishop, "Q": Queen, "K": King}


class Board:
    def __init__(self):
        self.board = [["." for i in range(8)] for n in range(8)]
        self.width = len(self.board[0])
        self.height = len(self.board)

        # 2x2 array that contains the row-column configuration of each location on the board, instead of the piece in that location. Used for a variety of board tests.
        self.board_pos = [[(i, n) for n in range(self.width)] for i in range(self.height)]

        self.white_king = King("white", (0, 4), self)
        self.black_king = King("black", (7, 4), self)
        self.has_castled = {"white": False, "black": False}

        self.moves = []
        self.fifty_move_counter = 0
        self.pieces = []
        self.current_color = "white"

    def setup(self):
        # Piece Setup
        starting_white_pieces = [
            [Rook("white", (0, 0), self), Knight("white", (0, 1), self), Bishop("white", (0, 2), self), Queen("white", (0, 3), self), self.white_king,
             Bishop("white", (0, 5), self), Knight("white", (0, 6), self), Rook("white", (0, 7), self)],
            [Pawn("white", (1, i), self) for i in range(8)]]
        starting_black_pieces = [
            [Rook("black", (7, 0), self), Knight("black", (7, 1), self), Bishop("black", (7, 2), self), Queen("black", (7, 3), self), self.black_king,
             Bishop("black", (7, 5), self), Knight("black", (7, 6), self), Rook("black", (7, 7), self)],
            [Pawn("black", (6, i), self) for i in range(8)]]

        for i in starting_white_pieces:
            for n in i:
                self.addNew(n, n.getPos())
        for i in starting_black_pieces:
            for n in i:
                self.addNew(n, n.getPos())

    def empty(self):
        self.__init__()

    def reset(self):
        self.__init__()
        self.setup()

    def getFEN(self, fields=None):
        if fields is None:
            fields = [1, 2, 3, 4, 5, 6]

        # Returns a FEN string for the current state of the board.
        FEN = []

        # Field One
        if 1 in fields:
            for rank in self.board[::-1]:
                FEN.append("/")
                for square in rank:
                    if not isinstance(square, Piece):
                        if FEN[-1].isdigit():
                            FEN[-1] = str(int(FEN[-1]) + 1)
                        else:
                            FEN.append("1")
                    else:
                        FEN.append(square.FEN_char)
            FEN.append(" ")

        # Field Two
        if 2 in fields:
            FEN.append({"white": "w", "black": "b"}[self.current_color])
            FEN.append(" ")

        # Field Three
        if 3 in fields:
            if not self.has_castled["white"] and not self.white_king.has_moved:
                rook = self.get((0, 7))
                if isinstance(rook, Rook) and not rook.has_moved:
                    FEN.append("K")
                else:
                    FEN.append("-")
                rook = self.get((0, 0))
                if isinstance(rook, Rook) and not rook.has_moved:
                    FEN.append("Q")
            else:
                FEN.append("-")

            if not self.has_castled["black"] and not self.black_king.has_moved:
                rook = self.get((7, 7))
                if isinstance(rook, Rook) and not rook.has_moved:
                    FEN.append("k")
                else:
                    FEN.append("-")
                rook = self.get((7, 0))
                if isinstance(rook, Rook) and not rook.has_moved:
                    FEN.append("q")
            else:
                FEN.append("-")
            FEN.append(" ")

        # Field 4 En Passant Possibility
        if 4 in fields:
            FEN.append("-")
            for piece in self.pieces:
                if isinstance(piece, Pawn) and piece.has_moved_two:
                    print(piece)
                    if piece.color == "white":
                        FEN[-1] = f"{letters[piece.getPos()[1]]}{piece.getPos()[0]}"
                    elif piece.color == "black":
                        FEN[-1] = f"{letters[piece.getPos()[1]]}{piece.getPos()[0]+1}"
            FEN.append(" ")

        # Field 5 Halfmove counter
        if 5 in fields:
            FEN.append(str(self.fifty_move_counter))
            FEN.append(" ")

        # Field 6
        if 6 in fields:
            FEN.append(str(1 + int(len(self.moves)/2)))
            FEN.append(" ")

        return "".join(FEN[1:])

    def loadFEN(self, FEN):
        self.empty()

        # Resets the board to the position of an inputted FEN string with all fields.
        FEN = FEN.split()

        try:
            FEN_array = [i for i in FEN[0] if i != "/"]
            FEN_index = 0
            for rank in self.board_pos[::-1]:
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
                                self.white_king.setPos(pos)
                            else:
                                self.addNew(piece_icons[current]("white", pos, self), pos)
                        else:
                            if current == "k":
                                self.add(self.black_king, pos)
                                self.black_king.setPos(pos)
                            else:
                                self.addNew(piece_icons[current.upper()]("black", pos, self), pos)
                                
            # Currently Ignore Other Fields

        except (KeyError, IndexError):
            print("Invalid FEN string")

    def transpose(self, board="self.board"):
        if board == "self.board":
            return [[self.board[i][n] for i in range(self.width)] for n in range(self.height)]
        elif board == "self.board_pos":
            return [[self.board_pos[i][n] for i in range(self.width)] for n in range(self.height)]

    def add(self, piece, pos):
        # Put a piece on the board without adding it to the board's internal list of pieces. This is used for moving pieces already in the game.
        self.board[pos[0]][pos[1]] = piece
        return piece

    def addNew(self, piece, pos):
        # Put a new piece on the board, and add it to the board's internal list of pieces. It is now a new piece in the game.
        if piece not in self.pieces and isinstance(piece, Piece):
            self.pieces.append(piece)
        return self.add(piece, pos)

    def remove(self, pos):
        # Replace the piece with the typical black or white square without removing it from the board's internal list of pieces
        square = self.get(pos)
        self.add(".", pos)
        return square

    def take(self, pos):
        square = self.get(pos)
        # Replace the piece with the typical black or white square, and remove it from the board's internal list of pieces. It is now not part of the game.
        if square in self.pieces:
            self.pieces.remove(square)
        return self.remove(pos)

    def get(self, pos):
        return self.board[pos[0]][pos[1]]

    def getFilePos(self, pos1=None, pos2=None, move=None):
        if pos1 is None and pos2 is None:
            pos1, pos2 = move["pos1"], move["pos2"]

        if pos1[0] > pos2[0]:
            return self.transpose("self.board_pos")[pos1[1]][(pos2[0] + 1):pos1[0]]
        elif pos2[0] > pos1[0]:
            return self.transpose("self.board_pos")[pos1[1]][(pos1[0] + 1):pos2[0]]

    def getRankPos(self, pos1=None, pos2=None, move=None):
        if pos1 is None and pos2 is None:
            pos1, pos2 = move["pos1"], move["pos2"]

        if pos1[1] > pos2[1]:
            return self.board_pos[pos1[0]][(pos2[1] + 1):pos1[1]]
        elif pos2[1] > pos1[1]:
            return self.board_pos[pos1[0]][(pos1[1] + 1):pos2[1]]

    def getDiagonalPos(self, pos1=None, pos2=None, move=None):
        if pos1 is None and pos2 is None:
            pos1, pos2 = move["pos1"], move["pos2"]

        if pos1[0] > pos2[0] and pos1[1] > pos2[1]:
            return [self.board_pos[pos1[0] - i][pos1[1] - i] for i in range(1, abs(pos2[0] - pos1[0]))]
        elif pos1[0] < pos2[0] and pos1[1] < pos2[1]:
            return [self.board_pos[i + pos1[0]][i + pos1[1]] for i in range(1, abs(pos2[0] - pos1[0]))]
        elif pos1[0] > pos2[0] and pos1[1] < pos2[1]:
            return [self.board_pos[pos1[0] - i][i + pos1[1]] for i in range(1, abs(pos2[0] - pos1[0]))]
        elif pos1[0] < pos2[0] and pos1[1] > pos2[1]:
            return [self.board_pos[i + pos1[0]][pos1[1] - i] for i in range(1, abs(pos2[0] - pos1[0]))]

    def print(self, color="white"):
        if color == "white":
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
                if isinstance(piece, Piece):
                    print(piece.image, ' ', end='')
                else:
                    print("■" if (index1 + index2) % 2 == 0 else "□", ' ', end='')
            print(index1 + 1, ' ', end='')
            print("")

        print("   ", end='')
        for i in letters:
            print(i, ' ', end='')
        print("")

    def pressured(self, color, pos, exceptions=None):
        if exceptions is None:
            exceptions = []

        for piece in self.pieces:
            if piece.color != color and piece not in exceptions:
                if piece.checkMove(pos) and not self.testCheck(piece.getPos(), pos):
                    return True
        return False

    def check(self, color):

        # Find the position of the king
        if color == "black":
            king_pos = self.black_king.getPos()
        else:
            king_pos = self.white_king.getPos()

        # Check if any piece can move to that position, but it doesn't matter if said move causes check.
        for piece in self.pieces:
            if piece.color != color:
                if piece.checkMove(king_pos):
                    return True
        return False

    def checkMate(self, color):
        mate_pieces = []
        enemy_color = switch[color]

        # Find the position of the king
        if color == "black":
            king_pos = self.black_king.getPos()
            king = self.black_king
        else:
            king_pos = self.white_king.getPos()
            king = self.white_king

        # Find the pieces pressuring the king and assert that at least one piece is pressuring the king.
        for i in self.pieces:
            if i.color != color:
                if i.checkMove(king_pos):
                    mate_pieces.append(i)
        if len(mate_pieces) == 0:
            return False

        # Checks if the king can move away
        for i in self.board_pos:
            for n in i:
                if king.checkMove(n) and not self.testCheck(king.getPos(), n):
                    return False

        # Checks how many pieces are delivering checkmate (it is only possible to block one piece)
        if len(mate_pieces) <= 1:
            mate_piece = mate_pieces[0]

            # Checks if the piece delivering check can be taken
            if self.pressured(enemy_color, mate_piece.getPos(), exceptions=[king]):
                return False

            # Checks if a piece can block checkmate
            if "r" or "q" in mate_piece.name:
                if king_pos[0] == mate_piece.getPos()[0]:
                    for i in self.getRankPos(mate_piece.getPos(), king_pos):
                        for piece in self.pieces:
                            if piece.color == color:
                                if piece.checkMove(i) and not self.testCheck(piece.getPos(), i):
                                    return False
                if king_pos[1] == mate_piece.getPos()[1]:
                    for i in self.getFilePos(mate_piece.getPos(), king_pos):
                        for piece in self.pieces:
                            if piece.color == color:
                                if piece.checkMove(i) and not self.testCheck(piece.getPos(), i):
                                    return False
            if "b" or "q" in mate_piece.name:
                if abs(mate_piece.getPos()[0] - king_pos[0]) == abs(mate_piece.getPos()[1] - king_pos[1]):
                    for i in self.getDiagonalPos(mate_piece.getPos(), king_pos):
                        for piece in self.pieces:
                            if piece.color == color:
                                if piece.checkMove(i) and not self.testCheck(piece.getPos(), i):
                                    return False
        return True

    def stalemateNoMoves(self, color):
        if self.check(color):
            return False
        for i in self.pieces:
            if i.color == color:
                for x in self.board_pos:
                    for y in x:
                        if i.checkMove(y) and not self.testCheck(i.getPos(), y):
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

    def checkOpenFile(self, pos1=None, pos2=None, move=None):
        if pos1 is None and pos2 is None:
            pos1, pos2 = move["pos1"], move["pos2"]

        for i in self.getFilePos(pos1, pos2):
            if isinstance(self.get(i), Piece):
                return False
        return True

    def checkOpenRank(self, pos1=None, pos2=None, move=None):
        if pos1 is None and pos2 is None:
            pos1, pos2 = move["pos1"], move["pos2"]

        for i in self.getRankPos(pos1, pos2):
            if isinstance(self.get(i), Piece):
                return False
        return True

    def checkOpenDiagonal(self, pos1=None, pos2=None, move=None):
        if pos1 is None and pos2 is None:
            pos1, pos2 = move["pos1"], move["pos2"]

        for i in self.getDiagonalPos(pos1, pos2):
            if isinstance(self.get(i), Piece):
                return False
        return True

    def testCheck(self, pos1=None, pos2=None, move=None):
        is_check = False

        if move is None:
            move = configureMove(pos1, pos2)
        if pos1 is None and pos2 is None:
            pos1, pos2 = move["pos1"], move["pos2"]

        piece = self.get(pos1)
        target = self.get(pos2)

        self.parseMove(move, game_move=False)

        if self.check(piece.color):
            is_check = True

        self.parseMoveUndo(move, target, piece.color)

        return is_check

    def newMove(self):
        # Used exclusively for making sure pawns that moved two spaces in one move are only vulnerable to en passants the turn they were moved.
        for i in self.pieces:
            if isinstance(i, Pawn):
                i.has_moved_two = False

    def castle(self, castle_type, color):
        rank = {"white": 0, "black": 7}[color]

        if castle_type == "SHORT":
            self.board[rank][4].move((rank, 6))
            self.board[rank][7].move((rank, 5))
            self.has_castled[color] = True
            self.moves.append("SHORT_CASTLE")
        elif castle_type == "LONG":
            self.board[rank][4].move((rank, 2))
            self.board[rank][0].move((rank, 3))
            self.has_castled[color] = True
            self.moves.append("LONG_CASTLE")

    def canCastle(self, castle_type, color):
        rook_case = {"LONG": 0, "SHORT": 7}[castle_type]
        rank_case = {"white": 0, "black": 7}[color]
        rook = self.board[rank_case][rook_case]
        king = self.board[rank_case][4]

        if self.has_castled[color]:
            return False
        elif not (isinstance(rook, Rook) and not isinstance(king, King)):
            return False
        elif rook.has_moved or king.has_moved:
            return False
        elif self.check(color):
            return False
        else:
            for square in self.getRankPos((rank_case, 4), (rank_case, rook_case)):
                if isinstance(self.get(square), Piece):
                    return False
                elif self.pressured(color, square):
                    return False
        return True

    def allMoves(self, color):
        all_moves = []
        for rank in self.board_pos:
            for square in rank:
                for piece in self.pieces:
                    if piece.color == color:
                        if piece.checkMove(square) and not self.testCheck(piece.getPos(), square):
                            all_moves.append(configureMove(piece.getPos(), square))
        if self.canCastle("SHORT", color):
            if color == "black":
                all_moves.append("short_castle")
            else:
                all_moves.append("SHORT_CASTLE")
        if self.canCastle("LONG", color):
            if color == "black":
                all_moves.append("long_castle")
            else:
                all_moves.append("LONG_CASTLE")

        return all_moves

    def parseMove(self, move, game_move=True):
        try:
            if game_move:
                self.newMove()

            if move == "SHORT_CASTLE":
                self.castle("SHORT", "white")
            elif move == "short_castle":
                self.castle("SHORT", "black")
            elif move == "LONG_CASTLE":
                self.castle("LONG", "white")
            elif move == "long_castle":
                self.castle("LONG", "black")
            else:
                if game_move:  # Increment the # of moves since a capture or a pawn move for FEN strings
                    if isinstance(self.get(move["pos2"]), Piece) or isinstance(self.get(move["pos1"]), Pawn):
                        self.fifty_move_counter = 0
                    else:
                        self.fifty_move_counter += 1
                
                self.get(move["pos1"]).move(move["pos2"], game_move=game_move)

            if game_move:
                self.moves.append(move)
                self.current_color = switch[self.current_color]

        except (TypeError, AttributeError):
            print("Move Parsing Error")

    def parseMoveUndo(self, move, target=None, color=None):
        try:
            rank = {"white": 0, "black": 7}[color]

            if move == "SHORT_CASTLE":
                king, rook = self.remove((rank, 6)),  self.remove((rank, 5))
                if isinstance(king, Piece) and isinstance(rook, Piece):
                    self.add(king, (rank, 4))
                    king.setPos((rank, 4))
                    self.add(rook, (rank, 7))
                    rook.setPos((rank, 7))

            elif move == "LONG_CASTLE":
                king, rook = self.remove((rank, 2)), self.remove((rank, 3))
                if isinstance(king, Piece) and isinstance(rook, Piece):
                    self.add(king, (rank, 4))
                    king.setPos((rank, 4))
                    self.add(rook, (rank, 0))
                    rook.setPos((rank, 0))

            else:
                piece = self.remove(move["pos2"])
                if isinstance(piece, Piece):
                    self.add(piece, move["pos1"])
                    piece.setPos(move["pos1"])
                    if isinstance(target, Piece):
                        self.addNew(target, target.getPos())  # You have to use target.getPos because of en passants
        except (TypeError, AttributeError):
            print("Move Undo Parsing Error. Move to undo likely hasn't been made.")



