import chess
from general_comp import *



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
	
	attrib1 = [white_knight_centralised, black_knight_centralised]
	attrib2 = [white_knight_almost_centralised, black_knight_almost_centralised] # return info about centralised knights
	
	return ([white_piece_value/5.4, black_piece_value/5.4], [white_has_outpost, black_has_outpost], attrib1, attrib2) # we return piece value in percentage. 5.4 is the max value

