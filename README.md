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
python main2.py
```

## Project Structure

- `main.py`: The main script that runs the game loop and handles events.
- `chessboard.py`: Contains the ChessBoard class for rendering the chessboard.
- `piece.py`: Contains the Piece class and the respective chess piece logic (movement, validation, etc).
- `piece2.py`: Contains experimental changes to `piece.py` which may be used as the base in the future.
- `main2.py`: The main script which has drag&drop functionailty instead of point&click. Identical to `main.py`.

- _Caution_: Change import from `piece.py` to `piece2.py` in the starting of `chessboard.py` for changes to take effect.

## Documentation

For more information about Pygame and its functions, refer to the official Pygame documentation:

[Pygame Documentation](https://www.pygame.org/docs/)

## Next Steps

This project currently only renders the chessboard and has a simple turn-based gameplay loop. Future improvements could include:
- Adding a scoring system and winning conditions
- Implementing AI (Minimax, AB Pruning, etc)
- Comparison between algorithms implemented above
- Minor refactoring and performance improvements

Feel free to contribute to this project and expand its functionality!
