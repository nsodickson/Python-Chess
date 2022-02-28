from board import *
from bot import *
from time import sleep
import sys


def play(board, switch=False, show_FEN=False):
    color = "white"
    while True:
        while True:
            try:
                if switch:
                    board.print(color=color)
                else:
                    board.print()
                if show_FEN:
                    print(board.getFEN())

                move = input(f"\n{color}'s move: ").upper()
                if move == "PLAY.BREAK":
                    return 0

                # Castling
                if move == "SHORT CASTLE":
                    if board.canCastle("SHORT", color):
                        board.castle("SHORT", color)
                        break
                    else:
                        continue
                elif move == "LONG CASTLE":
                    if board.canCastle("LONG", color):
                        board.castle("LONG", color)
                        break
                    else:
                        continue

                move = transformMove(move)
                pos1, pos2 = move["pos1"], move["pos2"]
                piece = board.get(pos1)

                if type(piece) != str:
                    if piece.color == color:
                        if piece.checkMove(pos2):
                            if not board.testCheck(piece.pos, pos2):
                                board.newMove()
                                piece.move(pos2)
                                board.moves.append(move)
                                break
                            else:
                                print("\nInvalid move: Can't Move Into Check")
                                sleep(1)
                        else:
                            print("\nInvalid move: Against Move Rules")
                            sleep(1)
                    else:
                        print("\nInvalid move: Wrong color piece")
                        sleep(1)
                else:
                    print("\nInvalid move: No piece there")
                    sleep(1)

            except (ValueError, TypeError, IndexError):
                print("\nInvalid move")
                sleep(1)

        if board.check(color_switch[color]):
            if board.checkMate(color_switch[color]):
                if switch:
                    board.print(color=color)
                else:
                    board.print()
                if show_FEN:
                    print(board.getFEN())
                print(f"\nCHECKMATE, {color} wins")
                return 0
            else:
                print("\nCHECK")

        if board.stalemateNoMoves("black"):
            if switch:
                board.print(color=color)
            else:
                board.print()
            if show_FEN:
                print(board.getFEN())
            sleep(1)
            print("\nSTALEMATE: No available moves")
            sleep(1)
            return 0
        elif board.stalemateNoPieces():
            if switch:
                board.print(color=color)
            else:
                board.print()
            if show_FEN:
                print(board.getFEN())
            sleep(1)
            print("\nSTALEMATE: No player can win")
            sleep(1)
            return 0
        elif board.stalemateDraw():
            if switch:
                board.print(color=color)
            else:
                board.print()
            if show_FEN:
                print(board.getFEN())
            sleep(1)
            print("\nSTALEMATE: Repeated moves")
            sleep(1)
            return 0
        color = color_switch[color]


def loadMoves(board, moves, switch=False, show_FEN=False, sleep_time=0.5):
    for color, move in moves:
        move = move.upper()

        try:
            print(f"\nMove: {move.lower()}, Color: {color}")

            if move == "PLAY.BREAK":
                return 0

            # Castling
            if move == "SHORT CASTLE":
                if board.canCastle("SHORT", color):
                    board.castle("SHORT", color)
                    if switch:
                        board.print(color=color)
                    else:
                        board.print()
                continue

            elif move == "LONG CASTLE":
                if board.canCastle("LONG", color):
                    board.castle("LONG", color)
                    if switch:
                        board.print(color=color)
                    else:
                        board.print()
                continue

            if type(move) == str:
                move = transformMove(move)
            pos1, pos2 = move["pos1"], move["pos2"]
            piece = board.get(pos1)

            if type(piece) != str:
                if piece.color == color:
                    if piece.checkMove(pos2):
                        if not board.testCheck(piece.pos, pos2):
                            board.newMove()
                            piece.move(pos2)
                            board.moves.append(move)
                        else:
                            print("\nInvalid move: Can't Move Into Check")
                            sleep(sleep_time)
                    else:
                        print("\nInvalid move: Against Move Rules")
                        sleep(sleep_time)
                else:
                    print("\nInvalid move: Wrong color piece")
                    sleep(sleep_time)
            else:
                print("\nInvalid move: No piece there")
                sleep(sleep_time)

        except (ValueError, TypeError, IndexError):
            print("\nInvalid move")
            sleep(sleep_time)

        if switch:
            board.print(color=color)
        else:
            board.print()
        if show_FEN:
            print(board.getFEN())

        if board.check(color_switch[color]):
            if board.checkMate(color_switch[color]):
                print(f"\nCHECKMATE, {color} wins")
                return 0
            else:
                print("\nCHECK")

        if board.stalemateNoMoves("black"):
            sleep(sleep_time)
            print("\nSTALEMATE: No available moves")
            sleep(sleep_time)
            return 0
        elif board.stalemateNoPieces():
            sleep(sleep_time)
            print("\nSTALEMATE: No player can win")
            sleep(sleep_time)
            return 0
        elif board.stalemateDraw():
            sleep(sleep_time)
            print("\nSTALEMATE: Repeated moves")
            sleep(sleep_time)
            return 0
        sleep(sleep_time)


class Tests:
    def __init__(self):
        self.scholars_mate = [("white", "e2xe4"), ("white", "d1xf3"), ("white", "f1xc4"), ("white", "f3xf7")]
        self.fools_mate = [("white", "f2xf3"), ("black", "e7xe5"), ("white", "g2xg4"), ("black", "d8xh4")]
        self.short_castle_white = [("white", "e2xe4"), ("white", "g1xf3"), ("white", "f1xe2"), ("white", "SHORT CASTLE")]
        self.wrong_castle_white = [("white", "e2xe4"), ("white", "g1xf3"), ("white", "f1xe2"), ("white", "LONG CASTLE")]
        self.long_castle_white = [("white", "d2xd4"), ("white", "c1xe3"), ("white", "d1xd2"), ("white", "b1xc3"), ("white", "LONG CASTLE")]
        self.invalid_moves = [("white", "e2xf3"), ("black", "h7xg7")]
        self.en_passant = [("white", "e2xe4"), ("white", "e4xe5"), ("black", "f7xf5"), ("white", "e5xf6")]
        self.invalid_en_passant = [("white", "e2xe4"), ("black", "f7xf6"), ("white", "e4xe5"), ("black", "f6xf5"), ("white", "e5xf6")]


if __name__ == "__main__":
    board = Board()
    tests = Tests()
    board.setup()

    # If you want to use this chess directly from the console, you can still turn on and off switch and show_FEN
    switch = True if "switch" in sys.argv else False
    show_FEN = True if "show-fen" in sys.argv else False
    print("Welcome to Python Console Chess: ")
    sleep(1)
    play(board, switch=switch, show_FEN=show_FEN)
