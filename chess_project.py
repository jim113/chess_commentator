from pystockfish import *
import chess

deep = Engine(depth=15)
castle_white = [False, False] # set the castling flags to false for both sides, [kingside, queenside]
castle_black = [False, False]
	
def engines_pred(depth, poslist, cur_board):
	deep.setposition(poslist) # set engine's position
	tmp_board = cur_board.copy() # set local board
	tmp_poslist = poslist.copy() # set local moves' list
	global castle_black
	global castle_white
	
	for i in range(depth): # loop for given depth to find final position
		try:
			next_move = str(deep.bestmove()['move']) # engine's next best move
		except:
			best_move = 'Checkmate!'
			break
		if(tmp_board.turn and not(any(y==True for y in castle_white)) ): #if white's turn and has not castled yet, check if it is castle move
			castle_white = find_castling_choice(tmp_board,chess.Move.from_uci(next_move))
		
		if(not tmp_board.turn and not(any(y==True for y in castle_black)) ): #if black's turn and has not castled yet, check if it is castle move
			castle_black = find_castling_choice(tmp_board,chess.Move.from_uci(next_move))

		
		if(i == 0):
			best_move =  next_move
			
		tmp_poslist.append(next_move)
		next_move = tmp_board.san(chess.Move.from_uci(next_move))
		tmp_board.push_san(next_move)
		
		if(tmp_board.is_checkmate() == True):
			break
		deep.setposition(tmp_poslist) #update engine's position
		
	#print(castle_white, castle_black)	
	return(tmp_board, best_move)
	

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
			



def find_castling_choice(cur_board, move):
	[kingside, queenside] = [cur_board.is_kingside_castling(move), cur_board.is_queenside_castling(move)]
	return ([int(kingside), int(queenside)]) # return tuple of castling choices,if done, 1 for chosed side 0 for the other
	

	
	
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
		
	
	

def material_values(cur_board, color):
	value = {'p': 1, 'n': 3, 'b': 3.25, 'r': 5, 'q': 9, 'k': 0} # material values according to Fischer 1972
	total_value = [[], [], [], [], []] # return material counter, 8 pawns, 2 knights, 2 bishops, 2 rooks and 1 queen. King is neutral cause both pleyers have one to play.
	material_value = 0
	for i in chess.SQUARES:
		type_of_occupant = '' # no occupant until it is found
		if(cur_board.piece_at(i) != None): # if not empty square
			material = cur_board.piece_at(i).symbol()
			if(color == 1 and material == material.upper()): # if given is white and occupant is white
				type_of_occupant = material.lower()
			elif(color != 1 and material == material.lower()): # if given is black and occupant is black
				type_of_occupant = material
			if(type_of_occupant == ''):
				continue	
			if(type_of_occupant == 'p'):
				total_value[0].append(1) # add 1 for every pawn exists
			elif(type_of_occupant == 'n'):
				total_value[1].append(1) # add 1 for every knight exists
			elif(type_of_occupant == 'b'):
				total_value[2].append(1) # add 1 for every bishop exists
			elif(type_of_occupant == 'r'):
				total_value[3].append(1) # add 1 for every rook exists
			elif(type_of_occupant == 'q'):
				total_value[4].append(1) # add 1 for every queen exists	
			
			material_value = material_value + value[type_of_occupant] # total material value according to values
			
	return ([total_value, material_value])	
			


def compare_material_values(cur_board): # compare material values as white - black. Total material value and as individuals. Differences in every color
	[white_total_value, white_material_value] = material_values(cur_board, 1)
	[black_total_value, black_material_value] = material_values(cur_board, 2)
	
	total_value_difference = []
	material_value_difference = white_material_value - black_material_value # white - black value
	
	for i in range(5): # check all elements of every list to see if equal value comes from example rook for knight and 2 pawns exchange
		total_value_difference.append(len(white_total_value[i]) - len(black_total_value[i])) # white - black, if negative then black has more than white
		
	return([total_value_difference, material_value_difference])	
	
				

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
	
	attr1 = [white_doubled, black_doubled] # info about doubled/connected rooks
	attr2 = [white_open_files, black_open_files]
	
	return([white_piece_value/6, black_piece_value/6], attr1, attr2)





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

	return([white_piece_value/2, black_piece_value/2])
	
	



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
	


def materials_difference(cur_board, fut_board):
		
	[cur_material_dif, cur_gen_dif] = compare_material_values(cur_board) # White - Black values in current board
	[fut_material_dif, fut_gen_dif] = compare_material_values(fut_board) # White - Black values in future board
	
	material_dif = [i - j for i, j in zip(fut_material_dif, cur_material_dif)] # calculate element wise the difference. Example if in future board difference is positive meaning white win material and in current difference is zero then white is probably targetting something or making an attack.
	gen_dif = fut_gen_dif - cur_gen_dif
	return (material_dif, gen_dif)
	
	
	
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
	
		
	
	
	
def commentator(cur_board, moves_so_far):	
	board = cur_board.copy()
	result = ''
	future_board, best_move = engines_pred(4,moves_so_far, board)
	if(str(best_move) != 'Checkmate!'):# if nobody has won
	
		
		################################ ENGINE PREDICTIONS #####################################
		
		result += 'Best move: ' + str(best_move) + '\n'
		################################ CENTER CONTROL #########################################
		[pawns, pieces] = centre_control(future_board, 1)
		################################ KING SAFETY ############################################
		result += ('Castling results in form [white, black], (kingside, queenside): ' + str(castle_white) + str(castle_black) + '\n')
		###################################### MATERIALS ########################################
		
		######################################## PAWNS ##########################################
		[islands, passed_pawns, backward_pawns] = count_pawn_islands(future_board, 2)
		passed_pawns_conf = check_for_passed_pawn(future_board, 2, passed_pawns)
		
		backward_pawn_confirmed = check_for_backwards_pawn(future_board, 2, backward_pawns)
		
		doubled_pawns = multi_pawn_file(future_board, 1, 2)
		
		[square_controlling_dif, length_of_dif] = blocking_pawn_finder(future_board, 1)
		
		################################# DEVELOPMENT ##########################################
		############################# CHECK DIFFERENCES ########################################
		[center_control_dif, [center_pawns_dif, center_pieces_dif]] = center_control_difference(board, future_board)
		result += ('White and Black center control difference: ' + str(center_control_dif) + '\n')
		result += ('White and Black center pawns difference: ' + str(center_pawns_dif) + '\n')
		result += ('White and Black center pieces difference: ' + str(center_pieces_dif) + '\n')
	
		[king_safety_dif, [king_attacking_score_dif, king_pawn_struct_dif, king_free_square_dif]] = king_safety_difference(board, future_board)
		result += ('White and Black kings safety difference: ' + str(king_safety_dif) + '\n')
		result += ('White and Black kings attacking score difference: '+ str(king_attacking_score_dif) + '\n')
		result += ('White and Black pawns structure in front of king difference: ' + str(king_pawn_struct_dif) + '\n')
		result += ('White and Black kings free squares to move difference: ' + str(king_free_square_dif) + '\n')
	
		materialistic_power_dif = materials_difference(board, future_board) 
		result += ('Difference(future - now) of the materialistic difference White - Black: '+ str(materialistic_power_dif) + '\n')
	
		[pawn_islands_dif, passed_pawns_dif, backward_pawns_dif, doubled_pawns_dif, pawns_blocking_dif, pawn_struct_power_dif] = pawns_difference(board, future_board)
		result+=('White and Black pawn structure power difference: ' + str(pawn_struct_power_dif) + '\n')
		result+=('White and Black pawn islands difference: ' + str(pawn_islands_dif) + '\n')
		result+=('White and Black passed pawn difference: ' + str(passed_pawns_dif) + '\n')
		result+=('White and Black backward pawn difference: ' + str(backward_pawns_dif) + '\n')
		result+=('White and Black doubled pawn difference: ' + str(doubled_pawns_dif) + '\n')
		result+=('White and Black pawns blocking pieces value difference(the more negative the better it is): ' + str(pawns_blocking_dif) + '\n')
	
	
		dif_calc = lambda a, b: [i-j for i,j in zip(a,b)] # calculate elementwise difference of two lists
	
		[queen_power_now, queen_central_now] = queen_compare(board)
		[queen_power, queen_central] = queen_compare(future_board)
		queen_power_dif = dif_calc(queen_power, queen_power_now)
		queen_central_dif = dif_calc(queen_central, queen_central_now)
		result+=('White and Black queen power difference: ' + str(queen_power_dif) + '\n')
		result+=('White and Black queen being on central square difference: ' + str(queen_central_dif) + '\n')
	
	
		[rook_power_now, rook_doubled_now, rook_open_files_now] = rook_compare(board)
		[rook_power, rook_doubled, rook_open_files] = rook_compare(future_board)
		rook_power_dif = dif_calc(rook_power, rook_power_now)
		rook_doubled_dif = dif_calc(rook_doubled, rook_doubled_now)
		rook_open_files_dif = dif_calc(rook_doubled, rook_doubled_now)
		result+=('White and Black rooks power difference: ' + str(rook_power_dif) + '\n')
		result+=('White and Black doubled rooks difference: ' + str(rook_doubled_dif) + '\n')
		result+=('White and Black rooks control over open files difference: ' + str(rook_open_files_dif) + '\n')
	
	
		[knight_power_now, outposts_now, knight_central_now, knight_almost_central_now] = knight_compare(board)
		[knight_power, outposts, knight_central, knight_almost_central] = knight_compare(future_board)
		knight_power_dif = dif_calc(knight_power,  knight_power_now)
		knight_outpost_dif = dif_calc(outposts_now,  outposts)
		knight_central_dif = dif_calc(knight_central, knight_central_now)
		knight_almost_central_dif = dif_calc(knight_almost_central, knight_almost_central_now)
		result+=('White and Black knights power difference: ' + str(knight_power_dif) + '\n')
		result+=('White and Black knights outposts difference: ' + str(knight_outpost_dif) + '\n')
		result+=('White and Black knights number of central knights difference: ' + str(knight_central_dif) + '\n')
		result+=('White and Black knights number of almost central knights difference: ' + str(knight_almost_central_dif) + '\n')
	
	
		bishop_power_dif = dif_calc(bishop_compare(future_board), bishop_compare(board))
		result+=('White and Black bishops power difference: ' + str(bishop_power_dif) + '\n')
	
		############################# COMMENTATOR ################################################
		result+=('Commentator says:' + '\n')
		who_plays = 1
		if(not board.turn): # if turn is BLACK then previous WHITE played so comment for that side
			who_plays = 0 
	
		if(materialistic_power_dif[1] == 0.25):
			result+=('Win bishop over knight.')
		
		if(center_control_dif[who_plays] > 0):
			result+=('Wanting to improve center control, and in future develop in center' + str(center_pawns_dif[who_plays]) + 'pawns and' + str(center_pieces_dif[who_plays]) + 'pieces.' + '\n')
			
		if(king_safety_dif[who_plays] > 0):
	 		result+=('Wanting to improve kings safety by:')
	 		if(king_attacking_score_dif[who_plays] < 0):
	 			result+=('avoid incoming attack and hide king,')
	 		if(king_pawn_struct_dif[who_plays] > 0):
	 			result+=('strengthen kings pawn structure,')
	 		if(king_free_square_dif[who_plays] >0):
	 			result+=('create more free squares for the king')
	 		result+='.'
	 			
		if(pawn_struct_power_dif[who_plays] > 0):
	 		result+=('Wanting to improve pawn structure by:')
	 		if(pawn_islands_dif[who_plays] < 0):
	 			result+=('connecting pawn islands,')
	 		if(passed_pawns_dif[who_plays] > 0):
	 			result+=('creating passed pawn,')
	 		if(backward_pawns_dif[who_plays] < 0):
	 			result+=('reducing backward weaknesses,')
	 		if(doubled_pawns_dif[who_plays] < 0):
	 			result+=('undouble pawns,')
	 		if(pawns_blocking_dif[who_plays] < 0):
	 			result+=('less blocking pieces with pawns')
	 		result+=('.')	
		 			
		dev_maxer = max(queen_power_dif[who_plays], rook_power_dif[who_plays], knight_power_dif[who_plays], bishop_power_dif[who_plays]) # find main piece that is going to be developed in future
		if(dev_maxer == queen_power_dif[who_plays]):
	 		result+=('Queen is going to be developed/improved')
	 		if(queen_central_dif[who_plays] > 0):
	 			result+=('in central square')
		if(dev_maxer == rook_power_dif[who_plays]):
	 		result+=('Rook is going to be developed/improved')
	 		if(rook_doubled_dif[who_plays] > 0):
	 			result+=('with doubled rooks')
	 		if(rook_open_files_dif[who_plays] > 0):
	 			result+=('with rooks occupying open file')	
		if(dev_maxer == knight_power_dif[who_plays]):
	 		result+=('Knight is going to be developed/improved')
	 		if(knight_outpost_dif[who_plays] > 0):
	 			result+=('in an outpost (Great advantage)')
	 		if(knight_central_dif[who_plays] > 0):
	 			result+=('on a central square')
	 		if(knight_almost_central_dif[who_plays] > 0):
	 			result+=('on an almost central square')
		if(dev_maxer == bishop_power_dif[who_plays]):
	 		result+=('Bishop is going to be developed on a better square/diagonal')
		result+=('.')	
	
	else:
		result = 'Checkmate!'	
	return(result)
	
	
				
