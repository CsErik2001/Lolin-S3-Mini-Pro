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

class SnakeGame:
    SNAKE_SIZE = 8
    SCREEN_WIDTH, SCREEN_HEIGHT = 128, 128

    # Directions
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self):
        self.snake = [(64, 64), (56, 64), (48, 64)]
        self.direction = self.RIGHT
        self.new_direction = self.direction
        self.food = self.generate_food()
        self.paused = False
        self.game_over = False

        # Initialize RGB LED
        self.led = Pin(helper.RGB_POWER, Pin.OUT)
        self.rgb_timer = Timer(0)

        # Initialize display
        self.display = tft_config.config(0)

    def setup(self):
        self.initialize_display()
        self.initialize_game()
        self.setup_interrupts()

    def initialize_display(self):
        self.display.fill(st7789.BLACK)
        self.display.bitmap(icon, 0, 0, 0)
        sleep(3)

    def initialize_game(self):
        self.snake = [(64, 64), (56, 64), (48, 64)]
        self.direction = self.RIGHT
        self.new_direction = self.direction
        self.food = self.generate_food()
        self.display.fill(st7789.BLACK)
        self.led.value(0)
        self.paused = False
        self.draw_snake()
        self.draw_food()

    def generate_food(self):
        return (random.randint(0, (self.SCREEN_WIDTH // self.SNAKE_SIZE) - 1) * self.SNAKE_SIZE,
                random.randint(0, (self.SCREEN_HEIGHT // self.SNAKE_SIZE) - 1) * self.SNAKE_SIZE)

    def draw_rect(self, x, y, color):
        self.display.fill_rect(x, y, self.SNAKE_SIZE, self.SNAKE_SIZE, color)

    def draw_snake(self):
        for segment in self.snake:
            self.draw_rect(segment[0], segment[1], st7789.GREEN)

    def draw_food(self):
        self.draw_rect(self.food[0], self.food[1], st7789.RED)

    def pause_screen(self):
        self.led.value(1)
        self.display.fill(st7789.BLUE)
        helper.rgb_led(0, 0, 1)  # Blue LED to indicate paused state
        self.display.text(font, "Paused", 40, 38, st7789.BLUE, st7789.WHITE)
        self.display.text(font, f"Points: {str(len(self.snake) - 3)}", 27, 94, st7789.WHITE, st7789.BLUE)

    def game_over_screen(self):
        self.paused = False
        self.led.value(1)
        helper.rgb_led(1, 0, 0)  # Red LED for game over
        self.display.fill(st7789.RED)
        self.display.text(font, "Game Over!", 25, 10, st7789.WHITE, st7789.RED)
        self.display.text(font, f"Points: {str(len(self.snake) - 3)}", 27, 56, st7789.WHITE, st7789.RED)
        self.display.text(font, "Press", 27, 90, st7789.WHITE, st7789.RED)
        self.display.text(font, "RED", 73, 90, st7789.RED, st7789.WHITE)
        self.display.text(font, "to restart.", 23, 110, st7789.WHITE, st7789.RED)

    def move_snake(self):
        self.direction = self.new_direction
        head_x, head_y = self.snake[0]

        if self.direction == self.UP:
            head_y -= self.SNAKE_SIZE
        elif self.direction == self.DOWN:
            head_y += self.SNAKE_SIZE
        elif self.direction == self.LEFT:
            head_x -= self.SNAKE_SIZE
        elif self.direction == self.RIGHT:
            head_x += self.SNAKE_SIZE

        new_head = (head_x, head_y)

        if new_head == self.food:
            self.food = self.generate_food()
            self.flash_rgb_led(1, 1, 0)
        else:
            self.snake.pop()

        self.snake.insert(0, new_head)

    def check_collision(self):
        head = self.snake[0]
        if head[0] < 0 or head[0] >= self.SCREEN_WIDTH or head[1] < 0 or head[1] >= self.SCREEN_HEIGHT:
            return True
        if head in self.snake[1:]:
            return True
        return False

    def setup_interrupts(self):
        helper.button0.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.change_direction)
        helper.button48.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.change_direction)
        helper.button47.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.change_direction)

    def change_direction(self, pin):
        if self.game_over:
            return

        if pin == helper.button0:
            if self.direction == self.UP:
                self.new_direction = self.LEFT
            elif self.direction == self.DOWN:
                self.new_direction = self.RIGHT
            elif self.direction == self.LEFT:
                self.new_direction = self.DOWN
            elif self.direction == self.RIGHT:
                self.new_direction = self.UP
        elif pin == helper.button48:
            if self.direction == self.UP:
                self.new_direction = self.RIGHT
            elif self.direction == self.DOWN:
                self.new_direction = self.LEFT
            elif self.direction == self.LEFT:
                self.new_direction = self.UP
            elif self.direction == self.RIGHT:
                self.new_direction = self.DOWN
        elif pin == helper.button47:
            if not self.game_over:
                self.paused = not self.paused  # Toggle pause state
                if self.paused:
                    self.pause_screen()
                else:
                    self.led.value(0)
                    self.display.fill(st7789.BLACK)
                    self.draw_snake()
                    self.draw_food()

    def flash_rgb_led(self, r, g, b):
        self.led.value(1)
        helper.rgb_led(r, g, b)
        self.rgb_timer.init(mode=Timer.ONE_SHOT, period=1000, callback=lambda t: self.led.value(0))

    def reset_game(self):
        self.game_over = False
        self.initialize_game()

    def main_loop(self):
        while True:
            self.game_over = False
            while not self.game_over:
                if not self.paused:
                    self.display.fill(st7789.BLACK)
                    self.draw_snake()
                    self.draw_food()
                    self.move_snake()

                    if self.check_collision():
                        self.game_over = True

                    sleep(0.5)
                    gc.collect()

            self.game_over_screen()

            while self.game_over:
                if helper.button47.value() == 0:
                    self.reset_game()
                    self.game_over = False

# Main Execution
if __name__ == "__main__":
    game = SnakeGame()
    game.setup()
    game.main_loop()
