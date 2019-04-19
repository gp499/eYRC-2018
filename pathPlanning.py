class pathPlanning:
	
	# Defining a dictionary with keys a cell numbers and values as list of nodes in the map
    hexMap={ 1 : ["4","5","1","10","2","9"],
          2 :  ["8","9","15","3","14","4"],
          3 :  ["15","16","9","22","21","10"],
          4 :  ["11","10","5","17","16","6"],
          5 :  ["13","14","7","20","19","8"],
          6 :  ["20","21","14","27","26","15"],
          7 :  ["27","28","21","34","33","22"],
          8 :  ["23","22","16","29","28","17"],
          9 :  ["18","17","11","24","23","12"],
          10 : ["26","25","19","32","31","20"],
          11 : ["32","33","26","39","27","38"],
          12 : ["39","40","33","46","45","34"],
          13 : ["34","35","41","28","40","29"],
          14 : ["29","30","23","36","24","35"],
          15 : ["37","38","31","44","43","32"],
          16 : ["44","45","50","38","49","39"],
          17 : ["50","51","54","45","53","46"],
          18 : ["46","47","52","40","41","51"],
          19 : ["41","42","48","35","47","36"],        
          }

	#Defining a dictionary with keys as nodes of the map and values as their nearest nieghbours
    graphNodes = {     "1" : set(["2","4"]),
          "2" : set(["1","5"]),
          "3" : set(["8","4"]),
          "4" : set(["3","1","9"]),
          "5" : set(["2","10","6"]),
          "6" : set(["11","5"]),
          "7" :set (["8","13"]),
          "8" : set(["7","14","3"]),
          "9" : set(["15","4","10"]),
          "10" :set (["9","5","16"]),
          "11" : set(["17","6","12"]),
          "12" : set(["11","18"]),
          "13" : set(["19","7"]),
          "14" :set (["20","15","8"]), 
          "15" : set(["21","9","14"]),
          "16" : set(["22","10","17"]),
          "17" : set(["23","16","11"]),
          "18" : set(["12","24"]),
          "19" : set(["25","13","20"]),
          "20" : set(["26","14","19"]),
          "21" : set(["27","22","15"]),
          "22" :set (["21","28","16"]),
          "23" : set(["29","17","24"]),
          "24" :set (["23","30","18"]),
          "25" :set (["19","31"]),
          "26" : set(["32","20","27"]),
          "27" : set(["21","33","26"]),
          "28" :set (["29","22","34"]),
          "29" :set (["28","23","35"]),
          "30" : set(["24","36"]),
          "31" : set(["25","37","32"]),
          "32" : set(["38","31","26"]),
          "33" : set(["39","34","27"]),
          "34" : set(["33","40","28"]),
          "35" : set(["36","29","41"]),
          "36" : set(["42","35","30"]),
          "37" : set(["31","43"]),
          "38" : set(["39","44","32"]),
          "39" :set (["38","45","33"]),
          "40" : set(["41","34","46"]),
          "41" : set(["35","40","47"]),
          "42" : set(["36","48"]),
          "43" : set(["37","44"]),
          "44" : set(["43","38","49"]),
          "45" :set (["39","50","46"]),
          "46" :set (["51","40","45"]),
          "47" : set(["52","41","48"]),
          "48" :set (["47","42"]),
          "49" : set(["50","44"]),
          "50" : set(["49","45","53"]),
          "51" : set(["54","46","52"]),
          "52" : set(["51","47"]),
          "53" : set(["54","50"]),
          "54" : set(["53","51"]),
          "start1": set(["25"]),
          "start2": set(["30"]),
        }
	
"""
Function Name : bfs_paths(graph,start,goal)
Input: Graph in the form of set dictionary, start node , end node
Output: Path from start node to end node using the given graph
Purpose:Breadth first Algorithm which stores the path
"""
    def bfs_paths(graph, start, goal):
            queue = [(start, [start])]
            while queue:
                (vertex, path) = queue.pop(0)
                for next in graph[vertex] - set(path):
                    if next == goal:
                        yield path + [next]
                    else:
                        queue.append((next, path + [next]))

"""
Function Name : shortest_path(graph,start,goal)
Input: Graph in the form of set dictionary, start node , end node
Output: Shortest Path from start node to end node
Purpose: Shortest Path is found by repeadtedly calling the bfs_paths function
"""    
    def shortest_path(graph, start, goal):
            try:
                return next(pathPlanning.bfs_paths(graph, start, goal))
            except StopIteration:
                return None

"""
Function Name : paths(graph,start,goal)
Input: Graph in the form of set dictionary, start node ,cell Number, end node
Output: Updated graph and returns a path with approach of 2nd last node
Purpose:Path to made such that we omit other nieghbouring nodes of approachable entry nodes(Hexagons entry points due 
	to particular orientation) so that the bot orients itself straight and enters the hexagon
"""    
    def path(graphNodes ,start ,cellNumber ,lastNode):
        secLastNode=set(graphNodes[lastNode])-set(pathPlanning.hexMap[cellNumber])
        if secLastNode==set():
            return None
        else:
            omitNode=set(graphNodes[lastNode])-secLastNode
            graphNodes1=graphNodes.copy()
            d1={lastNode:secLastNode}
            d2={str(list(omitNode)[0]) : set(graphNodes1[str(list(omitNode)[0])])-{lastNode}}
            d3={str(list(omitNode)[1]) : set(graphNodes1[str(list(omitNode)[1])])-{lastNode}}
            graphNodes1.update(d1)
            graphNodes1.update(d2)
            graphNodes1.update(d3)
            return pathPlanning.shortest_path(graphNodes1,start,lastNode)

"""
Function Name : flow(start ,arena_config)
Input: Start (start1 /start2), arena configuration
Output: Gives the whole path with list of turns (by calling nextTurn) and also the order of aruco ids
Purpose: List of turns returned here is transmitted to the bot one by one whenever the bot reaches a node,
	 the list of order of visiting aruco ids is used later in AR part where the pebble diminishing animation is shown
"""
    def flow(start ,arena_config):
        lastNodes=[]					
        secLastNode=['','','','','','']
        visited=[False , False , False]		
        visitingOrder=['','','']
        d=list(arena_config.keys())
        for i in range(4):
            arena_config[i]=arena_config.pop(d[i])		#Updating the keys of arena_config for better indexing
        for i in range(4):								#Setting the corresponding approachable nodes as per orientation
            if (arena_config[i][2]=="1-1"):
                j=0
            if (arena_config[i][2]=="2-2"):
                j=2
            if (arena_config[i][2]=="3-3"):
                j=4
            lastNodes.append(pathPlanning.hexMap[arena_config[i][1]][j:j+2:1])
        
		##Checking if no path available for 1st approachable node of 1st pebble
		if pathPlanning.path(pathPlanning.graphNodes,start,arena_config[1][1],lastNodes[1][0]) == None:
          a1=pathPlanning.path(pathPlanning.graphNodes,start,arena_config[1][1],lastNodes[1][1])
          lastNode1=lastNodes[1][1]
        
		##Checking if no path available for 2nd approachable node of 1st pebble
		elif pathPlanning.path(pathPlanning.graphNodes,start,arena_config[1][1],lastNodes[1][1])== None:
          a1=pathPlanning.path(pathPlanning.graphNodes,start,arena_config[1][1],lastNodes[1][0])
          lastNode1=lastNodes[1][0]
        ##Comparing both approachable paths for 1st pebble and choosing the shorter path
		else:  
          if len(pathPlanning.path(pathPlanning.graphNodes,start,arena_config[1][1],lastNodes[1][0]))<=len(pathPlanning.path(pathPlanning.graphNodes,"25",arena_config[1][1],lastNodes[1][1])):
                 a1=pathPlanning.path(pathPlanning.graphNodes,start,arena_config[1][1],lastNodes[1][0])
                 lastNode1=lastNodes[1][0]
          else:
                 a1=pathPlanning.path(pathPlanning.graphNodes,start,arena_config[1][1],lastNodes[1][1])
                 lastNode1=lastNodes[1][1]
        
		## Similarly For other two pebbles checking if any approachable node has no path available and finding the 
		## shorter path of the two
		if pathPlanning.path(pathPlanning.graphNodes,start,arena_config[2][1],lastNodes[2][0]) == None:
          a2=pathPlanning.path(pathPlanning.graphNodes,start,arena_config[2][1],lastNodes[2][1])
          lastNode2=lastNodes[2][1]
        elif pathPlanning.path(pathPlanning.graphNodes,start,arena_config[2][1],lastNodes[2][1])== None:
          a2=pathPlanning.path(pathPlanning.graphNodes,start,arena_config[2][1],lastNodes[2][0])
          lastNode2=lastNodes[2][0]  
        else:  
          if len(pathPlanning.path(pathPlanning.graphNodes,start,arena_config[2][1],lastNodes[2][0]))<=len(pathPlanning.path(pathPlanning.graphNodes,"25",arena_config[2][1],lastNodes[2][1])):
                 a2=pathPlanning.path(pathPlanning.graphNodes,start,arena_config[2][1],lastNodes[2][0])
                 lastNode2=lastNodes[2][0]
          else:
                 a2=pathPlanning.path(pathPlanning.graphNodes,start,arena_config[2][1],lastNodes[2][1])
                 lastNode2=lastNodes[2][1]
        if pathPlanning.path(pathPlanning.graphNodes,start,arena_config[3][1],lastNodes[3][0]) == None:
          a3=pathPlanning.path(pathPlanning.graphNodes,start,arena_config[3][1],lastNodes[3][1])
          lastNode3=lastNodes[3][1]
        elif pathPlanning.path(pathPlanning.graphNodes,start,arena_config[3][1],lastNodes[3][1])== None:
          a3=pathPlanning.path(pathPlanning.graphNodes,start,arena_config[3][1],lastNodes[3][0])
          lastNode3=lastNodes[3][0]
        else:
          if len(pathPlanning.path(pathPlanning.graphNodes,start,arena_config[3][1],lastNodes[3][0]))<=len(pathPlanning.path(pathPlanning.graphNodes,"25",arena_config[3][1],lastNodes[3][1])):
                 a3=pathPlanning.path(pathPlanning.graphNodes,start,arena_config[3][1],lastNodes[3][0])
                 lastNode3=lastNodes[3][0]
          else:
                 a3=pathPlanning.path(pathPlanning.graphNodes,start,arena_config[3][1],lastNodes[3][1])
                 lastNode3=lastNodes[3][1]
        
		##Comparing lengths of paths for the 3 pebbles from start and choosing the shortest path
		if len(a1)<len(a2):
               if len(a1)<=len(a3):
                 a=a1
                 visited[0]=True		#Updating the flag if the pebble is visted
                 visitingOrder[0]=d[1]
                 lastNode=lastNode1
        elif len(a2) <= len(a3):
               a=a2
               visited[1]=True
               visitingOrder[0]=d[2]
               lastNode=lastNode2
        else:
               a=a3
               visited[2]=True
               visitingOrder[0]=d[3]
               lastNode=lastNode3
        secLastNode[0]=a[len(a)-2]		#Storing the last and 2nd last node for better path planning for next path
		##Checking for shortest path from 1st pebble to pitcher
        if pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][0])== None:
            b=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][1])
            lastNode=lastNodes[0][1]
        elif pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][1])==None:
            b=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][0])
            lastNode=lastNodes[0][0]
        else:
            if len(pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][0]))<=len(pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][1])):
                b=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][0])
                lastNode=lastNodes[0][0]
            else:
                b=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][1])
                lastNode=lastNodes[0][1]
        secLastNode[1]=b[len(b)-2]     #Updating last and 2nd last node 
        count=0
		
		## First checking which pebbles to visit next
        for i in range(3):
          if visited[i] ==False:
            if count ==0:
			## Finding shorter path similiarly
              if pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][0])==None:
                c1=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][1])
                lastNode1=lastNodes[i+1][1]
              elif pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][1])==None:
                c1=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][0])
                lastNode1=lastNodes[i+1][0]
              else:
                if len(pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][0]))<=len(pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][1])):
                   c1=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][0])
                   lastNode1=lastNodes[i+1][0]
                else:
                   c1=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][1])
                   lastNode1=lastNodes[i+1][1]
              temp1=i
              count=1
			  ##Finding shorter path for other unvisited pebble
            else :
              if pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][0])==None:
                c2=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][1])
                lastNode2=lastNodes[i+1][1]
              elif pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][1])==None:
                c2=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][0])
                lastNode2=lastNodes[i+1][0]
              else:  
                if len(pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][0]))<=len(pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][1])):
                   c2=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][0])
                   lastNode2=lastNodes[i+1][0]
                else:
                   c2=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][1])
                   lastNode2=lastNodes[i+1][1]
              temp2=i
        ## Comparing length of path for 2nd pebble visit for shorter path
        if len(c1)<len(c2):
          visited[temp1]=True
          visitingOrder[1]=d[temp1+1]
          visitingOrder[2]=d[temp2+1]
          c=c1
          lastNode=lastNode1
        else:
          visited[temp2]=True
          visitingOrder[1]=d[temp2+1]
          visitingOrder[2]=d[temp1+1]
          c=c2
          lastNode=lastNode2
        secLastNode[2]=c[len(c)-2] ## Updating visited flag, last node and secLastNode
        
		##Finding path back to pitcher for 2nd drop
		if pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][0])== None:
          d=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][1])
          lastNode=lastNodes[0][1]
        elif pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][1])==None:
          d=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][0])
          lastNode=lastNodes[0][0]
        else:
          if len(pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][0]))<=len(pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][1])):
            d=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][0])
            lastNode=lastNodes[0][0]
          else:
            d=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][1])
            lastNode=lastNodes[0][1]
        secLastNode[3]=d[len(d)-2]           
        
		##Visiting the last left pebble for 3rd pickup
		for i in range(3):
          if visited[i] ==False:
            if pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][0])== None:
              e=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][1])
              lastNode=lastNodes[i+1][1]
            elif pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][1])==None:
              e=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][0])
              lastNode=lastNodes[i+1][0]
            else:
              if len(pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][0]))<=len(pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][1])):
                e=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][0])
                lastNode=lastNodes[i+1][0]
              else:
                e=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[i+1][1],lastNodes[i+1][1])
                lastNode=lastNodes[i+1][1]
        secLastNode[4]=e[len(e)-2]
        
		##Path for final drop to pitcher
		if pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][0])== None:
          f=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][1])
          lastNode=lastNodes[0][1]
        elif pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][1])==None:
          f=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][0])
          lastNode=lastNodes[0][0]
        else:
          if len(pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][0]))<=len(pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][1])):
            f=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][0])
            lastNode=lastNodes[0][0]
          else:
            f=pathPlanning.path(pathPlanning.graphNodes,lastNode,arena_config[0][1],lastNodes[0][1])
            lastNode=lastNodes[0][1]
        secLastNode[5]=f[len(f)-2]
        ##The full path with 3 pickups and 3 drops
		path=a+b+c+d+e+f
        a=len(a)
        b=len(b)
        c=len(c)
        d=len(d)
        e=len(e)
        f=len(f)
        turns=[]
        i=0 
		
		#Iterating through the path list for finding the turns
        for i in range(len(path)-1):
          prevNode=path[i]
          currNode=path[i+1]
          if i+2 <len(path):
              nextNode=path[i+2]
              if (i == a-1):	# Instruction For 1st pickup 
                data=pathPlanning.nextTurn(secLastNode[0],currNode,nextNode)
              elif (i == a+b-1): #For 1st drop
                data=pathPlanning.nextTurn(secLastNode[1],currNode,nextNode)  
              elif (i == a+b+c-1): #For 2nd pickup
                data=pathPlanning.nextTurn(secLastNode[2],currNode,nextNode)    
              elif (i == a+b+c+d-1):	#For 2 nd drop
                data=pathPlanning.nextTurn(secLastNode[3],currNode,nextNode)    
              elif (i == a+b+c+d+e-1):  #For 3rd pickup
                data=pathPlanning.nextTurn(secLastNode[4],currNode,nextNode)    
              elif (i == a+b+c+d+e+f-1):	#For 3rd drop 
                data=pathPlanning.nextTurn(secLastNode[5],currNode,nextNode)
              else:			# For rest of turns .... calling nextTurn function
                data=pathPlanning.nextTurn(prevNode, currNode , nextNode)
              turns.append(data)
          else:			##To perform the end 
            data=pathPlanning.nextTurn(prevNode,currNode,currNode)
            turns.append(data)
            break
        return path ,turns, visitingOrder


"""
Function Name : nextTurn(prevNode,currNode,nextNode)
Input: previous node , current node , next node
Output: Returns the turns to be followed by bot in the form of character
Purpose: All turns for tranversing to any part of the arena is stored here. The special cases for drop/pickup 
		is also specified. Also has a logic for a U-Turn. Returns 'l' for left, 'r' for right,'p' for pebble pickup/drop
		'u' for u turn. It decides turns at each node on the basis of node it came from. Refer to Graph map for better understanding.
"""
    def nextTurn(prevNode ,currNode , nextNode):
        if(currNode==nextNode):		#If it is about to visit a node twice, it means it has to undergo pickup / drop function
            return'p'

        if (prevNode == nextNode):	#If previous and next node are same, it means it has to undergo a u turn 
            return 'u'
	##	If bot approaches node 25 from start1, it'll get node 19 on left and node 31 on right
        if(currNode =='25' and prevNode =='start1'):
            if nextNode == '19' :
                return 'l'
            if nextNode == '31':
                return 'r'
        
        if(currNode =='30' and prevNode =='start2'):
            if nextNode == '36' :
                return 'l'
            if nextNode == '24':
                return 'r'

        if currNode>='41':
            if(currNode =='54' and prevNode =='51'):
                if nextNode == '53':
                    return 'r'


            if(currNode =='54' and prevNode =='53'):
                if nextNode == '51' :
                    return 'l'

            if(currNode =='53' and prevNode =='54'):
                if nextNode == '50':
                    return 'r'

            if(currNode =='53' and prevNode =='50'):
                if nextNode == '54' :
                    return 'l'

            if(currNode =='52' and prevNode =='51'):
                if nextNode == '47' :
                    return 'l'

            if(currNode =='52' and prevNode =='47'):
                if nextNode == '51':
                    return 'r'

            if(currNode =='51' and prevNode =='54'):
                if nextNode == '46' :
                    return 'l'
                if nextNode == '52':
                    return 'r'

            if(currNode =='51' and prevNode =='52'):
                if nextNode == '54' :
                    return 'l'
                if nextNode == '46':
                    return 'r'

            if(currNode =='51' and prevNode =='46'):
                if nextNode == '52' :
                    return 'l'
                if nextNode == '54':
                    return 'r'

            if(currNode =='50' and prevNode =='49'):
                if nextNode == '45' :
                    return 'l'
                if nextNode == '53':
                    return 'r'

            if(currNode =='50' and prevNode =='45'):
                if nextNode == '53' :
                    return 'l'
                if nextNode == '49':
                    return 'r'

            if(currNode =='50' and prevNode =='53'):
                if nextNode == '49' :
                    return 'l'
                if nextNode == '45':
                    return 'r'

            if(currNode =='49' and prevNode =='50'):
                if nextNode == '44':
                    return 'r'

            if(currNode =='49' and prevNode =='44'):
                if nextNode == '50' :
                    return 'l'

            if(currNode =='48' and prevNode =='47'):
                if nextNode == '42' :
                    return 'l'

            if(currNode =='48' and prevNode =='42'):
                if nextNode == '47':
                    return 'r'

            if(currNode =='47' and prevNode =='48'):
                if nextNode == '52' :
                    return 'l'
                if nextNode == '46':
                    return 'r'

            if(currNode =='47' and prevNode =='41'):
                if nextNode == '48' :
                    return 'l'
                if nextNode == '52':
                    return 'r'

            if(currNode =='47' and prevNode =='52'):
                if nextNode == '41' :
                    return 'l'
                if nextNode == '48':
                    return 'r'

            if(currNode =='46' and prevNode =='51'):
                if nextNode == '45' :
                    return 'l'
                if nextNode == '40':
                    return 'r'

            if(currNode =='46' and prevNode =='40'):
                if nextNode == '51' :
                    return 'l'
                if nextNode == '45':
                    return 'r'

            if(currNode =='46' and prevNode =='45'):
                if nextNode == '40' :
                    return 'l'
                if nextNode == '51':
                    return 'r'

            if(currNode =='45' and prevNode =='39'):
                if nextNode == '46' :
                    return 'l'
                if nextNode == '50':
                    return 'r'

            if(currNode =='45' and prevNode =='50'):
                if nextNode == '39' :
                    return 'l'
                if nextNode == '46':
                    return 'r'

            if(currNode =='45' and prevNode =='46'):
                if nextNode == '50' :
                    return 'l'
                if nextNode == '36':
                    return 'r'

            if(currNode =='44' and prevNode =='43'):
                if nextNode == '38' :
                    return 'l'
                if nextNode == '49':
                    return 'r'

            if(currNode =='44' and prevNode =='38'):
                if nextNode == '49' :
                    return 'l'
                if nextNode == '43':
                    return 'r'

            if(currNode =='44' and prevNode =='49'):
                if nextNode == '43' :
                    return 'l'
                if nextNode == '38':
                    return 'r'

            if(currNode =='43' and prevNode =='37'):
                if nextNode == '44' :
                    return 'l'

            if(currNode =='43' and prevNode =='44'):
                if nextNode == '37':
                    return 'r'

            if(currNode =='42' and prevNode =='36'):
                if nextNode == '48':
                    return 'r'

            if(currNode =='42' and prevNode =='48'):
                if nextNode == '36' :
                    return 'l'

            if(currNode =='41' and prevNode =='35'):
                if nextNode == '47' :
                    return 'l'
                if nextNode == '40':
                    return 'r'

            if(currNode =='41' and prevNode =='47'):
                if nextNode == '40' :
                    return 'l'
                if nextNode == '35':
                    return 'r'

            if(currNode =='41' and prevNode =='40'):
                if nextNode == '35' :
                    return 'l'
                if nextNode == '47':
                    return 'r'

        if currNode<='13':
            if(currNode =='1' and prevNode =='2'):
                if nextNode == '4' :
                    return 'l'
                
            if(currNode =='1' and prevNode =='4'):
                if nextNode == '2':
                    return 'r'

            if(currNode =='2' and prevNode =='1'):
                if nextNode == '5':
                    return 'r'

            if(currNode =='2' and prevNode =='5'):
                if nextNode == '1' :
                    return 'l'

            if(currNode =='3' and prevNode =='4'):
                if nextNode == '8' :
                    return 'l'

            if(currNode =='3' and prevNode =='8'):
                if nextNode == '4' :
                    return 'r'

            if(currNode =='4' and prevNode =='3'):
                if nextNode == '1' :
                    return 'l'
                if nextNode == '9':
                    return 'r'

            if(currNode =='4' and prevNode =='1'):
                if nextNode == '9' :
                    return 'l'
                if nextNode == '3':
                    return 'r'

            if(currNode =='4' and prevNode =='9'):
                if nextNode == '3' :
                    return 'l'
                if nextNode == '1':
                    return 'r'

            if(currNode =='5' and prevNode =='2'):
                if nextNode == '6' :
                    return 'l'
                if nextNode == '10':
                    return 'r'

            if(currNode =='5' and prevNode =='10'):
                if nextNode == '2' :
                    return 'l'
                if nextNode == '6':
                    return 'r'

            if(currNode =='5' and prevNode =='6'):
                if nextNode == '10' :
                    return 'l'
                if nextNode == '2':
                    return 'r'

            if(currNode =='6' and prevNode =='5'):
                if nextNode == '11' :
                    return 'r'

            if(currNode =='6' and prevNode =='11'):
                if nextNode == '5' :
                    return 'l'

            if(currNode =='7' and prevNode =='8'):
                if nextNode == '13' :
                    return 'l'

            if(currNode =='7' and prevNode =='13'):
                if nextNode == '8' :
                    return 'r'

            if(currNode =='8' and prevNode =='7'):
                if nextNode == '3' :
                    return 'l'
                if nextNode == '14':
                    return 'r'

            if(currNode =='8' and prevNode =='3'):
                if nextNode == '14' :
                    return 'l'
                if nextNode == '7':
                    return 'r'

            if(currNode =='8' and prevNode =='14'):
                if nextNode == '7' :
                    return 'l'
                if nextNode == '3':
                    return 'r'

            if(currNode =='9' and prevNode =='4'):
                if nextNode == '10' :
                    return 'l'
                if nextNode == '15':
                    return 'r'


            if(currNode =='9' and prevNode =='15'):
                if nextNode == '4' :
                    return 'l'
                if nextNode == '10':
                    return 'r'

            if(currNode =='9' and prevNode =='10'):
                if nextNode == '15' :
                    return 'l'
                if nextNode == '4':
                    return 'r'

            if(currNode =='10' and prevNode =='5'):
                if nextNode == '16' :
                    return 'l'
                if nextNode == '9':
                    return 'r'

            if(currNode =='10' and prevNode =='9'):
                if nextNode == '5' :
                    return 'l'
                if nextNode == '16':
                    return 'r'

            if(currNode =='10' and prevNode =='16'):
                if nextNode == '9' :
                    return 'l'
                if nextNode == '5':
                    return 'r'

            if(currNode =='11' and prevNode =='6'):
                if nextNode == '12' :
                    return 'l'
                if nextNode == '17':
                    return 'r'

            if(currNode =='11' and prevNode =='17'):
                if nextNode == '6' :
                    return 'l'
                if nextNode == '12':
                    return 'r'

            if(currNode =='11' and prevNode =='12'):
                if nextNode == '17' :
                    return 'l'
                if nextNode == '6':
                    return 'r'

            if(currNode =='12' and prevNode =='11'):
                if nextNode == '18':
                    return 'r'

            if(currNode =='12' and prevNode =='18'):
                if nextNode == '11' :
                    return 'l'

            if(currNode =='13' and prevNode =='7'):
                if nextNode == '19' :
                    return 'l'

            if(currNode =='13' and prevNode =='19'):
                if nextNode == '7' :
                    return 'r'

        if (currNode>'13') and (currNode <='27'):
            if(currNode =='14' and prevNode =='8'):
                if nextNode == '15' :
                    return 'l'
                if nextNode == '20':
                    return 'r'

            if(currNode =='14' and prevNode =='15'):
                if nextNode == '20' :
                    return 'l'
                if nextNode == '8':
                    return 'r'

            if(currNode =='14' and prevNode =='20'):
                if nextNode == '8' :
                    return 'l'
                if nextNode == '15':
                    return 'r'

            if(currNode =='15' and prevNode =='9'):
                if nextNode == '21' :
                    return 'l'
                if nextNode == '14':
                    return 'r'

            if(currNode =='15' and prevNode =='14'):
                if nextNode == '9' :
                    return 'l'
                if nextNode == '21':
                    return 'r'

            if(currNode =='15' and prevNode =='21'):
                if nextNode == '14' :
                    return 'l'
                if nextNode == '9':
                    return 'r'

            if(currNode =='16' and prevNode =='10'):
                if nextNode == '17' :
                    return 'l'
                if nextNode == '22':
                    return 'r'

            if(currNode =='16' and prevNode =='17'):
                if nextNode == '22' :
                    return 'l'
                if nextNode == '10':
                    return 'r'

            if(currNode =='16' and prevNode =='22'):
                if nextNode == '10' :
                    return 'l'
                if nextNode == '17':
                    return 'r'

            if(currNode =='17' and prevNode =='11'):
                if nextNode == '23' :
                    return 'l'
                if nextNode == '16':
                    return 'r'

            if(currNode =='17' and prevNode =='16'):
                if nextNode == '11' :
                    return 'l'
                if nextNode == '23':
                    return 'r'

            if(currNode =='17' and prevNode =='23'):
                if nextNode == '16' :
                    return 'l'
                if nextNode == '11':
                    return 'r'

            if(currNode =='18' and prevNode =='12'):
                if nextNode == '24' :
                    return 'r'

            if(currNode =='18' and prevNode =='24'):
                if nextNode == '12' :
                    return 'l'

            if(currNode=='19' and prevNode=='13'):
                if nextNode== '20' :
                    return 'l'
                if nextNode=='25 ':
                    return 'r'

            if(currNode=='19' and prevNode=='25'):
                if nextNode== '13' :
                    return 'l'
                if nextNode=='20':
                    return 'r'
            
            if(currNode=='19' and prevNode=='20'):
                if nextNode== '25' :
                    return 'l'
                if nextNode=='13 ':
                    return 'r'
            
            if(currNode=='20' and prevNode=='19'):
                if nextNode== '14' :
                    return 'l'
                if nextNode=='26':
                    return 'r'
            
            if(currNode=='20' and prevNode=='26'):
                if nextNode== '19' :
                    return 'l'
                if nextNode=='14':
                    return 'r'
            
            if(currNode=='20' and prevNode=='14'):
                if nextNode== '26' :
                    return 'l'
                if nextNode=='19':
                    return 'r'
            
            if(currNode=='21' and prevNode=='22'):
                if nextNode== '27' :
                    return 'l'
                if nextNode=='15':
                    return 'r'
            
            if(currNode=='21' and prevNode=='27'):
                if nextNode== '15' :
                    return 'l'
                if nextNode=='22':
                    return 'r'
            
            if(currNode=='21' and prevNode=='15'):
                if nextNode== '22' :
                    return 'l'
                if nextNode=='27':
                    return 'r'
            
            if(currNode=='22' and prevNode=='21'):
                if nextNode== '16' :
                    return 'l'
                if nextNode=='28':
                    return 'r'
            
            if(currNode=='22' and prevNode=='16'):
                if nextNode== '28' :
                    return 'l'
                if nextNode=='21':
                    return 'r'
            
            if(currNode=='22' and prevNode=='28'):
                if nextNode== '21' :
                    return 'l'
                if nextNode=='16':
                    return 'r'
            
            if(currNode=='23' and prevNode=='24'):
                if nextNode== '29' :
                    return 'l'
                if nextNode=='17':
                    return 'r'
            
            if(currNode=='23' and prevNode=='29'):
                if nextNode== '17' :
                    return 'l'
                if nextNode=='24':
                    return 'r'
            
            if(currNode=='23' and prevNode=='17'):
                if nextNode== '24' :
                    return 'l'
                if nextNode=='29':
                    return 'r'
            
            if(currNode=='24' and prevNode=='23'):
                if nextNode== '18' :
                    return 'l'
                if nextNode=='30':
                    return 'r'
            
            if(currNode=='24' and prevNode=='30'):
                if nextNode== '23' :
                    return 'l'
                if nextNode=='18':
                    return 'r'
            
            if(currNode=='24' and prevNode=='18'):
                if nextNode== '30' :
                    return 'l'
                if nextNode=='23':
                    return 'r'
            
            if(currNode=='26' and prevNode=='27'):
                if nextNode== '32' :
                    return 'l'
                if nextNode=='20':
                    return 'r'
            
            if(currNode=='26' and prevNode=='20'):
                if nextNode== '27' :
                    return 'l'
                if nextNode=='32':
                    return 'r'
            
            if(currNode=='26' and prevNode=='32'):
                if nextNode== '20' :
                    return 'l'
                if nextNode=='27':
                    return 'r'
            
            if(currNode=='27' and prevNode=='26'):
                if nextNode== '21' :
                    return 'l'
                if nextNode=='33':
                    return 'r'
            
            if(currNode=='27' and prevNode=='33'):
                if nextNode== '26' :
                    return 'l'
                if nextNode=='21':
                    return 'r'
            
            if(currNode=='27' and prevNode=='21'):
                if nextNode== '33' :
                    return 'l'
                if nextNode=='26':
                    return 'r'
            
            if(currNode=='25' and prevNode=='19'):
                if nextNode== '31' :
                    return 'l'
            
            if(currNode=='25' and prevNode=='31'):
                if nextNode== '19' :
                    return 'r'
        
        if(currNode>'27') and (currNode<='40'): 
            if(currNode=='28' and prevNode=='29'):
                if nextNode== '34' :
                    return 'l'
                if nextNode=='22':
                    return 'r'
            
            if(currNode=='28' and prevNode=='22'):
                if nextNode== '29' :
                    return 'l'
                if nextNode=='34':
                    return 'r'
            
            if(currNode=='28' and prevNode=='34'):
                if nextNode== '22' :
                    return 'l'
                if nextNode=='29':
                    return 'r'
            
            if(currNode=='29' and prevNode=='28'):
                if nextNode== '23' :
                    return 'l'
                if nextNode=='35':
                    return 'r'
            
            if(currNode=='29' and prevNode=='23'):
                if nextNode== '35' :
                    return 'l'
                if nextNode=='28':
                    return 'r'
            
            if(currNode=='29' and prevNode=='35'):
                if nextNode== '28' :
                    return 'l'
                if nextNode=='23':
                    return 'r'
            
            if(currNode=='30' and prevNode=='24'):
                if nextNode=='36':
                    return 'r'
            
            if(currNode=='30' and prevNode=='36'):
                if nextNode== '24' :
                    return 'l'
            
            if(currNode=='31' and prevNode=='32'):
                if nextNode== '37' :
                    return 'l'
                if nextNode=='25':
                    return 'r'
            
            if(currNode=='31' and prevNode=='37'):
                if nextNode== '25' :
                    return 'l'
                if nextNode=='32':
                    return 'r'
            
            if(currNode=='31' and prevNode=='25'):
                if nextNode== '32' :
                    return 'l'
                if nextNode=='37':
                    return 'r'
            
            if(currNode=='32' and prevNode=='31'):
                if nextNode== '26' :
                    return 'l'
                if nextNode=='38':
                    return 'r'
            
            if(currNode=='32' and prevNode=='26'):
                if nextNode== '38' :
                    return 'l'
                if nextNode=='31':
                    return 'r'
            
            if(currNode=='32' and prevNode=='38'):
                if nextNode== '31' :
                    return 'l'
                if nextNode=='26':
                    return 'r'
            
            if(currNode=='33' and prevNode=='39'):
                if nextNode== '27' :
                    return 'l'
                if nextNode=='24':
                    return 'r'
                    
            if(currNode=='33' and prevNode=='34'):
                if nextNode== '39' :
                    return 'l'
                if nextNode=='27':
                    return 'r'
                    
            if(currNode=='33' and prevNode=='27'):
                if nextNode== '34' :
                    return 'l'
                if nextNode=='39':
                    return 'r'
                    
            if(currNode=='34' and prevNode=='33'):
                if nextNode== '28' :
                    return 'l'
                if nextNode=='40':
                    return 'r'
                    
            if(currNode=='34' and prevNode=='40'):
                if nextNode== '33' :
                    return 'l'
                if nextNode=='28':
                    return 'r'
                    
            if(currNode=='34' and prevNode=='28'):
                if nextNode== '40' :
                    return 'l'
                if nextNode=='33':
                    return 'r'
                    
            if(currNode=='35' and prevNode=='36'):
                if nextNode== '41' :
                    return 'l'
                if nextNode=='29':
                    return 'r'
                    
            if(currNode=='35' and prevNode=='29'):
                if nextNode== '36' :
                    return 'l'
                if nextNode=='41':
                    return 'r'
                    
            if(currNode=='35' and prevNode=='41'):
                if nextNode== '29' :
                    return 'l'
                if nextNode=='36':
                    return 'r'
                    
            if(currNode=='36' and prevNode=='42'):
                if nextNode== '35' :
                    return 'l'
                if nextNode=='30':
                    return 'r'
                    
            if(currNode=='36' and prevNode=='35'):
                if nextNode== '30' :
                    return 'l'
                if nextNode=='42':
                    return 'r'
                    
            if(currNode=='36' and prevNode=='30'):
                if nextNode== '42' :
                    return 'l'
                if nextNode=='35':
                    return 'r'
                    
            if(currNode=='37' and prevNode=='31'):
                if nextNode== '43' :
                    return 'l'
                if nextNode=='':
                    return 'r'
                    
            if(currNode=='37' and prevNode=='43'):
                if nextNode== '' :
                    return 'l'
                if nextNode=='43':
                    return 'r'
                    
            if(currNode=='38' and prevNode=='39'):
                if nextNode== '44' :
                    return 'l'
                if nextNode=='32':
                    return 'r'
                    
            if(currNode=='38' and prevNode=='44'):
                if nextNode== '32' :
                    return 'l'
                if nextNode=='39':
                    return 'r'
                    
            if(currNode=='38' and prevNode=='32'):
                if nextNode== '39' :
                    return 'l'
                if nextNode=='44':
                    return 'r'
                    
            if(currNode=='39' and prevNode=='38'):
                if nextNode== '33' :
                    return 'l'
                if nextNode=='45':
                    return 'r'
                    
            if(currNode=='39' and prevNode=='45'):
                if nextNode== '38' :
                    return 'l'
                if nextNode=='33':
                    return 'r'
                    
            if(currNode=='39' and prevNode=='33'):
                if nextNode== '45' :
                    return 'l'
                if nextNode=='38':
                    return 'r'

            if(currNode =='40' and prevNode =='34'):
                if nextNode == '41' :
                    return 'l'
                if nextNode == '46':
                    return 'r'

            if(currNode =='40' and prevNode =='41'):
                if nextNode == '46' :
                    return 'l'
                if nextNode == '34':
                    return 'r'

            if(currNode =='40' and prevNode =='46'):
                if nextNode == '34' :
                    return 'l'
                if nextNode == '41':
                    return 'r'