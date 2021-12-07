
import numpy as np
import random
import time

def NextMove(grid, step):

	#move_list = ['up', 'down', 'left', 'right']

	#number of moves to go down in the monte carlow thing
	search_length = 50
	search_depth = 10

	# numpy arrays are easier to work with
	grid_np = np.asarray(grid)
	#print(grid_np)

	# tap out if too far ahead
	if(findMax(grid_np) >= 2000):
		return 4

	# list holding first move scores
	#first_moves = [0, 1, 2, 3]
	scores = np.zeros(4)
	num_moves = np.zeros(4)

	# loop each possible first move
	for i in range(4):

		first_board, first_score, first_valid = make_move(grid_np, i)
		
		if first_valid:
			first_board = add_new_tile(first_board)
			scores[i] = first_score * search_length
			#print('Inital move: ', i, 'score: ', scores[i])
		
		else:
			#print('Inital move: ', i, ' is invalid')
			continue


		for later_moves in range(search_length):
			move_number = 1
			search_board = np.copy(first_board)
			is_valid = True

			while (not game_over(search_board)) and move_number <= search_depth:

				# true random
				move_direction = random.randint(0, 3)

				# add some human strategy
				#move_direction = random.choice([0, 0, 0, 0, 1, 2, 2, 3])


				#print('direction chosen: ', move_direction)
				search_board, score, is_valid = make_move(search_board, move_direction)					

				if is_valid:
					search_board = add_new_tile(search_board) 
					scores[i] += score
					num_moves[i] += 1

					#print('depth: ', move_number)
					#print('move: ', move_list[move_direction])
					#print(search_board)
					#print('score: ', score)
					#print('totals: ', scores)

					move_number += 1

	# add some human intuition
	#scores[0] = scores[0] * 2
	#scores[2] = scores[2] * 1.5
	#print("move scores: ", scores)
	best_move = np.argmax(scores)
	
	return best_move

def move_and_tile(grid, move):
	grid, score, valid = make_move(grid, move)
	
	continue_game = False

	if(not game_over(grid)):
		grid = add_new_tile(grid)
		continue_game = True
	#print ('end move_and_tile')
	return grid, continue_game

def make_move(input_grid, move):
	#print("start of move:")
	#print(grid)

	grid = input_grid

	score = 0

	# up
	if move == 0:
		grid = transpose(grid)
		grid = stack(grid)
		grid, score = combine(grid)
		grid = stack(grid)
		grid = transpose(grid)


	# down
	if move == 1:
		grid = transpose(grid)
		grid = reverse(grid)
		grid = stack(grid)
		grid, score = combine(grid)
		grid = stack(grid)
		grid = reverse(grid)
		grid = transpose(grid)

	# left
	if move == 2:
		grid = stack(grid)
		grid, score = combine(grid)
		grid = stack(grid)

	# right
	if move == 3:
		grid = reverse(grid)
		grid = stack(grid)
		grid, score = combine(grid)
		grid = stack(grid)
		grid = reverse(grid)

	valid = not np.array_equal(grid, input_grid)

	return grid, score, valid

def stack(grid):
	#print('stack')
	#print(grid)
	new_matrix = [[0]*4 for _ in range(4)]
	for i in range(4):
		fill_position = 0
		for j in range(4):
			if grid[i][j] != 0:
				new_matrix[i][fill_position] = grid[i][j]
				fill_position += 1
	return np.asarray(new_matrix)

def combine(grid):
	#print('combine')
	#print(grid)
	score = 0
	for i in range(4):
		for j in range(3):
			if grid[i][j] != 0 and grid[i][j] == grid[i][j+1]:
				grid[i][j] *= 2
				grid[i][j+1] = 0
				score += grid[i][j]
	return np.asarray(grid), score

def reverse(grid):
	#print('reverse')
	#print(grid)
	return np.flip(grid, 1)

def transpose(grid):
	#print('transpose')
	#print(grid)
	return np.transpose(grid)


def add_new_tile(grid):
	row = random.randint(0, 3)
	col = random.randint(0, 3)

	#print(row, col)
	#print(grid[row][col])

	while(grid[row][col] != 0):
		row = random.randint(0, 3)
		col = random.randint(0, 3)
		#print(row, col)
		#print(grid[row][col])

	#print('found open slot')
	num = 2
	if random.randint(0, 9) == 9:
		num = 4

	grid[row][col] = num

	return grid

def h_move_exists(grid):
	for i in range(4):
		for j in range(3):
			if grid[i][j] == grid[i][j+1]:
				return True
	return False

def v_move_exists(grid):
	for i in range(3):
		for j in range(4):
			if grid[i][j] == grid[i+1][j]:
				return True
	return False


def game_over(grid):
	return ((not any(0 in row for row in grid)) and (not h_move_exists(grid)) and (not v_move_exists(grid)))


def findMax(grid):
	return np.amax(grid)

t0 = time.time()

test_grid1 = [[0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 2, 0], [0, 0, 0, 0]]
test_grid2 = [[0, 4, 8, 4], [4, 32, 8, 2], [4, 32, 4, 8], [2, 8, 4, 2]]

move_list = ['up', 'down', 'left', 'right']

test_grid = test_grid1

print(np.asarray(test_grid))

# single weird move test
#weird_move = NextMove(test_grid, 0)

#print(test_grid)

for i in range(10000):
	
	ai_move = NextMove(test_grid, i)

	#print('Move:', i, '   direction: ', move_list[ai_move])

	temp_grid, continue_game = move_and_tile(test_grid, ai_move)
	test_grid = temp_grid.tolist()

	if i % 100 == 0:
		print(np.asarray(test_grid))
	
	if not continue_game:
		 break

print(np.asarray(test_grid))

t1 = time.time()
total = t1-t0

print('time elapsed: ', total)
