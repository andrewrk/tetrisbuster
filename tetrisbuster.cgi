#!/home/superjoe/python/bin/python

import cgi

pieces = {
		'i':[ [ [True, False, False, False],[True, False, False, False],[True, False, False, False],[True, False, False, False] ], [  [True, True, True, True],[False, False, False, False],[False, False, False, False],[False, False, False, False] ], [ [True, False, False, False],[True, False, False, False],[True, False, False, False],[True, False, False, False] ], [ [True, True, True, True],[False, False, False, False],[False, False, False, False],[False, False, False, False] ] ],
		'j':[ [ [False, True, False, False],[False, True, False, False],[True, True, False, False],[False, False, False, False] ], [ [True, False, False, False],[True, True, True, False],[False, False, False, False],[False, False, False, False] ], [ [True, True, False, False],[True, False, False, False],[True, False, False, False],[False, False, False, False] ], [ [True, True, True, False],[False, False, True, False],[False, False, False, False],[False, False, False, False] ] ],
		'l':[ [ [True, False, False, False],[True, False, False, False],[True, True, False, False],[False, False, False, False] ], [ [True, True, True, False],[True, False, False, False],[False, False, False, False],[False, False, False, False] ], [ [True, True, False, False],[False, True, False, False],[False, True, False, False],[False, False, False, False] ], [ [False, False, True, False],[True, True, True, False],[False, False, False, False],[False, False, False, False] ] ],
		'o':[ [ [True, True, False, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ], [  [True, True, False, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ], [  [True, True, False, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ], [  [True, True, False, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ] ],
		's':[ [ [False, True, True, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ], [  [True, False, False, False],[True, True, False, False],[False, True, False, False],[False, False, False, False] ], [ [False, True, True, False],[True, True, False, False],[False, False, False, False],[False, False, False, False] ], [ [True, False, False, False],[True, True, False, False],[False, True, False, False],[False, False, False, False] ] ],
		't':[ [ [True, True, True, False],[False, True, False, False],[False, False, False, False],[False, False, False, False] ], [ [False, True, False, False],[True, True, False, False],[False, True, False, False],[False, False, False, False] ], [ [False, True, False, False],[True, True, True, False],[False, False, False, False],[False, False, False, False] ], [ [True, False, False, False],[True, True, False, False],[True, False, False, False],[False, False, False, False] ], ],
		'z':[ [ [True, True, False, False],[False, True, True, False],[False, False, False, False],[False, False, False, False] ], [ [False, True, False, False],[True, True, False, False],[True, False, False, False],[False, False, False, False] ], [ [True, True, False, False],[False, True, True, False],[False, False, False, False],[False, False, False, False] ], [ [False, True, False, False],[True, True, False, False],[True, False, False, False],[False, False, False, False] ], ],
	}



print "Content-Type: text/plain\n"

board_height = 20
board_width = 10

def canPutPiece(board, piece, left, top, rot):
	new_board = board[:]
	
	for y in range(4):
		for x in range(4):
			bx = left+x
			by = top+y
			
			
			if pieces[piece][rot][y][x]:
				if by >= board_height or bx >= board_width or \
				bx < 0 or by < 0 or board[by][bx] != '.':
					return (board, False,) # illegal move
				else:
					row = list(new_board[by])
					row[bx] = piece
					new_board[by] = ''.join(row)

	return (new_board, True,) # legal move

def doMove(board, piece, position, rot):
	# put piece at top of board
	y = 0
		
	# move piece down until we can't anymore
	new_board = board[:]
	while True:
		ret_board = new_board[:]
		new_board, legal = canPutPiece(board, piece, position, y, rot)
		if not legal:
			break
		
		y += 1
	
	# delete complete rows
	ret_board = filter(lambda row: any(item == '.' for item in row), ret_board)
	for i in range(board_height-len(ret_board)):
		ret_board.insert(0, '.' * board_width)
	
	
	if y == 0:
		# cannot place piece; return illegal move
		return (board, False,)
	else:
		# put the changes into board
		return (ret_board, True,) # 'True' - move is legal

form = cgi.FieldStorage()
if form.has_key("piece") and form.has_key("board"):
	board = form['board'].value.decode("utf-8").encode("ascii", "ignore").split()
	piece = form['piece'].value.decode("utf-8").encode("ascii", "ignore")

	outstr = ""

	# try every combination and compute a score for that combo.
	combos = {}
	for x in range(board_width):
		for rot in range(4):
			new_board, legal = doMove(board, piece, x, rot)
			if legal:
				# determine how many points this board is worth
				pts = 0
				for by in range(board_height):
					# negative score for each block, blocks toward the bottom
					# don't hurt as much
					pts += sum(-10*(board_height-by) for char in new_board[by] if char != ".")
					# find holes and give them a penalty
					for bx in range(board_width):
						if new_board[by][bx] == '.':
							# see if there is a block anywhere above it
							for check_y in range(by):
								if new_board[check_y][bx] != ".":
									pts -= 50 * (board_height-check_y)
									break

				combos[pts] = [x, rot]
	
	# best combo is lowest key
	keys = combos.keys()
	keys.sort(reverse=True)

	# log
	if len(keys) > 0:
		new_board, legal = doMove(board, piece, combos[keys[0]][0],  combos[keys[0]][1])
		outstr += "\nexpected board:\n%s" % '\n'.join(new_board)
	open('lastrun.txt', 'a').write("\n---------------------\nboard:\n%s\npiece: %s\n combos: %s\noutstr: %s\n" % ('\n'.join(board), piece, combos, outstr))
	
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

