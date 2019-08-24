import chess

def controlling_squares(cur_board, color):
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
		
		

def blocking_pawn_finder(cur_board, color): # for every pawn check if its square is blocking the mobility or attacking lines of friendly piece, if yes then add to list that piece. To check that we take a board and remove all pawns. Count attacked squares and then compare that number with the attacked squares with the pawns in their positions. The difference indicates how 'blockating' the pawns are.
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
	
	print (square_controlling_difference, len(square_controlling_difference))
			
		
			
		
		


b = chess.Board()
#print(b)
#b.set_piece_at(32, chess.Piece(1,0)) # pawn
#b.set_piece_at(42, chess.Piece(1,1))
#b.set_piece_at(38, chess.Piece(1,1))
#b.set_piece_at(28, chess.Piece(1,1))
#b.set_piece_at(44, chess.Piece(1,1))

#b.remove_piece_at(8)
#b.remove_piece_at(10)
#b.remove_piece_at(12)
#b.remove_piece_at(14)

b.clear_board()
b.set_piece_at(16, chess.Piece(1, 0))
b.set_piece_at(56, chess.Piece(4, 0))

print(b)
blocking_pawn_finder(b, 2)
