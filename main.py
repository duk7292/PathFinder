import tkinter as tk
import random
import math

#pointsAmount = int( input("the amount of points:"))
SPREAD_MAX = 10 
pointsAmount = 5
antsAmount = 1
#spread_input = int(input("the strength of the spread 1-{}:".format(SPREAD_MAX)))
#spread = 1 if spread_input < 1 else 10 if spread_input > 10 else spread_input
spread = 10

PROBABILITY_CONSTANT = 3

rate = 0.1
target = 1+(1-(PROBABILITY_CONSTANT))

canvasWidth = 1000
CanvasHeight = 750




root = tk.Tk()

root.geometry("1000x750")
root.resizable(False, False)




canvas = tk.Canvas(root, width=canvasWidth, height=CanvasHeight)
canvas.place(x=0)
def nextPointCalc(path,curPoint,startPoint):
    def quicksort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2][1]
        left = [x for x in arr if x[1] < pivot]
        middle = [x for x in arr if x[1] == pivot]
        right = [x for x in arr if x[1] > pivot]
        return quicksort(left) + middle + quicksort(right)
   
    curX , curY = curPoint.getCoordinates()
    pointSet = set(pointsList)
    pathSet = set(path)
    openPointsSet=pointSet-pathSet
    openPoints = list(openPointsSet)
    openPointsDistance = []
    for point in openPoints:
        x,y = point.getCoordinates()
        openPointsDistance.append([point,math.sqrt((curX-x)**2+(curY-y)**2)])
    openPointsDistanceSorted = quicksort(openPointsDistance)
    

    
    if(len(path) == pointsAmount or len(path) == 0):
        x,y = startPoint.getCoordinates()
        startPointDistance = (math.sqrt((curX-x)**2+(curY-y)**2))
        nextPoint,nextPointDistance = startPoint,startPointDistance
    else:
        found = False
        while not found:
            for i,point in enumerate(openPointsDistanceSorted):
                if(random.random()<1/(pointsAmount/PROBABILITY_CONSTANT)):
                    nextPoint,nextPointDistance = openPointsDistanceSorted[i][0], openPointsDistanceSorted[i][1]
                    found = True
                    break
                    
            
        
    
    return  nextPoint,nextPointDistance
        
class Point:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.radius = 5
        self.color = "black"
    def getCoordinates(self):
        return self.x , self.y
    def setColor(self,color):
        self.color = color
    def draw(self):
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        canvas.create_oval(x1,y1,x2,y2,fill = self.color)


class Ant:
    def __init__(self,startPoint,id) -> None:
        self.startPoint = startPoint
        self.currentPoint = startPoint
        self.radius = 5
        self.color = "red"
        self.offsetToPoint = 5
        self.path = []
        self.pathLength = 0
        self.id = id
        
    def draw(self):
        canvas.delete("Ant{}".format(self.id))
        x1 = self.currentPoint.getCoordinates()[0]+self.offsetToPoint - self.radius
        y1 = self.currentPoint.getCoordinates()[1] - self.radius
        x2 = self.currentPoint.getCoordinates()[0]+self.offsetToPoint + self.radius
        y2 = self.currentPoint.getCoordinates()[1] + self.radius
        canvas.create_oval(x1,y1,x2,y2,fill = self.color,tags="Ant{}".format(self.id))
    def move(self):
        nextPoint , nextPointDistance = nextPointCalc(self.path,self.currentPoint,self.startPoint)
        self.currentPoint = nextPoint
        self.pathLength += nextPointDistance
        self.path.append(self.currentPoint)
    def killPath(self):
        self.path = []
        self.pathLength = 0
    def getPathInfo(self):
        return self.path , self.pathLength
    def getCurrentPoint(self):
        return self.currentPoint

pointsList=[Point(canvasWidth/2,CanvasHeight/2)]

#fill the point list randomly with the parameters spread and pointsAmount

for newPoint in range(pointsAmount-1):
    # calculate the new Points Coordinates based on the spread Parameter and the mid Point
    startX,startY = pointsList[0].getCoordinates()

    xSpaceSize = int(canvasWidth / SPREAD_MAX * spread /2)
    ySpaceSize = int(CanvasHeight / SPREAD_MAX * spread /2)

    newX = random.randint(startX-xSpaceSize,startX+xSpaceSize)
    newY = random.randint(startY-ySpaceSize,startY+ySpaceSize)
    pointsList.append(Point(newX,newY))

antsList = []
for newAnt in range(antsAmount):
    antsList.append(Ant(pointsList[random.randint(0,pointsAmount-1)],newAnt))

for point in pointsList:
    point.draw()
  
    
def update():
    
    for ant in antsList:
        ant.move()
        ant.draw()
    if(len(antsList[0].getPathInfo()[0])==pointsAmount+1):
            for ant in antsList:
                ant.killPath()
                ant.move()
    for point in pointsList:
        point.draw()    
    
    root.after(10000// 5,update)
    
update()



root.mainloop()
