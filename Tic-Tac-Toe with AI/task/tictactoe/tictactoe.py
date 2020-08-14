import random

player_types = ('user', 'easy', 'medium', 'hard')


class Move:
    def __init__(self, index, score):
        self.index = index
        self.score = score


class TicTacToe:
    def __init__(self):
        self.size = 3
        self.field = [i for i in range(self.size * self.size)]
        self.players = dict()

    def print_field(self):
        print('-' * self.size * self.size)
        for i in range(self.size):
            TicTacToe.print_row(self.slice_row(self.field, i))
        print('-' * self.size * self.size)

    @staticmethod
    def print_row(row):
        print('|', end=' ')
        for cell in row:
            if str(cell).isdigit():
                print(' ', end=' ')
            else:
                print(cell, end=' ')
        print('|')

    @staticmethod
    def minus_one(pair):
        return [pair[0] - 1, pair[1] - 1]

    @staticmethod
    def flip(pair):
        return [pair[0], (pair[1] * 2 + 2) % 3]

    @staticmethod
    def transpose(pair):
        return [pair[1], pair[0]]

    def convert(self, pair):
        x, y = TicTacToe.transpose(TicTacToe.flip(TicTacToe.minus_one(pair)))
        return x * self.size + y

    @staticmethod
    def count_symbol(field, symbol):
        count = 0
        for cell in field:
            if cell == symbol:
                count += 1
        return count

    def run(self):
        random.seed()
        while True:
            self.field = [i for i in range(self.size * self.size)]
            print('Input command:', end=' ')
            command = input()
            if command == 'exit':
                break
            command = command.split()
            if len(command) != 3:
                print('Bad parameters!')
                continue
            if command[0] != 'start':
                print('Bad parameters!')
                continue
            if any(command[i] not in player_types for i in range(1, 3)):
                print('Bad parameters!')
                continue
            self.players['X'] = command[1]
            self.players['O'] = command[2]
            self.run_game()

    def run_game(self):
        self.print_field()
        while True:
            self.play(self.players[self.get_player_symbol(self.field)])
            self.print_field()
            if self.get_state() != 'Game not finished':
                break
        print(self.get_state())

    def play(self, player_type):
        if player_type == player_types[0]:
            self.play_user()
        elif player_type == player_types[1]:
            self.play_easy()
        elif player_type == player_types[2]:
            self.play_medium(self.get_player_symbol(self.field), self.get_enemy_symbol(self.field))
        elif player_type == player_types[3]:
            self.play_hard()

    def minimax(self, new_board, player_symbol):
        empty_cells = TicTacToe.get_empty_cells(new_board)
        if self.has_three(new_board, self.get_enemy_symbol(self.field)):
            return Move(-1, -10)
        elif self.has_three(new_board, self.get_player_symbol(self.field)):
            return Move(-1, 10)
        elif not empty_cells:
            return Move(-1, 0)
        moves = list()
        for cell in empty_cells:
            move = Move(cell, 0)
            new_board[int(cell)] = player_symbol
            if player_symbol == self.get_player_symbol(self.field):
                result = self.minimax(new_board, self.get_enemy_symbol(self.field))
                move.score = result.score
            else:
                result = self.minimax(new_board, self.get_player_symbol(self.field))
                move.score = result.score
            new_board[int(cell)] = move.index
            moves.append(move)
        if player_symbol == self.get_player_symbol(self.field):
            best_score = -10000
            best_index = -1
            for i in range(len(moves)):
                if moves[i].score > best_score:
                    best_score = moves[i].score
                    best_index = i
        else:
            best_score = 10000
            best_index = -1
            for i in range(len(moves)):
                if moves[i].score < best_score:
                    best_score = moves[i].score
                    best_index = i
        return moves[best_index]

    def play_hard(self):
        print('Making move level "hard"')
        new_board = self.field.copy()
        move = self.minimax(new_board, self.get_player_symbol(self.field))
        self.field[move.index] = self.get_player_symbol(self.field)

    def play_medium(self, player_symbol, enemy_symbol):
        print('Making move level "medium"')
        if self.has_two(self.field, player_symbol):
            self.field[self.get_win_cell(self.field, player_symbol)] = player_symbol
        elif self.has_two(self.field, enemy_symbol):
            self.field[self.get_win_cell(self.field, enemy_symbol)] = player_symbol
        else:
            self.play_random(self.field)

    def play_easy(self):
        print('Making move level "easy"')
        self.play_random(self.field)

    @staticmethod
    def get_empty_cells(field):
        return [cell for cell in field if str(cell).isdigit()]

    @staticmethod
    def get_random_empty(field):
        return int(random.choice(TicTacToe.get_empty_cells(field)))

    def play_random(self, field):
        self.field[self.get_random_empty(field)] = self.get_player_symbol(field)

    def play_user(self):
        while True:
            print('Enter the coordinates:', end=' ')
            coordinates = input().split()
            if len(coordinates) != 2:
                print('You should enter numbers!')
                continue
            x = coordinates[0]
            y = coordinates[1]
            if not x.isdigit() or not y.isdigit():
                print('You should enter numbers!')
                continue
            x = int(x)
            y = int(y)
            if not 0 < x < 4 or not 0 < y < 4:
                print('Coordinates should be from 1 to 3!')
                continue
            index = self.convert([x, y])
            if not str(self.field[index]).isdigit():
                print('This cell is occupied! Choose another one!')
                continue
            break
        self.field[index] = self.get_player_symbol(self.field)

    def get_player_symbol(self, field):
        return 'X' if self.count_symbol(field, 'X') == self.count_symbol(field, 'O') else 'O'

    def get_enemy_symbol(self, field):
        return 'O' if self.count_symbol(field, 'X') == self.count_symbol(field, 'O') else 'X'

    def get_state(self):
        if not self.has_three_any(self.field) and self.has_empty_cells():
            return 'Game not finished'
        elif not self.has_three_any(self.field) and not self.has_empty_cells():
            return 'Draw'
        elif self.has_three(self.field, 'X'):
            return 'X wins'
        elif self.has_three(self.field, 'O'):
            return 'O wins'

    def has_empty_cells(self):
        for cell in self.field:
            if str(cell).isdigit():
                return True
        return False

    @staticmethod
    def has_three_in_slice(field_slice, symbol):
        return all(cell == symbol for cell in field_slice)

    @staticmethod
    def has_empty_in_slice(field_slice):
        return any(str(cell).isdigit() for cell in field_slice)

    @staticmethod
    def has_two_in_slice(field_slice, symbol):
        if not TicTacToe.has_empty_in_slice(field_slice):
            return False
        count = 0
        for cell in field_slice:
            if cell == symbol:
                count += 1
        return count == 2

    @staticmethod
    def get_empty_index(field_slice):
        for cell in field_slice:
            if str(cell).isdigit():
                return int(cell)
        return -1

    def cut_to_slices(self, field):
        slices = list()
        for i in range(self.size):
            slices.append(self.slice_row(field, i))
        for j in range(self.size):
            slices.append(self.slice_column(field, j))
        slices.append(self.slice_major_diagonal(field))
        slices.append(self.slice_minor_diagonal(field))
        return slices

    def get_win_cell(self, field, symbol):
        for field_slice in self.cut_to_slices(field):
            if self.has_two_in_slice(field_slice, symbol):
                return self.get_empty_index(field_slice)
        return -1

    def slice_row(self, field, i):
        return field[self.size * i: self.size * (i + 1)]

    def slice_column(self, field, j):
        return field[j: self.size * self.size: self.size]

    def slice_major_diagonal(self, field):
        return field[0: self.size * self.size: self.size + 1]

    def slice_minor_diagonal(self, field):
        return field[self.size - 1: self.size * self.size - 1: self.size - 1]

    def has_three(self, field, symbol):
        for field_slice in self.cut_to_slices(field):
            if self.has_three_in_slice(field_slice, symbol):
                return True
        return False

    def has_two(self, field, symbol):
        for field_slice in self.cut_to_slices(field):
            if self.has_two_in_slice(field_slice, symbol):
                return True
        return False

    def has_three_any(self, field):
        return self.has_three(field, 'X') or self.has_three(field, 'O')


game = TicTacToe()
game.run()
