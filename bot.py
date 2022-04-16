from board import *
import random as rand
import torch
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle as pkl

global ChessDataset
global trainLoop
global testLoop
global yToTensor

def FENToOneHot(FEN):
    FEN = FEN.split()
    array = []

    # Field One (More Fields to come)
    for i in FEN[0].split("/"):
        array.append([])
        for n in i:
            if n.isalpha():
                array[-1].append(one_hot_pieces[n])
            elif n.isdigit():
                for q in range(int(n)):
                    array[-1].append(one_hot_pieces["."])

    return torch.tensor(array, dtype=torch.float32)

class EvalBot(torch.nn.Module):
    def __init__(self):
        super(EvalBot, self).__init__()
        self.flatten_train = torch.nn.Flatten(start_dim=1)
        self.flatten_apply = torch.nn.Flatten(start_dim=0)
        self.linear_relu_stack = torch.nn.Sequential(
            torch.nn.Linear(768, 600),
            torch.nn.ReLU(),
            torch.nn.Linear(600, 500),
            torch.nn.ReLU(),
            torch.nn.Linear(500, 400),
            torch.nn.ReLU(),
            torch.nn.Linear(400, 300),
            torch.nn.ReLU(),
            torch.nn.Linear(300, 200),
            torch.nn.ReLU(),
            torch.nn.Linear(200, 100),
            torch.nn.ReLU(),
            torch.nn.Linear(100, 1)
        )

    def trainForward(self, board_state):
        board_state = self.flatten_train(board_state)
        board_state = self.linear_relu_stack(board_state)
        return board_state

    def forward(self, board_state):
        board_state = self.flatten_apply(board_state)
        board_state = self.linear_relu_stack(board_state)
        return board_state[0]

class Bot:
    def __init__(self, color, eval_early, eval_middle, eval_late):
        self.color = color
        self.eval_early = eval_early
        self.eval_middle = eval_middle
        self.eval_late = eval_late
    
    def setColor(self, color):
        self.color = color
    
    def eval(self, FEN, turns):
        if turns <= 18:  # Arbitrary Number
            return self.eval_early.forward(FENToOneHot(FEN))
        elif turns <= 31:  # Arbitrary Number
            return self.eval_middle.forward(FENToOneHot(FEN))
        else:
            return self.eval_late.forward(FENToOneHot(FEN))

    def random(self, board):
        all_moves = board.allMoves(self.color)
        rand.shuffle(all_moves)
        return all_moves[0]

    def deepSearch(self, board, depth=2, color=None):
        if color is None:
            color = self.color
        else:
            color = color

        best_move = None
        best_score = None

        all_moves = board.allMoves(color)
        rand.shuffle(all_moves)

        for move in all_moves:
            if type(move) == dict:
                target = board.get(move["pos2"])
            else:
                target = None
            piece = board.get(move["pos1"])

            board.parseMove(move, game_move=False)

            if depth > 1:
                next_move = self.deepSearch(board, depth-1, color=switch[color])
                next_piece = board.get(next_move["pos1"])
                next_target = board.get(next_move["pos2"])

                board.parseMove(next_move, game_move=False)

                if self.color == "black":
                    score = -1 * self.eval(board.getFEN(fields=[1]), 1+int(board.half_move_counter/2))
                else:
                    score = self.eval(board.getFEN(fields=[1]), 1+int(board.half_move_counter/2))

                if best_score is None or score > best_score:
                    best_score = score
                    best_move = move

                board.parseMoveUndo(next_move, next_target, next_piece.color)

            else:
                
                if self.color == "black":
                    score = -1 * self.eval(board.getFEN(fields=[1]), 1+int(board.half_move_counter/2))
                else:
                    score = self.eval(board.getFEN(fields=[1]), 1+int(board.half_move_counter/2))

                if best_score is None or score > best_score:
                    best_score = score
                    best_move = move

            board.parseMoveUndo(move, target, piece.color)

        return best_move
        

def yToTensor(y):
    output = []
    for i in y:
        try:
            output.append(int(i))
        except ValueError:
            output.append(int(i[1:]))
    return torch.tensor(output)


def trainLoop(dataloader, model, loss_fn, optimizer, epochs):
    size = len(dataloader)
    for epoch in range(epochs):
        print(f"Epoch: {epoch}")
        for batch, (X, y) in enumerate(dataloader):
            y = yToTensor(y)
            # Compute prediction and loss
            pred = model.trainForward(X).flatten(start_dim=0)
            loss = loss_fn(pred, y)

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            loss, current = loss.item(), batch
            if batch % 10 == 0:
                print(f"loss: {loss:>7f} [{current:>5d}/{size:>5d}]")


def testLoop(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    test_loss = 0
    with torch.no_grad():
        for X, y in dataloader:
            y = yToTensor(y)

            pred = model.forward(X).flatten(start_dim=0)
            test_loss += loss_fn(pred, y).item()

    test_loss /= size
    print(f"Avg loss: {test_loss:>8f} \n")


class ChessDataset(torch.utils.data.Dataset):
    def __init__(self, X_data, y_data, pre_encoded=True):
        if not pre_encoded:
            self.X_data = X_data.apply(FENToOneHot)
        else:
            self.X_data = X_data
        self.y_data = y_data

    def __len__(self):
        return len(self.X_data)

    def __getitem__(self, idx):
        return self.X_data.iloc[idx], self.y_data.iloc[idx]

def chessTrainTestLoop(data, model, loss, optim, epochs):
    data_X, data_y = data["FEN"], data["Evaluation"]
    data_X = data_X.apply(FENToOneHot)
    X_train, X_test, y_train, y_test = train_test_split(data_X, data_y, train_size=0.8, test_size=0.2)

    train_data = ChessDataset(X_train, y_train)
    test_data = ChessDataset(X_test, y_test)

    training_data = torch.utils.data.DataLoader(train_data, batch_size=64)

    testing_data = torch.utils.data.DataLoader(test_data)
    
    trainLoop(training_data, model, loss, optim, epochs)
    testLoop(testing_data, model, loss)

if __name__ == "__main__":
    bot_early = EvalBot()
    bot_middle = EvalBot()
    bot_late = EvalBot()

    """
    MIT License

    Copyright (c) 2020 Ronak Badhe

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    
    The Chess data has the above lisence 
    """
    rows = 9e5
    chess_data = pd.read_csv("ChessData/chessData.csv", nrows=rows)
    chess_data["Turns"] = chess_data["FEN"].apply(lambda FEN: int(FEN.split()[-1]))
    chess_data = chess_data.sort_values(by=["Turns"])

    chess_data_early = chess_data.iloc[0:int(rows/3), :]
    chess_data_middle = chess_data.iloc[int(rows/3):int(2*rows/3), :]
    chess_data_late = chess_data.iloc[int(2*rows/3):int(rows), :]

    chessTrainTestLoop(chess_data_early, bot_early, torch.nn.L1Loss(), torch.optim.Adam(bot_early.parameters(), lr=1e-3), 5)
    chessTrainTestLoop(chess_data_middle, bot_middle, torch.nn.L1Loss(), torch.optim.Adam(bot_middle.parameters(), lr=1e-3), 5)
    chessTrainTestLoop(chess_data_late, bot_late, torch.nn.L1Loss(), torch.optim.Adam(bot_late.parameters(), lr=1e-3), 5)

    bot = Bot("white", bot_early, bot_middle, bot_late)

    with torch.no_grad():
        with open("bot.pkl", 'wb') as f:
            pkl.dump(bot, f)
