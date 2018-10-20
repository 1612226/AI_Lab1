#global variable
grid =[]
sizeOfGrid=0

#function and class
import heapq
class PriorityQueue:
	def __init__(self):
		self.elements=[]

	def empty(self):
		return len(self.elements)==0
	def put(self,item,value):
		heapq.heappush(self.elements,(value,item)) #tham số đầu là cái xét độ ưu tiên
	def get(self):
		return heapq.heappop(self.elements)[1]  #ko chứa 2 phần tử giống nhau và tự update cái nào có value nhỏ hơn
	def topValue(self):
		return self.elements[0][0]
	def topItem(self):
		return self.elements[0][1]

#heuristic
import math
def h(a,b):  #euclid distance heuristic
	(x1,y1) =a
	(x2,y2)=b
	return math.sqrt((x2-x1)**2+(y2-y1)**2)

def neighbor(robot):
	(x,y)=robot
	xplus=[-1,-1,-1,0,1,1,1,0]
	yplus=[-1,0,1,1,1,0,-1,-1]
	listNeighbor = []
	for i in range(8):
		xx=x+xplus[i]
		yy=y+yplus[i]
		if 0<=xx<sizeOfGrid and 0<=yy<sizeOfGrid and grid[xx][yy]!='1':
			listNeighbor.append((xx,yy))
	return listNeighbor

#Anytime Repair A*

#fvalue funtion
def fvalue(state,g,E):
	# print("E ne ne:",E,"\n")
	return g[state]+E*h(state,goal)
def ImprovePath(start,goal,g,E,OPEN,CLOSED,INCONS,came_from):
	tmp=fvalue(goal,g,E)
	while fvalue(goal,g,E)>OPEN.topValue():
		current=OPEN.get()
		CLOSED.append(current)
		for nxt in neighbor(current):
			if nxt not in g:
				g[nxt]=10**9
				came_from[nxt]=current
			if g[nxt]>g[current]+1:  #dung roi, g[current]+1 = new_cost
				g[nxt]=g[current]+1
				came_from[nxt]=current
				if nxt not in CLOSED:
					OPEN.put(nxt,fvalue(nxt,g,E))
				else:
					INCONS.put(nxt,g[nxt]+h(nxt,goal))
	if came_from[goal]==None: #lan sau ko tim duoc duong nao tot hon lan dau
		return -1
	else: 
		return came_from

def ARA(start,goal,E):
    g = {}
    came_from={}
    came_from[start]=None
    came_from[goal]=None
    OPEN = PriorityQueue()
    CLOSED = []
    INCONS = PriorityQueue()
    g[start]=0
    g[goal]=10**9
    OPEN.put(start,fvalue(start,g,E))
    CameFrom=ImprovePath(start,goal,g,E,OPEN,CLOSED,INCONS,came_from);
    duongDi=reconstruct_path(CameFrom)
    print ("Duong di vs E=",E,"\n",duongDi,"\n")
    while E>1:
        E-=0.5
        INCONS.elements+=OPEN.elements
        OPEN.elements.clear()
        while not INCONS.empty():
            state = INCONS.get()
            OPEN.put(state,fvalue(state,g,E))
        CLOSED.clear()
        CameFrom2=ImprovePath(start,goal,g,E,OPEN,CLOSED,INCONS,came_from);
        duongDi2=reconstruct_path(CameFrom2)
        print("DUong di vs E=",E,":\n",duongDi2,"\n")

def reconstruct_path(came_from):
    current = goal
    if came_from==-1:
    	return "DEO co duong nao khac ca, ok\n"
    path = []
    while current != start:
        # print("path current ",current,"\n")
        path.append(current)
        current = came_from[current]

    path.append(start) # optional
    path.reverse() # optional
    return path

#read input
file_obj = open("input.txt","r")
sizeOfGrid = int(file_obj.readline())
iS, jS = map(int,file_obj.readline().split()); #iStart, jStart
iG, jG = map(int,file_obj.readline().split()); #iGoal, jGoal
for line in file_obj:
	grid.append(line.strip().split(' '))
file_obj.close()

#write output
start = (iS,jS) #g_ mean global_
goal = (iG,jG)
E=3

ARA(start,goal,E)
