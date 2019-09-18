import chess
from general_comp import *



def rook_compare(cur_board): 
	white_rook_square = []
	black_rook_square = []
	for i in chess.SQUARES:
		if(cur_board.piece_at(i) != None):
			if(cur_board.piece_at(i).symbol() == 'R'): # find rooks location
				white_rook_square.append(i)
			if(cur_board.piece_at(i).symbol() == 'r'):
				black_rook_square.append(i)
	
	[white_piece_value, black_piece_value] = [0, 0]
	for i in range( min(len(white_rook_square), len(black_rook_square)) ):
		[white_piece_value, black_piece_value] = [sum(x) for x in zip(two_pieces_compare(white_rook_square[i], black_rook_square[i], cur_board), [white_piece_value, black_piece_value])] # total value of the rooks
	

	white_doubled = False # if rooks are doubled it is considered as great advantage
	black_doubled = False 
	if(len(white_rook_square) > 1):
		rook1_file = chess.square_file(white_rook_square[0])
		rook1_rank = chess.square_rank(white_rook_square[0])
		
		rook2_file = chess.square_file(white_rook_square[1])
		rook2_rank = chess.square_rank(white_rook_square[1])
		
		if( rook1_rank == rook2_rank ): # if on same rank/file then check if squares between them are empty. If so then they are indeed doubled
			possible_squares = [chess.square(i, rook1_rank) for i in range(min(rook1_file, rook2_file) + 1, max(rook1_file, rook2_file))] # the squares between the two rooks
			if(all(cur_board.piece_at(k) == None for k in possible_squares)):
				white_doubled = True
		
		if( rook1_file == rook2_file ): # if rooks aligned
			possible_squares = [chess.square(rook1_file, i) for i in range(min(rook1_rank, rook2_rank) + 1, max(rook1_rank, rook2_rank))] # the squares between the two rooks
			if(all(cur_board.piece_at(k) == None for k in possible_squares)):
				white_doubled = True
				
	if(len(black_rook_square) > 1):
		rook1_file = chess.square_file(white_rook_square[0])
		rook1_rank = chess.square_rank(white_rook_square[0])
		
		rook2_file = chess.square_file(white_rook_square[1])
		rook2_rank = chess.square_rank(white_rook_square[1])
		
		if( rook1_rank == rook2_rank ): # if on same rank/file then check if squares between them are empty. If so then they are indeed doubled
			possible_squares = [chess.square(i, rook1_rank) for i in range(min(rook1_file, rook2_file) + 1, max(rook1_file, rook2_file))] # the squares between the two rooks
			if(all(cur_board.piece_at(k) == None for k in possible_squares)):
				black_doubled = True
		
		if( rook1_file == rook2_file ): # if rooks aligned
			possible_squares = [chess.square(rook1_file, i) for i in range(min(rook1_rank, rook2_rank) + 1, max(rook1_rank, rook2_rank))] # the squares between the two rooks
			if(all(cur_board.piece_at(k) == None for k in possible_squares)):
				black_doubled = True
	
	white_open_files = [] # rooks controlling open file is great advantage
	black_open_files = []
	for i in white_rook_square:
		possible_file = chess.square_file(i)
		open_file = 0
		for j in range(8):
			if(cur_board.piece_at(chess.square(possible_file, j)) == None or (cur_board.piece_at(chess.square(possible_file, j)).color and cur_board.piece_at(chess.square(possible_file, j)).symbol() != 'P') ): # check all squares in the same file (file, rank) if empty or there are only friendly pieces it is open
				open_file = open_file + 1
		if(open_file == 8):
			white_open_files.append(possible_file)
	
	for i in black_rook_square:
		possible_file = chess.square_file(i)
		open_file = 0
		for j in range(8):
			if(cur_board.piece_at(chess.square(possible_file, j)) == None or (not cur_board.piece_at(chess.square(possible_file, j)).color and cur_board.piece_at(chess.square(possible_file, j)).symbol() != 'p') ): # check all squares in the same file (file, rank) if empty or there are only friendly pieces it is open
				open_file = open_file + 1
		if(open_file == 8):
			black_open_files.append(possible_file)
	
	white_open_files = len(list(set(white_open_files))) # if rooks on same file considered it as one open file so we use set in order to remove duplicates
	black_open_files = len(list(set(black_open_files)))
	
	[white_piece_value, black_piece_value] = [sum(x) for x in zip([white_piece_value, black_piece_value], [white_doubled + white_open_files * 1.5, black_doubled + black_open_files * 1.5])] # give more value to open files than doubled rook
	
	attr1 = [white_doubled, black_doubled] # info about doubled/connected rooks
	attr2 = [white_open_files, black_open_files]
	
	return([white_piece_value/6, black_piece_value/6], attr1, attr2)

