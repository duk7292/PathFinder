import tkinter as tk
import random
import math

#pointsAmount = int( input("the amount of points:"))
SPREAD_MAX = 10 
pointsAmount = 100
#spread_input = int(input("the strength of the spread 1-{}:".format(SPREAD_MAX)))
#spread = 1 if spread_input < 1 else 10 if spread_input > 10 else spread_input
spread = 7


canvasWidth = 1000
CanvasHeight = 750


root = tk.Tk()

root.geometry("1200x750")
root.resizable(False, False)


text_widget = tk.Text(root)
text_widget.place(x = 0,y=0,height=750,width=200)

canvas = tk.Canvas(root, width=canvasWidth, height=CanvasHeight)
canvas.place(x=200)
def nextPointCalc(path,curPoint):
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
    return openPointsDistanceSorted[0][0]
        
class Point:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.radius = 5
        self.color = "black"
    def getCoordinates(self):
        return self.x , self.y
    def draw(self):
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        canvas.create_oval(x1,y1,x2,y2,fill = self.color)


class Ant:
    def __init__(self,startPoint) -> None:
        self.startPoint = startPoint
        self.currentPoint = startPoint
        self.radius = 5
        self.color = "red"
        self.offsetToPoint = 5
        self.path = []
    def draw(self):
        canvas.delete("Ant")
        x1 = self.currentPoint.getCoordinates()[0]+self.offsetToPoint - self.radius
        y1 = self.currentPoint.getCoordinates()[1] - self.radius
        x2 = self.currentPoint.getCoordinates()[0]+self.offsetToPoint + self.radius
        y2 = self.currentPoint.getCoordinates()[1] + self.radius
        canvas.create_oval(x1,y1,x2,y2,fill = self.color,tags="Ant")
    def move(self):
        
        self.currentPoint = nextPointCalc(self.path,self.currentPoint)
        self.path.append(self.currentPoint)

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

ant = Ant(pointsList[0])
ant.draw()
for point in pointsList:
    point.draw()
    
    
def update():
    ant.move()
    ant.draw()
    print(len(ant.path))
    root.after(10000// 250,update)
    
update()



root.mainloop()
