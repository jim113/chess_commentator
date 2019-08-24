import chess

def check_for_passed_pawn(cur_board, color, probably_passed): # a pawn is considered as passed if the file is open from enemy's pawns and no square of the file can be attacked by enemy pawn
	pawn = 'p' # pawn symbol if color is black
	if(color == 1):
		pawn = 'P'
	passed_pawn_confirmed = [] 
	file_index = []
	rank_index = probably_passed[0] # all of probably has same value, the rank
	
	for i in range(8): # check all files to spot the possible passed pawn
		if(cur_board.piece_at(chess.square(i, rank_index)) != None and cur_board.piece_at(chess.square(i, rank_index)).symbol() == pawn): # square as (file, rank)
			file_index.append(i) # append all file indexes
	
	print(file_index)
	
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
				if(cur_board.piece_at(chess.square(i, k)) != None and cur_board.piece_at(chess.square(i, k)).symbol() == 'p'):
					is_passed = False # if enemy pawn in same file then it is not passed pawn
					break
				blockers = cur_board.attackers(chess.WHITE, chess.square(i, k))
				for blocker in blockers:
					if(cur_board.piece_at(blocker).symbol() == 'P'): # if pawn attacker exists then it is not passed
						is_passed = False # if attackers exists
	
		if(is_passed):
			passed_pawn_confirmed.append(chess.square(i, rank_index))
		
	print(passed_pawn_confirmed)
		
		
b = chess.Board()
#print(b)

b.remove_piece_at(49)
b.remove_piece_at(50)
b.remove_piece_at(51)
print(b)
check_for_passed_pawn(b, 1, [1])
