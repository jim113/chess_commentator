import chess

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
		if(pawns_in_file == number): # if there are number pawns of the given color on that file then add it to resutl
			pawn_files.append(files)
	
	print(pawn_files)
		
b = chess.Board()
#print(b)
#b.push_san(b.san(chess.Move.from_uci('e2e4')))
#b.push_san(b.san(chess.Move.from_uci('e7e5')))
#b.push_san(b.san(chess.Move.from_uci('c2c4')))
b.set_piece_at(32, chess.Piece(1,0)) # pawn
b.set_piece_at(42, chess.Piece(1,1))
b.set_piece_at(38, chess.Piece(1,1))
b.set_piece_at(28, chess.Piece(1,1))
b.set_piece_at(44, chess.Piece(1,1))

#b.remove_piece_at(8)
#b.remove_piece_at(10)
#b.remove_piece_at(12)
#b.remove_piece_at(14)
print(b)
multi_pawn_file(b, 2,2)
