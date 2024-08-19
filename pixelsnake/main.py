import tft_config
import vga1_8x16 as font
import random
from time import sleep
import gc
import machine
import st7789py as st7789
import s3minipro as helper
from machine import Pin, Timer
import boot_icon as icon

# Constants
SNAKE_SIZE = 8
SCREEN_WIDTH, SCREEN_HEIGHT = 128, 128

# Directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Initialize RGB LED
led = Pin(helper.RGB_POWER, Pin.OUT)
rgb_timer = Timer(0)

# Initialize display
display = tft_config.config(0)

# Initialize buttons
btn_left = helper.button0
btn_right = helper.button48
btn_restart = helper.button47

# Snake initial position
snake = [(64, 64), (56, 64), (48, 64)]
direction = RIGHT
new_direction = direction

# Food initial position
food = (random.randint(0, (SCREEN_WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE,
        random.randint(0, (SCREEN_HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE)

# Pause state
paused = False
game_over = False


def initialize_display():
    display.fill(st7789.BLACK)
    display.bitmap(icon, 0, 0, 0)
    sleep(3)


def initialize_game():
    global snake, direction, new_direction, food, paused
    snake = [(64, 64), (56, 64), (48, 64)]
    direction = RIGHT
    new_direction = direction
    food = (random.randint(0, (SCREEN_WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE,
            random.randint(0, (SCREEN_HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE)
    display.fill(st7789.BLACK)
    led.value(0)
    paused = False
    draw_snake()
    draw_food()


def draw_rect(x, y, color):
    display.fill_rect(x, y, SNAKE_SIZE, SNAKE_SIZE, color)


def draw_snake():
    for segment in snake:
        draw_rect(segment[0], segment[1], st7789.GREEN)


def draw_food():
    draw_rect(food[0], food[1], st7789.RED)


def move_snake():
    global snake, food, direction, new_direction

    direction = new_direction
    head_x, head_y = snake[0]

    if direction == UP:
        head_y -= SNAKE_SIZE
    elif direction == DOWN:
        head_y += SNAKE_SIZE
    elif direction == LEFT:
        head_x -= SNAKE_SIZE
    elif direction == RIGHT:
        head_x += SNAKE_SIZE

    new_head = (head_x, head_y)

    if new_head == food:
        food = (random.randint(0, (SCREEN_WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE,
                random.randint(0, (SCREEN_HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE)
        flash_rgb_led(1, 1, 0)
    else:
        snake.pop()

    snake.insert(0, new_head)


def check_collision():
    head = snake[0]
    if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
        return True
    if head in snake[1:]:
        return True
    return False


def flash_rgb_led(r, g, b):
    led.value(1)
    helper.rgb_led(r, g, b)
    rgb_timer.init(mode=Timer.ONE_SHOT, period=1000, callback=lambda t: led.value(0))


def change_direction(pin):
    global new_direction, direction, paused, game_over

    if game_over:
        return

    if pin == btn_left:
        if direction == UP:
            new_direction = LEFT
        elif direction == DOWN:
            new_direction = RIGHT
        elif direction == LEFT:
            new_direction = DOWN
        elif direction == RIGHT:
            new_direction = UP
    elif pin == btn_right:
        if direction == UP:
            new_direction = RIGHT
        elif direction == DOWN:
            new_direction = LEFT
        elif direction == LEFT:
            new_direction = UP
        elif direction == RIGHT:
            new_direction = DOWN
    elif pin == btn_restart:
        if not game_over:
            paused = not paused  # Toggle pause state
            if paused:
                pause_screen()
            else:
                led.value(0)
                display.fill(st7789.BLACK)
                draw_snake()
                draw_food()


def reset_game():
    global game_over
    game_over = False
    initialize_game()


def pause_screen():
    led.value(1)
    display.fill(st7789.BLUE)
    helper.rgb_led(0, 0, 1)  # Blue LED to indicate paused state
    display.text(font, "Paused", 40, 38, st7789.BLUE, st7789.WHITE)
    display.text(font, f"Points: {str(len(snake) - 3)}", 27, 94, st7789.WHITE, st7789.BLUE)


def game_over_screen():
    global paused
    paused = False
    led.value(1)
    helper.rgb_led(1, 0, 0)
    display.fill(st7789.RED)
    display.text(font, "Game Over!", 25, 10, st7789.WHITE, st7789.RED)
    display.text(font, f"Points: {str(len(snake) - 3)}", 27, 56, st7789.WHITE, st7789.RED)
    display.text(font, "Press", 27, 90, st7789.WHITE, st7789.RED)
    display.text(font, "RED", 73, 90, st7789.RED, st7789.WHITE)
    display.text(font, "to restart.", 23, 110, st7789.WHITE, st7789.RED)


def main_loop():
    global game_over

    while True:
        game_over = False
        while not game_over:
            if not paused:
                display.fill(st7789.BLACK)
                draw_snake()
                draw_food()
                move_snake()

                if check_collision():
                    game_over = True

                sleep(0.5)
                gc.collect()

        game_over_screen()

        while game_over:
            if btn_restart.value() == 0:
                reset_game()
                game_over = False


def setup():
    initialize_display()
    initialize_game()
    btn_left.irq(trigger=machine.Pin.IRQ_FALLING, handler=change_direction)
    btn_right.irq(trigger=machine.Pin.IRQ_FALLING, handler=change_direction)
    btn_restart.irq(trigger=machine.Pin.IRQ_FALLING, handler=change_direction)


if __name__ == "__main__":
    setup()
    main_loop()
