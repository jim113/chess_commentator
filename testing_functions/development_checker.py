import chess

def queen_compare(cur_board):
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
	
	
	if(white_queen_checks):
		return ([2.5, 0]) # white queen is better. 2.5 is th max value of a queen theoretically
	if(black_queen_checks):
		return ([0, 2.5]) # black queen is better
	
	return ([white_queen_value, black_queen_value])
	
	
	
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
	
	print(white_doubled, white_open_files)
	return([white_piece_value, black_piece_value])
	


def knight_compare(cur_board):
	white_knight_square = []
	black_knight_square = []
	for i in chess.SQUARES:
		if(cur_board.piece_at(i) != None):
			if(cur_board.piece_at(i).symbol() == 'N'): # find knights location
				white_knight_square.append(i)
			if(cur_board.piece_at(i).symbol() == 'n'):
				black_knight_square.append(i)
	
	[white_piece_value, black_piece_value] = [0, 0]
	for i in range( min(len(white_knight_square), len(black_knight_square)) ):
		[white_piece_value, black_piece_value] = [sum(x) for x in zip(two_pieces_compare(white_knight_square[i], black_knight_square[i], cur_board), [white_piece_value, black_piece_value])] # total value of the knights according to their diffenders and the squares they control
	
	white_knight_centralised = 0 # check if knight is in center. Centralised knights have better mobility and controll more squares. Knight in center can reach any square in 4 moves. As the folks says knight in the rim is dim ;p
	black_knight_centralised = 0
	center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
	
	white_knight_almost_centralised = 0 # check if knight is in extended center
	black_knight_almost_centralised = 0
	extended_center_squares = [chess.C4, chess.C5, chess.D3, chess.D6, chess.E3, chess.E6, chess.F4, chess.F5]
	
	for i in range(len(white_knight_square)):
		if(white_knight_square[i] in center_squares): # if white knight is in central squares
			white_knight_centralised = white_knight_centralised + 1
		if(white_knight_square[i] in extended_center_squares): # if white knight is in extened central squares
			white_knight_almost_centralised = white_knight_almost_centralised + 1
		
	for i in range(len(black_knight_square)):
		if(black_knight_square[i] in center_squares):
			black_knight_centralised = black_knight_centralised + 1
		if(black_knight_square[i] in extended_center_squares):
			black_knight_almost_centralised = black_knight_almost_centralised + 1
		
	
	white_has_outpost = 0 # a knight having an outpost is a great advantage. A square is considered as outpost if there is no enemy pawn to kick away the night and the night is protected here. An outpost is the best square to put your knight
	black_has_outpost = 0
	
	for i in white_knight_square:
		outpost = True
		white_att = cur_board.attackers(chess.BLACK, i)
		white_def = cur_board.attackers(chess.WHITE, i)
		for j in white_att:
			if(cur_board.piece_at(j).symbol() == 'p'): # if enemy pawn is attacking then it is not outpost
				outpost = False
		if(len(white_def) == 0): # if no one is defending the knight it is not outpost
			outpost = False
		
		neighbor_files = [chess.square_file(i) + dx for dx in [-1, 1] if (0 <= chess.square_file(i) + dx <= 7)] # find neighbor files and check in these files to ranks ahead if there are enemy pawns able to move 2 or 3 positions forward, meaning there is no one to block them then there is no outpost. If no pawns exist in neighbor files or there are enemy pawns in neighbor files but are blocked to approach the night then this square is indeed outpost.
		
		neighbor_ranks = [chess.square_rank(i) + dy for dy in [2, 3, 4, 5, 6, 7] if(0 <= chess.square_rank(i) + dy <= 7)]
		possible_squares = [chess.square(i, j) for i in neighbor_files for j in neighbor_ranks] # possible squares. If in these squares there are unblocked pawns then knight is not on an oupost
		
		for j in possible_squares:
			if(cur_board.piece_at(j) != None and cur_board.piece_at(j).symbol() == 'p'): # if squares ahead are not empty check if there is a pawn. If there is pawn check if it can move to attack knight. If it can then the square is not outpost.
				pawn_file = chess.square_file(j) # locate pawn that possibly can kick out knight
				pawn_rank = chess.square_rank(j)
				knight_rank = chess.square_rank(i)
				blockers_squares = [chess.square(pawn_file, dx) for dx in range(pawn_rank - 1,  knight_rank + 1, -1)] # these are the squares where friendly pawn/pieces should exist in order to block enemy pawn from kicking the knight away. These squares are squares on same file as pawn and ranks ahead until reaching knight.
				
				
				if( all(cur_board.piece_at(k) == None or not cur_board.piece_at(k).color for k in blockers_squares) ): # if there are no blockers or there are only enemy material on blockers squares
					outpost = False
		
		if(outpost): white_has_outpost = white_has_outpost + 1
		
		
	for i in black_knight_square:
		outpost = True
		black_att = cur_board.attackers(chess.WHITE, i)
		black_def = cur_board.attackers(chess.BLACK, i)
		for j in black_att:
			if(cur_board.piece_at(j).symbol() == 'P'): # if enemy pawn is attacking then it is not outpost
				outpost = False
		if(len(black_def) == 0): # if no one is defending the knight it is not outpost
			outpost = False
		
		neighbor_files = [chess.square_file(i) + dx for dx in [-1, 1] if (0 <= chess.square_file(i) + dx <= 7)] # find neighbor files and check in these files to ranks ahead if there are enemy pawns able to move 2 or 3 positions forward, meaning there is no one to block them then there is no outpost. If no pawns exist in neighbor files or there are enemy pawns in neighbor files but are blocked to approach the night then this square is indeed outpost.
		
		neighbor_ranks = [chess.square_rank(i) - dy for dy in [2, 3, 4, 5, 6, 7] if(0 <= chess.square_rank(i) - dy <= 7)]
		possible_squares = [chess.square(i, j) for i in neighbor_files for j in neighbor_ranks] # possible squares. If in these squares there are unblocked pawns then knight is not on an oupost
		
		for j in possible_squares:
			if(cur_board.piece_at(j) != None and cur_board.piece_at(j).symbol() == 'P'): # if squares ahead are not empty check if there is a pawn. If there is pawn check if it can move to attack knight. If it can then the square is not outpost.
				
				pawn_file = chess.square_file(j) # locate pawn that possibly can kick out knight
				pawn_rank = chess.square_rank(j)
				knight_rank = chess.square_rank(i)
				blockers_squares = [chess.square(pawn_file, dx) for dx in range(pawn_rank + 1,  knight_rank - 1)] # these are the squares where friendly pawn/pieces should exist in order to block enemy pawn from kicking the knight away. These squares are squares on same file as pawn and ranks ahead until reaching knight.
				
				if( all(cur_board.piece_at(k) == None or cur_board.piece_at(k).color for k in blockers_squares) ): # if there are no blockers or there are only enemy material on blockers squares
					outpost = False
		
		if(outpost): black_has_outpost = black_has_outpost + 1
	
	
	white_piece_value = white_piece_value + white_knight_centralised * 0.5 + white_knight_almost_centralised * 0.3 + 1.2 * white_has_outpost # give more weight if it has outpost
	
	black_piece_value = black_piece_value + black_knight_centralised * 0.5 + black_knight_almost_centralised * 0.3 + 1.2 * black_has_outpost
	
	
	return ([white_piece_value, black_piece_value], [white_has_outpost, black_has_outpost])
	



def bishop_compare(cur_board):
	white_bishop_square = []
	black_bishop_square = []
	for i in chess.SQUARES:
		if(cur_board.piece_at(i) != None):
			if(cur_board.piece_at(i).symbol() == 'B'): # find bishops location
				white_bishop_square.append(i)
			if(cur_board.piece_at(i).symbol() == 'b'):
				black_bishop_square.append(i)
	
	if(len(white_bishop_square) == 2): # if we have pair of bishops then sort them as [light, dark]
		rank1 = chess.square_rank(white_bishop_square[0])
		file1 = chess.square_file(white_bishop_square[0])
		if((rank1 + file1) % 2 == 0 ) : # meaning dark square then swap them
			white_bishop_square[0] = white_bishop_square[1]
			white_bishop_square[1] = white_bishop_square[0]	
	
	if(len(black_bishop_square) == 2): # if we have pair of bishops then sort them as [light, dark]
		rank1 = chess.square_rank(black_bishop_square[0])
		file1 = chess.square_file(black_bishop_square[0])
		if((rank1 + file1) % 2 == 0 ) : # meaning dark square then swap them
			black_bishop_square[0] = black_bishop_square[1]
			black_bishop_square[1] = black_bishop_square[0]	
	
	[white_piece_value, black_piece_value] = [0, 0]
	for i in range( min(len(white_bishop_square), len(black_bishop_square)) ):
		[white_piece_value, black_piece_value] = [sum(x) for x in zip(two_pieces_compare(white_bishop_square[i], black_bishop_square[i], cur_board), [white_piece_value, black_piece_value])] # total value of the bishops according to their diffenders and the squares they control. Bishop pair is considered as advantage but it is indicated from material values so we dont take it under consideration here.

	return([white_piece_value, black_piece_value])

b = chess.Board()

b.clear_board()
b.set_piece_at(28, chess.Piece(4, 1)) # white queen
b.set_piece_at(44, chess.Piece(4, 1))
#b.set_piece_at(36, chess.Piece(3, 1)) # black queen
b.set_piece_at(29, chess.Piece(4, 1))
#b.set_piece_at(11, chess.Piece(1, 1))

print(b)
print(rook_compare(b))
