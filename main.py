import tkinter as tk
import random
import math


SPREAD_MAX = 10 
GOODNESS_CONST = 0.8
NEAR_POWER_CONST = 8
MAX_WEIGHT = 5
spread_input = int(input("the strength of the spread 1-{}:".format(SPREAD_MAX)))
spread = 1 if spread_input < 1 else 10 if spread_input > 10 else spread_input
pointsAmount = int( input("the amount of points:"))
antsAmount = int (input("Amount Of Ants :"))




canvasWidth = 1000
CanvasHeight = 750




root = tk.Tk()

root.geometry("1000x750")
root.resizable(False, False)




canvas = tk.Canvas(root, width=canvasWidth, height=CanvasHeight)
canvas.place(x=0)

max_strength = 500


def drawPath(path):
    canvas.delete("line")
    for i,point in enumerate(path):
        nextPoint = path[0]
        if i != len(path)-1:
            nextPoint = path[i+1]
        canvas.create_line(point.getCoordinates(),nextPoint.getCoordinates(),width = 3 ,fill="black",tags ="line")

def getScoreCalculatePoint(p):
    low = None
    high = None
    for ant in antsList:
        pathLength = ant.getPathInfo()[1]
        if(low is None or pathLength < low):
            low = pathLength
        if(high is None or pathLength > high):
            high = pathLength
    dif = high -low

    return low +(dif*p)
   
def recalcScores():
    scoreCalculatePoint =  getScoreCalculatePoint(GOODNESS_CONST)
    for ant in antsList:
        path,pathLength = ant.getPathInfo()
        multiply = (((scoreCalculatePoint / pathLength)-1)/2)+1
        for i,point in enumerate(path):
            nextPoint = path[0]
            if(i != len(path)-1):
                nextPoint = path[i+1]
            multiply_score(point,nextPoint,multiply)


def multiply_score(main_point, sub_point, multiplier):
    global pointScorecard
    for item in pointScorecard:
        if item[0] == main_point:
            for sub_item in item[1]:
                if sub_item[0] == sub_point:
                    sub_item[1] *= multiplier
                    
                    return
def find_score(main_point, sub_point):
    for item in pointScorecard:
        if item[0] == main_point:
            for sub_item in item[1]:
                if sub_item[0] == sub_point:
                    return sub_item[1]
    return 1
def create_scorecard(pointsList):
    global pointScorecard
    pointScorecard = []
    for point in pointsList:
        connections = [[other_point, 1] for other_point in pointsList if other_point != point]
        pointScorecard.append([point, connections])
def nextPointCalc(path,curPoint,startPoint):
   
    curX , curY = curPoint.getCoordinates()
    pointSet = set(pointsList)
    pathSet = set(path)
    openPointsSet=pointSet-pathSet
    openPoints = list(openPointsSet)
    openPointsDistance = []
    for point in openPoints:
        x,y = point.getCoordinates()

        multiplyer =find_score(curPoint,point)
        
        distance = math.sqrt((curX-x)**2+(curY-y)**2)
        score = (((math.sqrt((canvasWidth*spread/10)**2+(CanvasHeight*spread/10)**2))-distance)**NEAR_POWER_CONST)*multiplyer
        openPointsDistance.append([point,distance,score])
    
    

    
    if(len(path) == pointsAmount or len(path) == 0):
        x,y = startPoint.getCoordinates()
        startPointDistance = (math.sqrt((curX-x)**2+(curY-y)**2))
        nextPoint,nextPointDistance = startPoint,startPointDistance
    else:
        sum = 0
        for point in openPointsDistance:
            sum += point[2]
        randomScoreSum = random.random() * sum
        currentscoreSum = 0
        
        for i,point in enumerate(openPointsDistance):
            
            currentscoreSum+=point[2]
            if currentscoreSum >randomScoreSum:
                
                nextPoint,nextPointDistance =point[0], point[1]
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
pointScorecard = []

#fill the point list randomly with the parameters spread and pointsAmount

for newPoint in range(pointsAmount-1):
    # calculate the new Points Coordinates based on the spread Parameter and the mid Point
    startX,startY = pointsList[0].getCoordinates()

    xSpaceSize = int(canvasWidth / SPREAD_MAX * spread /2)
    ySpaceSize = int(CanvasHeight / SPREAD_MAX * spread /2)

    newX = random.randint(startX-xSpaceSize,startX+xSpaceSize)
    newY = random.randint(startY-ySpaceSize,startY+ySpaceSize)
    pointsList.append(Point(newX,newY))

create_scorecard(pointsList)

antsList = []


for newAnt in range(antsAmount):
    antsList.append(Ant(pointsList[random.randint(0,pointsAmount-1)],newAnt))

for point in pointsList:
    point.draw()
bestPath = []
bestPathLength = None
    
def update():
    global bestPath
    global bestPathLength
    for ant in antsList:
        ant.move()
       # ant.draw()
    if(len(antsList[0].getPathInfo()[0])==pointsAmount+1):
        recalcScores()
        for ant in antsList:
            path,pathLength = ant.getPathInfo()
            if(bestPathLength is None or pathLength<bestPathLength):
                bestPath = path
                bestPathLength = pathLength
                drawPath(bestPath)
            #draw_connections()
            ant.killPath()
            ant.move()
        
    for point in pointsList:
        point.draw()    
    
    root.after(10000// 10000,update)
    
update()



root.mainloop()
