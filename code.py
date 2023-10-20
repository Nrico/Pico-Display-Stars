import board
import displayio
import busio
import adafruit_st7789
import random
import time
import math
from adafruit_display_shapes.polygon import Polygon
from adafruit_display_shapes.circle import Circle

# Release any resources currently in use for the displays
displayio.release_displays()

# Initialize SPI
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)

# Pimoroni Pico Display configuration and initialization
tft_cs = board.GP17
tft_dc = board.GP16
tft_reset = board.GP15

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset)
display = adafruit_st7789.ST7789(display_bus, width=240, height=135, rowstart=40, colstart=53, rotation=270)

def generate_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def create_star(num_arms, color):
    # Calculate the points of the star
    cx, cy = 120, 67  # Center of the screen
    outer_radius = 40
    inner_radius = 15

    angle_step = 360 / num_arms
    points = []

    for i in range(num_arms * 2):  # Double the arms to create the star
        angle = i * angle_step
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = cx + radius * math.cos(math.radians(angle))
        y = cy + radius * math.sin(math.radians(angle))
        points.append((int(x), int(y)))  # Convert float to int

    # Create the outline of the star
    star_outline = Polygon(points, outline=color)

    # Create a circle to fill the star
    circle_fill = Circle(cx, cy, inner_radius, fill=color)

    return star_outline, circle_fill

num_arms = 3  # Initial number of star arms
current_color = generate_random_color()

while True:
    # Create the star with the current number of arms and color
    star_outline, circle_fill = create_star(num_arms, current_color)

    # Display the star
    group = displayio.Group()
    group.append(star_outline)
    group.append(circle_fill)
    display.show(group)

    # Wait for a moment before changing the star
    time.sleep(2)  # Adjust the duration as needed

    # Generate a new random color
    current_color = generate_random_color()

    # Increase the number of arms, looping back to 3 if it exceeds 20
    num_arms += 1
    if num_arms > 20:
        num_arms = 3
