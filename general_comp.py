import chess


def two_pieces_compare(white_piece_square, black_piece_square, cur_board): # value same pieces according to their attackers and their controll range
	white_piece_attackers = cur_board.attackers(chess.BLACK, white_piece_square) # the more attackers the worse it is
	black_piece_attackers = cur_board.attackers(chess.WHITE, black_piece_square)
	
	white_piece_controlled = [] # square controlled by white piece
	black_piece_controlled = []
	for i in chess.SQUARES:
		white_att = cur_board.attackers(chess.WHITE, i)
		black_att = cur_board.attackers(chess.BLACK, i)
		if(white_piece_square in white_att): # if white piece attacks that square then it controlls it
			white_piece_controlled.append(i)
		if(black_piece_square in black_att):	
			black_piece_controlled.append(i)
		
	white_factor = len(white_piece_attackers)
	black_factor = len(black_piece_attackers) 
	if(white_factor == 0): white_factor = 1 # if no attacker then neutrile it and consider it as better scenario than having attackers
	if(black_factor == 0): black_factor = 1	
	
	white_piece_value = len(white_piece_controlled) / 64 + (1 / white_factor)
	black_piece_value = len(black_piece_controlled) / 64 + (1 / black_factor)
	
	return ([white_piece_value, black_piece_value]) 	

