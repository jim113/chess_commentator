from pystockfish import *
import chess

deep = Engine(depth=15)
castle_white = [False, False] # set the castling flags to false for both sides, [kingside, queenside]
castle_black = [False, False]


def find_castling_choice(cur_board, move):
	[kingside, queenside] = [cur_board.is_kingside_castling(move), cur_board.is_queenside_castling(move)]
	return ([int(kingside), int(queenside)]) # return tuple of castling choices,if done, 1 for chosed side 0 for the other
	
	
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

