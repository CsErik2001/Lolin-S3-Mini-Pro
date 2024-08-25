import st7789py as st7789
from machine import Pin
import time
import tft_config
import vga1_8x16 as font
import s3minipro as helper

# Initialize display
tft = tft_config.config(0)

# Initialize buttons
button_a = helper.button48
button_b = helper.button0
button_c = helper.button47

# Constants
CELL_SIZE = 42
GRID_SIZE = 3
DISPLAY_SIZE = 128
PADDING = (DISPLAY_SIZE - CELL_SIZE * GRID_SIZE) // 2
FONT_WIDTH = 8
FONT_HEIGHT = 16

# Game variables
grid = [['', '', ''], ['', '', ''], ['', '', '']]
current_player = 'X'
game_over = False
cursor_x, cursor_y = 0, 0

def draw_grid():
    tft.fill(st7789.BLACK)
    tft.rect(0, 0, tft.width, tft.height, st7789.WHITE)  # Draw a white border around the screen
    for x in range(1, GRID_SIZE):
        tft.hline(PADDING, PADDING + x * CELL_SIZE, DISPLAY_SIZE - 2 * PADDING, st7789.WHITE)
        tft.vline(PADDING + x * CELL_SIZE, PADDING, DISPLAY_SIZE - 2 * PADDING, st7789.WHITE)
    # Draw the moves
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] != '':
                draw_move(x, y, grid[y][x])
    # Draw the cursor indicator
    draw_indicator(cursor_x, cursor_y)

def draw_move(x, y, player):
    color = st7789.RED if player == 'X' else st7789.BLUE
    # Calculate the position to center the text
    text_x = PADDING + x * CELL_SIZE + (CELL_SIZE - FONT_WIDTH) // 2
    text_y = PADDING + y * CELL_SIZE + (CELL_SIZE - FONT_HEIGHT) // 2
    tft.text(font, str(player), text_x, text_y, color)

def draw_winner(message):
    tft.fill(st7789.BLACK)
    tft.text(font, message, (DISPLAY_SIZE - len(message) * FONT_WIDTH) // 2, 40)
    tft.text(font, "Press", 27, 80, st7789.WHITE, st7789.BLACK)
    tft.text(font, "RED", 73, 80, st7789.RED, st7789.BLACK)
    tft.text(font, "to restart.", 23, 100, st7789.WHITE, st7789.BLACK)


def draw_indicator(x, y):
    # Choose color based on the current player
    color = st7789.RED if current_player == 'X' else st7789.BLUE
    # Position and size for the indicator
    indicator_size = CELL_SIZE - 12  # Slightly smaller than CELL_SIZE
    indicator_x = PADDING + x * CELL_SIZE + 6  # Center the indicator within the cell
    indicator_y = PADDING + y * CELL_SIZE + 6  # Center the indicator within the cell

    # Draw the smaller highlight rectangle
    tft.rect(indicator_x, indicator_y, indicator_size, indicator_size, color)

def handle_button_press():
    global cursor_x, cursor_y, current_player, game_over

    # Move cursor with buttons
    if not button_a.value():  # Button A moves left
        cursor_x = (cursor_x + 1) % GRID_SIZE
        time.sleep(0.2)
        draw_grid()  # Redraw grid to update indicator
    if not button_b.value():  # Button B moves down
        cursor_y = (cursor_y + 1) % GRID_SIZE
        time.sleep(0.2)
        draw_grid()  # Redraw grid to update indicator
    if not button_c.value():  # Button C places move
        if grid[cursor_y][cursor_x] == '' and not game_over:
            grid[cursor_y][cursor_x] = current_player
            draw_move(cursor_x, cursor_y, current_player)
            if check_win():
                game_over = True
                draw_winner(f"{current_player} won!")
            elif is_grid_full():
                game_over = True
                draw_winner("Draw!")
            else:
                current_player = 'O' if current_player == 'X' else 'X'
        time.sleep(0.2)
        if not game_over:
            draw_grid()  # Redraw grid to update indicator

def check_win():
    for row in grid:
        if row[0] == row[1] == row[2] != '':
            return True
    for col in range(GRID_SIZE):
        if grid[0][col] == grid[1][col] == grid[2][col] != '':
            return True
    if grid[0][0] == grid[1][1] == grid[2][2] != '' or grid[0][2] == grid[1][1] == grid[2][0] != '':
        return True
    return False

def is_grid_full():
    for row in grid:
        for cell in row:
            if cell == '':
                return False
    return True

def reset_game():
    global grid, current_player, game_over, cursor_x, cursor_y
    grid = [['', '', ''], ['', '', ''], ['', '', '']]
    current_player = 'X'
    game_over = False
    cursor_x, cursor_y = 0, 0
    draw_grid()  # Redraw grid and reset indicator

# Main loop
draw_grid()
while True:
    if game_over:
        # Keep the winner or draw message displayed until a reset is triggered
        if not button_c.value():  # Reset the game with Button C
            reset_game()
            time.sleep(0.2)
    else:
        handle_button_press()
