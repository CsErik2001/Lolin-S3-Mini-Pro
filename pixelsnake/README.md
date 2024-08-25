# PixelSnake

This project implements a classic Snake game on an ESP32 microcontroller with an ST7789 display. The game features RGB LED effects, game pause functionality, and a game over screen with score display. The game is controlled using three buttons for direction and game control.

## Hardware Requirements

- **ESP32 microcontroller**
- **ST7789 display** (128x128 resolution)
- **RGB LED**
- **Three buttons** for controlling the game
- **Wiring and connectors** as needed

## Software Requirements

- **MicroPython** or **CircuitPython** installed on the ESP32
- **Required libraries**:
  - `st7789py`: Driver for the ST7789 display
  - `s3minipro`: Helper library for pinout management
  - `tft_config`: Configuration for the display
  - `vga1_8x8`: Font library for text rendering
  - `boot_icon`: Boot screen bitmap

## Game Controls

- **Button 1 (Left)**: Turn the snake counterclockwise
- **Button 2 (Restart / Pause)**: Pause/Resume the game during play, or restart the game after game over
- **Button 3 (Right)**: Turn the snake clockwise

## How to Start

1. **Setup the hardware**:
   - Connect the ST7789 display to the ESP32 according to your specific wiring configuration.
   - Connect the RGB LED and buttons to appropriate GPIO pins on the ESP32.

2. **Load the code**:
   - Upload the Python files (`main.py`, `tft_config.py`, `s3minipro.py`, `boot_icon.py`) to your ESP32.
   - Make sure all necessary libraries are also uploaded and properly imported.

3. **Power up the ESP32**:
   - Once powered, the display will show a boot screen for a few seconds.

4. **Start the game**:
   - The game starts automatically after the boot screen.
   - Control the snake using the left and right buttons.
   - The game ends when the snake collides with itself or the wall.

5. **Pause/Resume and Restart**:
   - Press the restart button during gameplay to pause or resume the game.
   - After the game is over, press the restart button to reset and start a new game.

## Customization

- You can customize the game by modifying the initial snake position, speed, or display messages.
- Adjust the RGB LED effects to your preference by modifying the `flash_rgb_led` function.

## Future Improvements

- Implement different difficulty levels.
- Add more visual effects for special events like eating food.

## License

This project is open-source. Feel free to modify and distribute it as you wish.
