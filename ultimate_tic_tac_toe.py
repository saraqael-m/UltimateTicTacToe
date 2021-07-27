import cv2, sys, numpy as np, tkinter as tk; from copy import deepcopy, copy; from random import shuffle; from tqdm import tqdm

class Board:

	def __init__(self, name = "Ultimate Tic Tac Toe", big_board = np.zeros([3,3], dtype=int), small_boards = np.zeros([3,3,3,3], dtype=int), selected_board = [None, None], show_image = True) -> None:
		self.show_image = show_image
		self.big_board = big_board # every conquered small board
		self.small_boards = small_boards # every position of every player
		self.selected_board = selected_board
		self.winner = 0
		if show_image:
			self.window = Window(name = name, board = self)
			self.window.draw_board()
			self.window.highlight_selected_board()

	def place_small_marker(self, marker_pos : list, marker_type : int, check = True) -> None:
		'''Places small circle or cross at position on board into array'''
		if self.is_marker_pos_valid(marker_pos) == False and check:
			return
		if abs(marker_type) == 1:
			self.small_boards[marker_pos[0], marker_pos[1], marker_pos[2], marker_pos[3]] = marker_type
			self.winner = self.draw_wins()
			self.selected_board = [marker_pos[2], marker_pos[3]] if self.big_board[marker_pos[2], marker_pos[3]] == 0 else [None, None]
		elif marker_type == 0:
			self.small_boards[marker_pos[0], marker_pos[1], marker_pos[2], marker_pos[3]] = 0
			self.big_board[marker_pos[0], marker_pos[1]] = 0
		else:
			raise ValueError("Marker Type "+str(marker_type)+" non-existent.")
		if self.show_image:
			self.window.draw_small_marker(marker_pos, marker_type)
			self.window.highlight_selected_board()
			if self.winner != 0:
				self.window.remove_highlighting()

	def place_big_marker(self, marker_pos : list, marker_type : int) -> None:
		'''Places big circle or cross (indicates win of small board) at position on board into array'''
		if marker_type in [10,1,0,-1]:
			self.big_board[marker_pos[0], marker_pos[1]] = marker_type
		else:
			raise ValueError("Marker Type "+str(marker_type)+" non-existent.")
		if self.show_image:
			self.window.draw_big_marker(marker_pos, marker_type)

	def draw_wins(self) -> int:
		'''Checks if any board was won and denotes/draws it'''
		checkable_indeces = [list(index) for index, val in np.ndenumerate(self.big_board) if val == 0] # all board indeces who aren't conquered
		for i in checkable_indeces:
			is_newly_won = self.board_win_check(self.small_boards[i[0], i[1]])
			if is_newly_won != 0:
				if self.selected_board == i:
					self.selected_board = [None, None]
				self.place_big_marker(i, is_newly_won)
		return self.board_win_check(self.big_board)

	def board_win_check(self, board : list) -> int:
		'''Checks if someone won on a given board'''
		sum_list = list(np.sum(board, axis=1)) + list(np.sum(board, axis=0)) + [np.trace(board), np.trace(np.rot90(board))]
		if 3 in sum_list: # circle wins
			return 1
		if -3 in sum_list: # cross wins
			return -1
		if 0 in list(board.flatten()): # ties
			return 0
		return 10

	def place_marker_by_mouse(self, mouse_x : int, mouse_y : int, marker_type : int) -> bool:
		'''Convert mouse position to position in grid and place marker'''
		big_pos = [(mouse_x-50)//100,(mouse_y-50)//100]
		marker_pos = [big_pos[0],big_pos[1],(mouse_x-big_pos[0]*100-62)//25,(mouse_y-big_pos[1]*100-62)//25]
		if True in [(abs(m-1) >= 2) for m in marker_pos]: # is grid pos oob (3s or -1s)
			return False
		is_valid = self.is_marker_pos_valid(marker_pos)
		if is_valid:
			self.place_small_marker(marker_pos, marker_type)
		return is_valid

	def is_marker_pos_valid(self, marker_pos : list) -> bool:
		'''Checks if marker position is valid'''
		if abs(self.big_board[marker_pos[0], marker_pos[1]]) == 1: # is board already won
			return False
		if abs(self.small_boards[marker_pos[0], marker_pos[1], marker_pos[2], marker_pos[3]]) == 1: # is grid pos already filled
			return False
		if self.selected_board != [None, None]:
			if self.selected_board != [marker_pos[0], marker_pos[1]]:
				return False
		return True

	def evaluate_board_state(self) -> float:
		'''evaluates the current board position with a score between -1 and 1 depending on who won more small boards, mainly used by computer'''
		sum_board = deepcopy(self.big_board)
		sum_board[sum_board == 10] = 0
		return np.sum(sum_board) / 9

class Window:

	def __init__(self, name : str, board) -> None:
		self.board = board
		self.img = np.zeros([399,399,3]) # image
		self.name = name
		self.colors = [(255,0,0),(0,0,255),(0,255,0)] # cross: blue; circle: red, preview: green (BGR format)
		self.draw_board()

	def draw_board(self) -> None:
		'''Draws the grids onto the image'''
		self.img = np.zeros([399,399,3]) # image
		for i in [[(0,100),(300,100)],[(0,200),(300,200)],[(100,0),(100,300)],[(200,0),(200,300)]]:
			cv2.line(self.img,(i[0][0]+50,i[0][1]+50),(i[1][0]+50,i[1][1]+50),(255,255,255),2) # big grid
			for (x, y), _ in np.ndenumerate(np.zeros((3,3))):
				cv2.line(self.img,(i[0][0]//4+62+100*x,i[0][1]//4+62+100*y),(i[1][0]//4+62+100*x,i[1][1]//4+62+100*y),(255,255,255),2)
		self.show_img()

	def highlight_selected_board(self) -> None:
		'''Highlight all possible selectable boards with rectangles'''
		self.remove_highlighting()
		for i in [index for index, val in np.ndenumerate(self.board.big_board) if val == 0] if self.board.selected_board == [None, None] else [self.board.selected_board]:
			cv2.rectangle(self.img,(55+100*i[0],55+100*i[1]),(145+100*i[0],145+100*i[1]),(0,255,255),2)
		self.show_img()

	def remove_highlighting(self) -> None:
		'''Remove highlighting of selected board'''
		for i, _ in np.ndenumerate(self.board.big_board): # remove all highlighting
			cv2.rectangle(self.img,(55+100*i[0],55+100*i[1]),(145+100*i[0],145+100*i[1]),(0,0,0),2)
		self.show_img()

	def draw_small_marker(self, marker_pos : list, marker_type : int) -> None:
		'''Draws small circle or cross at position on image'''
		corners = [67+100*marker_pos[0]+25*marker_pos[2],67+100*marker_pos[1]+25*marker_pos[3],82+100*marker_pos[0]+25*marker_pos[2],82+100*marker_pos[1]+25*marker_pos[3]]
		if marker_type == -1: # cross
			cv2.line(self.img,(corners[0],corners[1]),(corners[2],corners[3]),self.colors[0],2)
			cv2.line(self.img,(corners[2],corners[1]),(corners[0],corners[3]),self.colors[0],2)
		elif marker_type == 1: # circle
			cv2.circle(self.img,(corners[0]+8,corners[1]+8),8,self.colors[1],2)
		elif marker_type == 0: # remove marker
			cv2.rectangle(self.img,(corners[0]-2,corners[1]-2),(corners[2]+2,corners[3]+2),(0,0,0),-1)
		self.show_img()

	def draw_big_marker(self, marker_pos : list, marker_type : int) -> None:
		'''Draws big circle or cross (indicates win of small board) at position on image'''
		if marker_type == 10 or marker_type == 0: # tie or nothing has no marker
			return
		if marker_type == -1: # cross marker
			cv2.line(self.img,(60+100*marker_pos[0],60+100*marker_pos[1]),(140+100*marker_pos[0],140+100*marker_pos[1]),self.colors[0],5)
			cv2.line(self.img,(60+100*marker_pos[0],140+100*marker_pos[1]),(140+100*marker_pos[0],60+100*marker_pos[1]),self.colors[0],5)
		elif marker_type == 1: # circle marker
			cv2.circle(self.img,(100*(marker_pos[0]+1),100*(marker_pos[1]+1)),40,self.colors[1],3)
		self.show_img()

	def refresh_all_markers(self) -> None:
		'''Empties the image and draws everything again'''
		self.draw_board()
		for index, val in np.ndenumerate(self.board.small_boards):
			self.draw_small_marker(index, val)
		for index, val in np.ndenumerate(self.board.big_board):
			self.draw_big_marker(index, val)
		self.show_img()

	def show_img(self):
		cv2.imshow(self.name, self.img)
		cv2.waitKey(1)

class Mouse:

	def __init__(self, name : str) -> None:
		self.left_clicked = False
		self.x, self.y = 0, 0
		cv2.setMouseCallback(name, self.clicked)

	def clicked(self, event, x, y, flags, param) -> None:
		'''Executed when mouse event is triggered, player chooses grid cell with mouse'''
		if event == cv2.EVENT_LBUTTONDOWN:
			self.x, self.y = x, y
			self.left_clicked = True

class Player:

	def __init__(self, board, mouse, marker_type : int) -> None:
		self.board = board
		self.mouse = mouse
		self.marker_type = marker_type

	def turn(self) -> bool:
		if self.mouse.left_clicked == True:
			if self.board.place_marker_by_mouse(self.mouse.x, self.mouse.y, self.marker_type):
				return True
		return False

class Computer:

	def __init__(self, board, marker_type : int, max_recursion_depth = 0) -> None:
		self.marker_type = marker_type
		self.board = board
		self.max_recursion_depth = max_recursion_depth
		self.reset_max_depth = 0
		self.min_recursion_depth = 10
		if self.max_recursion_depth < 0:
			self.max_recursion_depth *= -1
			self.reset_depth = self.max_recursion_depth
			self.reset_max_depth = 10
		elif self.max_recursion_depth == 0:
			self.max_recursion_depth = 4
			self.reset_depth = 20
			self.reset_max_depth = 3
			self.min_recursion_depth = 4

	def minimax_general(self, test_board, alpha : int, beta : int, minimax_type : int) -> tuple:
		'''Both min and max of "minimax" depending on minimax_type input (-1 : min or 1 : max)'''
		self.recursion_depth += 1 # variable takes track of recursion depth
		self.moves_checked += 1 # variable takes track of checked possible board positions
		if self.moves_checked % 5000 == 0 and self.max_recursion_depth > self.min_recursion_depth and self.reset_max_depth != 0:
			self.max_recursion_depth -= 1
		if self.recursion_depth >= self.max_recursion_depth: # vaguely evaluate board state if recursion to high
			self.recursion_depth -= 1
			return (test_board.evaluate_board_state()*self.marker_type, [0, 0, 0, 0])
		extreme_val = -2*minimax_type # worst case value
		pos = [None, None, None, None] # position
		winner = test_board.board_win_check(test_board.big_board) # winenr of game
		if winner != 0: # if game has ended
			self.recursion_depth -= 1
			if winner == 10: # tie
				return (0, [0, 0, 0, 0])
			return (winner*self.marker_type, [0, 0, 0, 0]) # win
		selected_board = copy(test_board.selected_board) # set selected board
		possible_moves = []
		if selected_board[0] != None: # one board possible #possible_moves = [[selected_board[0], selected_board[1], index[0], index[1]] for index, val in np.ndenumerate(test_board.small_boards[selected_board[0], selected_board[1]]) if val == 0]
			for x in range(3):
				for y in range(3):
					if test_board.small_boards[selected_board[0], selected_board[1], x, y] == 0:
						possible_moves.append([selected_board[0], selected_board[1], x, y])
		else: # all boards possible, fastest way is a lot of for loops apparently and not list comprehension smh #possible_moves = [i for sub in [[[i2[0], i2[1], i1[0], i1[1]] for i1, v1 in np.ndenumerate(test_board.small_boards[i2[0], i2[1]]) if v1 == 0] for i2, v2 in np.ndenumerate(test_board.big_board) if v2 == 0] for i in sub]
			for x1 in range(3):
				for y1 in range(3):
					if test_board.big_board[x1,y1] == 0:
						for x2 in range(3):
							for y2 in range(3):
								if test_board.small_boards[x1, y1, x2, y2] == 0:
									possible_moves.append([x1, y1, x2, y2])
		shuffle(possible_moves)
		for i in (tqdm(possible_moves) if self.recursion_depth == 1 else possible_moves): # all empty cells
			test_board.selected_board = selected_board
			test_board.place_small_marker(i, self.marker_type*minimax_type, check=False) # try possible move
			m, _ = self.minimax_general(test_board, alpha, beta, minimax_type*(-1)) # min / max for all possible moves of other player
			if m*minimax_type > extreme_val*minimax_type: # if new value is better
				extreme_val = m
				pos = i
			test_board.place_small_marker(i, 0, check=False) # place the 0 back
			if minimax_type == 1: # alpha-beta pruning
				if extreme_val >= beta:
					self.recursion_depth -= 1
					return (extreme_val, pos)
				if extreme_val > alpha:
					alpha = extreme_val
			else:
				if extreme_val <= alpha:
					self.recursion_depth -= 1
					return (extreme_val, pos)
				if extreme_val < beta:
					beta = extreme_val
		self.recursion_depth -= 1
		return (extreme_val, pos)

	def turn(self) -> None:
		'''Computer chooses a grid cell by minimax algorithm'''
		if self.board.winner != 0:
			return
		self.recursion_depth = 0
		self.moves_checked = 0
		_, marker_pos = self.minimax_general(Board(big_board=deepcopy(self.board.big_board), small_boards=deepcopy(self.board.small_boards), selected_board=deepcopy(self.board.selected_board), show_image=False), -2, 2, 1)
		self.board.place_small_marker(marker_pos, self.marker_type)
		if self.reset_max_depth != 0:
			self.max_recursion_depth = min(self.reset_depth, self.max_recursion_depth + self.reset_max_depth)

class GameSelection:

	def __init__(self, controller) -> None:
		self.window = tk.Tk()
		self.controller = controller
		self.com1_val, self.com2_val = 2, 2
		self.add_widgets()
		self.window.mainloop()

	def add_widgets(self) -> None:
		title = tk.Label(self.window, text="Ultimate Tic Tac Toe")
		pvp_btn = tk.Button(self.window, text="Player vs Player", command=self.pvp)
		pvc_btn = tk.Button(self.window, text="Player vs Computer", command=self.pvc)
		#cvp_btn = tk.Button(self.window, text="Computer vs Player")
		cvc_btn = tk.Button(self.window, text="Computer vs Computer", command=self.cvc)
		exit_btn = tk.Button(self.window, text="Exit", command=sys.exit)
		for i in [title, pvp_btn, pvc_btn, cvc_btn, exit_btn]:
			i.pack()

	def val1(self, val):
		self.com1_val = int(val)

	def val2(self, val):
		self.com2_val = int(val)

	def pvp(self) -> None:
		self.window.destroy()
		self.controller.player_vs_player()

	def pvc(self) -> None:
		self.window.destroy()
		window = tk.Tk()
		com1_lbl = tk.Label(window, text="Computer Difficulty")
		com1_scl = tk.Scale(window, from_=1, to=8, orient=tk.HORIZONTAL, command=self.val1)
		start_btn = tk.Button(window, text="Start", command=window.destroy)
		exit_btn = tk.Button(window, text="Exit", command=sys.exit)
		for i in [com1_lbl, com1_scl, start_btn, exit_btn]:
			i.pack()
		window.mainloop()
		self.controller.player_vs_computer(self.com1_val+1)

	def cvc(self) -> None:
		self.window.destroy()
		window = tk.Tk()
		com1_lbl = tk.Label(window, text="Computer 1 Difficulty")
		com1_scl = tk.Scale(window, from_=1, to=8, orient=tk.HORIZONTAL, command=self.val1)
		com2_lbl = tk.Label(window, text="Computer 2 Difficulty")
		com2_scl = tk.Scale(window, from_=1, to=8, orient=tk.HORIZONTAL, command=self.val2)
		start_btn = tk.Button(window, text="Start", command=window.destroy)
		exit_btn = tk.Button(window, text="Exit", command=sys.exit)
		for i in [com1_lbl, com1_scl, com2_lbl, com2_scl, start_btn, exit_btn]:
			i.pack()
		window.mainloop()
		self.controller.computer_vs_computer(self.com1_val+1, self.com2_val+1)

class Controller:

	def __init__(self) -> None:
		self.game_selection = GameSelection(self)

	def start(self) -> None:
		'''Initializes values needed to start the game'''
		self.board = Board(name = self.name)
		self.mouse = Mouse(self.name)

	def player_vs_player(self, starter = -1) -> None:
		'''Two player game'''
		self.name = "Ultimate Tic Tac Toe: Player vs Player"
		self.start()
		players = [Player(board = self.board, mouse = self.mouse, marker_type = starter), Player(board = self.board, mouse = self.mouse, marker_type = starter*(-1))]
		while self.board.winner == 0:
			self.player_turn(players[0])
			players = [players[1], players[0]]
		self.won()

	def player_vs_computer(self, com_level = 2, starter = -1) -> None:
		'''Game of computer versus player'''
		self.name = "Ultimate Tic Tac Toe: Player vs Computer"
		self.start()
		player = Player(board = self.board, mouse = self.mouse, marker_type = starter)
		computer = Computer(board = self.board, marker_type = starter*(-1), max_recursion_depth = com_level)
		while self.board.winner == 0:
			self.player_turn(player)
			if self.board.winner != 0:
				break
			computer.turn()
		self.won()

	def computer_vs_computer(self, com1_level = 8, com2_level = 8, starter = -1):
		'''Watch two AIs battle'''
		self.name = "Ultimate Tic Tac Toe: Computer vs Computer"
		self.start()
		com1 = Computer(board = self.board, marker_type = starter, max_recursion_depth = com1_level)
		com2 = Computer(board = self.board, marker_type = starter*(-1), max_recursion_depth = com2_level)
		while self.board.winner == 0:
			com1.turn()
			if self.board.winner != 0:
				break
			com2.turn()
		self.won()

	def player_turn(self, player) -> None:
		'''One player turn'''
		if self.board.winner != 0:
			return 
		next_turn = False
		while next_turn == False:
			next_turn = player.turn()
			cv2.waitKey(1)
			if cv2.getWindowProperty(self.name, cv2.WND_PROP_VISIBLE) < 1:
				sys.exit()

	def won(self) -> None:
		'''Somebody won the game'''
		self.board.window.remove_highlighting()
		winner = self.board.winner
		if winner == -1:
			print("Cross won!")
		elif winner == 1:
			print("Circle won!")
		elif winner == 10:
			print("Tie!")
		cv2.waitKey(4000)

if __name__ == "__main__":
	controller = Controller()
