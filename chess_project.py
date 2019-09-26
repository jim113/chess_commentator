from pystockfish import *
import chess
from predictor import *
from center_control import *
from king_safety import *
from materials import *
from pawn_strength import *
from queen_comp import *
from rook_comp import *
from knight_comp import *
from bishop_comp import *	
	
	
	
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
			result+=('Wanting to improve center control, and in future develop in center ' + str(center_pawns_dif[who_plays]) + ' pawns and ' + str(center_pieces_dif[who_plays]) + ' pieces.' + '\n')
			
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
	
	
				
