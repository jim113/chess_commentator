import chess



def queen_compare(cur_board):
	white_queen_square = -1
	black_queen_square = -1
	for i in chess.SQUARES:
		if(cur_board.piece_at(i) != None):
			if(cur_board.piece_at(i).symbol() == 'Q'): # find queens location
				white_queen_square = i
			if(cur_board.piece_at(i).symbol() == 'q'):
				black_queen_square = i
	
	white_queen_attackers = cur_board.attackers(chess.BLACK, white_queen_square) # the more attackers the worse it is
	black_queen_attackers = cur_board.attackers(chess.WHITE, black_queen_square)
	
	white_queen_controlled = [] # square controlled by white queen
	black_queen_controlled = []
	for i in chess.SQUARES:
		white_att = cur_board.attackers(chess.WHITE, i)
		black_att = cur_board.attackers(chess.BLACK, i)
		if(white_queen_square in white_att): # if white queen attacks that square then she controlls it
			white_queen_controlled.append(i)
		if(black_queen_square in black_att):	
			black_queen_controlled.append(i)
	
	white_queen_checks = False # if any queen gives check she has better position because probably taking part in attack and the enemy must protect the king before doing any plans
	black_queen_checks = False
	if(cur_board.king(chess.WHITE) in black_queen_controlled): # if black queen is in check with white king
		black_queen_checks = True
	if(cur_board.king(chess.BLACK) in white_queen_controlled):
		white_queen_checks = True
		
	white_queen_centralised = False # check if queen is in center. Centralised queens have better mobility
	black_queen_centralised = False
	center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
	if(white_queen_square in center_squares): # if white queen is in central squares
		white_queen_centralised = True
	if(black_queen_square in center_squares):
		black_queen_centralised = True
	
	white_factor = len(white_queen_attackers)
	black_factor = len(black_queen_attackers) 
	if(white_factor == 0): white_factor = 1 # if no attacker then neutrile it and consider it as better scenario than having attackers
	if(black_factor == 0): black_factor = 1
	
	white_queen_value = len(white_queen_controlled) / 64 + 0.5 * white_queen_centralised + (1 / white_factor) # value of queen if no checks are given and white queen attackers are 0. We give much value to centralised queen cause it is more mobile and more if queen is attacked
	black_queen_value = len(black_queen_controlled) / 64 + 0.5 * black_queen_centralised + (1 / black_factor)
	
	if(white_queen_square == -1): white_queen_value = 0
	if(black_queen_square == -1): black_queen_value = 0
	attr1 = [white_queen_centralised, black_queen_centralised]
	if(white_queen_checks):
		return ([2.5/2.5, 0], attr1) # white queen is better. 2.5 is th max value of a queen theoretically
	if(black_queen_checks):
		return ([0, 2.5/2.5], attr1) # black queen is better
	
	
	
	return ([white_queen_value/2.5, black_queen_value/2.5], attr1)


