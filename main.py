# this is the first algorithm to find the best path its brute force 

import tkinter as tk
import random
import time
import itertools
import math

pointsAmount = int( input("the amount of points:"))
SPREAD_MAX = 10 

spread_input = int(input("the strength of the spread 1-{}:".format(SPREAD_MAX)))

if spread_input < 4:
    spread_input = 4
spread = 1 if spread_input < 1 else 10 if spread_input > 10 else spread_input




canvasWidth = 1000
CanvasHeight = 750


root = tk.Tk()

root.geometry("1200x750")
root.resizable(False, False)


text_widget = tk.Text(root)
text_widget.place(x = 0,y=0,height=750,width=200)

canvas = tk.Canvas(root, width=canvasWidth, height=CanvasHeight)
canvas.place(x=200)

class Point:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.radius = 5
        self.color = "black"
    def getCordinates(self):
        return self.x , self.y
    def draw(self):
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        canvas.create_oval(x1,y1,x2,y2,fill = self.color)
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
    point.draw()
permutations = itertools.permutations(pointsList)
shortestPathLength = None
shortestPath = []
input()
def update(last_time):
    global shortestPathLength
    global shortestPath
    current_time = time.time()
    try:
        permutation = next(permutations)
    except StopIteration:
        for i,point in enumerate(shortestPath):
            nextPoint = None
            if(len(shortestPath)-1 == i):
                nextPoint = shortestPath[0]
            else:
                nextPoint = shortestPath[i+1]

            canvas.create_line(point.getCordinates()[0], point.getCordinates()[1], nextPoint.getCordinates()[0], nextPoint.getCordinates()[1], fill="black", width=5)

        return
    
    delta_time = current_time - last_time
    pathLength = 0
    for i,point in enumerate(permutation):
        length = 0
        nextPoint = None
        if(len(permutation)-1 == i):
            nextPoint = permutation[0]
        else:
            nextPoint = permutation[i+1]
        x,y = point.getCordinates()[0]-nextPoint.getCordinates()[0],point.getCordinates()[1]-nextPoint.getCordinates()[1]
        length = math.sqrt(x**2+y**2)   
           
        pathLength += length
    if ( shortestPathLength is None):
        shortestPathLength = pathLength
        shortestPath = permutation
    elif(shortestPathLength >pathLength):
        shortestPathLength = pathLength
        shortestPath = permutation
        
        canvas.delete("line")
        for i,point in enumerate(shortestPath):
            nextPoint = None
            if(len(shortestPath)-1 == i):
                nextPoint = shortestPath[0]
            else:
                nextPoint = shortestPath[i+1]

            canvas.create_line(point.getCordinates()[0], point.getCordinates()[1], nextPoint.getCordinates()[0], nextPoint.getCordinates()[1], fill="black", width=5, tags="line")


    
    root.after(1000 // 800, update, current_time)  

update(time.time())



root.mainloop()
