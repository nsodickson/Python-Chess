from bot import Bot, FENToOneHot
from board import *
from sys import argv
import pickle as pkl
from time import sleep

pieces = {"PAWN": Pawn, "ROOK": Rook, "BISHOP": Bishop, "QUEEN": Queen, "KNIGHT": Knight}


def play(board, ai_player=None, switch_view=False, show_FEN=False, show_eval=False):

    color = "white"

    while True:  # Game Loop
        if switch_view:
            board.print(color=color)
        else:
            board.print()
        if show_FEN:
            print(board.getFEN())

        print("\n" + "-"*50)

        if ai_player is not None and ai_player.color == color:
            move = ai_player.nextMove(board)
            print(f"\n{color[0].upper() + color[1:]}'s move: {detransformMove(move)}")
            board.parseMove(move, game_move=True)
            if show_eval:
                print(f"\nEval: {ai_player.forward(FENToOneHot(board.getFEN()))}")
            sleep(1)

        else:
            while True:
                # Turn Loop
                try:
                    move = input(f"\n{color[0].upper() + color[1:]}'s move: ").upper()
                    # Sentinel Value
                    if move == "PLAY.BREAK":
                        return 0

                    # Castling
                    if move == "SHORT CASTLE":
                        if board.canCastle("SHORT", color):
                            board.castle("SHORT", color)
                            print(f"\n{color} has short castled")
                            break
                        else:
                            print("\nInvalid Castle")
                            continue
                    elif move == "LONG CASTLE":
                        if board.canCastle("LONG", color):
                            board.castle("LONG", color)
                            print(f"\n{color} has long castled")
                            break
                        else:
                            print("\nInvalid Castle")
                            continue

                    move = transformMove(move)
                    pos1, pos2 = move["pos1"], move["pos2"]
                    piece = board.get(pos1)

                    if isinstance(piece, Piece):
                        if piece.color == color:
                            if piece.checkMove(pos2):
                                if not board.testCheck(pos1, pos2):
                                    board.parseMove(move)

                                    # Pawn Promotion
                                    if isinstance(piece, Pawn):
                                        if piece.color == "white" and piece.getPos()[0] == 7:
                                            new_piece = input("Promote your pawn: ").upper()
                                            board.take(piece.getPos())
                                            board.addNew(pieces[new_piece]("white", piece.getPos(), board), piece.getPos())
                                        elif piece.color == "black" and piece.getPos()[0] == 0:
                                            new_piece = input("Promote your pawn: ").upper()
                                            board.take(piece.getPos())
                                            board.addNew(pieces[new_piece]("black", piece.getPos(), board), piece.getPos())

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

                except (ValueError, TypeError, IndexError, KeyError):
                    print("\nInvalid move")
                    sleep(1)
                # End of Turn Loop

        if board.check(switch[color]):
            if board.checkMate(switch[color]):
                print(f"\nCHECKMATE, {color} wins")
                break
            else:
                print("\nCHECK")

        if board.stalemateNoMoves(color):
            print("\nSTALEMATE: No available moves")
            break
        elif board.stalemateNoPieces():
            print("\nSTALEMATE: No player can win")
            break
        elif board.stalemateDraw():
            print("\nSTALEMATE: Repeated moves")
            break
        elif board.fifty_move_counter >= 100:
            print("\nSTALEMATEF: Fifty move rule initiated")

        color = switch[color]

    if switch_view:
        board.print(color=color)
    else:
        board.print()
    if show_FEN:
        print(board.getFEN())


def playFromCommandLine():
    param1 = True if "switch" in argv else False
    param2 = True if "show-fen" in argv else False
    print("Welcome to Python Console Chess: ")
    sleep(0.5)
    play(board, switch_view=param2, show_FEN=param1)


def openBot():
    with open("bot.pkl", 'rb') as f:
        return pkl.load(f)


if __name__ == "__main__":
    board = Board()
    board.setup()

    print("Welcome to Python Chess")

    play(board)
