#!/usr/bin/python3

from TSPClasses import *
import heapq


# Function to create and return a cost matrix based on the cities O(n^2)
def create_matrix(cities):
	# Initialize matrix O(1)
	matrix = []
	# Loop through each city to create cost matrix O(n^2)
	for city in cities:
		row = []
		for neighbor in cities:
			cost = city.costTo(neighbor)
			row.append(cost)
		# Update matrix O(1)
		matrix.append(row)
	# Return completed cost matrix O(1)
	return matrix


# Function to reduce a matrix O(n^2) due to numpy
def reduce(matrix, lower, cost):

	# Set the columns and rows based on matrix length O(1)
	columns = len(matrix[0])
	rows = len(matrix)

	# Loop through each column and update the necessary matrix values O(n^2)
	for column in range(columns):
		minimum = np.min(matrix[:, column])
		if minimum == math.inf:
			continue
		lower += minimum
		matrix[:, column] -= np.min(matrix[:, column])

	# Loop through each row and update the necessary matrix values O(n^2)
	for row in range(rows):
		minimum = np.min(matrix[row, :])
		if minimum == math.inf:
			continue
		lower += minimum
		matrix[row, :] -= np.min(matrix[row, :])

	# Update the lower bound O(1)
	lower += cost

	# Return the reduced matrix and new lower bound O(1)
	return matrix, lower


# Function to create a child from the next index in the matrix O(n^2)
def make_child(matrix, bound, row, column, cost):

	# Set the index, row, and column to infinity O(1)
	matrix[column][row] = math.inf
	matrix[row, :] = math.inf
	matrix[:, column] = math.inf

	# Reduce the updated matrix and get the new lower bound O(n^2)
	matrix, lower = reduce(matrix, bound, cost)

	# Return the final values O(1)
	return matrix, lower


# Class to solve the Traveling Salesperson Problem
class TSPSolver:
	def __init__(self, _):
		self._scenario = None
		self._bssf = None

	def setupWithScenario(self, scenario):
		self._scenario = scenario

	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''
    # This is the default function that finds one random complete path O(n!) at worst case
    # However in practice, it comes out to O(n)
	def defaultRandomTour(self, time_allowance=60.0):
		results = {}
		cities = self._scenario.getCities()
		number_of_cities = len(cities)
		found_tour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not found_tour and time.time()-start_time < time_allowance:
			# Create a random permutation
			perm = np.random.permutation(number_of_cities)
			route = []
			# Now build the route using the random permutation
			for i in range(number_of_cities):
				route.append(cities[perm[i]])
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				found_tour = True
		end_time = time.time()
		results['cost'] = bssf.cost if found_tour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results

	''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''
	# Greedy algorithm for group project
	def greedy(self, time_allowance=60.0):
		pass

	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''
	# Branch and bound algorithm implementation O(n^2 * b^n)
	# Where b is the branching factor and n is the number of cities
	def branchAndBound(self, time_allowance=60.0):
		# Set up initial variables O(1)
		results = {}
		cities = self._scenario.getCities()
		number_of_cities = len(cities)
		found_tour = False
		count = 0
		total = 0
		maximum = 0
		pruned = 0
		depth = 1
		visited = []
		# Initialize priority queue and heapify it O(1)
		priority = []
		heapq.heapify(priority)
		# Set the default bssf to the default tour found O(1)
		bssf = self.defaultRandomTour()['soln']

		# Start the timer O(1)
		start_time = time.time()

		# Append the first city to our visited array O(1)
		visited.append(cities[0])

		# Create cost matrix O(n^2)
		matrix = create_matrix(cities)

		# Convert the matrix to a numpy array O(1)
		matrix = np.asarray(matrix)

		# Reduce the new numpy matrix and set the cost O(n^2)
		matrix, lower = reduce(matrix, 0, 0)
		cost = lower/depth

		# Create tuple to store needed values for cost matrix and push it onto the heap O(1)
		matrix_tuple = (cost, total, lower, visited, matrix, depth)
		heapq.heappush(priority, matrix_tuple)

		# Loop while time remains and our priority queue isn't empty
		while time.time() - start_time < time_allowance and len(priority) >= 1:
			# Pop the matrix and tuple items off the priority queue O(1)
			heap_matrix = heapq.heappop(priority)
			parent_depth = heap_matrix[5]
			parent_matrix = heap_matrix[4]
			visited_cities = heap_matrix[3]
			parent_lower = heap_matrix[2]
			last_city = visited_cities[-1]

			# Check to see if we need to create children O(1)
			if bssf.cost < parent_lower:
				pruned += 1
				continue

			# Grab the row index and parent length O(1)
			row = last_city._index
			parent_length = len(parent_matrix[0, :])

			# Loop through each column in the row O(n)
			for column in range(parent_length):
				child_cities = visited_cities.copy()
				if parent_matrix[row][column] == math.inf:
					continue

				# Create the child matrix and update the total O(n^2)
				child_matrix, lower = make_child(parent_matrix.copy(), parent_lower, row, column, parent_matrix[row][column])
				child_cities.append(cities[column])
				total += 1

				# Check to see if we have a solution O(1)
				if number_of_cities == len(child_cities):
					found = TSPSolution(child_cities)

					# Compare the solution to our best one O(1)
					if found.cost < bssf.cost:
						bssf = found
						found_tour = True
						count += 1

				# Set the updated child depth and cost O(1)
				child_depth = parent_depth + 1
				cost = lower/child_depth

				# Create tuple to store needed values for cost matrix and push it onto the heap O(1)
				child_tuple = (cost, total, lower, child_cities, child_matrix, child_depth)
				heapq.heappush(priority, child_tuple)

				# Update the maximum queue size if necessary O(1)
				if len(priority) > maximum:
					maximum = len(priority)

		# Stop the time and return the found results O(1)
		end_time = time.time()
		results['cost'] = bssf.cost if found_tour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = maximum
		results['total'] = total
		results['pruned'] = pruned
		return results

	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''
	# Fancy algorithm for group project
	def fancy(self, time_allowance=60.0):
		pass
