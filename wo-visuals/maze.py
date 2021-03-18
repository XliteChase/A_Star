from node import Node
import math


class Maze:
    def __init__(self):
        self.maze = [[]]
        self.rows = 0
        self.cols = 0

    # Load in file and initialize the maze
    def init(self, file):
        dimensions = file.readline().split()
        self.rows = int(dimensions[0])
        self.cols = int(dimensions[1])
        self.maze = [[None for x in range(self.cols)]
                     for y in range(self.rows)]

        nodes = []
        currentRow = 0
        # Iterate through file line by line
        for line in file:
            currentColumn = 0
            fileNodes = line.split()
            for node in fileNodes:
                nodeData = node.split("-")
                self.maze[currentRow][currentColumn] = Node(
                    *nodeData, currentRow, currentColumn)
                currentColumn += 1
            currentRow += 1

    def aStar(self, start, mode, sbs=False):
        if mode == 's':
            return self.shortest_path(start, sbs)
        else:
            return self.fewest_nodes(start, sbs)

    def fewest_nodes(self, start, sbs):
        visited = set()
        yet_to_visit = []

        goal = self.maze[self.rows-1][self.cols-1]
        cNode = start
        yet_to_visit.append(cNode)

        while yet_to_visit:
            cNode = yet_to_visit.pop(0)
            visited.add(cNode)

            node_to_visit = []
            for node in self.getChildren(cNode.xIndex, cNode.yIndex):
                node_to_visit.append(node)
                if node in visited:
                    continue
                if node in yet_to_visit:
                    continue
                    # newDistance = cNode.g + \
                    #     self.calcDistance(cNode, node, mode="f")
                    # if newDistance < node.g:
                    #     node.parent = cNode
                    #     node.g = newDistance
                    #     node.f = node.g + node.h
                else:
                    node.g = cNode.g + self.calcDistance(cNode, node, mode="f")
                    node.h = self.calcDistance(node, goal, mode="f")
                    node.f = node.g + node.h
                    node.parent = cNode
                    yet_to_visit.append(node)

            if sbs:
                text_file = open("maze-sol.txt", "a")
                text_file.write(f"Node Selected: {cNode.value}\n")

                node_string = ""
                for node in node_to_visit:
                    node_string += f" {node.value}"
                text_file.write(f"Possible Node to Travel: {node_string}\n")

                node_dist = ""
                for node in sorted(yet_to_visit, key=lambda x: x.f):
                    node_dist += f" {node.value}(f={round(node.f, 3)})"
                text_file.write(
                    f"node at the end of possible path: {node_dist} \n")
                text_file.write("*****************************************\n")

            if cNode == goal:
                shortestPath = []
                while cNode.parent:
                    shortestPath.append(cNode)
                    cNode = cNode.parent
                shortestPath.append(cNode)
                shortestPath.reverse()
                return shortestPath

    def shortest_path(self, start, sbs):
        yet_to_visit = set()
        visited = set()

        goal = self.maze[self.rows-1][self.cols-1]
        cNode = start
        yet_to_visit.add(cNode)
        while yet_to_visit:
            cNode = min(yet_to_visit, key=lambda node: node.f)

            yet_to_visit.remove(cNode)
            visited.add(cNode)

            node_to_visit = []
            for node in self.getChildren(cNode.xIndex, cNode.yIndex):
                node_to_visit.append(node)
                if node in visited:
                    continue
                if node in yet_to_visit:
                    newDistance = cNode.g + self.calcDistance(cNode, node, "s")
                    if newDistance < node.g:
                        node.parent = cNode
                        node.g = newDistance
                        node.f = node.g + node.h
                else:
                    node.g = cNode.g + self.calcDistance(cNode, node, "s")
                    node.h = self.calcDistance(node, goal, "s")
                    node.f = node.g + node.h
                    node.parent = cNode
                    yet_to_visit.add(node)

            if sbs:
                text_file = open("maze-sol.txt", "a")
                text_file.write(f"Node Selected: {cNode.value}\n")

                node_string = ""
                for node in node_to_visit:
                    node_string += f" {node.value}"
                text_file.write(f"Possible Node to Travel: {node_string}\n")

                node_dist = ""
                for node in sorted(yet_to_visit, key=lambda x: x.f):
                    node_dist += f" {node.value}(f={round(node.f, 3)})"
                text_file.write(
                    f"node at the end of possible path: {node_dist} \n")
                text_file.write("*****************************************\n")

            if cNode == goal:
                shortestPath = []
                while cNode.parent:
                    shortestPath.append(cNode)
                    cNode = cNode.parent
                shortestPath.append(cNode)
                shortestPath.reverse()
                return shortestPath
        return []

    def calcDistance(self, current, nxt, mode):
        if mode == "f":
            return 1
        a = (int(current.x) - int(nxt.x))**2
        b = (int(current.y) - int(nxt.y))**2
        return math.sqrt(a+b)

    def getChildren(self, x, y):
        nodelist = []
        curr_y = y
        curr_x = x

        color = self.maze[x][y].color
        if self.maze[x][y].direction == 'N':
            curr_x -= 1
            while curr_x >= 0:
                if self.maze[curr_x][curr_y].color != color:
                    nodelist.append(self.maze[curr_x][curr_y])
                    # print("appended North")
                curr_x -= 1
        if self.maze[x][y].direction == 'NE':
            curr_x -= 1
            curr_y += 1
            while curr_x >= 0 and curr_y < self.cols:
                if self.maze[curr_x][curr_y].color != color:
                    nodelist.append(self.maze[curr_x][curr_y])
                    # print("appended North-East")
                curr_x -= 1
                curr_y += 1
        if self.maze[x][y].direction == 'E':
            curr_y += 1
            while curr_y < self.cols:
                if self.maze[curr_x][curr_y].color != color:
                    nodelist.append(self.maze[curr_x][curr_y])
                    # print("appended East")
                curr_y += 1
        if self.maze[x][y].direction == 'SE':
            curr_x += 1
            curr_y += 1
            while curr_x < self.rows and curr_y < self.cols:
                if self.maze[curr_x][curr_y].color != color:
                    nodelist.append(self.maze[curr_x][curr_y])
                    # print("appended South East")
                curr_x += 1
                curr_y += 1
        if self.maze[x][y].direction == 'S':
            curr_x += 1
            while curr_x < self.rows:
                if self.maze[curr_x][curr_y].color != color:
                    nodelist.append(self.maze[curr_x][curr_y])
                    # print("appended South")
                curr_x += 1

        if self.maze[x][y].direction == 'SW':
            curr_x += 1
            curr_y -= 1
            while curr_x < self.rows and curr_y >= 0:
                if self.maze[curr_x][curr_y].color != color:
                    nodelist.append(self.maze[curr_x][curr_y])
                    # print("appended South West")
                curr_x += 1
                curr_y -= 1
        if self.maze[x][y].direction == 'W':
            curr_y -= 1
            while curr_y >= 0:
                if self.maze[curr_x][curr_y].color != color:
                    nodelist.append(self.maze[curr_x][curr_y])
                    # print("appended West")
                curr_y -= 1
        if self.maze[x][y].direction == 'NW':
            curr_y -= 1
            curr_x -= 1
            while curr_x >= 0 and curr_y >= 0:
                if self.maze[curr_x][curr_y].color != color:
                    nodelist.append(self.maze[curr_x][curr_y])
                    # print("appended North-West")
                curr_y -= 1
                curr_x -= 1
        return nodelist
