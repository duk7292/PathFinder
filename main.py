#Ameisen Ansatz

import tkinter as tk
import random
import math
import time

#pointsAmount = int( input("the amount of points:"))
SPREAD_MAX = 10 
pointsAmount = 10
agentAmountPerGen = 50
curGen = 0
gensWithSamePath = 0
GEN_STOP = 10
#spread_input = int(input("the strength of the spread 1-{}:".format(SPREAD_MAX)))
#spread = 1 if spread_input < 1 else 10 if spread_input > 10 else spread_input
spread = 7




canvasWidth = 1000
CanvasHeight = 750
MAX_DISTANCE = math.sqrt(canvasWidth**2 + CanvasHeight **2)

root = tk.Tk()

root.geometry("1000x750")
root.resizable(False, False)



canvas = tk.Canvas(root, width=canvasWidth, height=CanvasHeight)
canvas.pack()
#functions 

def quickSortPointDistance(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2][1]
    left = [x for x in arr if x[1] < pivot]
    middle = [x for x in arr if x[1] == pivot]
    right = [x for x in arr if x[1] > pivot]
    return quickSortPointDistance(right) + middle + quickSortPointDistance(left)
def quicksort_agents(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2].getPathInfo()[1]
    left = [x for x in arr if x.getPathInfo()[1] < pivot]
    middle = [x for x in arr if x.getPathInfo()[1] == pivot]
    right = [x for x in arr if x.getPathInfo()[1] > pivot]
    return quicksort_agents(left) + middle + quicksort_agents(right)
class Point:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.radius = 3
        self.color = "black"
        self.sortedPointDistanceList = []
    def getCordinates(self):
        return self.x , self.y
    def draw(self):
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        canvas.create_oval(x1,y1,x2,y2,fill = self.color)

    def calculateSortedPointList(self,pointsList):
        
        pointDistanceList = []
        for point in pointsList:
            if point == self:
                continue
            pointX , pointY = point.getCordinates()
            distanceX = self.x -pointX 
            distanceY = self.y -pointY
            distance = math.sqrt(distanceX**2 + distanceY**2)
            pointDistanceList.append([point,distance,1])
            self.sortedPointDistanceList = quickSortPointDistance(pointDistanceList)
    def addWeight(self,i,addedWeight):
        self.sortedPointDistanceList[i][2] += addedWeight

    def getSortedDistancePointList(self):
        return self.sortedPointDistanceList
class Agent:
    def __init__(self,startPoint) -> None:
        self.startPoint = startPoint
        self.curPoint = startPoint
        self.path = []
        self.pathLength = 0
    def move(self,step):
        weights = self.curPoint.getSortedDistancePointList()
        while True:
            for con in weights:
                
                if random.random() < 1/pointsAmount*con[2]:
                    
                    if (con[0] in self.path ):

                        continue
                    self.curPoint = con[0]
                    self.pathLength += con[1]
                    self.path.append(self.curPoint)
                    return
        
    def getPathInfo(self):
        return self.path , self.pathLength
        
pointsList=[Point(canvasWidth/2,CanvasHeight/2)]

#fill the point list randomly with the parameters spread and pointsAmount

for newPoint in range(pointsAmount-1):
    # calculate the new Points Coordinates based on the spread Parameter and the mid Point
    startX,startY = pointsList[0].getCordinates()

    xSpaceSize = int(canvasWidth / SPREAD_MAX * spread /2)
    ySpaceSize = int(CanvasHeight / SPREAD_MAX * spread /2)

    newX = random.randint(startX-xSpaceSize,startX+xSpaceSize)
    newY = random.randint(startY-ySpaceSize,startY+ySpaceSize)
    pointsList.append(Point(newX,newY))

for point in pointsList:
    
    point.calculateSortedPointList(pointsList)
    point.draw()
agentsList = []
for newAgent in range(agentAmountPerGen):
    agentsList.append(Agent(pointsList[0]))
def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb
shortestPath = []
shortestPathLength = None
def update():
    global shortestPath
    global shortestPathLength
    global agentsList
    for step in range(pointsAmount):
        for agent in agentsList:
            agent.move(step)
                 
             
    sortedAgents = quicksort_agents(agentsList)

    for j,agent in enumerate(sortedAgents[3:]):
        takenPath = agent.getPathInfo()[0]
        for i,point in enumerate(takenPath):
            nextPoint = takenPath[0]
            
            if(i != len(takenPath)-1):
                nextPoint = takenPath[i+1]
            for k,point2 in enumerate(point.getSortedDistancePointList()):
                if point2[0] == nextPoint:
                    point.addWeight(k,1/((j+1)*20))


    bestPath , bestPathLength =  sortedAgents[0].getPathInfo()
    if ( shortestPathLength is None or bestPathLength < shortestPathLength ):
        print(bestPathLength)
       
        
    '''   shortestPathLength = bestPathLength
        shortestPath = bestPath
        canvas.delete("line")
        for i,point in enumerate(shortestPath):
            nextPoint = None
            if(len(shortestPath)-1 == i):
                nextPoint = shortestPath[0]
            else:
                nextPoint = shortestPath[i+1]

            canvas.create_line(point.getCordinates()[0], point.getCordinates()[1], nextPoint.getCordinates()[0], nextPoint.getCordinates()[1], fill="black", width=5, tags="line")
    '''
    canvas.delete("line")
    for point in pointsList:
        for point2 in point.getSortedDistancePointList():
            print(point2[2])
            canvas.create_line(point.getCordinates()[0], point.getCordinates()[1],point2[0].getCordinates()[0], point2[0].getCordinates()[1],fill = rgb_to_hex((round(255-point2[2]/2),round(255-point2[2]/2),round(255-point2[2]/2))),width=4,tags="line")
    



    agentsList = []
    for newAgent in range(agentAmountPerGen):
        agentsList.append(Agent(pointsList[0]))  
    root.after(1000 // 2, update) 

update()  


root.mainloop()
