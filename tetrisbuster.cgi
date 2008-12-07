#!/home/superjoe/python/bin/python

import cgi

pieces = {
		'i':[ [ [True, False, False, False],[True, False, False, False],[True, False, False, False],[True, False, False, False] ], [  [True, True, True, True],[False, False, False, False],[False, False, False, False],[False, False, False, False] ], [ [True, False, False, False],[True, False, False, False],[True, False, False, False],[True, False, False, False] ], [ [True, True, True, True],[False, False, False, False],[False, False, False, False],[False, False, False, False] ] ],
		'j':[ [ [False, True, False, False],[False, True, False, False],[True, True, False, False],[False, False, False, False] ], [ [True, False, False, False],[True, True, True, False],[False, False, False, False],[False, False, False, False] ], [ [True, True, False, False],[True, False, False, False],[True, False, False, False],[False, False, False, False] ], [ [True, True, True, False],[False, False, True, False],[False, False, False, False],[False, False, False, False] ] ],
		'l':[ [ [True, False, False, False],[True, False, False, False],[True, True, False, False],[False, False, False, False] ], [ [True, True, True, False],[True, False, False, False],[False, False, False, False],[False, False, False, False] ], [ [True, True, False, False],[False, True, False, False],[False, True, False, False],[False, False, False, False] ], [ [False, False, True, False],[True, True, True, False],[False, False, False, False],[False, False, False, False] ] ],
		'o':[ [ [True, True, False, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ], [  [True, True, False, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ], [  [True, True, False, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ], [  [True, True, False, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ] ],
		's':[ [ [False, True, True, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ], [  [True, False, False, False],[True, True, False, False],[False, True, False, False],[False, False, False, False] ], [ [False, True, True, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ], [ [True, False, False, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ] ],
		't':[ [ [True, True, True, False],[False, True, False, False],[False, False, False, False],[False, False, False, False] ], [ [False, True, False, False],[True, True, False, False],[False, True, False, False],[False, False, False, False] ], [ [False, True, False, False],[True, True, True, False],[False, False, False, False],[False, False, False, False] ], [ [True, False, False, False],[True, True, False, False],[True, False, False, False],[False, False, False, False] ], ],
		'z':[ [ [True, True, False, False],[False, True, True, False],[False, False, False, False],[False, False, False, False] ], [ [False, True, False, False],[True, True, False, False],[True, False, False, False],[False, False, False, False] ], [ [True, True, False, False],[False, True, True, False],[False, False, False, False],[False, False, False, False] ], [ [False, True, False, False],[True, True, False, False],[True, False, False, False],[False, False, False, False] ], ],
	}



print "Content-Type: text/plain\n"

board_height = 20
board_width = 10

def canPutPiece(board, piece, left, top, rot):
	new_board = board[:]
	#print "canputpiece: board:"
	#print board
	#print "checking piece %s: %s" % (piece, pieces[piece][rot])
	
	for y in range(4):
		for x in range(4):
			bx = left+x
			by = top+y
			
			
			if pieces[piece][rot][y][x]:
				if by >= board_height or bx >= board_width or \
				bx < 0 or by < 0 or board[by][bx] != '.':
					reason = "something funny is going on..."
					if by >= board_height:
						reason = "y >= board_height"
					elif bx >= board_width:
						reason = "x >= board_width"
					elif bx < 0:
						reason = "x < 0"
					elif by < 0:
						reason = "y < 0"
					elif board[by][bx] != '.':
						reason = "board[by][bx] = %s" % board[by][bx]
					
					#print "can't put %s at (%i, %i) with rotation %i because %s" % (piece, bx, by, rot * 90, reason)
					return (board, False,) # illegal move
				else:
					row = list(new_board[by])
					row[bx] = piece
					new_board[by] = ''.join(row)
	#print "canputpiece: yes. returning board:"
	#print new_board
	return (new_board, True,) # legal move

def doMove(board, piece, position, rot):
	# put piece at top of board
	y = 0
		
	# move piece down until we can't anymore
	new_board = board[:]
	while True:
		old_board = new_board[:]
		#print "trying %s at (%i, %i) with rotation %i" % (piece, position,y, rot*90)
		new_board, legal = canPutPiece(board, piece, position, y, rot)
		if not legal:
			#print "can't put %s at (%i, %i) with rotation %i" % (piece, position, y, rot*90)
			break
		
		y += 1
	
	# delete complete rows
	new_board = filter(lambda row: any(item != '.' for item in row), new_board)
	for i in range(board_height-len(new_board)):
		new_board.insert(0, '.' * board_width)
	
	
	if y == 0:
		# cannot place piece; return illegal move
		#print "can't put %s at %i with rotation %i" % (piece, position, rot*90)
		return (board, False,)
	else:
		# put the changes into board
		return (old_board, True,) # 'True' - move is legal

def boardHeight(board):
	# count nonzero rows up from the bottom
	count = 0
	for row in board:
		if any( item != '.' for item in row):
			break;
		count += 1
	
	return board_height - count

form = cgi.FieldStorage()
if form.has_key("piece") and form.has_key("board"):
	board = form['board'].value.decode("utf-8").encode("ascii", "ignore").split()
	piece = form['piece'].value.decode("utf-8").encode("ascii", "ignore")

	#print "initial board:"
	#print board
	# try every combination and compute a score for that combo.
	combos = {}
	for x in range(board_width):
		for rot in range(4):
			#print "trying position %i, %i degrees" % (x, rot*90)
			new_board, legal = doMove(board, piece, x, rot)
			if legal:
				# determine how many points this board is worth
				# negative score for each block, blocks toward the bottom
				# don't hurt as much
				pts = 0
				for by in range(board_height):
					pts += sum(-10*(board_height-by) for char in new_board[by] if char != ".")
				#print "position %i, rotation %i is %i points" % (x, rot*90, pts)
				#print "height: %i" % h
				combos[pts] = [x, rot]
			#else:
				#print "not legal"
	
	# best combo is lowest key
	keys = combos.keys()
	keys.sort(reverse=True)
	open('lastrun.txt', 'a').write("\n---------------------\nboard: %s\npiece: %s\n combos: %s" % (board, piece, combos))
	
	if len(keys) == 0:
		# random, we're about to lose
		position = 0
		degrees = 0
	else:
		position = combos[keys[0]][0]
		degrees = combos[keys[0]][1] * 90
	
	print "position=%i&degrees=%i" % (position, degrees )
else:
	print "invalid input"

