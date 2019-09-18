import chess
from predictor import castle_white, castle_black

def king_neighborhood_finder(cur_board, color):
	for i in chess.SQUARES:
		if(cur_board.piece_at(i) != None):	#if there is a piece on square
			content = cur_board.piece_at(i).symbol()
			content_color = cur_board.piece_at(i).color
			if(color == 1 and content_color and content == 'K'): # if given is white and we have white king
				king_square = i
			if(color != 1 and (not content_color) and content == 'k'): # if given is black and we have black king
				king_square = i
	
	king_circle = [king_square] # king's neighborhood
	for dx in {-1, 1, -8, 8, -9, 9, -7, 7}: # all squares adjacent to king's square
		if(0 <= (king_square + dx) <= 63):
			king_circle.append(king_square + dx)
	king_circle.sort()
	return ([king_circle,king_square])



def attacking_king_zone(cur_board, king_zone, color): #the less the score the safer the king
	value_of_attacks = {'p': 7, 'n': 20, 'b': 20, 'r': 40, 'q': 80} # value of attackers
	attack_weight = {0: 0, 1: 0, 2: 50, 3: 75, 4: 88, 5: 94, 6: 97, 7: 99} # attack weight according to book
	already_checked = []
	total_value_of_attack = 0
	total_attackers = 0
	for i in king_zone:
		if(color == 1): # to find white king's attack score, the less the score the safer the king
			tmp_attackers = cur_board.attackers(chess.BLACK, i)
		else:
			tmp_attackers = cur_board.attackers(chess.WHITE, i) # if color != 1 then we want black king score so we search for white attackers
			
		for j in tmp_attackers:
			if(j in already_checked): # if we have seen this piece/pawn continue
				continue
			else:
				already_checked.append(j)

			type_of_attacker = cur_board.piece_at(j).symbol().lower() # who is attacking in lower case symbol
			total_value_of_attack = total_value_of_attack + value_of_attacks[type_of_attacker] #update attack value
			total_attackers = total_attackers + 1
	
	king_attack_score = (total_value_of_attack * attack_weight[total_attackers]) / 100
	return (king_attack_score)
			


def find_kings_free_squares(cur_board, king_zone, color): #free squares for the king to move
	free_squares = 0
	for i in king_zone:
		if(color == 1):
			num_of_attackers = len(cur_board.attackers(chess.BLACK, i)) # number of enemy pieces attacking
		else:
			num_of_attackers = len(cur_board.attackers(chess.WHITE, i))
		if(cur_board.piece_at(i) == None and  num_of_attackers == 0): # if sqare is empty and no enemy attacks it. It is free for the king
			free_squares = free_squares + 1
	return (free_squares)
			


def king_pawn_shield(cur_board, king_zone, king_position, color): # what is the condition of pawns in front of king
	pawns_in_zone = 0 # shield in front of king, most effective
	pawns_one_forward = 0 # shield two rows away from king, medium effective
	pawns_two_forward = 0 # shield three rows away from king, less effective
	if(color == 1):
		pawn = 'P'
		one_forward_zones = [15, 16, 17] # what to add to find squares 2 rows ahead of white king
		two_forward_zones = [23, 24, 25] # what to add to find squares 3 rows ahead of white king
	else:
		pawn = 'p'
		one_forward_zones = [-15, -16, -17] # what to subtruct to find squares 2 rows ahead of black king
		two_forward_zones = [-23, -24, -25] # what to subtruct to find squares 3 rows ahead of black king
	
	for i in king_zone:
		if(cur_board.piece_at(i) != None and cur_board.piece_at(i).symbol() == pawn): # if pawn exists
			pawns_in_zone = pawns_in_zone + 1
	for i in range(3):
		if(not (0<= king_position + one_forward_zones[i] <= 63) or cur_board.piece_at(king_position + one_forward_zones[i]) == None): # if not valid squares or empty skip and continue
			continue
		if(cur_board.piece_at(king_position + one_forward_zones[i]).symbol() == pawn): # if pawn found 2 rows away add it  
			pawns_one_forward = pawns_one_forward + 1
	for i in range(3):
		if(not (0<= king_position + two_forward_zones[i] <= 63) or cur_board.piece_at(king_position + two_forward_zones[i]) == None): # if not valid squares or empty skip and continue
			continue
		if(cur_board.piece_at(king_position + two_forward_zones[i]).symbol() == pawn): # if pawn found 3 rows away add it  
			pawns_two_forward = pawns_two_forward + 1
			
	#print(pawns_in_zone, pawns_one_forward, pawns_two_forward)
	pawn_strength = (pawns_two_forward * 10 + pawns_one_forward * 20 + pawns_in_zone * 50) / 150 # best case 3 pawns in zone as a shield, or in some games even more as doubled pawns. Strength max = 1 if no doubled pawns
	return (pawn_strength)
	
	
	
def king_safety_objective(cur_board, color): # function to calculate given color king's safety using pawns strength, attacking in king's zone score and castling. The greater it is the safer the king
	[king_circle, king_square] = king_neighborhood_finder(cur_board, color) # find squares near the king and king's square
	king_attacking_score = attacking_king_zone(cur_board, king_circle, color) # according to algorithm find attacking score
	pawn_strength = king_pawn_shield(cur_board, king_circle, king_square, color) # count pawn shield in fornt of king and its strength/weakness
	free_squares = find_kings_free_squares(cur_board, king_circle, color) # free squares for the king
	white_castle_done = 0
	black_castle_done = 0
	if(any(i == 1 for i in castle_white)):
		white_castle_done = 1
	if(any(i == 1 for i in castle_black)):
		black_castle_done = 1	
	
	if(king_attacking_score == 0): king_attacking_score = 1	# if no attack is happening neutralize it
	
	king_safety = ( (1.0 / king_attacking_score) * 0.5 + pawn_strength * 0.3 + (free_squares/8) * 0.2) # if both castled or no castled then castle not taken into consideration
	
	if(color == 1): # white chosen and check for castling
		if(white_castle_done == 1 and black_castle_done == 0): # if white castled and black did not it is advantage
			king_safety = ( (1.0 / king_attacking_score) * 0.5 + pawn_strength * 0.3 + (free_squares/8) * 0.1 + 0.1)
		else:
			king_safety = ( (1.0 / king_attacking_score) * 0.5 + pawn_strength * 0.3 + (free_squares/8) * 0.1)
	else:
		if(white_castle_done == 0 and black_castle_done == 1): # if black castled and white did not it is advantage
			king_safety = ( (1.0 / king_attacking_score) * 0.5 + pawn_strength * 0.3 + (free_squares/8) * 0.1 + 0.1)
		else:
			king_safety = ( (1.0 / king_attacking_score) * 0.5 + pawn_strength * 0.3 + (free_squares/8) * 0.1)
			
# king safety is taken as follows: the less the king attack score the safer the king so we take 1/score and give 0.5 weight after that we weight more the pawn shiled with 0.3. At most there are 8 free squares and we value the percentage of them that are free with 0.1. Finaly if one castled and the other did not then value that with 0.1

	attr1 = [king_attacking_score, pawn_strength, free_squares]

	return ([king_safety, attr1])
	
	
	
def king_safety_difference(cur_board, fut_board):	
	white_dif = 0
	black_dif = 0
	[w_king_now, w_attr_now] = king_safety_objective(cur_board, 1) # compute king safety's objective difference from future to now for both sides
	[b_king_now, b_attr_now] = king_safety_objective(cur_board, 2)
	
	[w_king, w_attr] = king_safety_objective(fut_board, 1)
	[b_king, b_attr] = king_safety_objective(fut_board, 2)
	
	white_dif = w_king - w_king_now
	black_dif = b_king - b_king_now
	
	w_attr_dif = [i - j for i, j in zip(w_attr, w_attr_now)] # king safety attributes. These are [king attacking score, pawn structure, free squares]
	b_attr_dif = [i - j for i, j in zip(b_attr, b_attr_now)]
	
	return ([white_dif, black_dif], list(zip(w_attr_dif, b_attr_dif)))


