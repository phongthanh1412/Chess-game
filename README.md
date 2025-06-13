# 👑♟️ Chess game

## 🔍 Overview

Chess is a two-player strategic board game played on a 64-square checkered board. Each player controls an army of pieces, all with unique moves. The goal of the game is to checkmate your opponent's king, meaning you've put it in a position where it can be captured and has no escape, while simultaneously safeguarding your own. Chess is well-known for its intricate nature, demanding critical thinking, foresight, and tactical skill from its players.


## 📁 Project Structure

```text
chessgame/
├── assets/
│   ├── images/
│   │   ├── {piece_name}.png   # Picture of specific pieces
│   └── sounds/
│       ├── capture.wav        # Sound when pieces are captured
│       └── move.wav           # Sound when move one piece
├── snapshot/                  # Picture of chessboard
├── source/
│   └── file.py                # Source code of the project
├──files.txt                   # Chess record sheet
├──README.md                   # Project overview and metadata
├──.gitignore                  # Files ignored by Git
└── requirements.txt           # External Python packages your project needs to run
```

## 📌 Objectives

- Spot and carry out sequences of tatics that lead to a material win, **checkmate**, or a decisive positional advantage
- Prioritize the safety of your **King** and do not be so greedy
- Look for vulnerabilities of your opponent's position, discover their **blunders** and develop your own move
- Carefully make your decisive move and **brilliant** move to force your opponent into a trap  


## 🧰 Tools and Technologies

- Visual Studio Code

## 📕 Language
- Python 
  

## 🎮 Game Snapshot

 <div align="center">
   <img src="snapshot/chess.png" alt="chess">
 </div>

## 📄 List of game futures
- **Standard Chess Gameplay:** Support all chess rules, including piece movements, captures, castling, en passant and pawn promotion.
- **Graphical Interface:** Render an 8x8 chessboard using Pygame with piece display, valid move highlights, last move indicators, hover effects and row/column labels.
- **Piece Dragging:** Enable piece dragging with highlighted valid move squares.
- **Game State Management:** Track player turns, game status, and detects end conditions such as checkmate, draw by stalemate, threefold repetition, 50-move rule, insufficient material and resignation.
- **PGN Recording:** Record moves in SAN format and saves them to a .txt file.
- **Sound Effects:** Play audio for piece movements and captures.
- **User Controls:** Offer mouse dragging for moves and keyboard inputs (C for theme change, R to resign, N for new game, Q to quit) with a result popup.
- **Promotion Handling:** Give player some options to select a piece (Queen, Rook, Knight, Bishop) when a pawn reaches the opponent’s back rank.
- **Error Handling:** Catch and prevent illegal moves.
## 🕹️ Instructions
- Drag a piece to move it
- Press button `n` to start a new game
- Press button `c` to change the theme of the chessboard
- Press button `r` to resign
- Press button `q` to quit the game

## 👥 Author

  **Thanh Phong**

## 🤖 Project Setup
### Global Environment Setup
- Install Python (version 3.8 or higher).
- Clone, fork or download the source code from GitHub.
  + Open Command Prompt (CMD) or Terminal.
  + Use `git clone <repository-url>` to create a local copy of the source code from GitHub.
  + Use `cd <repository-folder>` to navigate to the working directory.
- Run `pip install -r requirements.txt` to install all packages used in the source code.
- Alternatively, install libraries manually using `pip install <library_name>`.
### Virtual Environment Setup
- Install Python (version 3.8 or higher).
- Clone, fork or download the source code from GitHub and set up the virtual environment.
  + Open Command Prompt (CMD) or Terminal.
  + Use `git clone <repository-url>` to create a local copy of the source code from GitHub.
  + Use `cd <repository-folder>` to navigate to the working directory.
  + Run `python -m venv venv` to set up a virtual environment for the source code.
  + Verify Python installation by running `python --version`
  + After creating the virtual environment, activate it in the Terminal using `venv\Scripts\activate`.
  + Once you've finished working with the program, run `deactivate` to exit the virtual environment.
- Run `pip install -r requirements.txt` to install all packages used in the source code.
- Alternatively, install libraries manually using `pip install <library_name>`.
### Run Code
- Navigate to the project directory using the command `cd <full-path-to-project>`.
- Execute the main program by running `python <full-path-to-file>`.

## 📚 Appendix 
### Modules
- `pygame` is used for developing the game interface such as creating the game window, handling input...
- `os` accesses operating system functions like file paths.
- `sys` provides access to system-level functions.
- `copy` creates copies of objects especially deep copies like board states.
- `datetime` manages date and time information when recording game time or move timestamps
### References
- https://www.chess.com/learn-how-to-play-chess
- https://github.com/AlejoG10/python-chess-ai-yt