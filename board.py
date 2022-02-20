from pieces import *
from extras import *


class Board:
    def __init__(self):
        self.board = [["□" if (i+n) % 2 == 0 else "■" for i in range(8)] for n in range(8)]
        self.width = len(self.board[0])
        self.height = len(self.board)

        # 2x2 array that contains the row-column configuration of each location on the board, instead of the piece in that location. Used for a variety of board tests.
        self.board_pos = [[configure(i, n) for n in range(self.width)] for i in range(self.height)]
        self.white_king = King("white", configure(0, 4), self)
        self.black_king = King("black", configure(7, 4), self)
        self.starting_white_pieces = [[Rook("white", configure(0, 0), self), Knight("white", configure(0, 1), self), Bishop("white", configure(0, 2), self), Queen("white", configure(0, 3), self), self.white_king, Bishop("white", configure(0, 5), self), Knight("white", configure(0, 6), self), Rook("white", configure(0, 7), self)],
                                      [Pawn("white", configure(1, i), self) for i in range(8)]]
        self.starting_black_pieces = [[Rook("black", configure(7, 0), self), Knight("black", configure(7, 1), self), Bishop("black", configure(7, 2), self), Queen("black", configure(7, 3), self), self.black_king, Bishop("black", configure(7, 5), self), Knight("black", configure(7, 6), self), Rook("black", configure(7, 7), self)],
                                      [Pawn("black", configure(6, i), self) for i in range(8)]]
        self.pieces = []

        # Piece Setup
        for i in self.starting_white_pieces:
            for n in i:
                self.add(n, n.pos, new=True)
        for i in self.starting_black_pieces:
            for n in i:
                self.add(n, n.pos, new=True)

    def transpose(self, board="self.board"):
        if board == "self.board":
            return [[self.board[i][n] for i in range(self.width)] for n in range(self.height)]
        elif board == "self.board_pos":
            return [[self.board_pos[i][n] for i in range(self.width)] for n in range(self.height)]

    def add(self, piece, move, new=False):
        if new is True:
            if piece not in self.pieces and not type(piece) == str:
                self.pieces.append(piece)
        self.board[move["row"]][move["col"]] = piece

    def remove(self, pos, take=False):
        if take is True:
            if self.get(pos) in self.pieces:
                self.pieces.remove(self.get(pos))
        if (pos["row"]+pos["col"]) % 2 == 0:
            self.board[pos["row"]][pos["col"]] = "□"
        else:
            self.board[pos["row"]][pos["col"]] = "■"

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

    def print(self, color="WHITE"):

        if color.upper() == "WHITE":
            printable_board = list(enumerate(self.board))[::-1]
        else:
            printable_board = list(enumerate(self.board))

        # Prints the board so chess can be played on the console
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

    def pressured(self, color, pos):
        for i in self.pieces:
            if not i.color == color:
                if i.checkMove(pos):
                    if not self.testCheck(i, pos):
                        return True
        return False

    def check(self, color):
        # Find the position of the king
        if color == "white":
            king_pos = self.white_king.pos
        elif color == "black":
            king_pos = self.black_king.pos
        else:
            return False
        # Check if any piece can move to that position
        if type(king_pos["row"]) == int and type(king_pos["col"]) == int:
            if self.pressured(color, king_pos):
                return True
        return False

    def checkMate(self, color):
        if not self.check(color):
            return False
        matePieces = []
        # Find the position of the king
        if color == "white":
            king_pos = self.white_king.pos
            king = self.white_king
            enemyColor = "black"
        elif color == "black":
            king_pos = self.black_king.pos
            king = self.black_king
            enemyColor = "white"
        else:
            return False
        # Find the pieces pressuring the king
        for i in self.pieces:
            if not i.color == color:
                if i.checkMove(king_pos):
                    matePieces.append(i)
        # Checks if the king can move away
        for i in self.board_pos:
            for n in i:
                if king.checkMove(n):
                    if not self.testCheck(king, n):
                        return False
        # Checks how many pieces are delivering checkmate (it is only possible to block one piece)
        if len(matePieces) <= 1:
            matePiece = matePieces[0]
            # Checks if the piece delivering check can be taken
            if self.pressured(enemyColor, matePiece.pos):
                return False
            # Checks if a piece can block checkmate
            if "r" or "q" in matePiece.name:
                if king_pos["row"] == matePiece.pos["row"]:
                    for i in self.getRankPos(matePiece.pos, king_pos):
                        for n in self.pieces:
                            if n.checkMove(i):
                                if not self.testCheck(n, i):
                                    return False
                if king_pos["col"] == matePiece.pos["col"]:
                    for i in self.getFilePos(matePiece.pos, king_pos):
                        for n in self.pieces:
                            if n.checkMove(i):
                                if not self.testCheck(n, i):
                                    return False
            if "b" or "q" in matePiece.name:
                if abs(matePiece.pos["row"] - king_pos["row"]) == abs(matePiece.pos["col"] - king_pos["col"]):
                    for i in self.getDiagonalPos(matePiece.pos, king_pos):
                        for n in self.pieces:
                            if n.checkMove(i):
                                if not self.testCheck(n, i):
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
                            if not self.testCheck(i, y):
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

    def stalemateDraw(self, moves):
        if len(moves) >= 12:
            if moves[-4:] == moves[-8:-4] == moves[-12:-8]:
                return True
        return False

    def checkOpenFile(self, pos1, pos2):
        if pos1["row"] > pos2["row"]:
            for i in self.transpose()[pos1["col"]][(pos2["row"] + 1):pos1["row"]]:
                if not type(i) == str:
                    return False
            return True
        elif pos2["row"] > pos1["row"]:
            for i in self.transpose()[pos1["col"]][(pos1["row"] + 1):pos2["row"]]:
                if not type(i) == str:
                    return False
            return True

    def checkOpenRank(self, pos1, pos2):
        if pos1["col"] > pos2["col"]:
            for i in self.board[pos1["row"]][(pos2["col"] + 1):pos1["col"]]:
                if not type(i) == str:
                    return False
            return True
        elif pos2["col"] > pos1["col"]:
            for i in self.board[pos1["row"]][(pos1["col"] + 1):pos2["col"]]:
                if not type(i) == str:
                    return False
            return True

    def checkOpenDiagonal(self, pos1, pos2):
        if pos1["row"] > pos2["row"] and pos1["col"] > pos2["col"]:
            for i in [self.board[pos1["row"] - i][pos1["col"] - i] for i in range(1, abs(pos2["row"] - pos1["row"]))]:
                if not type(i) == str:
                    return False
            return True
        elif pos1["row"] < pos2["row"] and pos1["col"] < pos2["col"]:
            for i in [self.board[i + pos1["row"]][i + pos1["col"]] for i in range(1, abs(pos2["row"] - pos1["row"]))]:
                if not type(i) == str:
                    return False
            return True
        elif pos1["row"] > pos2["row"] and pos1["col"] < pos2["col"]:
            for i in [self.board[pos1["row"] - i][i + pos1["col"]] for i in range(1, abs(pos2["row"] - pos1["row"]))]:
                if not type(i) == str:
                    return False
            return True
        elif pos1["row"] < pos2["row"] and pos1["col"] > pos2["col"]:
            for i in [self.board[i + pos1["row"]][pos1["col"] - i] for i in range(1, abs(pos2["row"] - pos1["row"]))]:
                if not type(i) == str:
                    return False
            return True

    def testCheck(self, piece, pos2):
        pos1 = piece.pos
        target = self.get(pos2)
        piece.move(pos2)
        if self.check(piece.color):
            piece.undoMove(target, pos1)
            return True
        else:
            piece.undoMove(target, pos1)
            return False

    def newMove(self, piece):

        # Used exclusively for making sure pawns that moved two spaces in one move are only vulnerable to en passants the turn they were moved (extremely niche case)
        for i in self.pieces:
            if not i == piece and isinstance(i, Pawn):
                i.has_moved_two = False
