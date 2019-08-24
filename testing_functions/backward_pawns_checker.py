import chess

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
	
	print(file_index)
	
	for i in file_index: # for all file indexes
		neighbor_files = [i + j for j in [-1,1] if(0<= (i + j) <= 7)] # locate neighbor files in order to check pawn positions on these files
		print(neighbor_files)
		neighbors_rank = []
		for j in neighbor_files:
			for k in range(8):
				if(cur_board.piece_at(chess.square(j, k)) != None and cur_board.piece_at(chess.square(j, k)).symbol() == pawn): # check neighbor pawn's rank
					neighbors_rank.append(k) # list of all neighbors rank
		neighbors_rank.sort() # sort all ranks and then compare with pawn's rank
		if(neighbors_rank[0] > rank_index): # if all neighbors are ahead then it is backwards
			backward_pawn_confirmed.append(chess.square(i, rank_index)) # if it is backwards store its square
	
	print(backward_pawn_confirmed)
		
b = chess.Board()
#print(b)
#b.push_san(b.san(chess.Move.from_uci('e2e4')))
#b.push_san(b.san(chess.Move.from_uci('e7e5')))
#b.push_san(b.san(chess.Move.from_uci('c2c4')))
b.set_piece_at(32, chess.Piece(1,1)) # pawn
b.set_piece_at(42, chess.Piece(1,1))
b.set_piece_at(38, chess.Piece(1,1))
b.set_piece_at(28, chess.Piece(1,1))

b.remove_piece_at(8)
b.remove_piece_at(10)
b.remove_piece_at(12)
b.remove_piece_at(14)
print(b)
check_for_backwards_pawn(b, 1, [1])
