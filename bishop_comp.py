import chess
from general_comp import *



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

