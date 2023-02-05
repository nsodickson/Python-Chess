from bot import EvalBot, Bot, FENToOneHot
from board import *
from sys import argv
import pickle as pkl
from time import sleep

# pos[0]: row, pos[1]: col
# move[0]: position of piece, move[1]: position of target, move[2] whether or not the move is an en passant

pieces = {"PAWN": Pawn, "ROOK": Rook, "BISHOP": Bishop, "QUEEN": Queen, "KNIGHT": Knight}


def play(board, ai_player=None, ai_uses_nn=True, switch_view=False, show_FEN=False, show_eval=False):

    color = "white"

    while True:  # Game Loop
        if switch_view:
            board.print(color=color)
        else:
            board.print()
        if show_FEN:
            print(board.getFEN())

        print("\n" + "="*50)

        if ai_player is not None and ai_player.color == color:
            move, score = ai_player.deepSearch(board, uses_nn=ai_uses_nn, depth=1)
            print(f"\n{color[0].upper() + color[1:]}'s move: {moveToString(move)}")
            board.parseMove(move, game_move=True)
            if show_eval:
                print(f"\nEval: {ai_player.forward(FENToOneHot(board.getFEN()))}")
            sleep(1)

        else:
            while True:  # Turn Loop
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

                    pos1, pos2, enPassant = moveToTuple(move, False)
                    enPassant = board.isEnPassant(pos1, pos2)
                    move = (pos1, pos2, enPassant)
                    piece = board.get(pos1)

                    if isinstance(piece, Piece):
                        if piece.color == color:
                            if piece.checkMove(pos2):
                                if not board.testCheck(pos1, pos2):
                                    board.parseMove(move, game_move=True)

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
        elif board.getNumMoves() >= 50:
            print("\nSTALEMATE: Fifty move rule initiated")

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


def loadBot(stage=None):
    with open("/Users/noah/Documents/GitHub/Python-Chess/bot.pkl", 'rb') as f:
        return pkl.load(f)


if __name__ == "__main__":
    board = Board()
    board.setup()

    print("Welcome to Python Chess")

    param1 = True if "switch" in argv else False
    param2 = True if "show-fen" in argv else False

    with_ai = input("Would you like to play with the ai? (y)es/(n)o: ").upper()
    if with_ai == "YES" or with_ai == "Y":
        bot = loadBot()
        bot.setColor(input("What color would you like the ai to be (type the full color)? ").lower())
        uses_nn = int(input("What algorithm would you like the ai to use: 1) Neural Networks 2) Piece counting algorithm: ")) == 1
    else:
        uses_nn=None
        bot = None

    print("="*50)

    play(board, ai_player=bot, ai_uses_nn=uses_nn, switch_view=param2, show_FEN=param1)
