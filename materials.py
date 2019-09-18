import chess


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
	
	
	
def materials_difference(cur_board, fut_board):
		
	[cur_material_dif, cur_gen_dif] = compare_material_values(cur_board) # White - Black values in current board
	[fut_material_dif, fut_gen_dif] = compare_material_values(fut_board) # White - Black values in future board
	
	material_dif = [i - j for i, j in zip(fut_material_dif, cur_material_dif)] # calculate element wise the difference. Example if in future board difference is positive meaning white win material and in current difference is zero then white is probably targetting something or making an attack.
	gen_dif = fut_gen_dif - cur_gen_dif
	return (material_dif, gen_dif)
	

