# Mini Chess Game Project
This project is a simple implementation of a mini chess game using Python and Pygame.

## Installation
1. Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2. Install Pygame by running the following command in your terminal:

   ```
   pip install pygame
   ```
3. Clone or download this repository to your local machine.

## Running the Game
To run the game, navigate to the project directory in your terminal and run:

```
python main.py
```
or 
```
python main3.py
```

## Project Structure

### Main Game Files
- `main.py`: The main script that runs the game loop and handles events. Implements point-and-click chess gameplay with AI support.
- `main2.py`: Old backup implementation of the main game with drag-and-drop functionality.
- `main3.py`: Current active version with drag-and-drop functionality, functionally same as [`main.py`](main.py).

### Core Game Components
- `chessboard.py`: Contains the [`ChessBoard`](chessboard.py) class for rendering the chessboard, managing piece positions, and handling board-related operations.
- `game_rules.py`: Implements the [`GameRules`](game_rules.py) class that manages game logic, move validation, and game state checks.
- `chess_ai.py`: Contains the [`ChessAI`](chess_ai.py) class implementing minimax algorithm with alpha-beta pruning for AI opponents.

### Piece Management
- `piece.py`: Original implementation of chess pieces with basic movement logic.
- `piece2.py`: Refactored version with improved movement validation and cleaner inheritance structure.

### User Interface
- `ui/start_menu.py`: Implements the [`StartMenu`](ui/start_menu.py) class for game mode selection and initial setup.
- `ui/game_menu.py`: Contains the [`GameMenu`](ui/game_menu.py) class for in-game menu options (save/load/exit).
- `ui/status_display.py`: Manages the [`StatusDisplay`](ui/status_display.py) class for showing game state, moves, and notifications.

### Audio
- `sounds.py`: Contains the [`SoundManager`](sounds.py) class for handling game audio effects.
- `sounds/`: Directory containing audio files:
  - `move.wav`: Sound effect for piece movement
  - `check.wav`: Sound effect for check state
  - `checkmate.wav`: Sound effect for checkmate

### Assets
- `Pieces/`: Directory containing chess piece images
  - `ChessPiecesArray.png`: Sprite sheet containing all chess piece images

### Save System
- `saved_game.pkl`: Binary file storing saved game states (auto-generated when saving)

### Configuration
- `.gitignore`: Specifies which files Git should ignore

- _Important Note_: When switching between `piece.py` and `piece2.py`, make sure to update the import statement in `chessboard.py` accordingly.

## Next Steps

This project currently only renders the chessboard and has a simple turn-based gameplay loop. Future improvements could include:
- Comparison between algorithms implemented above
- Minor refactoring and performance improvements

Feel free to contribute to this project and expand its functionality!

## Documentation

For more information about Pygame and its functions, refer to the official Pygame documentation:

[Pygame Documentation](https://www.pygame.org/docs/)
