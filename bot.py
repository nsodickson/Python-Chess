from board import *
import random as rand
import torch
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle as pkl


def FENToOneHot(FEN):
    FEN = FEN.split()[0]
    array = []
    for i in FEN.split("/"):
        array.append([])
        for n in i:
            if n.isalpha():
                array[-1].append(one_hot_pieces[n])
            elif n.isdigit():
                for q in range(int(n)):
                    array[-1].append(one_hot_pieces["."])
    return torch.tensor(array, dtype=torch.float32)


class Bot(torch.nn.Module):
    def __init__(self, color):
        super(Bot, self).__init__()
        self.color = color

        # Initializing the Network
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

    def setColor(self, color):
        self.color = color

    def forward(self, board_state, batch_train=False):
        if batch_train:
            board_state = self.flatten_train(board_state)
        else:
            board_state = self.flatten_apply(board_state)
        board_state = self.linear_relu_stack(board_state)
        if batch_train:
            return board_state
        else:
            return board_state[0]

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
                    score = -1 * self.forward(FENToOneHot(board.getFEN(fields=[1])))
                else:
                    score = self.forward(FENToOneHot(board.getFEN(fields=[1])))

                if best_score is None or score > best_score:
                    best_score = score
                    best_move = move

                board.parseMoveUndo(next_move, next_target, next_piece.color)
            else:
                score = board.eval(color)
                if best_score is None or score > best_score:
                    best_score = score
                    best_move = move

            board.parseMoveUndo(move, target, piece.color)

        return best_move

    def nextMove(self, board, color=None):
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

            board.parseMove(move, game_move=False)

            if self.color == "black":
                score = -1 * self.forward(FENToOneHot(board.getFEN(fields=[1])))
            else:
                score = self.forward(FENToOneHot(board.getFEN(fields=[1])))

            if best_score is None or score > best_score:
                best_score = score
                best_move = move

            board.parseMoveUndo(move, target, color)

        return best_move


def yToTensor(y):
    output = []
    for i in y:
        try:
            output.append(int(i))
        except ValueError:
            output.append(int(i[1:]))
    return torch.tensor(output)


def trainLoop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader)
    for batch, (X, y) in enumerate(dataloader):
        y = yToTensor(y)

        # Compute prediction and loss
        pred = model.forward(X, batch_train=True).flatten(start_dim=0)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        loss, current = loss.item(), batch
        print(f"loss: {loss:>7f} [{current + 1:>5d}/{size:>5d}]")


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


def sortData():
    pass


if __name__ == "__main__":
    bot = Bot("white")

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
    chess_data = pd.read_csv("ChessData/chessData.csv", nrows=12000000)

    data_X, data_y = chess_data["FEN"], chess_data["Evaluation"]
    data_X = data_X.apply(FENToOneHot)
    X_train, X_test, y_train, y_test = train_test_split(data_X, data_y, train_size=0.8, test_size=0.2)

    train_data = ChessDataset(X_train, y_train)
    test_data = ChessDataset(X_test, y_test)

    training_data = torch.utils.data.DataLoader(train_data, batch_size=64)

    testing_data = torch.utils.data.DataLoader(test_data)

    trainLoop(training_data, bot, torch.nn.L1Loss(), torch.optim.Adam(bot.parameters(), lr=1e-3))
    testLoop(testing_data, bot, torch.nn.L1Loss())

    with torch.no_grad():
        with open("bot.pkl", 'wb') as f:
            pkl.dump(bot, f)
