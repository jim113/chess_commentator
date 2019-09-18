import chess


def centre_control_occupants(cur_board, color): # Returns number of central pawns/pieces of given color
	pawns = 0
	pieces = 0
	
	occupants = [cur_board.piece_at(chess.E4), cur_board.piece_at(chess.D4), cur_board.piece_at(chess.E5),  cur_board.piece_at(chess.D5)] # Pawns or pieces on the central squares
	
	for i in occupants:
		if(i != None):
			if( (color == 1) and (i.symbol() == i.symbol().upper()) ): # if given is White and pawn/piece is also White
				if(i.symbol() == 'P'):
					pawns = pawns + 1
				else:
					pieces = pieces + 1
			elif( (color != 1) and (i.symbol() != i.symbol().upper()) ): # if given is Black and pawn/piece is also Black
				if(i.symbol() == 'p'):
					pawns = pawns + 1
				else:
					pieces = pieces + 1
	return([pawns, pieces])
	


def centre_control(cur_board, color): #define centre as e4, d4, e5, d5
	pawns = 0
	pieces = 0
	if(color == 1): # 1 means White 
		e4_attackers = cur_board.attackers(chess.WHITE, chess.E4)
		d4_attackers = cur_board.attackers(chess.WHITE, chess.D4)
		e5_attackers = cur_board.attackers(chess.WHITE, chess.E5)
		d5_attackers = cur_board.attackers(chess.WHITE, chess.D5)
		colored_pawn = 'P' # if it is a pawn, P for White & p for Black
	else: # 2 means Black
		e4_attackers = cur_board.attackers(chess.BLACK, chess.E4)
		d4_attackers = cur_board.attackers(chess.BLACK, chess.D4)
		e5_attackers = cur_board.attackers(chess.BLACK, chess.E5)
		d5_attackers = cur_board.attackers(chess.BLACK, chess.D5)
		colored_pawn = 'p'
	
	center_list = [e4_attackers, d4_attackers, e5_attackers, d5_attackers]
	already_checked = [chess.E4, chess.D4, chess.E5, chess.D5]
	[center_pawns, center_pieces] = centre_control_occupants(cur_board, color) # Find pawns/pieces on center 
	pawns = pawns + center_pawns
	pieces = pieces + center_pieces
	
	for i in center_list:
		for j in i:
			if(j in already_checked): # if we have seen this piece/pawn continue
				continue
			else:
				already_checked.append(j)
				
			if(cur_board.piece_at(j).symbol() == colored_pawn ): 
				pawns = pawns + 1
			else: # it is a piece
				pieces = pieces + 1
				
	return ([pawns, pieces]) # return pawns/pieces of given color controling center
	


def center_control_difference(cur_board, fut_board):
	white_dif = 0
	black_dif = 0
	[w_pawns_now, w_pieces_now] = centre_control(cur_board, 1) # compute objective for current and future board for both sides and then compute de difference
	[b_pawns_now, b_pieces_now] = centre_control(cur_board, 2)
	[w_pawns, w_pieces] = centre_control(fut_board, 1)
	[b_pawns, b_pieces] = centre_control(fut_board, 2)
	
	w_pawns_dif = w_pawns - w_pawns_now
	w_pieces_dif = w_pieces - w_pieces_now
	
	b_pawns_dif = b_pawns - b_pawns_now
	b_pieces_dif = b_pieces - b_pieces_now 
	
	white_dif = w_pawns_dif + w_pieces_dif * 0.5 # it is more important to control center with pawns rather than pieces. So finding the difference between future and now we conclude to a metric of control improvement/ weakening
	black_dif = b_pawns_dif + b_pieces_dif * 0.5
	
	return ([white_dif, black_dif], [[w_pawns_dif, b_pawns_dif], [w_pieces_dif, b_pieces_dif]])


