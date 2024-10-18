import gc

import espnow
import network
from machine import Pin

import s3minipro as helper
import st7789py as st7789
import tft_config
import vga1_8x16 as font
import vga1_bold_16x16 as font_bold


CELL_SIZE = 42
GRID_SIZE = 3
DISPLAY_SIZE = 128
PADDING = (DISPLAY_SIZE - CELL_SIZE * GRID_SIZE) // 2
FONT_WIDTH = 8
FONT_HEIGHT = 16


led = Pin(helper.RGB_POWER, Pin.OUT)
led.value(1)
tft = tft_config.config()
b1 = helper.button48  
b2 = helper.button0  
b3 = helper.button47  


sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

e = espnow.ESPNow()
e.active(True)

# Replace with the correct MAC address of the peer device
peer = b''  # TODO
# peer = b'$\xevJ*\xf5C'  # EXAMPLE
e.add_peer(peer)


grid = [["", "", ""], ["", "", ""], ["", "", ""]]
cursor_x = 0
cursor_y = 0
current_player = "X"
game_over = False



def send_message(msg):
    try:
        e.send(peer, msg.encode())
        print(f"Message sent: {msg}")
    except Exception as ex:
        print("Send error:", ex)



def receive_message():
    try:
        host, msg = e.recv(500)
        if msg:
            return msg.decode()
        return None
    except Exception as ex:
        print("Receive error:", ex)
        return None



def display_grid():
    tft.fill(st7789.BLACK)
    tft.rect(0, 0, tft.width, tft.height, st7789.WHITE)
    for x in range(1, GRID_SIZE):
        tft.hline(PADDING, PADDING + x * CELL_SIZE, DISPLAY_SIZE - 2 * PADDING, st7789.WHITE)
        tft.vline(PADDING + x * CELL_SIZE, PADDING, DISPLAY_SIZE - 2 * PADDING, st7789.WHITE)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            draw_move(x, y, grid[y][x])


    draw_indicator(cursor_x, cursor_y)


def draw_winner(message):
    tft.fill(st7789.BLACK)
    None if message == "Draw" else tft.text(font, "Winner:", (DISPLAY_SIZE - 7 * 8) // 2, 10)
    tft.text(font_bold, message, (DISPLAY_SIZE - len(message) * 16) // 2, 40,
             color=st7789.RED if message == "X" else (st7789.BLUE if message == "O" else st7789.YELLOW))
    tft.text(font, "Press reset", (DISPLAY_SIZE - 11 * 8) // 2, 80, st7789.WHITE, st7789.BLACK)
    tft.text(font, "to restart.", (DISPLAY_SIZE - 11 * 8) // 2, 100, st7789.WHITE, st7789.BLACK)
    helper.rgb_led(1, 0, 0) if message == "X" else (
        helper.rgb_led(0, 0, 1) if message == "O" else helper.rgb_led(1, 1, 0))


def draw_grid():
    tft.fill(st7789.BLACK)
    tft.rect(0, 0, tft.width, tft.height, st7789.WHITE)
    for x in range(1, GRID_SIZE):
        tft.hline(PADDING, PADDING + x * CELL_SIZE, DISPLAY_SIZE - 2 * PADDING, st7789.WHITE)
        tft.vline(PADDING + x * CELL_SIZE, PADDING, DISPLAY_SIZE - 2 * PADDING, st7789.WHITE)
    # Draw the moves
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] != '':
                draw_move(x, y, grid[y][x])
    draw_indicator(cursor_x, cursor_y)


def draw_indicator(x, y):
    color = st7789.RED if current_player == 'X' else st7789.BLUE
    helper.rgb_led(1, 0, 0) if current_player == "X" else helper.rgb_led(0, 0, 1)
    indicator_size = CELL_SIZE - 12
    indicator_x = PADDING + x * CELL_SIZE + 6
    indicator_y = PADDING + y * CELL_SIZE + 6
    tft.rect(indicator_x, indicator_y, indicator_size, indicator_size, color)


def draw_move(x, y, player):
    color = st7789.RED if player == 'X' else st7789.BLUE
    text_x = PADDING + x * CELL_SIZE + (CELL_SIZE - 16) // 2
    text_y = PADDING + y * CELL_SIZE + (CELL_SIZE - 16) // 2
    tft.text(font_bold, str(player), text_x, text_y, color)


def check_winner():
    global game_over
    for row in grid:
        if row[0] == row[1] == row[2] != "":
            game_over = True
            return row[0]

    for col in range(3):
        if grid[0][col] == grid[1][col] == grid[2][col] != "":
            game_over = True
            return grid[0][col]

    if grid[0][0] == grid[1][1] == grid[2][2] != "":
        game_over = True
        return grid[0][0]

    if grid[0][2] == grid[1][1] == grid[2][0] != "":
        game_over = True
        return grid[0][2]

    if all(cell for row in grid for cell in row):
        game_over = True
        return "Draw"

    return None


def make_move():
    global current_player
    if grid[cursor_y][cursor_x] == "":
        grid[cursor_y][cursor_x] = current_player
        display_grid()
        send_message(f"{cursor_x},{cursor_y},{current_player}")
        winner = check_winner()
        if winner:
            send_message(f"winner,{winner}")
            draw_winner(winner)
            return True
        current_player = "O" if current_player == "X" else "X"
    return False



display_grid()

while not game_over:
    if b1.value() == 0:  # Move cursor right
        cursor_x = (cursor_x + 1) % 3
        display_grid()
    if b2.value() == 0:  # Move cursor down
        cursor_y = (cursor_y + 1) % 3
        display_grid()
    if b3.value() == 0:  # Mark the selected cell
        display_grid()
        if make_move():
            break  # Game over

    msg = receive_message()
    if msg:
        if "winner" in msg:
            _, winner = msg.split(",")
            draw_winner(winner)
            game_over = True
        else:
            x, y, player = msg.split(",")
            grid[int(y)][int(x)] = player
            current_player = "O" if player == "X" else "X"
            display_grid()

    gc.collect()
