from maze import Maze

if __name__ == "__main__":
    # run main code here
    file = open("new-maze.txt", "r")
    print("")
    maze = Maze()
    maze.init(file)
    found = 'false'
    heuristic = input(
        "A* algorithm heuristics:")
    choice = input("step-by-step? ")
    start = input("Enter the start node: ")
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
            mode = "s" if heuristic.lower() == "straight-line" else "f"
            distance = maze.calcDistance(
                current_node, next_node, mode)
            total_distance += distance
            text_file.write(
                f"{current_node.value} to {next_node.value}: {round(distance, 3)}\n")
        text_file.write("**************************************************\n")
        text_file.write(f"Total path distance: {round(total_distance,3)} \n")
    else:
        text_file.write("No Solution \n")

    text_file.close()
