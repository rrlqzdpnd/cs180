#!/usr/bin/python

from math import sqrt
import sys

class Analyzer:
	rows = 0
	columns = 0
	world = []
	source = 0
	destination = 0
	up = 0
	left = 0
	right = 0
	down = 0
	diagonal = 0

	# Initializes an object for the whole map, along with
	# its travel costs for going up, down, left, right,
	# and diagonal.
	# @params	filename	filename of input file
	def __init__(self, filename):
		try:
			file = open(filename, "r")

			# Read from file for size of map
			read = file.readline()
			rows, columns = read.split(" ")
			self.rows = int(rows)
			self.columns = int(columns)

			# Read from file the actual map
			for x in range(0,self.rows):
				read = file.readline()
				l = read.split(" ", self.columns)
				new = []
				for item in l:
					new.append(int(item))
				self.world.append(new)

			# Read from file the source coordinates
			read = file.readline()
			self.source = int(read.split(" ")[2]), int(read.split(" ")[1])

			# Read from file the destination coordinates
			read = file.readline()
			self.destination = int(read.split(" ")[2]), int(read.split(" ")[1])

			# Read from file the cost for going up
			read = file.readline()
			self.up = eval(read.split(" ")[1])

			# Read from file the cost for going down
			read = file.readline()
			self.down = eval(read.split(" ")[1])

			# Read from file the cost for going left
			read = file.readline()
			self.left = eval(read.split(" ")[1])

			# Read from file the cost for going right
			read = file.readline()
			self.right = eval(read.split(" ")[1])

			# Read from file the cost for going diagonal
			read = file.readline()
			self.diagonal = eval(read.split(" ")[1])

			file.close()
		except IOError:
			print("File does not exist")
			sys.exit(0)

	# Computes the heuristic cost (Euclidian distance) 
	# for a certain coordinate to the destination
	# @params	coord 	a tuple consisting of the 
	#					coordinates of the current node
	#					to be computed the Euclidian distance
	# @returns	heuristic for the given node
	def heuristic(self, coord):
		coordx, coordy = coord
		destx, desty = self.destination
		return sqrt((coordx - destx)**2 + (coordy - desty)**2)


	# Reverses a path given a dictionary of paths
	# @params 	came_from	dictionary of predecessors
	#						given a tuple of coordinates as
	#						keys
	# 			current		tuple of current coordinate
	# @returns	a tuple consisting of the generated path and
	#			the cost of traversing that path
	def reconstructpath(self, came_from, current):
		total = 0
		toreturn = [current]

		node, cost = came_from[current]
		total = total + cost
		toreturn.append(node)

		while node != self.source:
			node, cost = came_from[node]
			total = total + cost
			toreturn.append(node)

		toreturn.reverse()

		return (toreturn, total)

	# Generates traversable neighbors o a given node 
	# @params	node	node where you're checking its
	#					neighbors
	# @returns	list of tuples of possible traversable neighbors
	#			of given node and it's corresponding cost
	def generateneighbors(self, node):
		toreturn = []
		x, y = node

		for i in range(-1, 2):
			for j in range(-1, 2):
				coordx = x + j
				coordy = y + i
				if i == 0:
					if j == -1:
						cost = self.left
					elif j == 1:
						cost = self.right
				elif j == 0:
					if i == -1:
						cost = self.up
					elif i == 1:
						cost = self.down
				else:
					cost = self.diagonal

				if (coordx == -1) or (coordx == self.columns) or (coordy == -1) or (coordy == self.rows):
					continue
				elif self.world[coordy][coordx] == 0:
					toreturn.append(((coordx, coordy), cost))

		return toreturn

	# Searches the map using A* search
	def astar(self):
		closedset = []
		openset = [self.source]
		came_from = {}
		stepcost = {}
		predictedcost = {}

		stepcost[self.source] = 0
		predictedcost[self.source] = stepcost[self.source] + self.heuristic(self.source)

		while openset:
			openset = sorted(openset, key = lambda data: predictedcost[data])	# sorts the tuples according to the predicted cost (current + heuristic)
			openset.reverse()

			current = openset.pop()
			if current == self.destination:
				final = self.reconstructpath(came_from, self.destination)
				break

			openset = [x for x in openset if x != current]
			closedset.append(current)

			for neighbor in self.generateneighbors(current):
				coord, cost = neighbor

				temp_g = stepcost[current] + cost
				temp_f = temp_g + self.heuristic(coord)

				if coord in closedset and temp_f >= predictedcost[coord]:
					continue

				if coord not in openset or temp_f < predictedcost[coord]:
					came_from[coord] = (current, cost)
					stepcost[coord] = temp_g
					predictedcost[coord] = temp_f
					if coord not in openset:
						openset.append(coord)

		file = open("astar.out", "w")
		path, cost = final
		for item in path:
			x, y = item
			file.write(str(y) + " " + str(x) + "\n")
		file.write(str(cost))
		file.close()

	# Searches the map using Greedy Best-First Search
	def greedy(self):
		closedset = []
		openset = [self.source]
		came_from = {}
		stepcost = {}
		predictedcost = {}

		stepcost[self.source] = 0
		predictedcost[self.source] = self.heuristic(self.source)

		while openset:
			openset = sorted(openset, key = lambda data: predictedcost[data])	# sorts nodes by heuristic cost
			openset.reverse()

			current = openset.pop()
			if current == self.destination:
				final = self.reconstructpath(came_from, self.destination)
				break

			openset = [x for x in openset if x != current]
			closedset.append(current)

			for neighbor in self.generateneighbors(current):
				coord, cost = neighbor

				temp_g = stepcost[current] + cost
				temp_f = self.heuristic(coord)

				if coord in closedset and temp_f >= predictedcost[coord]:
					continue

				if coord not in openset or temp_f < predictedcost[coord]:
					came_from[coord] = (current, cost)
					stepcost[coord] = temp_g
					predictedcost[coord] = temp_f
					if coord not in openset:
						openset.append(coord)

				if coord == self.destination:
					final = self.reconstructpath(came_from, self.destination)
					break

			try:
				final
			except UnboundLocalError:
				pass
			else:
				break

		file = open("greedy.out", "w")
		path, cost = final
		for item in path:
			x, y = item
			file.write(str(y) + " " + str(x) + "\n")
		file.write(str(cost))
		file.close()

def main():
	args = sys.argv

	try:
		filename = args[1]
	except IndexError:
		filename = raw_input("Please enter filename of input file: ")
		sys.exit(2)

	analyzer = Analyzer(filename)
	analyzer.astar()
	analyzer.greedy()

if __name__ == "__main__":
	main()