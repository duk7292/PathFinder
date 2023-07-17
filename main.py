#Ameisen Ansatz

import tkinter as tk
import random
import math
import time

#pointsAmount = int( input("the amount of points:"))
SPREAD_MAX = 10 
pointsAmount = 200
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

class Point:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.radius = 1
        self.color = "black"
        self.weightList = []
    def getCordinates(self):
        return self.x , self.y
    def draw(self):
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        canvas.create_oval(x1,y1,x2,y2,fill = self.color)
    def calculateWeights(self,pointsList):
        for point in pointsList:
            if point == self:
                return
            pointX , pointY = point.getCordinates()
            distanceX = self.x -pointX 
            distanceY = self.y -pointY
            distance = math.sqrt(distanceX**2 + distanceY**2)
            weight = (MAX_DISTANCE - distance) / MAX_DISTANCE * 1000
            self.weightList.append([point,weight ])

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
    point.calculateWeights(pointsList)
    point.draw()

def update():


    root.after(1000 // 1000, update) 

update()  


root.mainloop()
