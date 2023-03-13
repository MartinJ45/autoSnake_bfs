# Name: Martin Jimenez
# Date: 03/13/2023 (last updated)

from cmu_graphics import *
import heapq
from snake_classes import Snake
from snake_classes import Apple


class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


# The default game speed is 10; this value can be changed by pressing the
# left and right arrow keys
app.stepsPerSecond = 10
isPaused = False
isPlaying = False

# Grabs size input
msg = 'Enter the board length (default 18 or press ENTER)'
size = app.getTextInput(msg)
while not size.isdigit() or int(size) % 2 != 0 or int(size) > 200 or int(size) < 4:
    if size == '':
        size = 18
        break
    if not size.isdigit():
        msg = 'Enter the board length (enter a digit)'
    if int(size) % 2 != 0:
        msg = 'Enter the board length (only evens)'
    if int(size) > 200:
        msg = 'Enter the board length (max size 200)'
    if int(size) < 4:
        msg = 'Enter the board length (min size 4)'

    size = app.getTextInput(msg)

size = int(size)
blockSize = 400 / (size + 2)

# This is the grid that the snake uses
# 0 represents open space
# 1 represents the border or the snake body
# 2 represents the path the snake plans to take towards the apple
# 3 represents the snake head
# 5 is a goal representing the end of the tail (used when it cannot locate the apple)
# 9 is a goal representing the apple
grid = [
    [1] * (size + 2)
]

for i in range(size):
    grid.append([1] + [0] * size + [1])
grid.append([1] * (size + 2))

# Draws the background grid
gridBackground = Group()
for x in range(size + 2):
    gridBackground.add(Line(blockSize * x, 0, blockSize * x, 400, lineWidth=1))
for y in range(size + 2):
    gridBackground.add(Line(0, blockSize * y, 400, blockSize * y, lineWidth=1))

# Draws the border and score
border = Polygon(
    0,
    0,
    400,
    0,
    400,
    400,
    0,
    400,
    0,
    blockSize,
    blockSize,
    blockSize,
    blockSize,
    400 - blockSize,
    400 - blockSize,
    400 - blockSize,
    400 - blockSize,
    blockSize,
    0,
    blockSize)
score = Label(0, 50, blockSize / 2, fill='white', size=blockSize)

path = []

# appleSeed = [(160, 160), (240, 100), (220, 260), (260, 240), (120, 80), (320, 120), (160, 200), (180, 120), (200, 160), (80, 220), (160, 20), (20, 20), (140, 180), (60, 120), (220, 300), (180, 300), (60, 20), (20, 40), (100, 160), (180, 220), (220, 160), (40, 240), (200, 100), (60, 320), (240, 180), (140, 60), (140, 160), (280, 280), (20, 140), (200, 320), (300, 60), (200, 20), (180, 260), (320, 120), (100, 240), (300, 100), (80, 280), (140, 120), (320, 320), (140, 60), (280, 240), (180, 200), (320, 260), (260, 60), (80, 260), (60, 220), (200, 160), (200, 40), (200, 280), (80, 100), (300, 280), (80, 240), (260, 120)]
# appleSeed = [(120, 180), (140, 280), (260, 140), (120, 240), (260, 280), (280, 160), (120, 280), (60, 60), (20, 240), (320, 220), (120, 100), (300, 300), (40, 80), (60, 260), (320, 140), (120, 120), (220, 160), (240, 100), (280, 320), (180, 180), (60, 260), (320, 220), (60, 80), (240, 180), (200, 180), (100, 240), (200, 240), (260, 180), (280, 100), (240, 80), (160, 60), (160, 140), (100, 40), (100, 100), (180, 180), (300, 40), (20, 20), (80, 40), (200, 320), (180, 140), (280, 100), (260, 60), (300, 300), (320, 60), (240, 280), (280, 200), (200, 320), (220, 20), (200, 220), (240, 100), (140, 220), (80, 140), (120, 260), (300, 40), (140, 320), (200, 220), (200, 80), (160, 40), (180, 20), (120, 200)]
# appleSeed = [(320, 20), (220, 180), (200, 220), (160, 320), (140, 20), (300, 100), (20, 180), (120, 200), (240, 320), (40, 280), (160, 40), (100, 320), (20, 100), (200, 160), (240, 320), (140, 260), (140, 140), (300, 220), (40, 120), (140, 180), (240, 280), (100, 280), (100, 220), (160, 40), (280, 120), (300, 40), (20, 200), (200, 260), (120, 120), (60, 140), (240, 40), (220, 100), (300, 100), (300, 160), (120, 200), (60, 60), (80, 20), (300, 200), (120, 300), (40, 20), (220, 140), (80, 140), (120, 280), (300, 180), (320, 120), (320, 220), (260, 80), (180, 180), (300, 300), (300, 20), (260, 120), (280, 140), (160, 140), (80, 200)]
appleSeed = []
snek = Snake(blockSize, blockSize, blockSize)
apple = Apple(200, blockSize, blockSize, size)


# Stops the program when the snake loses, wins, or if the game is ended early
def gameOver():
    # The max value it can achieve is 324 in an 18 by 18 grid
    if score.value == pow(size, 2) - 1:
        Label('YOU WIN', 200, 200, size=50, fill='lime')
    else:
        Label('GAME OVER', 200, 200, size=50, fill='red')

    print('appleSeed =', apple.get_seed())
    app.stop()


# Determines if the snake will get stuck if it follows the path to the apple
def futurePath(path):
    grid = genGrid()

    # Makes a copy of the grid
    newGrid = grid.copy()
    for i in range(len(newGrid)):
        newGrid[i] = grid[i].copy()

    if len(path) < len(snek.snake_body):
        # Changes the path the snake will take into 2s on the grid (2 is
        # treated as a body)

        for p in path:
            newGrid[p[0]][p[1]] = 2

        # Changes the end of the snake to empty spaces, so it is up to date
        for body in snek.snake_body:
            if snek.snake_body.index(body) < len(path) - 2:
                newGrid[int(body.top / blockSize)
                        ][int(body.left / blockSize)] = 0
            else:
                newGrid[int(body.top / blockSize)
                        ][int(body.left / blockSize)] = 5
                fEnd = (int(body.top/blockSize), int(body.left/blockSize))
                break

        # Uncomment to see the new grid
        print("Grid for future path")
        for g in newGrid:
           print(g)
        print('\n')

        # Finds a path from the apple to the end of the tail
        # If no path is found, the snake will get stuck if it follows the apple
        # If a path is found, the snake is safe to get the apple
        fStart = int(pythonRound(apple.apple.top / blockSize, 0)), int(pythonRound(apple.apple.left / blockSize, 0))
        fPath = astar(newGrid, fStart, fEnd, "future path")
        #print(fStart, fEnd)
        print("Future path", fPath)

        if fPath is not None:
            # Returns false if the snake will not get stuck
            return False
        else:
            # Returns true if the snake will get stuck
            return True


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent

    path.pop(-1)
    return path[::-1]  # Return reversed path

def astar(grid, start, end, msg=None):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param grid:
    :param start:
    :param end:
    :return:
    """

    valueGrid = [[0]*len(grid)]
    for i in range(len(grid)):
        valueGrid.append([0]*len(grid))

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = len(grid[0]) * len(grid)

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            # if we hit this point return the path such as it is
            # it will not contain the destination
            #print('Could not find apple')

            print("MAX")
            print("Value grid for", msg)
            for value in valueGrid:
                for v in value:
                    print(v, end=(4-len(str(v)))*' ')
                print(end='\n')
            print('\n')

            return return_path(current_node)

            # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            #print('Found apple')

            print("Value grid for", msg)
            for value in valueGrid:
                for v in value:
                    print(v, end=(4-len(str(v)))*' ')
                print(end='\n')
            print('\n')
            return return_path(current_node)

        # Generate children
        children = []

        for new_position in adjacent_squares:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(grid[len(grid) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if grid[node_position[0]][node_position[1]] in (1, 2, 3):
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            valueGrid[child.position[0]][child.position[1]] = child.f

            # Child is already in the open list
            if len([open_node for open_node in open_list if
                    child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    return None

# Updates the grid
def genGrid():
    for gridX in range(size + 2):
        if gridX != 0 and gridX != (
                size + 2) - 1:  # Avoids updated the border
            for gridY in range(size + 2):
                if gridY != 0 and gridY != (
                        size + 2) - 1:  # Avoids updated the border
                    if apple.apple.hits(
                            blockSize * gridX + blockSize / 2,
                            blockSize * gridY + blockSize / 2):
                        grid[gridY][gridX] = 9
                    elif border.hits(blockSize * gridX + blockSize / 2, blockSize * gridY + blockSize / 2):
                        grid[gridY][gridX] = 1
                    else:
                        grid[gridY][gridX] = 0

                    for body in snek.snake_body:
                        if body.hits(
                                blockSize * gridX + blockSize / 2,
                                blockSize * gridY + blockSize / 2):
                            grid[gridY][gridX] = 1
                            break

                    if snek.snake_head.hits(
                            blockSize * gridX + blockSize / 2,
                            blockSize * gridY + blockSize / 2):
                        grid[gridY][gridX] = 3

    return grid


def onKeyPress(key):
    global isPaused
    global isPlaying

    # Allows the player to play
    if key == 'P':
        if isPlaying:
            isPlaying = False
            print('Computer in control')
        else:
            isPlaying = True
            print('Player in control')
            print('Use WASD to move')

        isPaused = True
        print('Paused the game')

    # Player controls if the player is playing
    if isPlaying:
        if key == 'w':
            snek.set_direction('up')
        if key == 's':
            snek.set_direction('down')
        if key == 'a':
            snek.set_direction('left')
        if key == 'd':
            snek.set_direction('right')

    # Slows down the game
    if key == 'left':
        if app.stepsPerSecond == 1:
            print('Cannot lower speed past', app.stepsPerSecond)
        else:
            app.stepsPerSecond -= 1
            print('Lowered speed', app.stepsPerSecond)

    # Speeds up the game
    if key == 'right':
        app.stepsPerSecond += 1
        print('Increased speed', app.stepsPerSecond)

    # Pauses the game
    if key == 'space':
        if isPaused:
            isPaused = False
        else:
            isPaused = True
            print('Paused the game')

    if key == 'G':
        if gridBackground.visible:
            print('Grid hidden')
            gridBackground.visible = False
        else:
            print('Grid shown')
            gridBackground.visible = True

    # Prints information
    if key == 'I':
        # Prints the current grid
        print('Current grid')
        for g in grid:
            print(g)
        print('\n')
        # Prints out the apple seed
        print('appleSeed =', apple.get_seed())

    # Ends the game
    if key == 'E':
        print('Terminated game early')
        gameOver()


def onStep():
    global path
    global isPlaying
    global isPaused
    global grid

    if isPaused:
        return

    if snek.is_dead():
        gameOver()
        return

    # Stops path updating the grid and pathfinding if the player is in control
    if not isPlaying:
        # Updates the grid whenever the snake doesn't have a path to follow
        # The game would run significantly slower if the grid were to be
        # updated every single step
        start = (int(snek.snake_head.top / blockSize), int(snek.snake_head.left / blockSize))

        if not path:
            grid = genGrid()
            print("Grid for current path")
            for g in grid:
                print(g)
            print('\n')

            end = (int(apple.apple.top/blockSize), int(apple.apple.left/blockSize))
            path = astar(grid, start, end, "current path")
            print("Current path", path)

            # Calculates if the snake will get stuck
            if path and path[-1] == end:
                isStuck = futurePath(path)
                if isStuck:         # Nothing is in place yet if the snake does get stuck :(
                    print('STUCK')
                    isPaused = True

        try:
            # Calculates which direction the snake will move based on the path
            changeX = path[0][1] - start[1]
            changeY = path[0][0] - start[0]

            if changeX > 0:
                direction = 'right'
            if changeX < 0:
                direction = 'left'
            if changeY > 0:
                direction = 'down'
            if changeY < 0:
                direction = 'up'

            snek.set_direction(direction)
            # Moves onto the next direction
            path.pop(0)
        except BaseException:
            print('No path found')

    # Moves the snake
    snek.move()

    if snek.snake_head.hits(apple.apple.centerX, apple.apple.centerY):
        # Adds another body segment
        snek.add_body()

        if score.value == pow(size, 2) - 1:
            gameOver()
            return

        # Determines where the next apple will spawn
        if appleSeed:
            apple.set_apple(appleSeed[0])
            appleSeed.pop(0)
        else:
            apple.gen_apple(snek.snake_head, snek.snake_body)

        apple.update_seed((apple.apple.left, apple.apple.top))

        score.value += 1


if __name__ == '__main__':
    cmu_graphics.run()
