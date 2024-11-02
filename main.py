import time

from ursina import *
import random

app = Ursina()

window.color = color.black
window.size = (800, 600)

CUBE_SIZE = 0.5  # Increased size to make elements more visible
BORDERS = 5  # Boundary limit for the play area
SNAKE_BODY = []
LOCATION = Vec3(1, 0, 0)  # Initial movement direction along the X-axis
GRID = BORDERS*2 + 1
LENGTH = 1
LENGTH_text = Text(text=f"{LENGTH}", position=(0, 0.4), color=color.white, scale=2)
OFFSET = CUBE_SIZE / 2 - 0.8

# Create the head of the snake
HEAD = Entity(model='cube', color=color.green, scale=CUBE_SIZE, position=Vec3(0, 0, 0))

SNAKE_BODY.append(HEAD)
DELAY = 0.3
# Creation of the food
FOOD = Entity(model='cube', color=color.red, scale=CUBE_SIZE,
              position=Vec3(random.randint(-BORDERS, BORDERS), 0,
                            random.randint(-BORDERS, BORDERS)))


def spawn_food():
    # Spawn food within the play area boundary
    FOOD.position = Vec3(random.randint(-BORDERS, BORDERS), 0,
                         random.randint(-BORDERS, BORDERS))

def create_grid():
    for i in range(-BORDERS, BORDERS + 1):
        # Vertical lines
        Entity(model='cube', color=color.gray, scale=(0.02, 0.02, GRID + 0.5),
               position=Vec3(i + OFFSET, -0.25, 0), rotation=(0, 0, 0), collider=None)
        # Horizontal lines
        Entity(model='cube', color=color.gray, scale=(GRID + 0.5, 0.02, 0.02),
               position=Vec3(0, -0.25, i + OFFSET), rotation=(0, 0, 0), collider=None)

def updateSnake():
    global LOCATION, LENGTH

    new_position = SNAKE_BODY[0].position + LOCATION * CUBE_SIZE

    # Boundary check: Wrap the snake to the other side if it goes out of bounds
    if new_position.x > BORDERS:
        new_position.x = -BORDERS
    elif new_position.x < -BORDERS:
        new_position.x = BORDERS
    if new_position.z > BORDERS:
        new_position.z = -BORDERS
    elif new_position.z < -BORDERS:
        new_position.z = BORDERS

    SNAKE_BODY.insert(0, duplicate(SNAKE_BODY[0], position=new_position))

    # Snake meets food
    if SNAKE_BODY[0].position == FOOD.position:
        spawn_food()
        LENGTH += 1
        LENGTH_text.text = f"{LENGTH}"
    else:
        destroy(SNAKE_BODY.pop(-1))  # Removes the snake's tail if no food is eaten

    # Check if the snake hits itself -> end
    for body in SNAKE_BODY[1:]:
        if body.position == SNAKE_BODY[0].position:
            print("GAME OVER")
            application.quit()

    invoke(updateSnake, delay=DELAY)

def input(key):
    global LOCATION
    print(f"{key}")
    if key == 's' or key == 'down arrow':
        if LOCATION != Vec3(0, 0, 1):
            LOCATION = Vec3(0, 0, -1)
    if key == 'w' or key == 'up arrow':
        if LOCATION != Vec3(0, 0, -1):
            LOCATION = Vec3(0, 0, 1)
    if key == 'a' or key == 'left arrow':
        if LOCATION != Vec3(1, 0, 0):
            LOCATION = Vec3(-1, 0, 0)
    if key == 'd' or key == 'right arrow':
        if LOCATION != Vec3(-1, 0, 0):
            LOCATION = Vec3(1, 0, 0)
    if key == 'escape':
        application.quit()


# Adjust the camera position to focus on the play area
camera.position = (0, 15, -15)
camera.rotation_x = 45

create_grid()
updateSnake()
app.run()
