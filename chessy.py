import PySimpleGUI as sg
import os
import chess
import chess.pgn
import copy
import time
import chess_project

button_names = ('close', 'cookbook', 'cpu', 'github', 'pysimplegui', 'run', 'storage', 'timer')

CHESS_PATH = '/home/jim/chess_commentator/images'        # path to the chess pieces

BLANK = 0               # piece names
PAWNB = 1
KNIGHTB = 2
BISHOPB = 3
ROOKB = 4
KINGB = 5
QUEENB = 6
PAWNW = 7
KNIGHTW = 8
BISHOPW = 9
ROOKW = 10
KINGW = 11
QUEENW = 12

initial_board = [[ROOKB, KNIGHTB,  BISHOPB, KINGB, QUEENB, BISHOPB, KNIGHTB, ROOKB ],
              [PAWNB,]*8,
              [BLANK,]*8,
              [BLANK,]*8,
              [BLANK,]*8,
              [BLANK,]*8,
              [PAWNW,]*8,
              [ROOKW, KNIGHTW, BISHOPW, KINGW, QUEENW, BISHOPW, KNIGHTW, ROOKW]]

blank = os.path.join(CHESS_PATH, 'blank.png')
bishopB = os.path.join(CHESS_PATH, 'bishopb.png')
bishopW = os.path.join(CHESS_PATH, 'bishopw.png')
pawnB = os.path.join(CHESS_PATH, 'pawnb.png')
pawnW = os.path.join(CHESS_PATH, 'pawnw.png')
knightB = os.path.join(CHESS_PATH, 'knightb.png')
knightW = os.path.join(CHESS_PATH, 'knightw.png')
rookB = os.path.join(CHESS_PATH, 'rookb.png')
rookW = os.path.join(CHESS_PATH, 'rookw.png')
queenB = os.path.join(CHESS_PATH, 'queenb.png')
queenW = os.path.join(CHESS_PATH, 'queenw.png')
kingB = os.path.join(CHESS_PATH, 'kingb.png')
kingW = os.path.join(CHESS_PATH, 'kingw.png')

images = {BISHOPB: bishopB, BISHOPW: bishopW, PAWNB: pawnB, PAWNW: pawnW, KNIGHTB: knightB, KNIGHTW: knightW,
        ROOKB: rookB, ROOKW: rookW, KINGB: kingB, KINGW: kingW, QUEENB: queenB, QUEENW: queenW, BLANK: blank}

def open_pgn_file(filename):
  pgn = open(filename)
  first_game = chess.pgn.read_game(pgn)
  moves = [move for move in first_game.main_line()]
  return moves

def render_square(image, key, location):
  if (location[0] + location[1]) % 2:
      color =  '#B58863'
  else:
      color = '#F0D9B5'
  return sg.RButton('', image_filename=image, size=(1, 1), button_color=('white', color), pad=(0, 0), key=key)

def redraw_board(window, board):
  for i in range(8):
      for j in range(8):
          color = '#B58863' if (i+j) % 2 else '#F0D9B5'
          piece_image = images[board[i][j]]
          elem = window.FindElement(key=(i,j))
          elem.Update(button_color = ('white', color),
                      image_filename=piece_image,)

def PlayGame():

  menu_def = [['&File', ['&Open PGN File', 'E&xit' ]],
              ['&Help', '&About...'],]

  # sg.SetOptions(margins=(0,0))
  sg.ChangeLookAndFeel('GreenTan')
  # create initial board setup
  board = copy.deepcopy(initial_board)
  # the main board display layout
  board_layout = [[sg.T('     ')] + [sg.T('{}'.format(a), pad=((23,27),0), font='Any 13') for a in 'abcdefgh']]
  # loop though board and create buttons with images
  for i in range(8):
      row = [sg.T(str(8-i)+'   ', font='Any 13')]
      for j in range(8):
          piece_image = images[board[i][j]]
          row.append(render_square(piece_image, key=(i,j), location=(i,j)))
      row.append(sg.T(str(8-i)+'   ', font='Any 13'))
      board_layout.append(row)
  # add the labels across bottom of board
  board_layout.append([sg.T('     ')] + [sg.T('{}'.format(a), pad=((23,27),0), font='Any 13') for a in 'abcdefgh'])

  # setup the controls on the right side of screen
  
  board_controls = [[sg.RButton('New Game'), sg.RButton('Draw')],
                    [sg.RButton('Resign Game')],
                    [sg.Text('Move List')],
                    [sg.Multiline([], do_not_clear=False, autoscroll=True, size=(15,5),key='_movelist_')],
                    [sg.Text('Comments')],
                    [sg.Multiline([], do_not_clear=False, autoscroll=True, size=(85,20),key='_comments_')]]


  board_tab = [[sg.Column(board_layout)]]

  # the main window layout
  layout = [[sg.Menu(menu_def, tearoff=False)],
            [sg.TabGroup([[sg.Tab('Board',board_tab)]], title_color='red'),
             sg.Column(board_controls)],
            [sg.Text('Click anywhere on board for next move', font='_ 14')]]

  window = sg.Window('Chess', default_button_element_size=(12,1), auto_size_buttons=False, icon=CHESS_PATH + 'kingb.ico').Layout(layout)

  # ---===--- Loop taking in user input --- #
  i = 0
  moves = None
  tmp_board = chess.Board()
  cur_board = chess.Board()
  all_moves = []
  while True:
      button, value = window.Read()
      
      if button in (None, 'Exit'):
          break
      if button == 'Open PGN File':
          filename = sg.PopupGetFile('', no_window=True)
          if filename is not None:
              moves = open_pgn_file(filename)
              i = 0
              board = copy.deepcopy(initial_board)
              window.FindElement('_movelist_').Update(value='')
      if button == 'About...':
          sg.Popup('Created by Dimitrios K. Kelesis','Powerd by Engine Kibitz Chess Engine')
      
      replacer = {1: 'a', 2: 'b', 3:'c', 4:'d', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
      col_replacer = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
      
      if type(button) is tuple:
          #print(button[0], replacer[button[1]+1], button)
          move_from = str(replacer[button[1]+1]) + str(col_replacer[button[0]])
          button1, value = window.Read()
          move_to = str(replacer[button1[1]+1]) + str(col_replacer[button1[0]])
          move = move_from + move_to
          
          all_moves.append(str(move))
          if (cur_board.is_kingside_castling(chess.Move.from_uci(str(move)))):
          	if (cur_board.turn):
          		board[7][7] = BLANK # make the castle
          		board[7][5] = ROOKW
          	else:
          		board[0][7] = BLANK
          		board[0][5] = ROOKB 
          		
          if (cur_board.is_queenside_castling(chess.Move.from_uci(str(move)))):
          	if (cur_board.turn):
          		board[7][0] = BLANK
          		board[7][3] = ROOKW
          	else:
          		board[0][0] = BLANK
          		board[0][3] = ROOKB          	
          
          
          cur_board.push_san(cur_board.san(chess.Move.from_uci(str(move))))
          	
          moves1 = ( tmp_board.variation_san([chess.Move.from_uci(m) for m in all_moves]) )
          for jj in range(len(moves1)):
          	if (moves1[jj] == '.' and moves1[jj-1] != '1'):
          		mm = list(moves1)
          		mm[jj-2] = '\n'
          		moves1 = ''.join(mm)
          #print(moves1)
          window.FindElement('_movelist_').Update(value=moves1, append=True)
          window.FindElement('_comments_').Update(value = chess_project.commentator(cur_board, all_moves), append = True)
          row, col = button[0], button[1]
          piece = board[row][col]         # get the move-from piece
          button = window.FindElement(key=(row,col))
          for x in range(3):
              button.Update(button_color = ('white' , 'red' if x % 2 else 'white'))
              window.Refresh()
              time.sleep(.05)
          board[row][col] = BLANK         # place blank where piece was
          row, col = button1[0], button1[1]  # compute move-to square
          board[row][col] = piece         # place piece in the move-to square
          redraw_board(window, board)
          i += 1
          if(cur_board.is_checkmate() == True):
          	sg.Popup('Check Mate! Game over!')

PlayGame()
