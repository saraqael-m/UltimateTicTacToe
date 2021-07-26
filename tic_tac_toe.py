import numpy as np
from copy import deepcopy
from sys import exit

class Board:

	def __init__(self, board = np.zeros((3,3), dtype=int)) -> None:
		self.board = board

	def __str__(self) -> str:
		'''string representation'''
		return str(self.board).replace("-1", "X").replace("1", "O").replace("0", "-").replace(" ", "").replace("[", "").replace("]", "")+"\n"

	def place_marker(self, marker_pos : list, marker_type : int) -> bool:
		'''places marker and returns whether it was successful or not'''
		if marker_type == 0 or self.board[marker_pos[0], marker_pos[1]] == 0: # if marker will be removed or the posistion is not filled
			self.board[marker_pos[0], marker_pos[1]] = marker_type # place marker
			return True # successful
		return False

	def check_win(self) -> int:
		'''checks if anyone has won'''
		sum_list = list(np.sum(self.board, axis=1)) + list(np.sum(self.board, axis=0)) + [np.trace(self.board), np.trace(np.rot90(self.board))] # list of sums of diagonals, horizontals, verticals
		if 3 in sum_list: # a row of three 1s
			return 1
		if -3 in sum_list: # a row of three 0s
			return -1
		if 0 in list(self.board.flatten()): # there are still moves
			return None
		return 0

class Player:

	def __init__(self, board, marker_type, keybinds : list) -> None:
		self.board = board
		self.marker_type = marker_type
		self.keybinds = keybinds

	def turn(self) -> None:
		'''executes one player turn by getting the input pos and placing a marker if it is valid'''
		while True:
			marker_pos_in = str(input("Input the position of your next marker: "))
			if marker_pos_in in self.keybinds:
				marker_pos_num = self.keybinds.index(marker_pos_in)
				marker_pos = [marker_pos_num // 3, marker_pos_num % 3]
				if self.board.place_marker(marker_pos, self.marker_type):
					break
			elif marker_pos_in == "":
				exit()

class Computer:

	def __init__(self, board, marker_type : int) -> None:
		self.board = board
		self.marker_type = marker_type

	def unified_minimax(self, test_board, minimax_type : int, alpha : int, beta : int) -> tuple:
		'''max and min of "minimax"; depending on "minimax_type" variable (max : 1, min : -1)'''
		extreme_val = -2*minimax_type # worst case
		x, y = None, None
		winner = test_board.check_win()
		if winner != None:
			return (winner*self.marker_type, 0, 0)
		for i in [index for index, val in np.ndenumerate(test_board.board) if val == 0]: # all empty cells
			test_board.place_marker(i, self.marker_type*minimax_type)
			m, _, _ = self.unified_minimax(test_board, -minimax_type, alpha, beta)
			if m*minimax_type > extreme_val*minimax_type:
				extreme_val = m
				x, y = i
			test_board.place_marker(i, 0)
			a, b = (alpha, beta) if minimax_type == 1 else (beta, alpha)
			if extreme_val*minimax_type >= b*minimax_type:
				return (extreme_val, x, y)
			if extreme_val*minimax_type > a*minimax_type:
				a = extreme_val
			alpha, beta = (a, b) if minimax_type == 1 else (b, a)
		return (extreme_val, x, y)

	def turn(self) -> None: 
		'''executes one computer turn by running the minimax algorithm'''
		_, x, y = self.unified_minimax(Board(board=deepcopy(self.board.board)), 1, -2, 2)
		print("Computer chose a marker position:")
		self.board.place_marker([x, y], self.marker_type)

class Controller:

	def __init__(self, keybinds = [1,2,3,4,5,6,7,8,9]) -> None:
		self.keybinds = [str(i) for i in keybinds]
		self.board = Board()
		self.winner = None

	def game(self, player1, player2) -> None:
		'''does a whole game of tic tac toe between the two specified players'''
		players = [player1, player2]
		while self.winner == None:
			players[0].turn()
			players = [players[1], players[0]]
			print(self.board)
			self.winner = self.board.check_win()
		print(["Nobody","Circle","Cross"][self.winner]+" won.")

	def player_vs_player(self, starter = -1):
		self.game(Player(board=self.board, marker_type=starter, keybinds=self.keybinds), Player(board=self.board, marker_type=starter*(-1), keybinds=self.keybinds))

	def player_vs_computer(self, starter = -1):
		self.game(Player(board=self.board, marker_type=starter, keybinds=self.keybinds), Computer(board=self.board, marker_type=starter*(-1)))

	def computer_vs_player(self, starter = -1):
		self.game(Computer(board=self.board, marker_type=starter), Player(board=self.board, marker_type=starter*(-1), keybinds=self.keybinds))

	def computer_vs_computer(self, starter = -1):
		self.game(Computer(board=self.board, marker_type=starter), Computer(board=self.board, marker_type=starter*(-1)))

if __name__ == "__main__":
	controller = Controller(keybinds=[7,8,9,4,5,6,1,2,3])
	controller.computer_vs_player()