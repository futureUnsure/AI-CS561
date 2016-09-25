Mancala : Game Playing Agent for an old African Board Game
==========================================================

Summary:
--------
- Simulates the board game with an adversarial opponent
- Computes the best next move for the player against the opponent using AI
- Built the exhaustive game search space
- Used greedy, minimax and alpha beta pruning to determine the next best move from the game search space
- Generated the traverse logs of each path taken by the algorithm

Introduction to Mancala:
------------------------
- Mancala is a two-player game from Africa in which players moves stones around a [board](http://imgur.com/GnqbdJ4)
- The players try to capture as many stones as possible
- Player 1 owns the bottom row, while Player 2 owns the top row
- There are also two special pits on the board, called Mancalas
- In the Mancalas, each player accumulates his or her captured stones (player 1's Mancala is on the right and player 2's Mancala is on the left).
- On a player's turn, he or she chooses one of the pits on his or her side of the board (not the Mancala) and removes all of the stones from that pit
- The player then places one stone in each pit, moving counterclockwise around the board, starting with the pit immediately next to the chosen pit, including his or her Mancala but NOT his or her opponents Mancala, until he or she has run out of stones.
- If the player's last stone ends in his or her own Mancala, the player gets another turn
- If the player's last stone ends in an empty pit on his or her own side, the player captures all of the stones in the pit directly across the board from where the last stone was placed (the opponents stones are removed from the pit and placed in the player's Mancala) as well as the last stone placed (the one placed in the empty pit)
- The game ends when one player cannot move on his or her turn, at which time the other player captures all of the stones remaining on his or her side of the board.

Evaluation Function:
--------------------
- In order to quickly compute the utility of the game sub tree, used the following evaluation function
	Eval(state) = No. of player's stones - No. of opponent's stones

Tie-Breaking:
-------------
- Ties between pits are broken by selecting the node that is first in the position order.
- Order for the traverse logs are in the position order as well.

Input Specifications:
---------------------
- Algorithm to be used: <code> 1 - Greedy, 2 - Minimax, 3 - Alpha Beta </code>
- Game Player : <code> 1 - Bottom Row, 2 - Top Row </code>
- Cut-off depth
- Board state for player 2
- Board state for player 1
- Number of stones in player 2's mancala
- Number of stones in player 1's mancala

Output:
-------
- Display the state of the board after playing the generated best next move
- Generate traverse logs in the following format (for each move)
	
	Node, Depth, Value
	
	Node: The chosen pit
	Depth: Depth of the node
	Value: Value of the node

- Generated output files are:

	next_state.txt
	traverse_log.txt

Usage:
------
	python mancala.py <path_to_input_file> 
	 




