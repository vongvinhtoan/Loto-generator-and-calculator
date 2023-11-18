class LotoSheet:
    def __init__(self, sheet_array: list[list[str]]) -> None:
        self.sheet_array = sheet_array
        self.positions = {}
        for i in range(0, 9):
            for j in range(0, 5):
                self.positions[self.sheet_array[i][j]] = (i, j)
        self.count = [5] * 9
        self.marked = [[False] * 5 for _ in range(0, 9)]

    def id(self) -> str:
        return "".join([str(x) for x in self.sheet_array[0]])

    def isMarked(self, x: int) -> bool:
        pos = self.positions[x]
        return self.marked[pos[0]][pos[1]]

    def mark(self, x: int) -> None:
        if self.positions.get(x) == None:
            return
        pos = self.positions[x]
        if not self.isMarked(x):
            self.marked[pos[0]][pos[1]] = True
            self.count[pos[0]] -= 1

    def unmark(self, x: int) -> None:
        if self.positions.get(x) == None:
            return
        pos = self.positions[x]
        if self.isMarked(x):
            self.marked[pos[0]][pos[1]] = False
            self.count[pos[0]] += 1

    def isComplete(self) -> bool:
        for i in range(0, 9):
            if self.count[i] == 0:
                return True
        return False
    
    def reset(self) -> None:
        self.count = [5] * 9
        self.marked = [[False] * 5 for _ in range(0, 9)]

########################################################################################

import random

def create_slot() -> (bool, list[list[str]]):
    col_count = [5] * 9
    row_count = [5] * 9
    total_count = 5 * 9
    board = [['X' for _ in range(0, 9)] for _ in range(0, 9)]
    for _ in range(0, total_count):
        available_cells = []
        for i in range(0, 9):
            for j in range(0, 9):
                if board[i][j] == 'X' and col_count[j] > 0 and row_count[i] > 0:
                    available_cells.append((i, j))

        if len(available_cells) == 0:
            return False, board

        cell = random.choice(available_cells)
        board[cell[0]][cell[1]] = 'O'
        row_count[cell[0]] -= 1
        col_count[cell[1]] -= 1
    
    return True, board

def get_random_distinct_integers(count: int, min: int, max: int) -> list[int]:
    if count > max - min + 1:
        raise Exception("count > max - min + 1")
    result = list[int]([])
    while len(result) < count:
        rand = random.randint(min, max)
        if rand not in result:
            result.append(rand)
    random.shuffle(result)
    return result

def create_random_board() -> list[list[str]]:
    while True:
        result, board = create_slot()
        if result:
            break

    for i in range(0, 9):
        values = []
        if i != 0:
            values = get_random_distinct_integers(5, 0, 9)
        else:
            values = get_random_distinct_integers(5, 1, 9)

        for j in range(0, 9):
            if board[i][j] == 'O':
                result_string = ""
                if i > 0:
                    result_string += str(i)
                result_string += str(values.pop())
                board[i][j] = result_string
    return board

def create_random_lotoSheet() -> LotoSheet:
    while True:
        result, board = create_slot()
        if result:
            break

    for i in range(0, 9):
        values = []
        if i != 0:
            values = get_random_distinct_integers(5, 0, 9)
        else:
            values = get_random_distinct_integers(5, 1, 9)

        for j in range(0, 9):
            if board[i][j] == 'O':
                result_string = ""
                if i > 0:
                    result_string += str(i)
                result_string += str(values.pop())
                board[i][j] = result_string
    
    board = [[board[j][i] for j in range(0, 9)] for i in range(0, 9)]
    board = [[int(x) for x in board[i] if x != 'X'] for i in range(0, len(board))]
    return LotoSheet(board)

def create_distinct_random_sheet(count: int) -> list[LotoSheet]:
    result = []
    while len(result) < count:
        sheet = create_random_lotoSheet()
        if sheet not in result:
            result.append(sheet)
    return result