import os
import inference
import unittest

class TestIntermediateOutputs(unittest.Testcase):
	def setUp(self):
		pass

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
		self.assertEqual(result.board,
		 collections.OrderedDict([('A1', 0), ('B2', 3), ('B3', 0), ('B4', 0),
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
		self.assertEqual(result.board,
		 collections.OrderedDict([('A1', 4), ('B2', 0), ('B3', 3), ('B4', 3),
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
		self.assertEqual(result.board,
		 collections.OrderedDict([('A1', 0), ('B2', 4), ('B3', 1), ('B4', 2),
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
		self.assertEqual(result.mancala_is_last_stop, True)
	
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
		self.assertEqual(result.mancala_is_last_stop, False)
	
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
		self.assertEqual(M.moves, ['B2', 'B3', 'B4', 'A4', 'A3', 'A2'])
		max_payoff, max_payoff_move = minimax_decision(M.initial_state, M)
		self.assertEqual((max_payoff, max_payoff_move), (1, 'A4'))
	
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
		self.assertEqual(M.moves, ['B2', 'B3', 'B4', 'A4', 'A3', 'A2'])
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
		self.assertEqual(M.moves, ['B2', 'B3', 'B4', 'A4', 'A3', 'A2'])
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
		self.assertEqual(result.board,
		 collections.OrderedDict([('A1', 0), ('B2', 0), ('B3', 4), ('B4', 4),
		 							('B5', 1), ('A4', 3), ('A3', 3), ('A2', 3)]))


def main():
	unittest.main()

if __name__ == '__main__':
	main()
