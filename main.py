#Ameisen Ansatz

import tkinter as tk
import random
import math
import time

#pointsAmount = int( input("the amount of points:"))
SPREAD_MAX = 10 
pointsAmount = 100
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

class Point:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.radius = 1
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
                return
            pointX , pointY = point.getCordinates()
            distanceX = self.x -pointX 
            distanceY = self.y -pointY
            distance = math.sqrt(distanceX**2 + distanceY**2)
            pointDistanceList.append([point,distance,1])
            self.sortedPointDistanceList = quickSortPointDistance(pointDistanceList)
    def getSortedDistancePointList(self):
        return self.sortedPointDistanceList
class Agent:
    def __init__(self,startPoint) -> None:
        self.curPoint = startPoint
        self.path = [startPoint]
        self.pathLength = 0
    def move(self):
        weights = self.curPoint.getSortedDistancePointList()
        while True:
            for con in weights:
                if random.random() < 1/pointsAmount*weights[2]:

                    return
        
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

def update():


    root.after(1000 // 1000, update) 

update()  


root.mainloop()
