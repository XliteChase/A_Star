from maze import Maze
import time
import pygame


# constants
display_width = 800
display_height = 800
radius = 20  # node size
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)


if __name__ == "__main__":
    # run main code here
    file = open("maze.txt", "r")
    print("")
    maze = Maze()
    maze.init(file)
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))  # param is color tuple
    font1 = pygame.font.SysFont(None, 20)
    found = 'false'
    heuristic = input(
        "A* algorithm heuristics:")
    choice = input("step-by-step? ")
    start = input("Starting node: ")
    if start == 'O-O':
        print("Start and end cannot be the same.")
        quit()

    for i in range(maze.rows):
        if found == 'true':
            break
        for j in range(maze.cols):
            if maze.maze[i][j].value == start:
                found = 'true'
                x = i
                y = j
            elif i == maze.rows and j == maze.cols:
                print("Invalid starting node.")
                quit()

    if found != 'true':
        print("Invalid Starting node.")
        quit()

    if choice.lower() == 'yes' or choice.lower() == 'y':
        text_file = open("maze-sol.txt", "w")
        text_file.close()
        if heuristic.lower() == 'straight-line':
            path = maze.aStar(maze.maze[x][y], sbs=True, mode='s')
        elif heuristic.lower() == 'fewest-nodes':
            path = maze.aStar(maze.maze[x][y], sbs=True, mode='f')
        else:
            print("Invalid choice")
            quit()

    elif choice.lower() == 'no' or choice.lower() == 'n':
        text_file = open("maze-sol.txt", "w")
        text_file.close()
        if heuristic.lower() == 'straight-line':
            path = maze.aStar(maze.maze[x][y], sbs=False, mode='s')
        elif heuristic.lower() == 'fewest-nodes':
            path = maze.aStar(maze.maze[x][y], sbs=False, mode='f')
        else:
            print("Invalid choice")
            quit()

    text_file = open("maze-sol.txt", "a")
    if path:
        text_file.write("Final Solution is: \n")
        total_distance = 0
        for index in range(len(path)-1):
            current_node = path[index]
            next_node = path[index + 1]
            distance = maze.calcDistance(
                current_node, next_node, mode="" if heuristic.lower() == 's' else "f")
            total_distance += distance
            text_file.write(
                f"{current_node.value} to {next_node.value}: {round(distance, 3)}\n")
        text_file.write("**************************************************\n")
        text_file.write(f"Total path distance: {round(total_distance,3)} \n")
    else:
        text_file.write("No Solution \n")

    text_file.close()

    # loop to draw cicle at each node center
    x = 150
    y = 150
    for i in range(maze.rows):
        for j in range(maze.cols):

            img1 = font1.render(maze.maze[i][j].value, True, WHITE)
            x += 60
            if maze.maze[i][j].value[0] == 'R':
                pygame.draw.circle(screen, (255, 255, 255), (x, y), radius)
                pygame.draw.circle(screen, (255, 0, 0), (x, y), radius-4)
            else:
                pygame.draw.circle(screen, (255, 255, 255), (x, y), radius)
                pygame.draw.circle(screen, (0, 0, 255), (x, y), radius-4)
            screen.blit(img1, (x-10, y-5))
        pygame.display.update()
        y += 60
        x = 150

    timer = 0
    img1 = font1.render("Solution:", True, WHITE)
    screen.blit(img1, (100, 600))
    img1 = font1.render("Direction:", True, WHITE)
    screen.blit(img1, (100, 625))
    pygame.display.update()
    x = 150
    y = 150
    xs = 150
    ys = 600
    xd = 150
    yd = 625

    i = 0
    for node in path:
        if i < len(path)-1:
            xls = 210 + path[i].yIndex * 60
            yls = 150 + (path[i].xIndex * 60)
            xle = 210 + path[i+1].yIndex * 60
            yle = 150 + (path[i+1].xIndex * 60)
        time.sleep(1)
        x = 210 + (node.yIndex * 60)
        y = 150 + (node.xIndex * 60)
        img1 = font1.render(node.value, True, WHITE)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), radius)
        pygame.draw.circle(screen, (66, 245, 96), (x, y), radius-4)
        screen.blit(img1, (x-10, y-5))
        xs += 50
        xd += 50
        img1 = font1.render(node.value, True, WHITE)
        screen.blit(img1, (xs, ys))
        img1 = font1.render(node.direction, True, WHITE)
        screen.blit(img1, (xd, yd))
        pygame.display.update()
        pygame.draw.line(screen, GREEN, (xls, yls), (xle, yle), 2)
        i += 1

    # wait for stop, for repl.it
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
