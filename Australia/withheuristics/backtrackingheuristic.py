# Python program for solution of M Coloring 
# problem using backtracking 

from datetime import datetime
starting_time = datetime.now()

change_position = [[3,4,6],[3,4,7],[1,2,4],[1,2,3,4,6,7],[],[1,4],[2,4]]

positions = []
for i in range(0,7) :
    individual=[]
    for j in range(0,7) : 
        individual.append(0)
    for j in change_position[i] : 
        individual[j-1] =1 
    positions.append(individual)
    
states= ['New South Wales','Northern Territory','Queensland','South Australia','Tasmania','Victoria','Westren Australia']
i=1
state_dictionary = {}
for state in states:
    state_dictionary[str(i)]=state
    i=i+1
color_dictionary = {"1": "red", "2": "green", "3": "blue"}
result_dictionary = {}
domain_dictionary = {}

class Backtrackingheuristic(): 

	def __init__(self, vertexs): 
		self.V = vertexs 
		self.graph = [[0 for column in range(vertexs)]
							for row in range(vertexs)] 

	## heuristic functions
	def most_remaining_values(self, domain_dictionary, colours):
		minimum_values_states = {0:[],1:[],2:[],3:[]}

		for key, value in domain_dictionary.items():
			if len(value)==0 and colours[key-1] == 0:
				minimum_values_states[0].append(key-1)

			elif(len(value)==1 and colours[key-1]==0):
				minimum_values_states[1].append(key-1)

			elif(len(value)==2 and colours[key-1]==0):
				minimum_values_states[2].append(key-1)

			elif(len(value)==3 and colours[key-1]==0):
				minimum_values_states[3].append(key-1)


		if len(minimum_values_states[0])>0:
			return minimum_values_states[0]

		elif len(minimum_values_states[1])>0:
			return minimum_values_states[1]

		elif len(minimum_values_states[2])>0:
			return minimum_values_states[2]

		elif len(minimum_values_states[3])>0:
			return minimum_values_states[3]


	def degree_constraint(self, domain_dictionary, colours):
		maxdegree_constraint = 0
		max_degree_constraint_state = -1

		for v in range(self.V): 
			if colours[v]!=0:
				continue
			count = 0
			for i in range(self.V):
				if self.graph[v][i] == 1:
					count = count + 1
			if count > maxdegree_constraint:
				maxdegree_constraint = count
				max_degree_constraint_state = v
		return max_degree_constraint_state


	def least_constraining_values(self, domain_dictionary, colours):
		Min_degree_constraint = 0
		min_degree_constraint_state = -1

		for v in range(self.V): 
			if colours[v]!=0:
				continue
			count = 0
			for i in range(self.V):
				if self.graph[v][i] == 0:
					count = count + 1
			if count > Min_degree_constraint:
				Min_degree_constraint = count
				min_degree_constraint_state = v

		return min_degree_constraint_state

	def get_next_state(self, domain_dictionary, colours):
		if self.check_if_coloured(colours):
			return 0
		next_state = 0

		next_MRV_states = self.most_remaining_values(domain_dictionary, colours)
		next_degree_constraint_states = self.degree_constraint(domain_dictionary, colours)
		next_LCV_states = self.least_constraining_values(domain_dictionary, colours)
		
		if (len(next_MRV_states)==1):
			next_state = next_MRV_states[0]
		elif(next_degree_constraint_states!=-1):
			next_state = next_degree_constraint_states
		else:
			next_state = next_LCV_states

		return next_state



	# A utility function to check if the current color assignment 
	# is safe for vertex v 
	def check_safe(self, v, colour, c): 
		for i in range(self.V): 
			if self.graph[v][i] == 1 and colour[i] == c: 
				return False
		return True
	
	def get_neighbors(self, state):
		neighbours = []
		for i in range(self.V):
			if self.graph[state][i] == 1:
				neighbours.append(i)
		return neighbours


	#singleton methods
	def check_if_coloured(self, colors):
		totalvertex = 0

		for color in colors:
			if color != 0:
				totalvertex = totalvertex + 1

		# check if all states has been assigned.
		if totalvertex == 7:
			return True
		else:
			return False

	# A recursive utility function to solve m 
	# coloring problem 
	def graph_color(self, m, colour, v):
		try:
			if self.check_if_coloured(colour):
				return True
			if v == self.V:  ## just to check if we have reached 50th end state.
				return True

			if not domain_dictionary[v+1]: ## check if the domain has no colors in their domain variables. if it is empty return false
				return False

			for c in domain_dictionary[v+1]:
				if self.check_safe(v, colour, c) == True:
					colour[v] = c ## assign the color to that state
					neighbors = self.get_neighbors(v) ## get the neighbors of the current state.

					# code to remove colors in its neighboring states
					for neighbor in neighbors:
						if c in domain_dictionary[neighbor+1]:
							domain_dictionary[neighbor+1].remove(c) ## remove the color from the neighbor domain list

					next_state = self.get_next_state(domain_dictionary, colour)
					if next_state != -1:
						if self.graph_color(m, colour, next_state) == True:
							return True
					else:
						if self.graph_color(m, colour, v+1) == True:
							return True

					# revert the domain values of all current neighbors
					for neighbor in neighbors:
						a = neighbor+1
						if c not in domain_dictionary[a]:
							domain_dictionary[a].append(c) ## remove the color from the neighbor domain list
							domain_dictionary[a].sort()
					colour[v] = 0
		except Exception as e:
			print("something wrong", e)

	def graph_colouring(self, m): 
		colour = [0] * self.V 
		if self.graph_color(m, colour, 0) == False: 
			return False

		# Print the solution 
		print("Solution exist and Following are the assigned colours:")
		for idx, val in enumerate(colour): 
			 result_dictionary[state_dictionary[str(idx+1)]] = color_dictionary[str(val)]
		return True




def createdomain_dictionary():
	for key, value in enumerate(state_dictionary):
		integers = list(range(1,4))
		domain_dictionary[key+1] = integers




createdomain_dictionary()


# Driver Code 
g = Backtrackingheuristic(7) #number of states 7

g.graph =  positions
m = 3  ## chromataic number


g.graph_colouring(m)

ending_time = datetime.now()

difference = ending_time - starting_time
print("THE TOTAL TIME TAKEN FOR EXEC ----------------",str(difference.total_seconds()))

for key, value in result_dictionary.items():
	print("{} ==> {}".format(key,value))
