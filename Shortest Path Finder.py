HEIGHT = WIDTH = 800
ROWS = 20

ITM_HEIGHT = HEIGHT // ROWS
ITM_WIDTH = ITM_HEIGHT

HEIGHT = ROWS * ITM_HEIGHT
COLUMNS = WIDTH // ITM_WIDTH
WIDTH = ITM_WIDTH * COLUMNS

print(WIDTH, " ", HEIGHT, " ", ITM_HEIGHT, " ", ITM_WIDTH, " ", ROWS, " ", COLUMNS)

COL_GRIDLINES = (0, 0, 0)  # BLACK
COL_WALL = (100, 0, 0)  # BLACK
COL_BG = (255, 255, 255)  # WHITE
COL_START = (0, 255, 0)  # GREEN
COL_END = (255, 0, 0)  # RED
COL_IMPOSSIBLE = (127, 127, 127)  # GREY
COL_VISIT = (0, 0, 200)  # BLUE
COL_PATH = (200, 200, 0)  # YELLOW


# helper
import pygame
from queue import PriorityQueue


def generate_grid(screen, rows, cols, Item):
    grid = []
    for row in range(rows):
        grid.append([])
        for col in range(cols):
            grid[row].append(Item(screen, row, col))

    return grid


def get_pos(x, y):
    return x // (WIDTH // ROWS), y // (WIDTH // ROWS)


def handle_mouse_event(board):
    grid = board.grid
    start = board.start
    end = board.end

    x, y = pygame.mouse.get_pos()
    row, col = get_pos(x, y)

    if not start:
        grid[row][col].set_start()
        board.start = grid[row][col]

    elif not end and grid[row][col] != start:
        grid[row][col].set_end()
        board.end = grid[row][col]

    elif grid[row][col] != start and grid[row][col] != end:
        grid[row][col].set_wall()


def draw_path(from_list, start, end):
    if end == start:
        return
    end.set_path()
    draw_path(from_list, start, from_list[end])


#######################ITEM CLASS########################
class Item:
    ITEM_HEIGHT = ITEM_WIDTH = ITM_HEIGHT

    def __init__(self, screen, row, col):
        self.screen = screen
        self.row = row
        self.col = col
        self.color = COL_BG
        self.neighbours = []

        self.x = self.row * self.ITEM_HEIGHT
        self.y = self.col * self.ITEM_WIDTH

    def make_last(self):
        self.row = -1
        self.col = -1

    def new_pos(self, x, y):
        self.row = x
        self.col = y

    def is_wall(self):
        return self.color == COL_WALL

    def set_start(self):
        self.color = COL_START

    def set_end(self):
        self.color = COL_END

    def set_wall(self):
        self.color = COL_WALL

    def set_visited(self):
        self.color = COL_VISIT

    def set_cantvisit(self):
        self.color = COL_IMPOSSIBLE

    def set_path(self):
        self.color = COL_PATH

    def get_neighbour(self, grid, start):
        neighbours = []

        if (
            self.row > 0
            and self.row < ROWS
            and self.col >= 0
            and self.col < COLUMNS
            and not grid[self.row - 1][self.col].is_wall()
            and not (self.row - 1 == start.row and self.col == start.col)
        ):
            neighbours.append(grid[self.row - 1][self.col])

        if (
            self.row < ROWS - 1
            and self.col >= 0
            and self.col < COLUMNS
            and not grid[self.row + 1][self.col].is_wall()
            and not (self.row + 1 == start.row and self.col == start.col)
        ):
            neighbours.append(grid[self.row + 1][self.col])

        if (
            self.col > 0
            and self.row >= 0
            and self.row < ROWS
            and not grid[self.row][self.col - 1].is_wall()
            and not (self.row == start.row and self.col - 1 == start.col)
        ):
            neighbours.append(grid[self.row][self.col - 1])

        if (
            self.col < COLUMNS - 1
            and self.col >= 0
            and self.row >= 0
            and self.row < ROWS
            and not grid[self.row][self.col + 1].is_wall()
            and not (self.row == start.row and self.col + 1 == start.col)
        ):
            neighbours.append(grid[self.row][self.col + 1])

        return neighbours

    def get_neighbours(self, grid):
        neighbours = []

        if (
            self.row > 0
            and self.row < ROWS
            and self.col >= 0
            and self.col < COLUMNS
            and not grid[self.row - 1][self.col].is_wall()
        ):
            neighbours.append(grid[self.row - 1][self.col])

        if (
            self.row < ROWS - 1
            and self.col >= 0
            and self.col < COLUMNS
            and not grid[self.row + 1][self.col].is_wall()
        ):
            neighbours.append(grid[self.row + 1][self.col])

        if (
            self.col > 0
            and self.row >= 0
            and self.row < ROWS
            and not grid[self.row][self.col - 1].is_wall()
        ):
            neighbours.append(grid[self.row][self.col - 1])

        if (
            self.col < COLUMNS - 1
            and self.col >= 0
            and self.row >= 0
            and self.row < ROWS
            and not grid[self.row][self.col + 1].is_wall()
        ):
            neighbours.append(grid[self.row][self.col + 1])

        return neighbours

    def draw(self):
        pygame.draw.rect(
            self.screen, self.color, (self.x, self.y, self.ITEM_HEIGHT, self.ITEM_WIDTH)
        )

    def get_pos(self):
        return self.x, self.y

    def __hash__(self):
        return self.x + self.y

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def out(self):
        print(self.row, " ", self.col)


#############BOARD CLASS######################
class Board:
    def __init__(self, screen):
        self.screen = screen
        self.grid = generate_grid(screen, ROWS, COLUMNS, Item)
        self.start = None
        self.end = None

    def _draw_lines(self):
        for row in self.grid:
            for col in row:
                x, y = col.get_pos()
                pygame.draw.rect(
                    self.screen,
                    COL_GRIDLINES,
                    pygame.Rect(x, y, col.ITEM_HEIGHT, col.ITEM_WIDTH),
                    1,
                )

    def draw(self):
        for row in self.grid:
            for col in row:
                col.draw()

        self._draw_lines()
        pygame.display.update()


# dikjstra


def Dikjstra(board):
    grid = board.grid
    start = board.start
    end = board.end
    last = board.start
    last.make_last

    visited = {col: 0 for row in grid for col in row}

    distance = {col: float("inf") for row in grid for col in row}
    distance[start] = 0

    open_set = PriorityQueue()
    open_set.put((0, 0, start))

    from_list = {}
    count = 0

    while not open_set.empty():
        current = open_set.get()[2]
        current.out()

        if visited[current]:
            continue

        if current == end:
            draw_path(from_list, start, end)
            return

        for neighbour in current.get_neighbour(grid, start):
            if distance[neighbour] > distance[current] + 1:
                distance[neighbour] = 1 + distance[current]
                count += 1
                open_set.put((distance[neighbour], count, neighbour))
                from_list[neighbour] = current

        current.set_visited()
        current.draw()
        pygame.display.update()
        visited[current] = True

    print("Not Found!")

    visited = {col: 0 for row in grid for col in row}

    distance = {col: float("inf") for row in grid for col in row}
    distance[start] = 0

    open_set = PriorityQueue()
    open_set.put((0, 0, start))

    count = 0
    while not open_set.empty():
        current = open_set.get()[2]

        if visited[current]:
            continue

        for neighbour in current.get_neighbour(grid, start):
            if distance[neighbour] > distance[current] + 1:
                distance[neighbour] = 1 + distance[current]
                count += 1
                open_set.put((distance[neighbour], count, neighbour))

        visited[current] = True
        current.set_cantvisit()

    return


# a_star
def heuristic(pos1, pos2):
    return abs(pos1.row - pos2.row) + abs(pos2.col - pos1.col)


def Astar(game):
    grid = game.grid
    start = game.start
    end = game.end

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    closed_set = [start]

    g_scores = {item: float("inf") for col in grid for item in col}
    g_scores[start] = 0

    f_score = {item: float("inf") for col in grid for item in col}
    f_score[start] = heuristic(start, end)

    from_list = {}

    while not open_set.empty():
        current = open_set.get()[2]
        print(current.row, " ", current.col, "\n")
        closed_set.remove(current)

        if current == end:
            draw_path(from_list, start, end)
            return

        for neighbour in current.get_neighbours(grid):
            temp_g_score = g_scores[current] + 1

            if temp_g_score < g_scores[neighbour]:
                from_list[neighbour] = current

                g_scores[neighbour] = temp_g_score
                h_score = heuristic(neighbour, end)
                f_score = temp_g_score + h_score

                current.set_visited()
                current.draw()
                start.set_start()
                start.draw()
                pygame.display.update()

                if neighbour not in closed_set:
                    count += 1
                    open_set.put((f_score, count, neighbour))
                    closed_set.append(neighbour)

    print("Not Found!")

    visited = {col: 0 for row in grid for col in row}

    distance = {col: float("inf") for row in grid for col in row}
    distance[start] = 0

    open_set = PriorityQueue()
    open_set.put((0, 0, start))

    count = 0
    while not open_set.empty():
        current = open_set.get()[2]

        if visited[current]:
            continue

        for neighbour in current.get_neighbour(grid, start):
            if distance[neighbour] > distance[current] + 1:
                distance[neighbour] = 1 + distance[current]
                count += 1
                open_set.put((distance[neighbour], count, neighbour))

        visited[current] = True
        current.set_cantvisit()

    return


import pygame

pygame.init()
pygame.display.set_caption("Path Finder")
screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen.fill(COL_BG)  # COLOR


def main():
    running = True
    dragging = False
    disabled = False

    board = Board(screen)
    grid = board.grid

    while running:
        board.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if disabled and (
                event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN
            ):
                disabled = False
                board = Board(screen)
                grid = board.grid

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    handle_mouse_event(board)

            elif event.type == pygame.MOUSEMOTION and dragging:
                handle_mouse_event(board)

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Dikjstra(board)
                    board.start.set_start()
                    board.end.set_end()
                    disabled = True

                elif event.key == pygame.K_RETURN:
                    Astar(board)
                    board.start.set_start()
                    board.end.set_end()
                    disabled = True

    pygame.quit()


if __name__ == "__main__":
    main()
