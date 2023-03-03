# Date: 03/03/2023 (last updated)
# Name: Martin Jimenez

from cmu_graphics import *
from random import *
from collections import deque

app.stepsPerSecond = 10
isPaused = False

grid = [
    [1] * 20,
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] * 20]

for x in range(20):
    Line(20 * x, 0, 20 * x, 400, lineWidth=1)
for y in range(20):
    Line(0, 20 * y, 400, 20 * y, lineWidth=1)

snakeHead = Rect(40, 20, 20, 20, fill='blue', border='black', borderWidth=1)
snakeBody = [Rect(20, 20, 20, 20, fill='green', border='black', borderWidth=1)]
#snakeHead =
#snakeBody =

border = Polygon(0, 0, 400, 0, 400, 400, 0, 400, 0, 20, 20, 20, 20, 380, 380, 380, 380, 20, 0, 20)
score = Label(1, 50, 10, fill='white')
path = []

appleSeed = []
apple = Rect(200, 20, 20, 20, fill='red', border='black', borderWidth=1)
if appleSeed:
    apple.left = appleSeed[len(snakeBody) - 1][0]
    apple.top = appleSeed[len(snakeBody) - 1][1]
    score.value = len(snakeBody)

newAppleSeed = [(apple.left, apple.top)]

snakeHead.direction = 'right'


def gameOver():
    Label('GAME OVER', 200, 200, size=50, fill='red')
    print('Apple seed:', newAppleSeed)
    print('Snake head:', snakeHead)
    print('Snake body:', snakeBody)
    app.stop()


def dfs(grid, start, goal):
    visited = set()
    stack = [start]
    parentMap = {}
    rows, cols, = len(grid), len(grid[0])

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)

            x, y = node[0], node[1]

            if ((x > 0) and (x < rows - 1) and (y > 0) and (y < cols - 1) and (grid[x][y]) == goal):
                return (x, y), parentMap

            if (x > 0) and (grid[x - 1][y] != 1) and ((x - 1, y) not in visited):
                stack.append((x - 1, y))
                parentMap[(x - 1, y)] = ((x, y), 'up')
            if (x < rows - 1) and (grid[x + 1][y] != 1) and ((x + 1, y) not in visited):
                stack.append((x + 1, y))
                parentMap[(x + 1, y)] = ((x, y), 'down')
            if (y > 0) and (grid[x][y - 1] != 1) and ((x, y - 1) not in visited):
                stack.append((x, y - 1))
                parentMap[(x, y - 1)] = ((x, y), 'left')
            if (y < cols - 1) and (grid[x][y + 1] != 1) and ((x, y + 1) not in visited):
                stack.append((x, y + 1))
                parentMap[(x, y + 1)] = ((x, y), 'right')

    return None, None


def bfs(grid, start, goal):
    visited = set()
    dq = deque([start])
    parentMap = {}
    rows, cols, = len(grid), len(grid[0])

    while dq:
        node = dq.pop()
        if node not in visited:
            visited.add(node)

            x, y = node[0], node[1]

            if ((x > 0) and (x < rows - 1) and (y > 0) and (y < cols - 1) and (grid[x][y]) == goal):
                return (x, y), parentMap

            if (x > 0) and (grid[x - 1][y] != 1) and ((x - 1, y) not in visited):
                dq.appendleft((x - 1, y))
                parentMap[(x - 1, y)] = ((x, y), 'up')
            if (x < rows - 1) and (grid[x + 1][y] != 1) and ((x + 1, y) not in visited):
                dq.appendleft((x + 1, y))
                parentMap[(x + 1, y)] = ((x, y), 'down')
            if (y > 0) and (grid[x][y - 1] != 1) and ((x, y - 1) not in visited):
                dq.appendleft((x, y - 1))
                parentMap[(x, y - 1)] = ((x, y), 'left')
            if (y < cols - 1) and (grid[x][y + 1] != 1) and ((x, y + 1) not in visited):
                dq.appendleft((x, y + 1))
                parentMap[(x, y + 1)] = ((x, y), 'right')

    return None, None


def findPath(goal, start, parentMap):
    curr = goal
    path = []
    while curr != start:
        curr, direction = parentMap[curr]
        path.append(direction)
    return path


def snakePath(path, goal):
    if not path:
        start = int(snakeHead.top / 20), int(snakeHead.left / 20)
        xy, parentMap = bfs(grid, start, goal)
        if xy is not None:
            path = findPath(xy, start, parentMap)
            path.reverse()
        else:
            print('Couldnt find goal', score.value)
            highPath = []
            for body in snakeBody:
                grid[int(body.top / 20)][int(body.left / 20)] = 5
                xy, parentMap = dfs(grid, start, goal)

                if xy is not None:
                    path = findPath(xy, start, parentMap)
                    path.reverse()

                    if len(path) > snakeBody.index(body):
                        print('Option', snakeBody.index(body), 'taken with', len(path), 'directions')
                        break
                    else:
                        print('Rejected option', snakeBody.index(body), 'with', len(path), 'directions')
                        if len(path) > len(highPath):
                            highPath = path

                if snakeBody.index(body) == len(snakeBody) - 1:
                    path = highPath
                    print('Best option chosen with', len(path), 'directions')
                    break

                grid[int(body.top / 20)][int(body.left / 20)] = 1

            for g in grid:
                print(g)

    return path


def genApple(apple, grid):
    global appleSeed
    global isPaused

    if appleSeed:
        try:
            apple.left = appleSeed[len(snakeBody) - 1][0]
            apple.top = appleSeed[len(snakeBody) - 1][1]
        except:
            appleSeed = []
            genApple(apple, grid)
    else:
        apple.left = randrange(0, 17) * 20 + 20
        apple.top = randrange(0, 17) * 20 + 20

    if snakeHead.hits(apple.centerX, apple.centerY):
        print('Apple spawned on head', score.value)
        if appleSeed:
            appleSeed.pop(len(snakeBody) - 1)
        genApple(apple, grid)

    for body in snakeBody:
        if body.hits(apple.centerX, apple.centerY):
            print('Apple spawned on body', score.value)
            if appleSeed:
                appleSeed.pop(len(snakeBody) - 1)
            genApple(apple, grid)

    newApple = (apple.left, apple.top)
    newAppleSeed.append(newApple)


def onKeyPress(key):
    global isPaused

    if key == 'left':
        if app.stepsPerSecond == 1:
            print('Cannot lower speed past', app.stepsPerSecond)
        else:
            app.stepsPerSecond -= 1
            print('Lowered speed', app.stepsPerSecond)

    if key == 'right':
        app.stepsPerSecond += 1
        print('Increased speed', app.stepsPerSecond)

    if key == 'space':
        if isPaused:
            isPaused = False
        else:
            isPaused = True
            print('Paused the game')

    if key == 'G':
        print('Current grid:')
        for g in grid:
            print(g)

    if key == 'E':
        print('Terminated game early')
        gameOver()


def onStep():
    global path
    global snakeBody
    global isPaused

    if isPaused:
        return

    if border.hits(snakeHead.centerX, snakeHead.centerY):
        gameOver()
        return
    for body in snakeBody:
        if body.hits(snakeHead.centerX, snakeHead.centerY):
            gameOver()
            return

    snakeBody.append(Rect(snakeHead.left, snakeHead.top, 20, 20, fill='green', border='black', borderWidth=1))
    snakeBody[0].visible = False
    snakeBody.pop(0)

    if not path:
        for x in range(20):
            if x != 0 and x != 19:
                for y in range(20):
                    if y != 0 and y != 19:
                        if apple.hits(20 * x + 10, 20 * y + 10):
                            grid[y][x] = 5
                        elif border.hits(20 * x + 10, 20 * y + 10):
                            grid[y][x] = 1
                        else:
                            grid[y][x] = 0
                        for body in snakeBody:
                            if body.hits(20 * x + 10, 20 * y + 10):
                                grid[y][x] = 1
                                break
                        if snakeHead.hits(20 * x + 10, 20 * y + 10):
                            grid[y][x] = 2

    path = snakePath(path, 5)
    try:
        snakeHead.direction = path[0]
        path.pop(0)
    except:
        pass

    if snakeHead.direction == 'right':
        snakeHead.centerX += 20
    if snakeHead.direction == 'left':
        snakeHead.centerX -= 20
    if snakeHead.direction == 'up':
        snakeHead.centerY -= 20
    if snakeHead.direction == 'down':
        snakeHead.centerY += 20

    if apple.hits(snakeHead.centerX, snakeHead.centerY):
        snakeBody.append(Rect(snakeBody[-1].left, snakeBody[-1].top, 20, 20, fill='green', border='black', borderWidth=1))
        score.value = len(snakeBody)
        genApple(apple, grid)

cmu_graphics.run()
