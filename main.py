from board import *
from extras import *
from time import *


def play(switch=True):
    board = Board()
    white_castled = False
    black_castled = False
    moves = []

    while True:

        # White Move
        while True:
            try:
                board.print(color="white")
                move = input("\nWhite's Move: ").upper()
                if move == "PLAY.BREAK":
                    return 0

                # Castling
                if move == "SHORT CASTLE":
                    if white_castled:
                        print("\nInvalid Move: Already Castled")
                        continue
                    if not board.starting_white_pieces[0][4].hasMoved and not board.starting_white_pieces[0][7].hasMoved:
                        if board.checkOpenRank(configure(0, 4), configure(0, 7)):
                            if not board.check("white"):
                                for i in board.getRankPos(configure(0, 4), configure(0, 7)):
                                    if not board.pressured("white", i):
                                        board.get(configure(0, 4)).move(configure(0, 6))
                                        board.get(configure(0, 7)).move(configure(0, 5))
                                        print("\nWhite has Castled")
                                        white_castled = True
                                        moves.append("SHORTCASTLE")
                                        sleep(1)
                                        break
                                    else:
                                        print("\nInvalid Move: Can't castle through check")
                                        sleep(1)
                                        continue
                            else:
                                print("\nInvalid Move: Can't Castle out of check")
                                sleep(1)
                                continue
                        else:
                            print("\nInvalid Move: Pieces in the way of castle")
                            sleep(1)
                            continue
                    else:
                        print("\nInvalid Move: Pieces have moved from their starting positions")
                        sleep(1)
                        continue
                elif move == "LONG CASTLE":
                    if white_castled:
                        print("\nInvalid Move: Already Castled")
                    if not board.starting_white_pieces[0][4].hasMoved and not board.starting_white_pieces[0][0].hasMoved:
                        if board.checkOpenRank(configure(0, 4), configure(0, 0)):
                            if not board.check("white"):
                                for i in board.getRankPos(configure(0, 4), configure(0, 0)):
                                    if not board.pressured("white", i):
                                        board.get(configure(0, 4)).move(configure(0, 2))
                                        board.get(configure(0, 0)).move(configure(0, 3))
                                        print("\nWhite has Castled")
                                        white_castled = True
                                        moves.append("LONGCASTLE")
                                        sleep(1)
                                        break
                                    else:
                                        print("\nInvalid Move: Can't castle through check")
                                        sleep(1)
                                        continue
                                if white_castled:
                                    break
                            else:
                                print("\nInvalid Move: Can't Castle out of check")
                                sleep(1)
                                continue
                        else:
                            print("\nInvalid Move: Pieces in the way of castle")
                            sleep(1)
                            continue
                    else:
                        print("\nInvalid Move: Pieces have moved from their starting positions")
                        sleep(1)
                        continue

                pos1 = {"row": int(move[1]) - 1, "col": letters.index(move[0])}
                pos2 = {"row": int(move[4]) - 1, "col": letters.index(move[3])}
                piece = board.get(pos1)

                if piece in board.pieces:
                    if piece.color == "white":
                        if piece.checkMove(pos2):
                            if not board.testCheck(piece, pos2):
                                piece.move(pos2)
                                moves.append({"pos1": pos1, "pos2": pos2})
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

        if board.check("black"):
            if board.checkMate("black"):
                board.print()
                print("\nCHECKMATE, White Wins")
                return 1
            else:
                print("\nCHECK")

        if board.stalemateNoMoves("black"):
            board.print()
            sleep(1)
            print("\nSTALEMATE: No available moves")
            sleep(1)
            return 0
        elif board.stalemateNoPieces():
            board.print()
            sleep(1)
            print("\nSTALEMATE: No player can win")
            sleep(1)
            return 0
        elif board.stalemateDraw(moves):
            board.print()
            sleep(1)
            print("\nSTALEMATE: Repeated moves")
            sleep(1)
            return 0

        # Black Move
        while True:
            try:
                if switch:
                    board.print(color="black")
                else:
                    board.print(color="white")

                move = input("\nBlack's Move: ").upper()
                if move == "PLAY.BREAK":
                    return 0

                # Castling
                if move == "SHORT CASTLE":
                    if black_castled:
                        print("\nInvalid Move: Already Castled")
                        continue
                    if not board.starting_black_pieces[0][4].hasMoved and not board.starting_black_pieces[0][7].hasMoved:
                        if board.checkOpenRank(configure(7, 4), configure(7, 7)):
                            if not board.check("white"):
                                for i in board.getRankPos(configure(7, 4), configure(7, 7)):
                                    if not board.pressured("white", i):
                                        board.get(configure(7, 4)).move(configure(7, 6))
                                        board.get(configure(7, 7)).move(configure(7, 5))
                                        print("\nBlack has Castled")
                                        black_castled = True
                                        moves.append("SHORTCASTLE")
                                        sleep(1)
                                        break
                                    else:
                                        print("\nInvalid Move: Can't castle through check")
                                        sleep(1)
                                        continue
                                if black_castled:
                                    break
                            else:
                                print("\nInvalid Move: Can't Castle out of check")
                                sleep(1)
                                continue
                        else:
                            print("\nInvalid Move: Pieces in the way of castle")
                            sleep(1)
                            continue
                    else:
                        print("\nInvalid Move: Pieces have moved from their starting positions")
                        sleep(1)
                        continue
                elif move == "LONG CASTLE":
                    if black_castled:
                        print("\nInvalid Move: Already Castled")
                        continue
                    if not board.starting_black_pieces[0][4].hasMoved and not board.starting_black_pieces[0][0].hasMoved:
                        if board.checkOpenRank(configure(7, 4), configure(7, 0)):
                            if not board.check("white"):
                                for i in board.getRankPos(configure(7, 4), configure(7, 0)):
                                    if not board.pressured("white", i):
                                        board.get(configure(7, 4)).move(configure(7, 2))
                                        board.get(configure(7, 0)).move(configure(7, 3))
                                        print("\nBlack has Castled")
                                        black_castled = True
                                        moves.append("LONGCASTLE")
                                        sleep(1)
                                        break
                                    else:
                                        print("\nInvalid Move: Can't castle through check")
                                        sleep(1)
                                        continue
                            else:
                                print("\nInvalid Move: Can't Castle out of check")
                                sleep(1)
                                continue
                        else:
                            print("\nInvalid Move: Pieces in the way of castle")
                            sleep(1)
                            continue
                    else:
                        print("\nInvalid Move: Pieces have moved from their starting positions")
                        sleep(1)
                        continue

                pos1 = {"row": int(move[1]) - 1, "col": letters.index(move[0])}
                pos2 = {"row": int(move[4]) - 1, "col": letters.index(move[3])}
                piece = board.get(pos1)

                if piece in board.pieces:
                    if piece.color == "black":
                        if piece.checkMove(pos2):
                            if not board.testCheck(piece, pos2):
                                piece.move(pos2)
                                moves.append({"pos1": pos1, "pos2": pos2})
                                break
                            else:
                                print("\nInvalid move: Can't Move Into Check")
                                print("\nWhite has Castled")
                                sleep(1)
                        else:
                            print("\ninvalid move: Against Move Rules")
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

        if board.check("white"):
            if board.checkMate("white"):
                board.print()
                sleep(1)
                print("\nCHECKMATE, Black Wins")
                sleep(1)
                return -1
            else:
                print("\nCHECK")

        if board.stalemateNoMoves("white"):
            board.print()
            sleep(1)
            print("\nSTALEMATE: No available moves")
            sleep(1)
            return 0
        elif board.stalemateNoPieces():
            board.print()
            sleep(1)
            print("\nSTALEMATE: No player can win")
            sleep(1)
            return 0
        elif board.stalemateDraw(moves):
            board.print()
            sleep(1)
            print("\nSTALEMATE: Repeated moves")
            sleep(1)
            return 0


if __name__ == "__main__":
    play(switch=False)
