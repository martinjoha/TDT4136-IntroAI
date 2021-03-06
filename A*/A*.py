from tkinter import *
import time

class SearchNode:

    def __init__(self, x, y, weight, char):
        self.char = char            # easily print the
        self.x = x                  # The x coordinates of the node in a search grid
        self.y = y                  # The y coordinates of the node in a search grid
        self.g = 0                  # The total cost of getting from start to this node
        self.weight = weight        # Cost of crossing node
        self.h = 0                  # The nodes euclidian distance to the goal
        self.f = self.g + self.h    # The estimated value from the node to the goal
        self.parent = None          # The current best parent to the node
        self.successors = []        # All the adjacent node, north, south, west, east

#Easy way to represent the node in a grid
    def __str__(self):
        return self.char


class AStar:

    def __init__(self, grid, startnode, endnode, algorithm="AStar"):
        self.grid = grid                        # The initial grid containing n nodes
        self.startnode = startnode              # The startpoint of the path we want to find.
        self.endnode = endnode                  # Goal
        self.algorithm = algorithm              # The selected algorithm we want to run on the grid, default will be A*.py


    # getting all the adjacent nodes. Will remove a node if it is the nodes parent
    def generate_successors(self, node):
        if node.x > 0: # Checking that a left successor e
            node.successors.append(self.grid.board[node.y][node.x - 1])
        if node.x < self.grid.width - 1:  # if node is on the right edge, it will only have three adjacent nodes
            node.successors.append(self.grid.board[node.y][node.x + 1])
        if node.y > 0:
            node.successors.append(self.grid.board[node.y - 1][node.x])
        if node.y < self.grid.height - 1:  # if the node is on the bottom, it can a most have three neighbors
            node.successors.append(self.grid.board[node.y + 1][node.x])
        if node.parent in node.successors:
            node.successors.remove(node.parent)

    def best_first_search(self):
        open = [self.startnode]
        closed = []
        self.startnode.h = abs(self.startnode.x - self.endnode.x) + abs(self.startnode.y - self.endnode.y)
        self.startnode.f = self.startnode.h

        while True:
            if not open:
                print("fail")
                return
            current = open.pop(0)
            self.generate_successors(current)
            # Just changing the char value of all the open and closed nodes for easy visualization
            if current == self.endnode and self.algorithm != "BFS":
                print("success")
                """for node in open:
                    node.char = "x"
                for node in closed:
                    if node != self.startnode:
                        node.char = "*" """
                return
            closed.append(current)
            # The general A*.py star algorithm
            for successor in current.successors:
                if successor.char == "#":
                    pass
                elif successor not in open and successor not in closed:
                    open.append(successor)
                    self.attach_and_eval(successor, current)
                elif current.g + successor.weight < successor.g:
                    self.attach_and_eval(successor, current)
                    self.propagate_path_improvements(current)
            if self.algorithm != "BFS":
                open.sort(key=lambda x: x.f)

    # Attaching the node to a parent node
    def attach_and_eval(self, child, parent):
        child.h = abs(child.x - self.endnode.x) + abs(child.y - self.endnode.y)
        child.g = parent.g + child.weight
        child.f = child.g + child.h
        # If not a star, we will not calculate distance to goal in the f value
        if self.algorithm != "AStar":
            child.f = child.g
        child.parent = parent

    # When a node has a parent, will evaluate the best path for the node
    def propagate_path_improvements(self, parent):
        for kid in parent.successors:
            if parent.g + kid.weight < kid.g:
                kid.parent = parent
                kid.g = parent.g + kid.weight
                kid.f = kid.g + kid.h
                if self.algorithm != "AStar":
                    kid.f = kid.g
                self.propagate_path_improvements(kid)


class Grid:

    def __init__(self, algorithm="AStar"):
        self.height = 0
        self.width = 0
        self.board = []
        self.startnode = None
        self.endnode = None
        self.algorithm = algorithm

    # Just so i can print the grid and see that the algorithm works
    def __str__(self):
        board = ""
        for line in self.board:
            for node in line:
                board += str(node)
            board += "\n"
        return board

    # generating the grid and then running the selected algorithm to find the best path
    def generate_path_board(self, inputboard):
        with open(inputboard, 'r') as inputboard:
            y = 0
            for line in inputboard:
                x = 0
                row = []
                for char in line:
                    if char == "w":
                        row.append(SearchNode(x, y, 100, char))
                    elif char == "m":
                        row.append(SearchNode(x, y, 50, char))
                    elif char == "f":
                        row.append(SearchNode(x, y, 10, char))
                    elif char == "g":
                        row.append(SearchNode(x, y, 5, char))
                    elif char == ".":
                        row.append(SearchNode(x, y, 1, char))
                    elif char == "#":
                        row.append(SearchNode(x, y, float("inf"), char))
                    elif char == "r":
                        row.append(SearchNode(x, y, 1, char))
                    elif char == "A":
                        start = SearchNode(x, y, 0, char)
                        row.append(start)
                        self.startnode = start
                    elif char == "B":
                        end = SearchNode(x, y, 1, char)
                        row.append(end)
                        self.endnode = end
                    x += 1
                self.board.append(row)
                y += 1
            self.width = len(self.board[1])
            self.height = len(self.board)
            astar = AStar(self, self.startnode, self.endnode, self.algorithm)
            astar.best_first_search()
            current = self.endnode.parent

            while True:
                if current == self.startnode:
                    break
                current.char = '•'
                current = current.parent
            print(self)


# Main part of the project where i will draw a canvas using tkinter to visualize the board and the path
# to take from A to B. Will also display the open and closed nodes
# where * is closed and x is open
def draw_task_1(inboard, algorithm):
    master = Tk()
    w = Canvas(master, width=600, height=210)
    w.pack()

    # Creating the grid in the canvas
    for i in range(0, 601, 30):
        w.create_line(i, 0, i, 210, fill="black")
    for i in range(0, 211, 30):
        w.create_line(0, i, 600, i, fill="black")

    #Drawing the initial canvas, then running the algorithm, and filling it in
    with open(inboard, 'r') as inputboard:
        lines = inputboard.read().splitlines()
        for j in range(len(lines)):
            for i in range(len(lines[0])):
                if lines[j][i] == "#":
                    w.create_rectangle(i * 30, j * 30, (i + 1) * 30, (j + 1) * 30, fill="grey")
                elif lines[j][i] == ".":
                    w.create_rectangle(i * 30, j * 30, (i + 1) * 30, (j + 1) * 30, fill="white")
                elif lines[j][i] == "A":
                    w.create_rectangle(i * 30, j * 30, (i + 1) * 30, (j + 1) * 30, fill="red")
                    w.create_text(i * 30 + 15, j * 30 + 15, font="Times 20", text="A")
                elif lines[j][i] == "B":
                    w.create_rectangle(i * 30, j * 30, (i + 1) * 30, (j + 1) * 30, fill="light green")
                    w.create_text(i * 30 + 15, j * 30 + 15, font="Times 20", text="B")
    grid = Grid(algorithm)
    grid.generate_path_board(inboard)
    for j in range(len(lines)):
            for i in range(len(lines[0])):
                if grid.board[j][i].char == "•":
                    w.create_text(i * 30 + 15, j * 30 + 15, font="Times 20", text="•")
                elif grid.board[j][i].char == "x":
                    w.create_text(i * 30 + 15, j * 30 + 15, font="Times 20", text="x")
                elif grid.board[j][i].char == "*":
                    w.create_text(i * 30 + 15, j * 30 + 15, font="Times 20", text="*")
    mainloop()


def draw_task_2(inboard, algorithm):
    master = Tk()
    w = Canvas(master, width=800, height=200)
    w.pack()

    # Creating the grid
    for i in range(0, 801, 20):
        w.create_line(i, 0, i, 200, fill="black")
    for i in range(0, 201, 20):
        w.create_line(0, i, 800, i, fill="black")

    #Drawing the initial canvas, then running the algorithm, and filling it in with the proper text
    with open(inboard, 'r') as inputboard:
        lines = inputboard.read().splitlines()
        for j in range(len(lines)):
            for i in range(len(lines[0])):
                if lines[j][i] == "w":
                    w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="blue")
                elif lines[j][i] == "m":
                    w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="grey")
                elif lines[j][i] == "f":
                    w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="dark green")
                elif lines[j][i] == "g":
                    w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="green")
                elif lines[j][i] == "r":
                    w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="chocolate")
                elif lines[j][i] == "A":
                    w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="red")
                    w.create_text(i * 20 + 10, j * 20 + 10, font="Times 20", text="A")
                elif lines[j][i] == "B":
                    w.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="light green")
                    w.create_text(i * 20 + 10, j * 20 + 10, font="Times 20", text="B")
    grid = Grid(algorithm)
    grid.generate_path_board(inboard)
    # Filling in the path, as well as the open and closed nodes if i want that
    for j in range(len(lines)):
            for i in range(len(lines[0])):
                #print(i, j, grid.board[j][i])
                if grid.board[j][i].char == "•":
                    w.create_text(i * 20 + 10, j * 20 + 10, font="Times 20", text="•")
                elif grid.board[j][i].char == "x":
                    w.create_text(i * 20 + 10, j * 20 + 10, font="Times 20", text="x")
                elif grid.board[j][i].char == "*":
                    w.create_text(i * 20 + 10, j * 20 + 10, font="Times 20", text="*")
    mainloop()


"""
draw_task_1('./boards/board-1-1.txt', "AStar")
draw_task_1('./boards/board-1-2.txt', "AStar")
draw_task_1('./boards/board-1-3.txt', "AStar")
draw_task_1('./boards/board-1-4.txt', "AStar")

draw_task_2('./boards/board-2-1.txt', "AStar")
draw_task_2('./boards/board-2-2.txt', "Astar")
draw_task_2('./boards/board-2-3.txt', "AStar")
draw_task_2('./boards/board-2-4.txt', "AStar")
draw_task_2('./boards/board-2-4.txt', "Dijkstra")
draw_task_2('./boards/board-2-4.txt', "BFS")
"""

#grid1 = Grid()
#grid1.generate_task_1('./boards/board-1-2.txt')
grid2 = Grid()
grid2.generate_path_board('./boards/board-2-2.txt')

