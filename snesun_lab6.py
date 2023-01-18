import numpy as np
import matplotlib.pyplot as plt 
import networkx as nx 
import random as rd

"""
Name: Sneha Sunilkumar
Directory ID: snesun
Section: 0102
"""

"""
Helper function to nodes that generates a usable nx graph
This graph will be plotted and displayed in the nodes method

No inputs, returns a tuple of the graph and the position dictionary used
"""
def us(): 
	#Alaska and Hawaii not included as they aren't part of the contiguous states, DC included
	#Nodes are individual states (keys in pos_dict)
	#Positions determined roughly from map of US with approximate x, y ordered pair position tuples (values in pos_dict)
	pos_dict = {'AL' : (10,2), 'AZ' : (2,2), 'AR' : (5,2), 'CA' : (1,3), 'CO' : (4,4), 'CT': (13,5), 'DC': (12, 3), 'DE' : (14,3), 'FL' : (13,0), 'GA' : (11,1),
				'ID' : (2,7), 'IL' : (6,5), 'IN' : (7,5), 'IA' : (5,5), 'KS' : (6,3), 'KY' : (8,4), 'LA' : (7,1), 'ME' : (16,7), 'MD' : (11,4), 
				'MA' : (12,6), 'MI' : (8,7), 'MN' : (5,7), 'MS' : (8,2), 'MO' : (7,4), 'MT' : (3,7), 'NE' : (5,3), 'NV' : (2,3), 'NH' : (11,7), 'NJ' : (14,4),
				'NM' : (3,2), 'NY' : (10,5), 'NC' : (13,2), 'ND' : (4,7), 'OH' : (8,5), 'OK' : (4,2), 'OR' : (1,5), 'PA' : (13,4), 'RI' : (14,6), 'SC' :(12,2) ,
				'SD' : (4,5), 'TN' : (10,3), 'TX' : (5,0), 'UT' : (3,3), 'VT' : (10,6), 'VA' : (11,3), 'WA' : (1, 7), 'WV' : (10,4), 'WI' : (7,7), 'WY' : (3,5)}

	#Edges represent connections between states (bordering states)
	edge_list = []
	
	#With open allows a file to be read in in read mode and closes file after use
	with open('contiguous-usa.dat', 'r') as input_file:
		us_plot = nx.Graph()									#Generating a graph
		for node in pos_dict.keys():
			us_plot.add_node(node, pos=pos_dict[node])          #Adding nodes with pos attributes
		for edge in input_file.readlines():						#Trimming and formatting the data to a list of edge tuples
			new_tuple = (edge.strip().split(' ')[0], edge.strip().split(' ')[1])
			edge_list.append(new_tuple)                         
		us_plot.add_edges_from(edge_list)						#Adding edges between nodes
	return (us_plot, pos_dict)                                  #Returning important values so this method can be used later


"""
Nodes function creates a set of nodes repsenting the US states
Produces edges between them representing states with direct borders
Plots a color coded map of these nodes

Inputs: 
	NO PARAMETERS
	reads contiguous-usa.dat file 

Outputs:
	NO RETURN VALUE
	displays plot
"""
def nodes():
		us_plot = us()[0]
		pos_dict = us()[1]
		cmap = []												#Generating color map based on node num_adj
		adj_iter = us_plot.adjacency()							#Iterator through tuples of nodes and their adjacency dicts
		for node in adj_iter:
			num_adj = len(node[1])								#Length of adj dict is number of adj
			if (num_adj == 1):
				cmap.append("paleturquoise")					#Establishing a color gradient
			elif (num_adj == 2):
				cmap.append("lightskyblue")						#Paler hues indicate fewer adjacencies
			elif (num_adj == 3):
				cmap.append("cornflowerblue")
			elif (num_adj == 4):
				cmap.append("deepskyblue")
			elif (num_adj == 5):
				cmap.append("dodgerblue")	
			elif (num_adj == 6):
				cmap.append("royalblue")
			elif (num_adj == 7):
				cmap.append("mediumblue")
			elif (num_adj == 8):
				cmap.append("navy")								#The most intense blue has the most adjacencies
		nx.draw_networkx_nodes(us_plot, pos=pos_dict, 
						node_color=cmap, node_shape="s", node_size=600)					#adding nodes to graph
		nx.draw_networkx_labels(us_plot, pos_dict, font_weight="semibold", font_size=9)	#adding state names to graph	
		nx.draw_networkx_edges(us_plot, pos_dict,edge_color="darkgreen")				#adding edges to graph
		plt.title('Contiguous US Graph')
		plt.show()											#Displaying the plot

"""
plot_paths takes a start and end node and finds the shortest, a_star, and dijkstra paths between them


Inputs: 
	Graph G
	Node node_from
	Nodenode_to

Outputs:
	Graph G (Dijkstra's path highlighted)
"""		
def plot_paths(G, node_from, node_to):
	D = nx.Graph(G)                                             #Creating a Dijkstra Graph
	shortest_path = nx.shortest_path(G, node_from, node_to)     #Outputting shortest path to list (can uncomment to print down below)
	a_star = nx.astar_path(G, node_from, node_to)               #Outputting a_star path
	dijkstra_nodes = nx.dijkstra_path(G, node_from, node_to)    #Outputting dijkstra path
	dijkstra_edges = []                                         #Edge list
	pos_dict = {}												#Positions

	if (len(nx.get_node_attributes(G, "pos")) > 0):             #If nodes have positions, use them to generate position dictionary
			pos_dict = nx.get_node_attributes(G, "pos")
	else:                                                       #Otherwise use a generic position map
		pos_dict = nx.planar_layout()

	for node in range(len(dijkstra_nodes) - 1):					#Iterate through nodes in dijkstra path
		if (node != len(dijkstra_nodes) - 1):					#If not the final edge
			dijkstra_edges.append((dijkstra_nodes[node], dijkstra_nodes[node + 1]))	#Append tuple of preceding node and succeeding node

	#Draw normal (G) node in pale turquoise and dijkstra nodes (visited) in royal blue
	nx.draw_networkx_nodes(D, pos_dict, G.nodes, node_color="paleturquoise", node_shape="s", node_size=300)
	nx.draw_networkx_nodes(D, pos_dict, dijkstra_nodes, node_color="royalblue", node_shape="s", node_size=300)

	#Labelling state names
	nx.draw_networkx_labels(D, pos_dict)

	#Draw normal edges in green, visited in royal blue and bolded (increase width)
	nx.draw_networkx_edges(D, pos_dict, list(D.edges), edge_color="forestgreen", width=1.0)
	nx.draw_networkx_edges(D, pos_dict, dijkstra_edges, edge_color="royalblue", width=1.5)

	plt.title('Dijkstra Path')
	plt.show()
	return D					#Return this plot for use in other functions

	#Uncomment to see other paths
	"""
	print("Dijkstra's Generated")
	print("\nSHORTEST PATH: ")
	print(shortest_path)
	print("\nDIJKSTRA'S: " )
	print(dijkstra_nodes)
	print("\nA STAR: ")
	print(a_star)
	"""

"""
Weights aux function adds a column of weights to a new file containing old edges
It then updates the edges of the graph
Generates a dict of weights that's used for edge labels
"""
def weights_aux():
	us_plot = us()[0]														#Call old function to make graph
	pos_dict = us()[1]														#Retrieve position dict
	weighted_plot = nx.Graph()												#New graph
	weighted_edges = []														#List to store new edges

	with open("contiguous-usa-weighted.dat", "w") as new_file:
		old_file = open("contiguous-usa.dat")								#Write to this file
		for line in old_file.readlines():
			new_line = line.strip() + ' ' + str(rd.randint(0, 10)) + '\n'	#Each line contains nodes + weights
			new_file.write(new_line)
		old_file.close()

	with open("contiguous-usa-weighted.dat", "r") as new_file:				#From the new file
		for line in new_file.readlines():
			line = line.strip().split(' ')									#Section the tuple into nodes and weights
			new_tuple = (line[0], line[1], int(line[2]))
			weighted_edges.append(new_tuple)								#Add weighted edges to a list

	for node in us_plot.nodes:
		weighted_plot.add_node(node, pos=pos_dict[node])					#Add positioned nodes to the new graph
	weighted_plot.add_weighted_edges_from(weighted_edges)					#Add weighted edges
	weight_dict = nx.get_edge_attributes(weighted_plot, "weight")			#Generate dictionary of weights
	return (weighted_plot, pos_dict, weighted_edges, weight_dict)			#Output these values so they can be used to provide graph for next function

"""
Calls aux function which returns a weighted graph
Plots the weighted graph
"""
def weights():
	inputs = weights_aux()	
	weighted_plot = inputs[0]		#Retrieving graph from aux function output
	pos_dict = inputs[1]
	weighted_edges = inputs[2]
	weight_dict = inputs[3]

	nx.draw_networkx_nodes(weighted_plot, pos_dict, pos_dict.keys(), node_shape= "s", node_color="aquamarine")		#Draw nodes
	nx.draw_networkx_edges(weighted_plot, pos_dict, weighted_edges, edge_color="royalblue")							#Draw edges
	nx.draw_networkx_labels(weighted_plot, pos_dict, font_weight="semibold", font_size=9)							#State names

	#Plots the weight of each edge above the edge using a dictionary that maps edges to corresponding weights 
	nx.draw_networkx_edge_labels(weighted_plot, pos_dict, edge_labels=weight_dict,font_color="royalblue", font_size=7, font_family="arial")
	plt.title("Weighted Graph")
	plt.show()


"""
Oregon Trail runs a command line game
When called, it generates a graph of the US states with weighted edges to travel between them
The user picks a start and end state and travels between them by calling adjacent nodes
If the path the user took has the shortest possible cost, they win
Quit the game/replay any time!

No inputs, outputs graphs with the dijkstra path and player path between states highlighted
"""
def oregon_trail():
	keep_playing = 'N'									#Set quit option
	us_weighted = weights_aux()[0]						#Call previous function to generate weighted us graph

	while (keep_playing == 'N' or keep_playing == 'n'):
		start = input("Pick a Starting State: ")		#User inputs start
		curr = start 									#Define references to store temp path values while traversing graph
		next = start
		dest = input("Pick a State to Go to: ")			#User inputs endpoint
		keep_playing = input("Want to Quit? (Y/N): ")	#Offer quit option
		if (keep_playing == 'Y' or keep_playing == 'y'):
			return

		dist = nx.dijkstra_path_length(us_weighted, start, dest)	#Calculate dijkstra (shortest path)
		user_nodes = [start]										#List to track states user visits
		user_edges = []												#List to store edges between states
		user_weight_sum = 0											#Tracks cost of user path

		while (curr != dest):
			print("You can travel to: ")							#Displaying states you can travel to from this one (border states)
			adj_iter = us_weighted.adjacency()						#Iterator over a dictionary with nodes as keys
			for node in adj_iter:									#Finding the key
				if node[0] == curr:
					adjacencies = node[1]							#adjacencies is a list of neighboring states
					for adj in adjacencies:							#Print them to user
						print(adj)
					break
			next = input("Where would you like to go? ")			#User picks a state to go to (hopefully in adj list)
			user_nodes.append(next)									#Add this state to their path
			weight_dict = (nx.get_edge_attributes(us_weighted, "weight"))	#Dictionary of edge weights
			if (curr, next) in weight_dict.keys():							#To find the weight of an edge, it could be either way
				key = (curr, next)
			else:															#NH to ME is actually listed as ME to NH
				key = (next, curr)
			user_edges.append((curr, next, weight_dict[key]))				#Retrieve value with the right key
			user_weight_sum = user_weight_sum + (nx.get_edge_attributes(us_weighted, "weight")[key])	#Add path cost to sum
			keep_playing = input("Want to Quit? (Y/N): ")
			if (keep_playing == 'Y' or keep_playing == 'y'):
				return
			curr = next														#Continue traversal

		plot_paths(us_weighted, start, dest)								#Plot paths displays dijkstra's path

		#To plot user path with other states in blue, visited states/edges in green, edge weights and state names displayed
		#Nodes displayed, turquoise and limegreen visited
		nx.draw_networkx_nodes(us_weighted, us()[1], us_weighted.nodes, node_color="paleturquoise", node_size=350, node_shape="s")
		nx.draw_networkx_nodes(us_weighted, us()[1], user_nodes, node_color="limegreen", node_size=350, node_shape="s")

		#Edges displayed, limegreen visited edges
		nx.draw_networkx_edges(us_weighted, us()[1], us_weighted.edges, edge_color="forestgreen")
		nx.draw_networkx_edges(us_weighted, us()[1], user_edges, edge_color="limegreen", width=2.5)

		#State names
		nx.draw_networkx_labels(us_weighted, us()[1])
		weight_list = nx.get_edge_attributes(us_weighted, "weight")
		nx.draw_networkx_edge_labels(us_weighted, us()[1], edge_labels=weight_list,font_color="royalblue", font_size=7, font_family="arial")
		plt.title('User Path')
		plt.show()

		if (user_weight_sum == dist):
			print("CONGRATS! You won!!")				#Win case
		else:
			print("Sorry, better luck next time")		#Lose case

		keep_playing = input("Want to Quit? (Y/N): ")

if __name__ == '__main__':
	#Function 1 nodes
	nodes()

	#Function 2 plot_paths 
	plot_paths(us()[0], 'SD', 'VT')

	#Function 3 weights
	weights()

	#Function 4 oregon trail
	oregon_trail()