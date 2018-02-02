import time

def newArrange(inputArray):
	#split strings into individual characters
	splitArrays = [[c for c in s] for s in inputArray]
	#obtain input dimensions
	inputLen, stringLen = len(splitArrays), len(splitArrays[0])
	#create matrix for adjacent nodes
	adjacentNodes = [[] for x in range(inputLen)]
	#this loop will check if each node is adjacent to each other
	#i.e. which strings are exactly one character apart
	for index in range(inputLen):
		array = splitArrays[index]
		for x in range(inputLen):
			#print array, splitArrays[x]
			arrayDif = 0
			for y in range(stringLen):
				if splitArrays[x][y] == array[y]:
					#print splitArrays[x][y], array[y]
					continue
				else:
					arrayDif +=1
			#print "array difference", arrayDif
			if arrayDif == 1:
				#print "oneDif"
				adjacentNodes[index].append(x)
	print adjacentNodes
	#getting indices for adjacent nodes to essentially get a node number
	indexedAdjacentNodes = [ list(x) for x in enumerate(adjacentNodes)]
	print indexedAdjacentNodes
	#getting degree of each node
	nodeDegrees = [ len(x[1]) for x in indexedAdjacentNodes]
	#appending degrees to list of nodes
	#so each node in indexedAdjacentNodes contains a list:
	#[index, [adjacent nodes], degree]
	for x in range(inputLen):
		indexedAdjacentNodes[x].append(nodeDegrees[x])
	#creating list for the building of the graph and 3 types of nodes:
	#Nodes with one degree [endNodes], those associated to the endNodes ["path to single", ptsNdoes]
	#and middle Nodes that are not critical in order
	endNodes, ptsNodes, midNodes, ptsIndices, graphPath, graphUsed = [], [], [], [], [], []
	#
	#getting end nodes and the associate ptsNodes
	#
	for x in range(inputLen):
		if indexedAdjacentNodes[x][2] == 1:
			endNodes.append(indexedAdjacentNodes[x])
			ptsIndices.append(indexedAdjacentNodes[x][1])
	for index in ptsIndices:
		ptsNodes.append(indexedAdjacentNodes[index[0]])
	criticalNodes = ptsNodes + endNodes
	criticalIndices = [index[0] for index in criticalNodes]
	#getting the rest that are non critical
	midNodes = [indexedAdjacentNodes[node] for node in range(inputLen) if node not in criticalIndices]
	#print ptsNodes
	#print endNodes
	#print midNodes
	#print nodeDegrees
	#print nodeDegrees.index(min(nodeDegrees))
	#starting ze graph ya!
	#if there are no endNodes it will start with a node that has the least amount of degrees
	if len(endNodes) > 0:
		graphPath.append(endNodes[0])
		graphUsed.append(graphPath[0][0])
	else:
		graphPath.append(midNodes[nodeDegrees.index(min(nodeDegrees))])
		graphUsed.append(graphPath[0][0])
	####print graphPath
	#building graph with the following algorithm:
	#get the nodes adjacent to the last node of the graph path
	#if there is more than one adjacent node then
	#    check if index is a "critical" node or if it's already been used
	#    if it's not then append it
	#    this needs logic for the last one
	#else if there's one and it's not been used yet then add it
	while len(graphUsed) < inputLen:
		adjacents = graphPath[-1][1]
		allUsed = [True if i in graphUsed else False for i in adjacents]
		if allUsed.count(False) == 0:
			###print "false"
			return False
		###print "current index", graphPath [-1][0]
		###print "adjacents = ", adjacents
		###print len(graphUsed), "<=", (inputLen-1)
		if len(adjacents) > 1:
			for index in adjacents:
				if index in graphUsed:
					continue
				elif index not in criticalIndices:
					graphPath.append(indexedAdjacentNodes[index])
					graphUsed.append(graphPath[-1][0])
					###print "path = ", graphPath
					###print "used = ", graphUsed
					break
				else:
					copiedAdjacents = adjacents[:]
					copiedAdjacents.remove(index)
					for copy in copiedAdjacents:
						if copy not in graphUsed and copy not in criticalIndices:
							graphPath.append(indexedAdjacentNodes[copy])
							graphUsed.append(graphPath[-1][0])
							###print "path (copy) = ", graphPath
							###print "used (copy) = ", graphUsed
							break
						else:
							continue
					graphPath.append(indexedAdjacentNodes[index])
					graphUsed.append(graphPath[-1][0])
					###print "path (lastoption) = ", graphPath
					###print "used (lastoption) = ", graphUsed
					break
		else:
			if adjacents[0] not in graphUsed:
				graphPath.append(indexedAdjacentNodes[adjacents[0]])
				graphUsed.append(graphPath[-1][0])
				###print "path = ", graphPath
				###print "used = ", graphUsed
			else:
				return False
	###print "out"
	###print graphPath
	###print graphUsed
	if len(graphUsed) == inputLen:
		return True
	else:
		return False









test2 = ["arc", "abc", "bbc", "bcc", "bdc", "bec", "bef", "ber", "bar", "arc", "abc", "bbc", "bcc", "bdc", "bec", "bef", "ber", "bar"]
test1 = ["abc", "abc", "acc", "acc", "azc"]


newArrange(test2)

newArrange(test1)