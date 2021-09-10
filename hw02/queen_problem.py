import random
import time


class NQPosition:
    board = []
    queen_list = []
    queen_moves = {}

    def __init__(self, N):
        queens = [random.randint(0, N - 1) for queen in range(N)]
        self.queen_list = [(x, queens[x]) for x in range(len(queens))]
        self.board = [["Q" if (row, col) in self.queen_list else "*" for col in range(N)] for row in range(N)]

    def value(self):
        number = len(self.board)
        cols = 0
        diagonals = 0
        for col in range(number):
            column = [x[col] for x in self.board]
            queens = len([x for x in column if x == "Q"])
            if queens > 1:
                cols += queens - 1

        for d in range(len(self.queen_list)):
            for d1 in range(d + 1, len(self.queen_list)):
                if abs(self.queen_list[d][0] - self.queen_list[d1][0]) == abs(
                        self.queen_list[d][1] - self.queen_list[d1][1]):
                    diagonals += 1
        return cols + diagonals

    def value_check(self, prev_new):
        new_queen_list = [x for x in self.queen_list]
        new_queen_list.remove(prev_new[0])
        new_queen_list.append(prev_new[1])
        cols = 0
        diagonals = 0
        for d in range(len(new_queen_list)):
            for d1 in range(d + 1, len(new_queen_list)):
                if new_queen_list[d][1] == new_queen_list[d1][1]:
                    cols += 1
                if abs(new_queen_list[d][0] - new_queen_list[d1][0]) == abs(
                        new_queen_list[d][1] - new_queen_list[d1][1]):
                    diagonals += 1
        return cols + diagonals

    def best_move(self):
        all_queens_moves = {}
        for queen in self.queen_list:
            possible_queen_moves = [(queen[0], x) for x in range(len(self.board)) if x != queen[1]]
            for move in possible_queen_moves:
                prev_new = (queen, move)
                all_queens_moves[prev_new] = self.value_check(prev_new)

        sorted_x = sorted(all_queens_moves.items(), key=lambda kv: kv[1])
        move = sorted_x[0][0]
        value = sorted_x[0][1]
        return move, value

    def make_move(self, move):
        new_queen_list = self.queen_list
        # queen list fix
        new_queen_list.remove(move[0])
        new_queen_list.append(move[1])
        # table fix
        self.board[move[0][0]][move[0][1]] = "*"
        self.board[move[1][0]][move[1][1]] = "Q"


def hill_climbing(pos):
    counter = 0
    while True:
        move, new_value = pos.best_move()
        if new_value == 0 or counter > 100:
            pos.make_move(move)
            counter += 1
            return pos, new_value, counter
        else:
            counter += 1
            pos.make_move(move)


def multiple_test(iterations, queens):
    iterations = iterations
    queen_number = queens
    times = []
    final_values = []
    ideal_finish = 0
    not_ideal_finish = 0
    total_start = time.time()
    for i in range(iterations):
        pos = NQPosition(queen_number)
        start = time.time()
        best_pos, best_value, counter = hill_climbing(pos)
        end = time.time()
        times.append(end - start)
        final_values.append(best_value)
        if best_value > 0:
            not_ideal_finish += 1
        else:
            ideal_finish += 1
    total_end = time.time()

    print(f"Iterations : {iterations}")
    print(f"Queen number : {queen_number}")
    print(f"Average time : {sum(times) / len(times)}")
    print(f"Ideal finish : {ideal_finish}")
    print(f"Not ideal finish : {not_ideal_finish}")
    not_ideal_percent = round((not_ideal_finish / ideal_finish) * 100, 2)
    print(f"Percentage of ideal tries : {100 - not_ideal_percent}%")
    print(f"Percentage of not ideal tries : {not_ideal_percent}%")
    print(f"Total time spent : {round(total_end - total_start, 2)} sec")


def single_test(queens):
    pos = NQPosition(queens)  # test with the tiny 4x4 board first

    print("\n========BOARD BEFORE IMPROVEMENTS==========")
    print("___________________________________________\n")
    [print(x) for x in pos.board]
    start = time.time()
    best_pos, best_value, counter = hill_climbing(pos)
    end = time.time()
    print("\n=========BOARD AFTER IMPROVEMENTS==========")
    print("___________________________________________\n")
    [print(x) for x in pos.board]

    print(f"Single test for {queens} queens")
    print("Final value", best_value)
    print(f"Moves : {counter} ")
    print(f"Time spent : {end - start} sec")


if __name__ == '__main__':
    # multiple_test(1000, 8)
    single_test(8)
