class Node:
    def __init__(self, value, direction, x, y, xIndex, yIndex):
        self.value = value
        self.color = value[0]
        self.x = x
        self.y = y
        self.xIndex = xIndex
        self.yIndex = yIndex
        self.direction = direction
        self.parent = None
        # Distance from start
        self.g = 0
        # Estimated distance from goal
        self.h = 0
        # Total distance: g + h
        self.f = 0
