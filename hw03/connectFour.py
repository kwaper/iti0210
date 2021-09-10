import random
from copy import deepcopy


class MCTS():
    player_side = None
    computer_side = None
    turn = None

    def __init__(self):
        self.board = [[" " for x in range(7)] for y in range(6)]
        while self.player_side is None:
            answer = input("Want to start? y/n ")
            if answer.lower() == "y":
                self.turn = True
                self.player_side = "X"
                self.computer_side = "O"
            elif answer.lower() == "n":
                self.turn = False
                self.computer_side = "X"
                self.player_side = "O"

    def print_board(self):
        [print(x) for x in self.board]
        print("[=================================]")
        print(["0", "1", "2", "3", "4", "5", "6"])

    def make_move(self, move):
        col = [self.board[y][move] for y in range(6)]
        if 0 <= move <= 6 and not self.is_over(self.board)[0] and len(col) > 0:
            for i in range(5, -1, -1):
                if " " in col[i]:
                    if self.turn:
                        self.board[i][move] = self.player_side
                        self.turn = False
                    else:
                        self.board[i][move] = self.computer_side
                        self.turn = True
                    break

    def is_over(self, board):
        # column check
        for col in range(7):
            player = 0
            pc = 0
            for row in range(6):
                if self.player_side in board[row][col]:
                    player += 1
                    pc = 0
                    if player >= 4:
                        return True, self.player_side
                if self.computer_side in board[row][col]:
                    pc += 1
                    player = 0
                    if pc >= 4:
                        return True, self.computer_side
        #  row check
        for row in range(6):
            player = 0
            pc = 0
            for col in range(7):
                if " " in board[row][col]:
                    player = 0
                    pc = 0
                if self.player_side in board[row][col]:
                    player += 1
                    pc = 0
                    if player >= 4:
                        return True, self.player_side
                if self.computer_side in board[row][col]:
                    pc += 1
                    player = 0
                    if pc >= 4:
                        return True, self.computer_side

        #  diag from up to down
        for c in range(4):
            for r in range(3):
                ai = self.computer_side
                if ai in board[r][c] and ai in board[r + 1][c + 1] and ai in board[r + 2][c + 2] and ai in board[r + 3][
                    c + 3]:
                    return True, self.computer_side
                p = self.player_side
                if p in board[r][c] and p in board[r + 1][c + 1] and p in board[r + 2][c + 2] and p in board[r + 3][
                    c + 3]:
                    return True, self.player_side

        #  diag from bottom to up
        for c in range(4):
            for r in range(3, 6):
                ai = self.computer_side
                if ai in board[r][c] and ai in board[r - 1][c + 1] and ai in board[r - 2][c + 2] and ai in board[r - 3][
                    c + 3]:
                    return True, self.computer_side
                p = self.player_side
                if p in board[r][c] and p in board[r - 1][c + 1] and p in board[r - 2][c + 2] and p in board[r - 3][
                    c + 3]:
                    return True, self.player_side

        #  draw check
        if len(self.moves(board)) == 0:
            return True, "DRAW"

        return False, "PLAY"

    def moves(self, pos):
        possible_moves = []
        for c in range(7):
            col = [pos[r][c] for r in range(6)]
            if " " in col:
                possible_moves.append(c)
        return possible_moves

    def simulate_move(self, move, pos, turn):
        col = [pos[y][move] for y in range(6)]
        if 0 <= move <= 6 and len(col) > 0:
            for i in range(5, -1, -1):
                if " " in col[i]:
                    if turn:
                        pos[i][move] = self.player_side
                    else:
                        pos[i][move] = self.computer_side
                    return pos
        return pos

    def simulate(self, move):
        pos = deepcopy(self.board)
        turn = False
        pos = self.simulate_move(move, pos, turn)

        while not self.is_over(pos)[0]:
            turn = True
            m = self.moves(pos)
            random_move = random.choice(m)
            pos = self.simulate_move(random_move, pos, turn)
            turn = False
            if self.is_over(pos)[0]:
                break
            random_move = random.choice(self.moves(pos))
            pos = self.simulate_move(random_move, pos, turn)
            if self.is_over(pos)[0]:
                break
        return self.is_over(pos)[1]

    def pure_mc(self, n):
        initial_moves = self.moves(self.board)
        win_counts = dict((move, 0) for move in initial_moves)

        for move in initial_moves:
            for i in range(n):
                res = self.simulate(move)
                if res == self.computer_side:
                    win_counts[move] += 1
                elif res == "DRAW":
                    win_counts[move] += 0.5
        print()
        print(win_counts)

        best_move = 0
        best_value = 0
        for move, value in win_counts.items():
            if value > best_value:
                best_value = value
                best_move = move

        return best_move


if __name__ == '__main__':
    mc = MCTS()
    mc.print_board()
    playing = True
    while playing:
        if mc.turn:
            print()
            turn = input("Choose move ")
            while not turn.isdecimal():
                turn = input("Choose move ")
            move = int(turn)
            print()
        else:
            move = mc.pure_mc(200)
            print(f"AI MOVE : {move}")
            print()

        mc.make_move(move)
        mc.print_board()

        state, winner = mc.is_over(mc.board)
        if state:
            if mc.computer_side == winner:
                print("\nAI WON!")
            if mc.player_side == winner:
                print("\nYOU WON!")
            playing = False
