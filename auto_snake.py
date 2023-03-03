from cmu_graphics import *
from random import *
from collections import deque

app.stepsPerSecond = 5

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
#snakeHead = Rect(20, 200, 20, 20, fill='blue', border='black', borderWidth=1)
#snakeBody = [Rect(20, 120, 20, 20), Rect(20, 140, 20, 20), Rect(20, 160, 20, 20), Rect(20, 180, 20, 20)]

border = Polygon(0, 0, 400, 0, 400, 400, 0, 400, 0, 20, 20, 20, 20, 380, 380, 380, 380, 20, 0, 20)
score = Label(1, 50, 10, fill='white')
path = []

appleSeed = [(200, 20), (180, 220), (280, 140), (140, 160), (40, 320), (320, 280), (80, 120), (100, 180), (260, 340), (160, 100), (300, 260), (240, 340), (120, 120), (160, 140), (160, 140), (20, 240), (340, 200), (240, 340), (260, 200), (40, 340), (60, 40), (40, 240), (200, 80), (100, 300), (100, 320), (280, 320), (80, 60), (300, 180), (300, 260), (60, 340), (40, 320), (80, 100), (80, 280), (20, 20), (120, 160), (160, 140), (220, 140), (300, 300), (180, 160), (220, 260), (260, 200), (260, 200), (40, 80), (340, 100), (340, 100), (280, 120), (140, 280), (180, 340), (40, 280), (80, 100), (200, 320), (240, 60), (300, 200), (180, 240), (220, 320), (80, 60), (20, 300), (240, 340), (240, 300), (140, 120), (200, 160), (340, 20), (80, 280), (100, 120), (100, 120), (120, 100), (200, 100), (300, 180), (220, 80), (220, 80), (60, 100), (60, 100), (40, 240), (200, 160), (180, 340), (340, 220), (140, 260), (140, 260), (280, 120), (160, 60), (200, 340), (160, 220), (120, 40), (60, 60), (180, 80), (100, 180), (260, 300), (200, 40), (280, 340), (320, 140), (100, 60), (280, 220), (200, 280), (60, 60), (100, 260), (280, 240), (280, 240), (20, 60), (160, 60), (160, 80), (260, 260), (260, 260), (160, 120), (180, 280), (80, 180), (280, 220), (280, 220), (280, 220), (40, 320), (20, 20), (20, 20), (20, 20), (280, 100), (300, 140), (240, 200), (120, 180), (280, 300), (220, 40), (20, 260), (40, 280), (40, 20), (140, 100), (20, 120), (320, 180), (320, 180), (300, 340), (280, 60), (120, 20), (40, 80), (120, 300)]
apple = Rect(200, 20, 20, 20, fill='red', border='black', borderWidth=1)
if appleSeed:
    apple.left = appleSeed[len(snakeBody) - 1][0]
    apple.top = appleSeed[len(snakeBody) - 1][1]
    score.value = len(snakeBody)

newAppleSeed = [(apple.left, apple.top)]

snakeHead.direction = 'right'


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
            print('\n')

    return path


def genApple(apple):
    global appleSeed

    if appleSeed:
        try:
            apple.left = appleSeed[len(snakeBody)][0]
            apple.top = appleSeed[len(snakeBody)][1]
        except:
            appleSeed = []
            genApple(apple)
    else:
        apple.left = randrange(0, 17) * 20 + 20
        apple.top = randrange(0, 17) * 20 + 20

    if snakeHead.hits(apple.centerX, apple.centerY):
        print('Apple spawned on head', score.value)
        if appleSeed:
            appleSeed.pop(len(snakeBody))
        genApple(apple)

    for body in snakeBody:
        if body.hits(apple.centerX, apple.centerY):
            print('Apple spawned on body', score.value)
            if appleSeed:
                appleSeed.pop(len(snakeBody))
            genApple(apple)

    newApple = (apple.left, apple.top)
    newAppleSeed.append(newApple)


def onKeyPress(key):
    if key == 'space':
        for g in grid:
            print(g)
    if key == 'E':
        Label('GAME OVER', 200, 200, size=50, fill='red')
        print('Terminated game early')
        print('Apple seed:', newAppleSeed)
        print('Snake head:', snakeHead)
        print('Snake body:', snakeBody)
        app.stop()


def onStep():
    global path
    global snakeBody

    if border.hits(snakeHead.centerX, snakeHead.centerY):
        Label('GAME OVER', 200, 200, size=50, fill='red')
        print('Apple seed:', newAppleSeed)
        print('Snake head:', snakeHead)
        print('Snake body:', snakeBody)
        app.stop()
    for body in snakeBody:
        if body.hits(snakeHead.centerX, snakeHead.centerY):
            for body in snakeBody:
                body.fill = rgb(snakeBody.index(body), 255, snakeBody.index(body))
            Label('GAME OVER', 200, 200, size=50, fill='red')
            print('Apple seed:', newAppleSeed)
            print('Snake head:', snakeHead)
            print('Snake body:', snakeBody)
            app.stop()

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
        genApple(apple)


cmu_graphics.run()