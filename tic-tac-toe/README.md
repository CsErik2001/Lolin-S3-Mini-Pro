# TicTacToe

This project implements a classic Tic-Tac-Toe game on an ESP32 microcontroller with an ST7789 display. The game features an intuitive grid layout, player turn indicators, and game over detection with winner or draw messages. The game is controlled using three buttons for navigation and move placement.

## Hardware Requirements

- **ESP32 microcontroller**
- **ST7789 display** (128x128 resolution)
- **Three buttons** for controlling the game
- **Wiring and connectors** as needed

## Software Requirements

- **MicroPython or CircuitPython** installed on the ESP32
- **Required libraries**:
  - `st7789py`: Driver for the ST7789 display
  - `s3minipro`: Helper library for pinout management
  - `tft_config`: Configuration for the display
  - `vga1_8x16`: Font library for text rendering

## Game Controls

- **Button 1 (Left)**: Move the cursor to the right
- **Button 2 (Down)**: Move the cursor downward
- **Button 3 (Select / Restart)**: Place the current player's move, or restart the game after a win or draw

## How to Start

### Setup the hardware:

1. **Connect the ST7789 display** to the ESP32 according to your specific wiring configuration.
2. **Connect the buttons** to appropriate GPIO pins on the ESP32.

### Load the code:

1. **Upload the Python files** (`main.py`, `tft_config.py`, `s3minipro.py`, `vga1_8x16.py`) to your ESP32.
2. Ensure all necessary libraries are uploaded and properly imported.

### Power up the ESP32:

- Once powered, the Tic-Tac-Toe grid will display on the screen.

### Start the game:

- The game starts automatically. Use the left and down buttons to move the cursor.
- Use the select button to place your move on the grid.

### Win, Draw, and Restart:

- The game ends when a player wins or the grid is full resulting in a draw.
- The winning player's message or a draw message is displayed on the screen.
- Press the select button to reset and start a new game after a win or draw.

## Customization

- **Initial Setup**: You can customize the game's grid size, colors, and player symbols by modifying the code.
- **Display Messages**: Adjust the text and layout for win or draw messages as needed.

## Future Improvements

- Implement sound effects for moves and game events.
- Add different game modes or difficulty levels.
- Enhance visual effects for the winner and draw conditions.

## License

This project is open-source. Feel free to modify and distribute it as you wish.
