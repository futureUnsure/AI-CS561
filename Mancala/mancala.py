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

def stringify(x):
    if x == infinity:
        return "Infinity"
    elif x == -infinity:
        return "-Infinity"
    else:
        return str(x)

def log_alpha_beta(file_handle, node, level, val, alpha, beta):
    log = str(node) + "," + str(level) + "," + str(val) + "," +
    stringify(alpha) + "," + stringify(beta) + "\n"
    file_handle.write(log)

def log_minimax(file_handle, node, level, val):
    log = str(node) + "," + str(level) + "," + str(val) + "\n"
    file_handle.write(log)

class GameState:
    def __init__(self, **assignments):
        self.__dict__.update(assignments)

def get_other_player(M):
    if M.max_player == 1:
        return 2
    else:
        return 1

def alpha_beta_decision(state, mancala, file_handle):
    def argmax(sequence, function1, function2, mancala):
        file_handle.write("Node,Depth,Value,Alpha,Beta\n")
        alpha = -infinity
        beta = infinity
        log_alpha_beta(file_handle, root, level, val, alpha, beta)

        if len(sequence) == 0:
            log_alpha_beta(file_handle, state.previous_move, 0,
            compute_eval(state), alpha, beta)
            return compute_eval(state), state.previous_move

        max_payoff_move = sequence[0]
        result = mancala.result(state, max_payoff_move)
        if result.mancala_is_last_stop is True:
            log_alpha_beta(file_handle, result.previous_move, 1,
                            "-Infinity", alpha, beta)
            max_payoff = function2(result,0, alpha, beta)
        elif mancala.cutoff != 1:
            log_alpha_beta(file_handle, result.previous_move, 1,
            "Infinity", alpha, beta)
            max_payoff = function1(result,1, alpha, beta)

        alpha = max(alpha, max_payoff)
        log_alpha_beta(file_handle, "root", 0, max_payoff, alpha, beta)
        for move in sequence[1:]:
            result = mancala.result(state, move)
            if result.mancala_is_last_stop is True:
                log_alpha_beta(file_handle, result.previous_move, 1,
                "-Infinity", alpha, beta)
                payoff = function2(result,0,alpha,beta)
            elif mancala.cutoff != 1:
                log_alpha_beta(file_handle, result.previous_move, 1,
                "Infinity", alpha, beta)
                payoff = function1(result,1,alpha,beta)
            if payoff > max_payoff:
                max_payoff_move = move
                max_payoff = payoff
            alpha = max(alpha, payoff)
            log_alpha_beta(file_handle, 0, max_payoff, alpha, beta)

        return max_payoff, max_payoff_move

    def min_value(state, level, alpha, beta):
        state.player = get_other_player(mancala)
        if(state.game_over is True):
            log_alpha_beta(file_handle, state.previous_move, level,
            compute_eval(state), alpha, beta)
            return compute_eval(state)
        if(cutoff_test(level)):
            log_alpha_beta(file_handle, state.previous_move, level,
            compute_eval(state), alpha, beta)
            return compute_eval(state)

        v = infinity
        if not state.mancala_is_last_stop and level != 1:
            log_alpha_beta(file_handle, state.previous_move, level,
            "Infinity", alpha, beta)
        for move in mancala.get_legal_moves(state):
            result = mancala.result(state, move)
            if result.mancala_is_last_stop is True:
                log_alpha_beta(file_handle, move, level + 1, "Infinity",
                alpha, beta)
                w = min_value(result, level, alpha, beta)
            elif level == 0:
                log_alpha_beta(file_handle, move, level + 1, "-Infinity",
                alpha, beta)
                w = max_value(result, level + 1, alpha, beta)

            v = min(w,v)
            if v <= alpha:
                if not state.mancala_is_last_stop:
                    log_alpha_beta(file_handle, state.previous_move,
                    level, v, alpha, beta)
                else:
                    log_alpha_beta(file_handle, state.previous_move,
                    level + 1, v, alpha, beta)
                return v
            else:
                beta = min(beta, v)
                if not state.mancala_is_last_stop:
                    log_alpha_beta(file_handle, state.previous_move,
                    level, v, alpha, beta)
                else:
                    log_alpha_beta(file_handle, state.previous_move,
                    level + 1, v, alpha, beta)
        return v

    def max_value(state, level, alpha, beta):
        state.player = mancala.max_player
        if(state.game_over is True):
            if not state.mancala_is_last_stop:
                log_alpha_beta(file_handle, state.previous_move,
                level, compute_eval(state), alpha, beta)
            else:
                log_alpha_beta(file_handle, state.previous_move,
                level + 1, compute_eval(state), alpha, beta)
            return compute_eval(state)
        if (cutoff_test(level)):
            log_alpha_beta(file_handle, state.previous_move, level,
            compute_eval(state), alpha, beta)
            return compute_eval(state)

        v = -infinity
        if not state.mancala_is_last_stop and level != 1:
                    log_alpha_beta(file_handle, state.previous_move, level,
                    "-Infinity", alpha, beta)

        for move in mancala.get_legal_moves(state):
            result = mancala.result(state, move)
            if result.mancala_is_last_stop is True:
                log_alpha_beta(file_handle, move, level + 1,
                "-Infinity", alpha, beta)
                w = max_value(result, level, alpha, beta)
            elif level == 0:
                log_alpha_beta(file_handle, move, level + 1,
                "Infinity", alpha, beta)
                w = min_value(result, level+ 1, alpha, beta)

            v = max(v, w)
            if v >= beta:
                if not state.mancala_is_last_stop:
                    log_alpha_beta(file_handle, state.previous_move,
                    level, v, alpha, beta)
                else:
                    log_alpha_beta(file_handle, state.previous_move,
                    level + 1, v, alpha, beta)
                return v
            else:
                alpha = max(v, alpha)
                if not state.mancala_is_last_stop:
                    log_alpha_beta(file_handle, state.previous_move,
                    level, v, alpha, beta)
                else:
                    log_alpha_beta(file_handle, state.previous_move,
                    level + 1, v, alpha, beta)
        return v

    def cutoff_test(level):
        return (level == mancala.cutoff)

    def compute_eval(state):
        diff = state.board.values()[len(state.board) / 2] - state.board.values()[0]
        return diff if mancala.max_player == 1 else -diff

    return argmax(mancala.get_legal_moves(state),
            lambda x,y,alpha,beta: min_value(x, y, alpha, beta),
                lambda x,y,alpha,beta: max_value(x, y, alpha, beta) , mancala )

def minimax_decision(state, mancala, file_handle):
    def argmax(sequence, function1, function2, mancala):
        file_handle.write("Node,Depth,Value\n")
        file_handle.write("root," + str(0) + ",-Infinity\n")
        if len(sequence) == 0:
        log_minimax(file_handle, state.previous_move, 0,
            compute_eval(state))
            return compute_eval(state), state.previous_move

        max_payoff_move = sequence[0]
        result = mancala.result(state, max_payoff_move)
        if result.mancala_is_last_stop is True:
            log_minimax(file_handle, state.previous_move, 1,
                "-Infinity")
            max_payoff = function2(result,0)
        elif mancala.cutoff != 1:
            log_minimax(file_handle, state.previous_move, 1,
                "Infinity")

        log_minimax(file_handle, "root", 0, max_payoff)
        for move in sequence[1:]:
            result = mancala.result(state, move)
            if result.mancala_is_last_stop is True:
                log_minimax(file_handle, result.previous_move, 1,
                    "-Infinity")
                payoff = function2(result,0)
            elif mancala.cutoff != 1:
                log_minimax(file_handle, result.previous_move, 1,
                    "Infinity")
                payoff = function1(result,1)
            if payoff > max_payoff:
                max_payoff_move = move
                max_payoff = payoff
                log_minimax(file_handle, root, 0, max_payoff)
        return max_payoff, max_payoff_move

    def min_value(state, level):
        state.player = get_other_player(mancala)
        if(state.game_over is True):
            log_minimax(file_handle, state.previous_move, level,
                compute_eval(state))
            return compute_eval(state)
        if(cutoff_test(level)):
            log_minimax(file_handle, state.previous_move, level,
                compute_eval(state))
            return compute_eval(state)

        v = infinity
        if not state.mancala_is_last_stop and level != 1:
            log_minimax(file_handle, state.previous_move, level,
                "Infinity")
        for move in mancala.get_legal_moves(state):
            result = mancala.result(state, move)
            if result.mancala_is_last_stop is True:
                log_minimax(file_handle, move, level + 1,
                    "Infinity")
                w = min_value(result, level)
            elif level == 0:
                log_minimax(file_handle, move, level + 1,
                    "-Infinity")
                w = max_value(result, level + 1)

            v = min(w,v)
            if not state.mancala_is_last_stop:
                log_minimax(file_handle, state.previous_move, level, v)
            else:
                log_minimax(file_handle, state.previous_move, level + 1, v)
        return v

    def max_value(state, level):
        state.player = mancala.max_player
        if(state.game_over is True):
            if not state.mancala_is_last_stop:
                log_minimax(file_handle, state.previous_move, level,
                    compute_eval(state))
            else:
                log_minimax(file_handle, state.previous_move, level + 1,
                    compute_eval(state))
            return compute_eval(state)

        if (cutoff_test(level)):
            if not state.mancala_is_last_stop:
                log_minimax(file_handle, state.previous_move, level,
                    compute_eval(state))
            else:
                log_minimax(file_handle, state.previous_move, level + 1,
                    compute_eval(state))
            return compute_eval(state)

        v = -infinity

        if not state.mancala_is_last_stop and level != 1:
            log_minimax(file_handle, state.previous_move, level, "-Infinity")
        for move in mancala.get_legal_moves(state):
            result = mancala.result(state, move)
            if result.mancala_is_last_stop is True:
                log_minimax(file_handle, move, level + 1, "-Infinity")
                w = max_value(result, level)
            elif level == 0:
                log_minimax(file_handle, move, level + 1, "Infinity")
                w = min_value(result, level+ 1)

            v = max(v, w)
            if not state.mancala_is_last_stop:
                log_minimax(file_handle, state.previous_move, level, v)
            else:
                log_minimax(file_handle, state.previous_move, level + 1, v)
        return v

    def cutoff_test(level):
        return (level == mancala.cutoff)

    def compute_eval(state):
        diff = state.board.values()[len(state.board) / 2] - state.board.values()[0]
        return diff if mancala.max_player == 1 else -diff

    return argmax(mancala.get_legal_moves(state),
    lambda x,y: min_value(x, y), lambda x,y: max_value(x, y), mancala)

class Mancala:
    def __init__(self, board, cutoff, player, task):
        self.task = task
        if(self.task == 1):
            self.cutoff = 1
        else:
            self.cutoff = cutoff
        self.moves = [ pit for (pit_idx, pit) in enumerate(board)\
                    if (pit_idx != 0 and (pit_idx != (len(board) / 2))\
                             and (board[pit] != 0)) ]
        self.max_player = player
        self.initial_state = GameState(board = board, player = player,
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
                and board[board.keys()[board_iter]] == 0\
                and 'B' in board.keys()[board_iter]) 
                                if state.player == 1\
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
                    and (idx != mancala_index) and (idx != other_mancala_index)) ]) == 0)\
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
        return GameState(player = state.player, board = board,
            mancala_is_last_stop = self.mancala_is_last_stop,
            game_over = self.game_over,previous_move = move)

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
    next_state_board =\
     get_next_state(M.initial_state, M, max_payoff_move, max_value)
    write_state(next_state_board, next_state_file_handle)
    input_file_handle.close()
    traverse_log_file_handle.close()
    next_state_file_handle.close()

if __name__ == '__main__':
    main()
