import pygame
from queue import PriorityQueue, Queue
from constants import *

WIN = pygame.display.set_mode((WIDTH, WIDTH))

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == BLUE

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == RED

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = BLUE

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = RED

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def draw_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()
	
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

"""
A star search implementation
"""
def algorithm1(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))		# f_score of start is zero
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			for spot in open_set_hash:
				spot.make_closed()
			draw_path(came_from, end, draw)
			end.make_end()
			start.make_start()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def astar(win, width):
	grid = make_grid(ROWS, width)

	start = None
	end = None

	running = True
	while running:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				return

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm1(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
				
				if event.key == pygame.K_ESCAPE:
					running = False
					return
	return

"""
Dijkstra's shortest path implementation
"""
def algorithm2(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))		# distance from start is 0
	came_from = {}
	weight = {spot: float("inf") for row in grid for spot in row}
	weight[start] = 0

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			for spot in open_set_hash:
				spot.make_closed()
			draw_path(came_from, end, draw)
			end.make_end()
			start.make_start()
			return True

		for neighbor in current.neighbors:
			if weight[neighbor] > weight[current] + h(current.get_pos(), neighbor.get_pos()):
				weight[neighbor] = weight[current] + h(current.get_pos(), neighbor.get_pos())
				came_from[neighbor] = current
				count += 1
				open_set.put((weight[neighbor], count, neighbor))
				open_set_hash.add(neighbor)
				neighbor.make_open()
			
		draw()

		if current != start:
			current.make_closed()

	return False

def dijkstras(win, width):
	grid = make_grid(ROWS, width)

	start = None
	end = None

	running = True
	while running:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				return

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm2(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
				
				if event.key == pygame.K_ESCAPE:
					running = False
					return
	return

"""
BFS implementation
"""
def algorithm3(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))		# distance from start is 0
	came_from = {}
	weight = {spot: float("inf") for row in grid for spot in row}
	weight[start] = 0

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		current = open_set.get()[2]
		if current == end:
			for spot in open_set_hash:
				spot.make_closed()
			draw_path(came_from, end, draw)
			end.make_end()
			start.make_start()
			return True

		for neighbor in current.neighbors:
			if neighbor not in open_set_hash:
				weight[neighbor] = weight[current] + 1
				came_from[neighbor] = current
				count += 1
				open_set.put((weight[neighbor], count, neighbor))
				open_set_hash.add(neighbor)
				neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def bfs(win, width):
	grid = make_grid(ROWS, width)

	start = None
	end = None

	running = True
	while running:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				return

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm3(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
				
				if event.key == pygame.K_ESCAPE:
					running = False
					return
	return

"""
Bidirectional search implementation
"""
def algorithm4(draw, grid, start, end):
	count = 0
	open_set_f = PriorityQueue()
	open_set_b = PriorityQueue()
	open_set_f.put((0, count, start))		# distance from start is 0
	open_set_b.put((0, count, end))			# distance from end is 0
	came_from_f = {}
	came_from_b = {}
	weight = {spot: float("inf") for row in grid for spot in row}
	weight[start] = 0
	weight[end] = 0

	open_set_hash_f = {start}
	open_set_hash_b = {end}

	while not open_set_f.empty() and not open_set_b.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			
		# forward bfs
		current_f = open_set_f.get()[2]
		for neighbor in current_f.neighbors:
			if neighbor not in open_set_hash_f:
				weight[neighbor] = weight[current_f] + 1
				came_from_f[neighbor] = current_f
				count += 1
				open_set_f.put((weight[neighbor], count, neighbor))
				open_set_hash_f.add(neighbor)
				neighbor.make_open()
		
		# backward bfs
		current_b = open_set_b.get()[2]
		for neighbor in current_b.neighbors:
			if neighbor not in open_set_hash_b:
				weight[neighbor] = weight[current_b] + 1
				came_from_b[neighbor] = current_b
				count += 1
				open_set_b.put((weight[neighbor], count, neighbor))
				open_set_hash_b.add(neighbor)
				neighbor.make_open()

		# if intersecting
		for intersect in open_set_hash_f:
			if intersect in open_set_hash_b:
				for spot in open_set_hash_f:
					spot.make_closed()
				for spot in open_set_hash_b:
					spot.make_closed()
				draw_path(came_from_f, intersect, draw)
				draw_path(came_from_b, intersect, draw)
				intersect.make_path()
				end.make_end()
				start.make_start()
				return True

		draw()

		if current_f != start and current_f != end:
			current_f.make_closed()
		if current_b != start and current_b != end:
			current_b.make_closed()

	return False

def bidirectional(win, width):
	grid = make_grid(ROWS, width)

	start = None
	end = None

	running = True
	while running:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				return

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm4(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
				
				if event.key == pygame.K_ESCAPE:
					running = False
					return
	return

# astar(WIN, WIDTH)
# dijkstras(WIN, WIDTH)
# bfs(WIN, WIDTH)
# bidirectional(WIN, WIDTH)