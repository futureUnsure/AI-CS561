import copy
import fileinput
import sys

Graph = {}
No_of_testcases = 0
InitTime = 0
InitialNode = ""
GoalNode = ""
Algorithm = ""
DFSPathCost = None
DFSGoalNode = None

def get_no_of_testcases(FileName):
	with open(FileName,"r") as file_handle:
		try:
			return int(file_handle.readline().rstrip('\n'))
		except ValueError:
			print "Please check if you have added the no. of testcases at the top of the test case set"
	

def read_graph(file_handle):
	global InitialNode
	global GoalNode
	global InitTime
	global Algorithm

	#To eat the extra newline after the testcase and to eat the no_of_testcase
	file_handle.readline()
	Algorithm = file_handle.readline().rstrip('\n')
	InitialNode = file_handle.readline().rstrip('\n')
	GoalNode = (file_handle.readline().rstrip('\n').split(' '))
	#to eat the destination node information
	file_handle.readline()
	NumberOfPipes = int(file_handle.readline().rstrip('\n'))
	while NumberOfPipes > 0:
		NumberOfPipes -= 1
		stream = file_handle.readline().rstrip('\n')
		graph_stream = stream.split(' ')
		source_node = graph_stream[0]
		#modding is necessary for time bounds
		time_limits = [ tuple((int(x) % 24) for x in graph_stream[3+i+1].split('-')) for i in range(0,int(graph_stream[3]))]

		if (source_node not in Graph.keys()):
			Graph[source_node] = []

		dest_node = []
		#destination node name
		dest_node.append(graph_stream[1])
		#destination node cost
		#don't mod the individual costs, just output the modded answer
		dest_node.append(int(graph_stream[2]))
		if len(time_limits) > 0:
			dest_node.append(time_limits)
		else:
			dest_node.append([0])
		Graph[source_node].append(dest_node)

	InitTime = (int(file_handle.readline().rstrip('\n')) % 24)

def is_list_empty(open_queue):
	return len(open_queue) == 0

def is_goal_state(state):
	if state in GoalNode:
		return True
	return False

def is_child_node_unexplored(child_node, Frontier, Visited):
	return ((child_node[0] not in Frontier) and (child_node[0] not in Visited))

def is_new_child_node_cheaper(time_at_child_node, child_node, Frontier):
	if(child_node[0] in Frontier):
		return ((time_at_child_node < Frontier[child_node[0]]))
	else:
		return False

def is_pipe_active(child_node, time_at_parent_node):
	for x in child_node[2]:
		if x != 0:
			return not(((time_at_parent_node % 24) <= x[1] and (time_at_parent_node % 24) >= x[0]))
		else: return True

def UCS():
	Frontier = {InitialNode:InitTime}

	#sorting child nodes by cost so that the link is easier to remove later if the pipe is off
	for node in Graph:
		Graph[node].sort(key = lambda x:x[1])

	Visited = {}

	while True:

		if (is_list_empty(Frontier)):
			return None

		#Frontier dict behaves as a priority queue!
		#added condition to pick alphabetically first child in case of tie for least cost child
		parent_node_name = sorted(Frontier, key = lambda x:(Frontier[x], x) )[0]
		parent_node_value = Frontier.pop(parent_node_name)

		parent_node = (parent_node_name, parent_node_value)

		if(is_goal_state(parent_node[0]) == True):
			return (str(parent_node[0])+' '+str(parent_node[1] % 24))

		Visited[parent_node[0]] = parent_node[1]

		#Have to do this so that all the children are looped over
		#(and the loop isn't broken just because the pipe is inactive
		#at some point of time)
		child_nodes = copy.deepcopy(Graph[parent_node[0]])
		#child_nodes = (Graph[parent_node[0]])

		#For UCS only. For DFS and BFS, its the alphabetical order
		child_nodes.sort(key = lambda x:x[1])

		for (index_of_child_node,child_node) in enumerate(child_nodes):
			time_at_child_node = Visited[parent_node[0]] + child_node[1]

			if ((child_node[0] in Graph) or (is_goal_state(child_node[0]) == True)):
				if (((is_child_node_unexplored(child_node, Frontier, Visited) == True) or \
					(is_new_child_node_cheaper(time_at_child_node, child_node, Frontier) == True)) and\
					(is_pipe_active(child_node, Visited[parent_node[0]]))):
					#Update the pathcost as parent's cost + child's cost
					Frontier[child_node[0]] = time_at_child_node
				elif (is_pipe_active(child_node, Visited[parent_node[0]]) == False):
					#Have to remove the connection of parent->child instead of the parent itself!
    					Graph[parent_node[0]].pop(index_of_child_node)
					#Visited.pop(parent_node[0])



def DFS(node, PathCost):
	global DFSPathCost
	global DFSGoalNode

	if(is_goal_state(node) == True):
		#To capture the PathCost at goal node
		DFSPathCost = PathCost
		DFSGoalNode = node
		return DFSPathCost

	if node in Graph:
		FoundSolution = False
		#check if child_nodes exist or not!
		child_nodes = Graph.pop(node)
		child_nodes.sort()

		for child_node in child_nodes:
			if(DFS(child_node[0], PathCost+1) != None):
				FoundSolution = True
				return DFSPathCost

		if FoundSolution == True:
			return DFSPathCost
		else:
			#if at the end of search goal isn't found, i.e. no goal node at all return None
			return None
	else:
		#if reached a leaf node which is non Goal, return None
		return None

def BFS():
	Frontier = {InitialNode:InitTime}
	Visited = {}

	while True:
		#assert(is_list_empty(Frontier) == False)
		if (is_list_empty(Frontier)):
			return None

		parent_node_name = sorted(Frontier)[0]
		parent_node_value = Frontier.pop(parent_node_name)

		parent_node = (parent_node_name, parent_node_value)
		#assert(len(Frontier) == 0)

		Visited[parent_node[0]] = parent_node[1]
		#assert(Visited == {'AA':InitTime})

		if (parent_node[0] in Graph):
			child_nodes = Graph[parent_node[0]]
			child_nodes.sort()
		else:
			continue

		for child_node in child_nodes:
			time_at_child_node = Visited[parent_node[0]] + 1
			if(is_goal_state(child_node[0]) == True):
				return (str(child_node[0])+' '+str(time_at_child_node))

			if (((is_child_node_unexplored(child_node, Frontier, Visited) == True))):
				#Update the pathcost as parent's cost + child's cost
				Frontier[child_node[0]] = time_at_child_node
	

def main():
	global InitialNode
	global GoalNode
	global InitTime
	global Algorithm
	global Graph
	global DFSPathCost
	global DFSGoalNode

	InputFileName = str(sys.argv[2])
	OutputFileName = "output.txt"
	NoOfTestCases = get_no_of_testcases(InputFileName)

	input_file_handle = open(InputFileName,'r')
	output_file_handle = open(OutputFileName, 'a')

	while NoOfTestCases > 0:
		NoOfTestCases -= 1
		Graph = {}
		InitTime = 0
		InitialNode = ""
		GoalNode = ""
		Algorithm = ""
		DFSPathCost = None
		DFSGoalNode = None

		read_graph(input_file_handle)
		
		if(Algorithm == 'UCS'):
                    try:
			output_file_handle.write(str(UCS()) + '\n')
                    except IndexError:
			output_file_handle.write('\n')

			
		elif(Algorithm == 'DFS'):
			PathCost = InitTime
			DFS(InitialNode, PathCost)
			if DFSPathCost == None:
				output_file_handle.write(str(DFSPathCost)+'\n')
			else:
				output_file_handle.write(str(DFSGoalNode)+ ' ' + str(DFSPathCost) + '\n')

		elif(Algorithm == 'BFS'):
			output_file_handle.write(str(BFS()) + '\n')
	


	input_file_handle.close()
	output_file_handle.close()
	


if __name__ == '__main__':
	main()

