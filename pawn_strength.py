import chess


def count_pawn_islands(cur_board, color):
	pawn = 'p' # pawn symbol if color is black
	if(color == 1):
		pawn = 'P'
	pawn_files = []
	pawn_ranks = []
	for i in chess.SQUARES: # search for all pawns 
		if(cur_board.piece_at(i) != None and cur_board.piece_at(i).symbol() == pawn): # if not empty and there is a pawn occupant then append file number
			pawn_files.append(chess.square_file(i))
			pawn_ranks.append(chess.square_rank(i))
	
	pawn_files.sort() # in case of not in order becaue the way we search
	islands = 1 # count pawn islands
	for i in range(len(pawn_files) - 1): 
		if (pawn_files[i + 1] != pawn_files[i] + 1): # if not consequtive then we have new island
			islands = islands + 1
	
	pawn_ranks.sort()
	pawn_ranks.reverse()
	passed_pawns = [i for i in pawn_ranks if i == pawn_ranks[0]] # find the most pushed pawn/s comparing it with the others after sorting their ranks. After with this rank we determine if it is pushed too much
	backward_pawns = [i for i in pawn_ranks if i == pawn_ranks[-1]] # find the most backward pawn/s comparing them with other pawns
	
	return ([islands, passed_pawns, backward_pawns])
	
	
def check_for_passed_pawn(cur_board, color, probably_passed): # a pawn is considered as passed if the file is open from enemy's pawns and no square of the file can be attacked by enemy pawn. Probably passed has the rank of most pushed pawns or rank of pawns to check if they are passed pawns. We check for whole rank's pawns when calling this function
	pawn = 'p' # pawn symbol if color is black
	if(color == 1):
		pawn = 'P'
	passed_pawn_confirmed = [] 
	file_index = []
	rank_index = probably_passed[0] # all of probably_passed has same value, the rank
	
	for i in range(8): # check all files to spot the possible passed pawn
		if(cur_board.piece_at(chess.square(i, rank_index)) != None and cur_board.piece_at(chess.square(i, rank_index)).symbol() == pawn): # square as (file, rank)
			file_index.append(i) # append all file indexes
	
	#print(file_index)
	
	for i in file_index: # for all file indexes
		is_passed = True 
		if(color == 1):	
			for k in range(rank_index, 8): # if white check all forward squares of the file. If none is attacked its passed pawn as mentioned	
				if(cur_board.piece_at(chess.square(i, k)) != None and cur_board.piece_at(chess.square(i, k)).symbol() == 'p'):
					is_passed = False # if enemy pawn in same file then it is not passed pawn
					break
				blockers = cur_board.attackers(chess.BLACK, chess.square(i, k))
			
				for blocker in blockers:
					if(cur_board.piece_at(blocker).symbol() == 'p'): # if pawn attacker exists then it is not passed
						is_passed = False # if attackers exists
		else:
			for k in range(rank_index, -1, -1): # if black check all backward squares of the file. If none is attacked its passed pawn as mentioned	
				if(cur_board.piece_at(chess.square(i, k)) != None and cur_board.piece_at(chess.square(i, k)).symbol() == 'P'):
					is_passed = False # if enemy pawn in same file then it is not passed pawn
					break
				blockers = cur_board.attackers(chess.WHITE, chess.square(i, k))
				for blocker in blockers:
					if(cur_board.piece_at(blocker).symbol() == 'P'): # if pawn attacker exists then it is not passed
						is_passed = False # if attackers exists
	
		if(is_passed):
			passed_pawn_confirmed.append(chess.square(i, rank_index))
		
	return (passed_pawn_confirmed)




def check_for_backwards_pawn(cur_board, color, backward_pawns): # a pawn is considered as backward if their neighbor pawns have moved forward
	pawn = 'p' # pawn symbol if color is black
	if(color == 1):
		pawn = 'P'
	backward_pawn_confirmed = [] 
	file_index = []
	rank_index = backward_pawns[0] # all of probably has same value, the rank
	
	for i in range(8): # check all files to spot the possible backward pawn
		if(cur_board.piece_at(chess.square(i, rank_index)) != None and cur_board.piece_at(chess.square(i, rank_index)).symbol() == pawn): # square as (file, rank)
			file_index.append(i) # append all file indexes
			
	
	for i in file_index: # for all file indexes
		neighbor_files = [i + j for j in [-1,1] if(0<= (i + j) <= 7)] # locate neighbor files in order to check pawn positions on these files
		neighbors_rank = []
		for j in neighbor_files:
			for k in range(8):
				if(cur_board.piece_at(chess.square(j, k)) != None and cur_board.piece_at(chess.square(j, k)).symbol() == pawn): # check neighbor pawn's rank
					neighbors_rank.append(k) # list of all neighbors rank
		neighbors_rank.sort() # sort all ranks and then compare with pawn's rank
		if(len(neighbors_rank) > 0 and color == 1 and neighbors_rank[0] > rank_index): # if all neighbors are ahead then it is backwards
			backward_pawn_confirmed.append(chess.square(i, rank_index)) # if it is backwards store its square
		if(len(neighbors_rank) > 0 and color != 1 and neighbors_rank[0] < rank_index): # if all neighbors are ahead then it is backwards
			backward_pawn_confirmed.append(chess.square(i, rank_index)) # if it is backwards store its square
	
	return(backward_pawn_confirmed)
				



def multi_pawn_file(cur_board, color, number): # given the number check if and which file/s has that number of pawns of color. Example number = 2 then find files of doubled pawns
	pawn = 'p' # pawn symbol if color is black
	if(color == 1):
		pawn = 'P'
	pawn_files = [] 
	for files in range(8):
		pawns_in_file = 0
		for ranks in range(8):
			if(cur_board.piece_at(chess.square(files, ranks)) != None and cur_board.piece_at(chess.square(files, ranks)).symbol() == pawn): # if pawn found then increase counter
				pawns_in_file = pawns_in_file + 1
		if(pawns_in_file == number): # if there are number pawns of the given color on that file then add it to result
			pawn_files.append(files)
	
	return(pawn_files)





def controlling_squares(cur_board, color): # find squares controlled by given color's pieces on give board
	pawn = 'p' # pawn symbol if color is black
	if(color == 1):
		pawn = 'P'	
	controlled_squares = []
	for i in chess.SQUARES:
		if(color == 1):
			attackers = cur_board.attackers(chess.WHITE, i) # find attackers to that square meaning that the given color controls this square
		else:
			attackers = cur_board.attackers(chess.BLACK, i)
		
		for j in attackers: # if there is at least one piece attacker to control the square then it belongs to the controlled squares of the given color
			if(cur_board.piece_at(j) != pawn):
				controlled_squares.append(i)
				break
		
	return (controlled_squares)
		
		

def blocking_pawn_finder(cur_board, color): # for every pawn check if its square is blocking the mobility or attacking lines of friendly piece, if yes then add to list that piece. To check that we take a board and remove all pawns. Count attacked squares and then compare that number with the attacked squares with the pawns in their positions. The difference indicates how 'blockating' the pawns are. Example a pawn ahead of a rook is blocking the squares on the file in front of the pawn and the rook cannot control these squares
	pawn = 'p' # pawn symbol if color is black
	if(color == 1):
		pawn = 'P'
	
	pawn_square = []
	for i in chess.SQUARES:
		if(cur_board.piece_at(i) != None and cur_board.piece_at(i).symbol() == pawn): # if there is pawn on that square then keep it in list
			pawn_square.append(i)

	without_pawns = cur_board.copy() # a copy of board in order to remove pawns
	for i in pawn_square:
		without_pawns.remove_piece_at(i)	

	controlled_with_pawns = controlling_squares(cur_board, color)
	controlled_without_pawns = controlling_squares(without_pawns, color)
	
	square_controlling_difference = [i for i in controlled_without_pawns  if i not in controlled_with_pawns]
	# this difference shows how bad a pawn stracture is. If it is very big when comparing it with the opponent's difference. If it is big then it means that pawns are blocking pieces and do not let them control more space over the board
	return (square_controlling_difference, len(square_controlling_difference))
	
	
	
def pawns_difference(cur_board, fut_board):
	[w_islands_now, w_passed_pawns_now, w_backward_pawns_now] = count_pawn_islands(cur_board, 1)
	[b_islands_now, b_passed_pawns_now, b_backward_pawns_now] = count_pawn_islands(cur_board, 2)
	w_passed_pawns_conf_now = check_for_passed_pawn(cur_board, 1, w_passed_pawns_now)
	b_passed_pawns_conf_now = check_for_passed_pawn(cur_board, 2, b_passed_pawns_now)	
	w_backward_pawn_confirmed_now = check_for_backwards_pawn(cur_board, 1, w_backward_pawns_now)
	b_backward_pawn_confirmed_now = check_for_backwards_pawn(cur_board, 2, b_backward_pawns_now)
	w_doubled_pawns_now = multi_pawn_file(cur_board, 1, 2)
	b_doubled_pawns_now = multi_pawn_file(cur_board, 2, 2)
	[w_square_controlling_dif_now, w_length_of_dif_now] = blocking_pawn_finder(cur_board, 1)
	[b_square_controlling_dif_now, b_length_of_dif_now] = blocking_pawn_finder(cur_board, 2)
	
	
	[w_islands, w_passed_pawns, w_backward_pawns] = count_pawn_islands(fut_board, 1)
	[b_islands, b_passed_pawns, b_backward_pawns] = count_pawn_islands(fut_board, 2)
	w_passed_pawns_conf = check_for_passed_pawn(fut_board, 1, w_passed_pawns)
	b_passed_pawns_conf = check_for_passed_pawn(fut_board, 2, b_passed_pawns)	
	w_backward_pawn_confirmed = check_for_backwards_pawn(fut_board, 1, w_backward_pawns)
	b_backward_pawn_confirmed = check_for_backwards_pawn(fut_board, 2, b_backward_pawns)
	w_doubled_pawns = multi_pawn_file(fut_board, 1, 2)
	b_doubled_pawns = multi_pawn_file(fut_board, 2, 2)
	[w_square_controlling_dif, w_length_of_dif] = blocking_pawn_finder(fut_board, 1)
	[b_square_controlling_dif, b_length_of_dif] = blocking_pawn_finder(fut_board, 2)	
	
	w_islands_dif = w_islands - w_islands_now # after calculating all metrics for pawns we calculate the differences and group them to produce the result. If a new pawn island is going to be created the dif will show it
	b_islands_dif = b_islands - b_islands_now
	
	w_passed_pawns_dif = len(w_passed_pawns_conf) - len(w_passed_pawns_conf_now) # if a passed pawn is about to be created then the difference will show it
	b_passed_pawns_dif = len(b_passed_pawns_conf) - len(b_passed_pawns_conf_now)
	
	w_backward_pawns_dif = len(w_backward_pawn_confirmed) - len(w_backward_pawn_confirmed_now) # if a backward pawn is about to be created then the difference will show it
	b_backward_pawns_dif = len(b_backward_pawn_confirmed) - len(b_backward_pawn_confirmed_now)
	
	
	w_doubled_dif = len(w_doubled_pawns) - len(w_doubled_pawns_now) # calculate the dif in order to spot if doubled pawns are about to be made
	b_doubled_dif = len(b_doubled_pawns) - len(b_doubled_pawns_now)
	
	w_block_dif = w_length_of_dif - w_length_of_dif_now # calculate blocking difference, if increases means that pawns block more your pieces and that is bad because pieces have less mobility
	b_block_dif = b_length_of_dif - b_length_of_dif_now	
	
	
	w_pawn_obj_now = 1 / w_islands_now + len(w_passed_pawns_conf_now) + 0.5 / max(len(w_backward_pawn_confirmed_now), 1) + 0.2 / max(1, len(w_doubled_pawns_now)) + 0.3 / max(1, w_length_of_dif_now) # pawn structure objective combining all metrics 
	b_pawn_obj_now = 1 / b_islands_now + len(b_passed_pawns_conf_now) + 0.5 / max(len(b_backward_pawn_confirmed_now), 1) + 0.2 / max(1, len(b_doubled_pawns_now)) + 0.3 / max(1, b_length_of_dif_now)
	
	w_pawn_obj = 1 / w_islands + len(w_passed_pawns_conf) + 0.5 / max(len(w_backward_pawn_confirmed), 1) + 0.2 / max(1, len(w_doubled_pawns)) + 0.3 / max(1, w_length_of_dif)
	b_pawn_obj = 1 / b_islands + len(b_passed_pawns_conf) + 0.5 / max(len(b_backward_pawn_confirmed), 1) + 0.2 / max(1, len(b_doubled_pawns)) + 0.3 / max(1, b_length_of_dif)
	
	w_obj_dif = w_pawn_obj - w_pawn_obj_now
	b_obj_dif = b_pawn_obj - b_pawn_obj_now
	
	res = [[w_islands_dif, b_islands_dif], [w_passed_pawns_dif, b_passed_pawns_dif], [w_backward_pawns_dif, b_backward_pawns_dif], [w_doubled_dif, b_doubled_dif], [w_block_dif/64, b_block_dif/64], [w_obj_dif, b_obj_dif]]
	
	return (res)


