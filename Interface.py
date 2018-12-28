from enum import Enum
import random


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class State(Enum):
    EMPTY = 1
    SNAKE = 2
    FOOD = 3


class Interface:

    def __init__(self, width=72, height=46):
        self.width = width
        self.height = height
        self.head = (int(width / 2), int(height / 2))
        self.dir = random.choice(list(Direction))
        self.body = [self.head]
        self.score = 0
        self.foodPos = self.randomFoodPos()
        self.steps = 0  # number of steps it has taken
        self.tick = 1  # game start speed

    def gameOver(self):
        if self.head[0] < 0 or self.head[0] >= self.width:
            return True
        if self.head[1] < 0 or self.head[1] >= self.height:
            return True
        for block in self.body[1:]:
            if block == self.head:
                return True
        return False

    def getState(self):
        state = [[State.EMPTY for _ in range(
            self.height)] for _ in range(self.width)]
        state[self.foodPos[0]][self.foodPos[1]] = State.FOOD
        for block in self.body:
            state[block[0]][block[1]] = State.SNAKE
        return state

    def randomFoodPos(self):
        foodPos = (random.randint(1, self.width),
                   random.randrange(1, self.height))
        while foodPos in self.body:
            foodPos = (random.randint(1, self.width),
                       random.randrange(1, self.height))
        return foodPos

    def update(self, key=None):
        if key is not None:
            # snake cannot go backwards
            if self.dir == Direction.UP and key == Direction.DOWN:
                key = Direction.UP
            if self.dir == Direction.DOWN and key == Direction.UP:
                key = Direction.DOWN
            if self.dir == Direction.LEFT and key == Direction.RIGHT:
                key = Direction.LEFT
            if self.dir == Direction.RIGHT and key == Direction.LEFT:
                key = Direction.RIGHT
            self.dir = key

        # update snake position
        self.head = {
            Direction.UP: (self.head[0], self.head[1] - 1),
            Direction.DOWN: (self.head[0], self.head[1] + 1),
            Direction.LEFT: (self.head[0] - 1, self.head[1]),
            Direction.RIGHT: (self.head[0] + 1, self.head[1])
        }[self.dir]

        self.body.insert(0, self.head)
        if self.head == self.foodPos:
            # scored!
            self.score += 1
            self.tick += 1
            self.foodPos = self.randomFoodPos()
        else:
            self.body.pop()

        self.steps += 1
