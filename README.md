# Console Chess in Python


A python program for playing chess in the console. The board is created using a mess of print statements and for loops.

How to play: First of all, if you don't know the rules of chess, click on [this](https://www.chess.com/learn-how-to-play-chess) link. To run a game of chess, run the [main.py](\main.py) file (all the files must be in the same directory). During each turn, the screen will be printed out from the current player's perspective, and the current player will be promted to type in a move. Type in the moves using the following format, the location of the piece and the target location are seperated by an x: NumberLetter**x**NumberLetter. The numbers and letters are the classic chess board grid system. For example, the famous kings pawn opening for white would be e4xe5.

The [main.py](\main.py) file contains the code that controls the actual gameplay. Run the main.py file to actually play chess.

The [board.py](\board.py) file contains the board class definition. The board class contains all the methods used to check the board to control how pieces move, such as testing if a certain diagonal is free of pieces.

The [pieces.py](\pieces.py) file contains the class definitions of all the different pieces. The individual pieces contain the methods that test if a given move is valid. When a piece object is created, it must be tied to a board object.

The [extras.py](extras.py) simply contains any extra global functions and variables used by all the other files. For now, it is relatively empty.

Why I made this: I am a computer science high school student who is interested in a variety of computer science related topics. I mostly code in python and java, but I have also dabbled in c and c++. A few months ago, I decided to set myself a challenge to code chess in python, something I didn't think I would be able to do at the time. Low and behold, a week or two of an unhealthy coding schedule later, I finished it! It isn't perfect, but I am proud of it, so a few days ago I decided to share it with the world.

What I do with it: The main purpose of this project was just to prove to myself that I could build a functioning console game in python, but since I made it, I've had a few fun explorations. For a while, I was working on a chess bot. I was able to make a semi-functioning algorithm that made semi-rational moves, but I decided not to include it yet in this repository because it is still very much a work in progress. Also, just for fun, I used this project to make a custom command that allows me to play chess simply by typing "chess" into the macOS terminal.

Disclaimers: I made this when I was relatively new to python, and coding in general, so don't be surprised if there are bugs hidden deep in the code. **En Passants and pawn promoting both currently don't work. Pawns are such a major headache to code because they have so many niche rules, and their moving and taking rules are different. I am currently working on fixing them**. Also, if you play this on a dark color scheme console, the colors of the pieces might appear switched. To fix this, you can go to the init method of the piece classes and switch the black and white icons. Finally, by default, the board switches between white's and black's perspective after every move, which looks very confusing on the console. You can turn the switch off by changing the switch parameter of the play function in main.py to False.

