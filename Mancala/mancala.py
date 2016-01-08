import collections
import copy
import sys
import re

infinity = 1.0e400

GameType = 0
MaxPlayer = 0
CutOff = 0
GameBoard = collections.OrderedDict()
Player1Board = []
Player2Board = []
Player1Mancala = 0
Player2Mancala = 0


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


class GameState:
	def __init__(self, **assignments):
		self.__dict__.update(assignments)

def get_other_player(M):
	if M.max_player == 1:
		return 2
	else:
		return 1

def alpha_beta_decision(state, mancala, file_handle):

	def stringify(x):
		if x == infinity:
			return "Infinity"
		elif x == -infinity:
			return "-Infinity"
		else:
			return str(x)

	def argmax(sequence, function1, function2, mancala):

		file_handle.write("Node,Depth,Value,Alpha,Beta\n")

		alpha = -infinity
		beta = infinity

		file_handle.write("root," + str(0) + ",-Infinity," + stringify(alpha) \
									+ "," + stringify(beta) + "\n")

		if len(sequence) == 0:
			file_handle.write(str(state.previous_move) + "," + str(0) + "," \
										+ str(compute_eval(state)) + "," \
										+ stringify(alpha) + "," \
										+ stringify(beta) + "\n")

			return compute_eval(state), state.previous_move


		max_payoff_move = sequence[0]
		
		result = mancala.result(state, max_payoff_move)
		
		if result.mancala_is_last_stop is True:

			file_handle.write(str(result.previous_move) + "," + str(1) + \
								",-Infinity,"+ stringify(alpha) + "," + \
								stringify(beta) + "\n")

			max_payoff = function2(result,0, alpha, beta)

		else:
			if mancala.cutoff != 1:

				file_handle.write(str(result.previous_move) + "," +str(1) + \
									",Infinity," + stringify(alpha) + "," + \
									stringify(beta) + "\n")

			max_payoff = function1(result,1, alpha, beta)

		alpha = max(alpha, max_payoff)

		file_handle.write("root," + str(0) + "," +str(max_payoff) + "," + \
							stringify(alpha) + "," + stringify(beta) + "\n")

		for move in sequence[1:]:
			result = mancala.result(state, move)

			if result.mancala_is_last_stop is True:

				file_handle.write(str(result.previous_move) + "," + str(1) + \
									",-Infinity," + stringify(alpha) + "," + \
									stringify(beta) + "\n")

				payoff = function2(result,0,alpha,beta)
			else:

				if mancala.cutoff != 1:

					file_handle.write(str(result.previous_move) + "," + str(1)\
										+ ",Infinity," + stringify(alpha) + ","\
										+ stringify(beta) + "\n")

				payoff = function1(result,1,alpha,beta)


			if payoff > max_payoff:
				max_payoff_move = move
				max_payoff = payoff

			alpha = max(alpha, payoff)

			file_handle.write("root," + str(0) + "," + str(max_payoff) + ","\
							+ stringify(alpha) + "," + stringify(beta) + "\n")



		return max_payoff, max_payoff_move


	def min_value(state, level, alpha, beta):
		state.player = get_other_player(mancala)

		if(state.game_over is True):
			file_handle.write(str(state.previous_move) + "," + str(level) + ","\
								+ str(compute_eval(state)) + ","\
								+ stringify(alpha) + "," + stringify(beta)\
								+ "\n")

			return compute_eval(state)


			
		if(cutoff_test(level)):

			file_handle.write(str(state.previous_move) + "," + str(level) + ","\
			 				+ str(compute_eval(state)) + "," + stringify(alpha)\
			 				+ "," + stringify(beta) + "\n")

			return compute_eval(state)

		v = infinity

		if not state.mancala_is_last_stop and level != 1:

			file_handle.write(str(state.previous_move) + "," + str(level) + \
								",Infinity," + stringify(alpha) + "," + \
								stringify(beta) + "\n")

		for move in mancala.get_legal_moves(state):

			result = mancala.result(state, move)

			if result.mancala_is_last_stop is True:

				file_handle.write(str(move) + "," + str(level + 1) \
								+ ",Infinity," + stringify(alpha) + ","\
								+ stringify(beta) + "\n")

				w = min_value(result, level, alpha, beta)

			else:
				if level == 0:
					file_handle.write(str(move) + "," + str(level + 1)\
										+",-Infinity," + stringify(alpha) + ","\
										+stringify(beta) + "\n")

				w = max_value(result, level + 1, alpha, beta)

			v = min(w,v)

			if v <= alpha:

				if not state.mancala_is_last_stop:
					file_handle.write(str(state.previous_move) + ","\
										+ str(level)\
										+ "," + str(v) + "," + stringify(alpha)\
										+ "," + stringify(beta) + "\n")

				else:
					file_handle.write(str(state.previous_move) + ","\
										 + str(level + 1)\
										 + "," + str(v) + "," +stringify(alpha)\
										 + "," + stringify(beta) + "\n")

				return v

			else:
				beta = min(beta, v)

				if not state.mancala_is_last_stop:

					file_handle.write(str(state.previous_move) + "," \
										+ str(level) + "," + str(v) + "," \
										+ stringify(alpha) \
										+ "," + stringify(beta) + "\n")

				else:
					file_handle.write(str(state.previous_move) + "," \
										+ str(level + 1) + "," + str(v) + "," \
										+ stringify(alpha) + ","\
										+ stringify(beta) + "\n")


		return v

	def max_value(state, level, alpha, beta):
		state.player = mancala.max_player

		if(state.game_over is True):
			if not state.mancala_is_last_stop:
				file_handle.write(str(state.previous_move) + "," + str(level) +\
										 "," + str(compute_eval(state)) \
										 + "," + stringify(alpha) \
										 + "," + stringify(beta) + "\n")
			else:
				file_handle.write(str(state.previous_move) + "," + str(level + 1)\
										+ "," + str(compute_eval(state)) \
										+ "," + stringify(alpha)\
										+ "," + stringify(beta) +"\n")


			return compute_eval(state)

		if (cutoff_test(level)):

			file_handle.write(str(state.previous_move) + "," + str(level) \
									+ "," + str(compute_eval(state)) \
									+ "," + stringify(alpha) + "," \
									+ stringify(beta) + "\n")

			return compute_eval(state)

		v = -infinity

		if not state.mancala_is_last_stop and level != 1:

			file_handle.write(str(state.previous_move) + "," + str(level) \
								+ ",-Infinity," + stringify(alpha) + "," \
								+ stringify(beta) + "\n")


		for move in mancala.get_legal_moves(state):
			result = mancala.result(state, move)

			if result.mancala_is_last_stop is True:

				file_handle.write(str(move) + "," + str(level + 1) \
											+ ",-Infinity," + stringify(alpha) \
											+ "," + stringify(beta) + "\n")

				w = max_value(result, level, alpha, beta)

			else:
				if level == 0:

					file_handle.write(str(move) + "," + str(level + 1) \
												+ ",Infinity," + stringify(alpha)\
												+ "," + stringify(beta) + "\n")

				w = min_value(result, level+ 1, alpha, beta)

			v = max(v, w)

			
			if v >= beta:
				if not state.mancala_is_last_stop:
					file_handle.write(str(state.previous_move) + "," \
									+ str(level) + "," + str(v) + ","\
									+ stringify(alpha) + "," + stringify(beta)\
									+ "\n")
				else:
					file_handle.write(str(state.previous_move) + ","\
									 + str(level + 1) + "," + str(v) + ","\
									 + stringify(alpha) + "," + stringify(beta)\
									 + "\n")
				return v
			else:
				alpha = max(v, alpha)
				if not state.mancala_is_last_stop:
					file_handle.write(str(state.previous_move) + ","\
									 + str(level) + "," + str(v) + ","\
									 + stringify(alpha)	+ "," + stringify(beta)\
									 + "\n")
				else:
					file_handle.write(str(state.previous_move) + ","\
									 + str(level + 1) + "," + str(v) + "," \
									 + stringify(alpha) + "," + stringify(beta)\
									 + "\n")

		return v

	def cutoff_test(level):
		return (level == mancala.cutoff)

	def compute_eval(state):
		diff =\
		 state.board.values()[len(state.board) / 2] - state.board.values()[0]
		return diff if mancala.max_player == 1 else -diff


	return argmax(mancala.get_legal_moves(state),
	  			lambda x,y,alpha,beta: min_value(x, y, alpha, beta),
	 			lambda x,y,alpha,beta: max_value(x, y, alpha, beta) , mancala )




def minimax_decision(state, mancala, file_handle):

	def argmax(sequence, function1, function2, mancala):
		file_handle.write("Node,Depth,Value\n")

		file_handle.write("root," + str(0) + ",-Infinity\n")

		if len(sequence) == 0:
			file_handle.write(str(state.previous_move) + "," + str(0) + ","\
							 + str(compute_eval(state)) + "\n")
			return compute_eval(state), state.previous_move

		max_payoff_move = sequence[0]
		result = mancala.result(state, max_payoff_move)

		
		if result.mancala_is_last_stop is True:
			file_handle.write(str(result.previous_move) + "," + str(1)\
								+ ",-Infinity\n")
			max_payoff = function2(result,0)
		else:
			
			if mancala.cutoff != 1:
				file_handle.write(str(result.previous_move) + "," + str(1) \
									+ ",Infinity\n")

			max_payoff = function1(result,1)

		file_handle.write("root," + str(0) + "," +str(max_payoff) + "\n")

		for move in sequence[1:]:
			result = mancala.result(state, move)

			if result.mancala_is_last_stop is True:
				file_handle.write(str(result.previous_move) + "," + str(1) \
									+ ",-Infinity\n")
				payoff = function2(result,0)
			else:
				if mancala.cutoff != 1:
					file_handle.write(str(result.previous_move) + "," + str(1)\
									 + ",Infinity\n")
					
				payoff = function1(result,1)


			if payoff > max_payoff:
				max_payoff_move = move
				max_payoff = payoff

			file_handle.write("root," + str(0) + "," + str(max_payoff) + "\n")


		return max_payoff, max_payoff_move

	def min_value(state, level):
		state.player = get_other_player(mancala)

		if(state.game_over is True):
			file_handle.write(str(state.previous_move) + "," + str(level) + ","\
							 + str(compute_eval(state)) + "\n")
			return compute_eval(state)


		if(cutoff_test(level)):
			file_handle.write(str(state.previous_move) + "," + str(level) \
							+ "," + str(compute_eval(state)) + "\n")
			return compute_eval(state)

		v = infinity

		if not state.mancala_is_last_stop and level != 1:
			file_handle.write(str(state.previous_move) + "," + str(level)\
							 + ",Infinity\n")

		for move in mancala.get_legal_moves(state):

			result = mancala.result(state, move)
			if result.mancala_is_last_stop is True:
				file_handle.write(str(move) + "," + str(level + 1)\
								 + ",Infinity\n")
				w = min_value(result, level)

			else:
				if level == 0:
					file_handle.write(str(move) + "," + str(level + 1)\
									 + ",-Infinity\n")
				w = max_value(result, level + 1)

			v = min(w,v)

			if not state.mancala_is_last_stop:
				file_handle.write(str(state.previous_move) + "," + str(level)\
								 + "," + str(v) + "\n")
			else:
				file_handle.write(str(state.previous_move) + ","\
								 + str(level + 1) + "," + str(v) + "\n")

		return v

	def max_value(state, level):
		state.player = mancala.max_player

		if(state.game_over is True):
			if not state.mancala_is_last_stop:
				file_handle.write(str(state.previous_move) + "," + str(level) \
									+ "," + str(compute_eval(state)) + "\n")
			else:
				file_handle.write(str(state.previous_move) + "," \
									+ str(level + 1) + ","\
									+ str(compute_eval(state)) + "\n")


			return compute_eval(state)

	

		if (cutoff_test(level)):
			if not state.mancala_is_last_stop:
				file_handle.write(str(state.previous_move) + "," + str(level) \
									+ "," + str(compute_eval(state)) + "\n")
			else:
				file_handle.write(str(state.previous_move) + ","\
								 + str(level + 1) + ","\
								 + str(compute_eval(state)) + "\n")

			return compute_eval(state)

		v = -infinity

		if not state.mancala_is_last_stop and level != 1:
			file_handle.write(str(state.previous_move) + "," + str(level)\
							 + ",-Infinity\n")



		for move in mancala.get_legal_moves(state):
			result = mancala.result(state, move)

			if result.mancala_is_last_stop is True:
				file_handle.write(str(move) + "," + str(level + 1)\
								 + ",-Infinity\n")
				w = max_value(result, level)

			else:
				if level == 0:
					file_handle.write(str(move) + "," + str(level + 1)\
									 + ",Infinity\n")
				w = min_value(result, level+ 1)

			v = max(v, w)

			if not state.mancala_is_last_stop:
				file_handle.write(str(state.previous_move) + "," + str(level)\
								 + "," + str(v) + "\n")
			else:
				file_handle.write(str(state.previous_move) + ","\
								 + str(level + 1) + "," + str(v) + "\n")


		return v

	def cutoff_test(level):
		return (level == mancala.cutoff)

	def compute_eval(state):
		diff =\
		 state.board.values()[len(state.board) / 2] - state.board.values()[0]
		return diff if mancala.max_player == 1 else -diff


	return argmax(mancala.get_legal_moves(state),
	  				lambda x,y: min_value(x, y),
	 				lambda x,y: max_value(x, y) , mancala )



class Mancala:
	def __init__(self, board, cutoff, player, task):
		self.task = task
		if(self.task == 1):
			self.cutoff = 1

		else:
			self.cutoff = cutoff
		self.moves = [ pit for (pit_idx, pit) in enumerate(board) \
						if (pit_idx != 0 and (pit_idx != (len(board) / 2))\
										 and (board[pit] != 0)) ]


		self.max_player = player
		self.initial_state = GameState(board = board, player = player, \
							previous_move = None, mancala_is_last_stop = False)

	def get_legal_moves(self, state):
		all_legal_moves = [ pit for (pit_idx, pit) in enumerate(state.board) \
				if (pit_idx != 0 and (pit_idx != (len(state.board) / 2))\
				and (state.board[pit] != 0)) ]


		player_2_moves = [move for move in all_legal_moves if 'A' in move]
		player_1_moves = [move for move in all_legal_moves if 'B' in move]

		return sorted(player_2_moves, key = natural_key) if state.player == 2\
						 else sorted(player_1_moves, key = natural_key)

	def result(self, state, move):
		board = copy.deepcopy(state.board)
		mancala_index = len(board) / 2 if state.player == 1 else 0
		other_mancala_index = abs(mancala_index - (len(board) / 2))

		board_iter = board.keys().index(move)
		no_of_stones = board[move]
		board[move] = 0
		
		def is_empty_pit_last_stop(i, board_iter):
			if board_iter != mancala_index:
				return (i == (no_of_stones - 1)\
						and	board[board.keys()[board_iter]] == 0\
						and 'B' in board.keys()[board_iter]) if state.player == 1\
				else (i == (no_of_stones - 1)\
					and board[board.keys()[board_iter]] == 0\
					and 'A' in board.keys()[board_iter])

		def get_opposite_pit_index(state, board, board_iter):
			dist_from_mirror = abs(((len(board) / 2) - board_iter))
			return (len(board) / 2) + dist_from_mirror if state.player == 1\
			else (len(board) / 2) - dist_from_mirror
		
		for i in range(0, no_of_stones):
			board_iter = (board_iter + 1) % len(board)
			if(board_iter != other_mancala_index):
				if (is_empty_pit_last_stop(i, board_iter)):
					opposite_pit_index =\
					get_opposite_pit_index(state, board, board_iter)

					board[board.keys()[mancala_index]] +=\
						board[board.keys()[opposite_pit_index]] + 1

					board[board.keys()[opposite_pit_index]] = 0
					continue 

				board[board.keys()[board_iter]] += 1
			else:
				board_iter += 1 % len(board)
				if (is_empty_pit_last_stop(i, board_iter)):
					opposite_pit_index =\
					 get_opposite_pit_index(state, board, board_iter)

					board[board.keys()[mancala_index]] +=\
						board[board.keys()[opposite_pit_index]] + 1

					board[board.keys()[opposite_pit_index]] = 0
					continue 

				board[board.keys()[board_iter]] += 1

		def is_game_over():
			return ((len([move for (idx, move) in enumerate(board)\
						if (('B' in move) and (board[move] != 0)\
									and (idx != mancala_index)
									and (idx != other_mancala_index)) ]) == 0)\
					or\
					(len([move for (idx, move) in enumerate(board)\
						if (('A' in move) and (board[move] != 0)\
									and (idx != mancala_index)\
									and (idx != other_mancala_index)) ]) == 0))


		def get_other_player_moves():
			if state.player == 1:
				return [move for (idx, move) in enumerate(board)\
							if ('A' in move and\
							  idx != mancala_index and\
							  idx != other_mancala_index)]
			else:
				return [move for (idx, move) in enumerate(board)\
							if ('B' in move and\
							idx != mancala_index and\
							idx != other_mancala_index)]

		def get_current_player_moves():
			if state.player == 1:
				return [move for (idx, move) in enumerate(board)\
						 	if ('B' in move and\
							   idx != mancala_index and\
							   idx != other_mancala_index)]
			else:
				return [move for (idx, move) in enumerate(board)\
							if ('A' in move and\
							   idx != mancala_index and\
							   idx != other_mancala_index)]


		def populate_mancala_game_over(pits, board, generic_mancala_index):
		
			for pit in pits:
				board[board.keys()[generic_mancala_index]] += board[pit]
				board[pit] = 0


		if is_game_over():
			other_player_pits = get_other_player_moves()
			current_player_pits = get_current_player_moves()

			populate_mancala_game_over(other_player_pits, board, other_mancala_index)
			populate_mancala_game_over(current_player_pits, board, mancala_index)
			
			self.game_over = True
		else:
			self.game_over = False

		self.mancala_is_last_stop = (board_iter == mancala_index)

		return GameState(player = state.player, board = board, \
						mancala_is_last_stop = self.mancala_is_last_stop,\
						game_over = self.game_over,previous_move = move)

def test_for_last_pit_empty_player1(player):
	board = collections.OrderedDict()
	board['A1'] = 0
	board['B2'] = 3
	board['B3'] = 1
	board['B4'] = 0
	board['B5'] = 0
	board['A4'] = 3
	board['A3'] = 3
	board['A2'] = 3
	cutoff = 1
	player = player
	task = 'Greedy'
	M = Mancala(board, cutoff, player, task)
	result = M.result(M.initial_state, 'B3')
	assert(result.board ==\
	 collections.OrderedDict([('A1', 0), ('B2', 3), ('B3', 0), ('B4', 0),\
	 							 ('B5', 4), ('A4', 0), ('A3', 3), ('A2', 3)]))

def test_for_last_pit_empty_player2(player):
	board = collections.OrderedDict()
	board['A1'] = 0
	board['B2'] = 3
	board['B3'] = 3
	board['B4'] = 3
	board['B5'] = 0
	board['A4'] = 3
	board['A3'] = 1
	board['A2'] = 0
	cutoff = 1
	player = player
	task = 'Greedy'
	M = Mancala(board, cutoff, player, task)
	result = M.result(M.initial_state, 'A3')
	assert(result.board ==\
	 collections.OrderedDict([('A1', 4), ('B2', 0), ('B3', 3), ('B4', 3),\
	 							 ('B5', 0), ('A4', 3), ('A3', 0), ('A2', 0)]))

def test_for_wrap_around_player1(player):
	board = collections.OrderedDict()
	board['A1'] = 0
	board['B2'] = 3
	board['B3'] = 10
	board['B4'] = 0
	board['B5'] = 0
	board['A4'] = 3
	board['A3'] = 3
	board['A2'] = 3
	cutoff = 1
	player = player
	task = 'Greedy'
	M = Mancala(board, cutoff, player, task)
	result = M.result(M.initial_state, 'B3')
	assert(result.board ==\
	 collections.OrderedDict([('A1', 0), ('B2', 4), ('B3', 1), ('B4', 2),\
	 							 ('B5', 2), ('A4', 5), ('A3', 4), ('A2', 4)]))

def test_for_mancala_is_last_stop_player1(player):
	board = collections.OrderedDict()
	board['A1'] = 0
	board['B2'] = 3
	board['B3'] = 3
	board['B4'] = 3
	board['B5'] = 0
	board['A4'] = 3
	board['A3'] = 3
	board['A2'] = 3
	cutoff = 1
	player = player
	task = 'Greedy'
	M = Mancala(board, cutoff, player, task)
	result = M.result(M.initial_state, 'B2')
	assert(result.mancala_is_last_stop == True)

def test_for_mancala_is_not_the_last_stop_player1(player):
	board = collections.OrderedDict()
	board['A1'] = 0
	board['B2'] = 3
	board['B3'] = 10
	board['B4'] = 0
	board['B5'] = 0
	board['A4'] = 3
	board['A3'] = 3
	board['A2'] = 3
	cutoff = 1
	player = player
	task = 'Greedy'
	M = Mancala(board, cutoff, player, task)
	result = M.result(M.initial_state, 'B3')
	assert(result.mancala_is_last_stop == False)

def test_for_minimax_working_correctly_player1(player):
	task = 'Minimax'
	board = collections.OrderedDict()
	cutoff = 2
	board['A1'] = 0
	board['B2'] = 3
	board['B3'] = 3
	board['B4'] = 3
	board['B5'] = 0
	board['A4'] = 3
	board['A3'] = 3
	board['A2'] = 3
	M = Mancala(board, cutoff, player, task)
	assert(M.moves == ['B2', 'B3', 'B4', 'A4', 'A3', 'A2'])
	max_payoff, max_payoff_move = minimax_decision(M.initial_state, M)
	assert((max_payoff, max_payoff_move) == (1, 'A4'))

def test2_for_minimax_working_correctly_player1(player):
	task = 'Minimax'
	board = collections.OrderedDict()
	cutoff = 2
	board['A1'] = 0
	board['B2'] = 2
	board['B3'] = 2
	board['B4'] = 2
	board['B5'] = 0
	board['A4'] = 2
	board['A3'] = 2
	board['A2'] = 2
	M = Mancala(board, cutoff, player, task)
	assert(M.moves == ['B2', 'B3', 'B4', 'A4', 'A3', 'A2'])
	max_payoff, max_payoff_move = minimax_decision(M.initial_state, M)
	print max_payoff, max_payoff_move


def test3_for_minimax_working_correctly_player1(player):
	task = 'Minimax'
	board = collections.OrderedDict()
	cutoff = 2
	board['A1'] = 0
	board['B2'] = 2
	board['B3'] = 1
	board['B4'] = 2
	board['B5'] = 0
	board['A4'] = 2
	board['A3'] = 1
	board['A2'] = 2
	M = Mancala(board, cutoff, player, task)
	assert(M.moves == ['B2', 'B3', 'B4', 'A4', 'A3', 'A2'])
	max_payoff, max_payoff_move = minimax_decision(M.initial_state, M)
	M.cutoff = 1
	result = M.result(M.initial_state, max_payoff_move)
	max_payoff, max_payoff_move = minimax_decision(result, M)
	print max_payoff, max_payoff_move


def test_for_simple_move_player1(player):
	task = 'Minimax'
	board = collections.OrderedDict()
	cutoff = 2
	board['A1'] = 0
	board['B2'] = 3
	board['B3'] = 3
	board['B4'] = 3
	board['B5'] = 0
	board['A4'] = 3
	board['A3'] = 3
	board['A2'] = 3
	M = Mancala(board, cutoff, player, task)
	result = M.result(M.initial_state, 'B2')
	assert(result.board ==\
	 collections.OrderedDict([('A1', 0), ('B2', 0), ('B3', 4), ('B4', 4),\
	 							('B5', 1), ('A4', 3), ('A3', 3), ('A2', 3)]))

def test_for_minimax_file_io(M, traverse_log_file_handle):
	max_payoff, max_value =\
	minimax_decision(M.initial_state, M, traverse_log_file_handle)
	print max_payoff, max_value

def test_for_alphabeta(M, traverse_log_file_handle):
	max_payoff, max_value =\
	alpha_beta_decision(M.initial_state, M, traverse_log_file_handle)
	print max_payoff, max_value

def write_state(board, file_handle):
	player2_board_iter = len(board) - 1
	Player1MancalaIdx = len(board) / 2
	Player2MancalaIdx = 0
	player1_board_iter = Player2MancalaIdx + 1

	Player2Board = []
	Player1Board = []

	while player2_board_iter > Player1MancalaIdx:
		Player2Board.append(board.values()[player2_board_iter])
		player2_board_iter -= 1

	file_handle.write(' '.join(map(str, Player2Board)))
	file_handle.write("\n")

	while player1_board_iter < Player1MancalaIdx:
		Player1Board.append(board.values()[player1_board_iter])
		player1_board_iter += 1

	file_handle.write(' '.join(map(str, Player1Board)))
	file_handle.write("\n")

	file_handle.write(str(board.values()[Player2MancalaIdx]) + "\n")
	file_handle.write(str(board.values()[Player1MancalaIdx]) + "\n")



def read_game(file_handle):
	global GameType, MaxPlayer, CutOff, Player1Board, Player2Board
	global Player1Mancala, Player2Mancala, GameBoard

	GameType = int(file_handle.readline().rstrip('\n'))
	MaxPlayer = int(file_handle.readline().rstrip('\n'))
	CutOff = int(file_handle.readline().rstrip('\n'))
	Player2Board = file_handle.readline().rstrip('\n').split(' ')
	Player2Board = [ int(no_of_stones) for no_of_stones in Player2Board ]
	Player1Board = file_handle.readline().rstrip('\n').split(' ')
	Player1Board = [ int(no_of_stones) for no_of_stones in Player1Board ]
	Player2Mancala = int(file_handle.readline().rstrip('\n'))
	Player1Mancala = int(file_handle.readline().rstrip('\n'))

	len_of_game_board = (len(Player2Board) * 2) + 2
	GameBoard['A1'] = Player2Mancala

	for (pit_index, board_iter) in enumerate(range(2, len(Player1Board) + 2)):
		pit = 'B'+str(board_iter)
		GameBoard[pit] = Player1Board[pit_index]

	player_1_mancala_pit = 'B' + str(board_iter + 1)

	GameBoard[player_1_mancala_pit] = Player1Mancala

	for (pit_index, board_iter) in enumerate(range(len(Player2Board) + 1, 1, -1)):
		pit = 'A'+str(board_iter)
		GameBoard[pit] = Player2Board[(len(Player2Board) - 1) - pit_index]


def get_next_state(state, mancala, move, value):
	state = copy.deepcopy(state)
	junk_file_handle = open("junk_file", "w")
	while True:
		state = mancala.result(state, move)
		print state.board
		if (not state.mancala_is_last_stop) or state.game_over :
			break
		# value, move = minimax_decision(state, mancala, junk_file_handle)
		value, move = alpha_beta_decision(state, mancala, junk_file_handle)

	junk_file_handle.close()
	return state.board

def main():
	max_payoff_move = None
	max_value = 0

	InputFileName = str(sys.argv[2])
	input_file_handle = open(InputFileName,'r')
	traverse_log_file_handle = open("traverse_log.txt", "w")
	next_state_file_handle = open("next_state.txt","w")
	read_game(input_file_handle)
	M = Mancala(GameBoard, CutOff, MaxPlayer, GameType)

	if M.task == 1 or M.task == 2:
		max_value, max_payoff_move =\
		 minimax_decision(M.initial_state, M, traverse_log_file_handle)
	elif M.task == 3:
		max_value, max_payoff_move =\
		 alpha_beta_decision(M.initial_state, M, traverse_log_file_handle)

	print max_value, max_payoff_move


	next_state_board =\
	 get_next_state(M.initial_state, M, max_payoff_move, max_value)

	write_state(next_state_board, next_state_file_handle)

	input_file_handle.close()
	traverse_log_file_handle.close()
	next_state_file_handle.close()


if __name__ == '__main__':
	main()
