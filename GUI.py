import tkinter as tk
from tkinter import messagebox
from time import sleep
import math
import heapq


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def emtpy(self):
        return len(self.elements) == 0

    def put(self, item, value):
        heapq.heappush(self.elements, (value, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class AStar(tk.Tk):
    def __init__(self):
        self.isExistGoal = False
        self.isExistStart = False
        self.isDrawableCanvas = True
        self.isSearched = False
        self.openSearchPos = []
        self.start = None
        self.goal = None
        super().__init__()
        self.title("Search Heuristic")
        # Create a list of button
        self.initButton()
        # Create a 2D array of canvas rectangle
        self.initCanvas()

    def initButton(self):
        # Make a frame and put 4 four button (prev, pause, start, continue)
        frame_btn = tk.Frame(self)
        frame_btn.pack(side=tk.BOTTOM, fill=tk.X)
        self.prev_btn = tk.Button(
            frame_btn, text="Prev", command=self.prevAction)
        self.prev_btn.pack(side=tk.LEFT)
        self.start_btn = tk.Button(
            frame_btn, text="Start", command=self.startAction)
        self.start_btn.pack(side=tk.LEFT)
        self.continue_btn = tk.Button(
            frame_btn, text="Continue", command=self.continueAction)
        self.continue_btn.pack(side=tk.LEFT)
        self.createNew_btn = tk.Button(
            frame_btn, text="Create New", command=self.createNewAction)
        self.createNew_btn.pack(side=tk.LEFT)

    def initCanvas(self):
        # Create a empty canvas
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
        self.rows = 10
        self.columns = 10
        # Make the canvas update their winfos
        self.update_idletasks()
        self.cellwidth = self.canvas.winfo_width() / self.columns
        self.cellheight = self.canvas.winfo_height() / self.rows
        for column in range(self.columns):
            for row in range(self.rows):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
        self.canvas.bind("<B1-Motion>", self.onCreateBarrier)
        self.canvas.bind("<Configure>", self.onResize)
        self.canvas.bind("<Double-Button-2>", self.onCreateStart)
        self.canvas.bind("<Double-Button-3>", self.onCreateGoal)

    def onCreateBarrier(self, event):
        if self.isDrawableCanvas == False:
            return
        else:
            item = self.canvas.find_closest(event.x, event.y)
            current_color = self.canvas.itemcget(item, 'fill')
            sleep(0.01)
            if current_color == 'blue':
                self.canvas.itemconfig(item, fill='grey')
            elif current_color == 'grey':
                self.canvas.itemconfig(item, fill='blue')

    def onCreateGoal(self, event):
        if self.isDrawableCanvas == False:
            return
        else:
            item = self.canvas.find_closest(event.x, event.y)
            current_color = self.canvas.itemcget(item, 'fill')
            if current_color == 'blue' and self.isExistGoal == False:
                self.canvas.itemconfig(item, fill='green')
                self.isExistGoal = True
                self.goal = (math.floor(event.x/self.cellwidth),
                             math.floor(event.y/self.cellheight))
            if current_color == 'green' and self.isExistGoal == True:
                self.canvas.itemconfig(item, fill='blue')
                self.isExistGoal = False
                self.goal = None

    def onCreateStart(self, event):
        if self.isDrawableCanvas == False:
            return
        else:
            item = self.canvas.find_closest(event.x, event.y)
            current_color = self.canvas.itemcget(item, 'fill')
            if current_color == 'blue' and self.isExistStart == False:
                self.canvas.itemconfig(item, fill='yellow')
                self.isExistStart = True
                self.start = (math.floor(event.x/self.cellwidth),
                              math.floor(event.y/self.cellheight))
            if current_color == 'yellow' and self.isExistStart == True:
                self.canvas.itemconfig(item, fill='blue')
                self.isExistStart = False
                self.start = None

    def onResize(self, event):
        widthRatio = self.canvas.winfo_width() / (self.cellwidth * self.columns)
        heightRatio = self.canvas.winfo_height() / (self.cellheight * self.rows)
        self.cellwidth = self.canvas.winfo_width() / self.columns
        self.cellheight = self.canvas.winfo_height() / self.rows
        self.canvas.scale("all", 0, 0, widthRatio, heightRatio)

    def prevAction(self):
        if self.isSearched:
            if self.pos == 0:
                messagebox.showinfo(
                    "Thông báo:", "Không thể lùi lại quá đỉnh xuất phát!")
            else:        
                if self.pos == len(self.openSearchPos):
                    for p in self.path:
                        if p != self.goal and p != self.start:
                            (x, y) = p
                            self.setColor(x, y, "white")
                if self.openSearchPos[self.pos -1] == self.goal:
                    (x, y) = self.goal
                    self.setColor(x, y, "green")
                else:
                    (x, y) = self.openSearchPos[self.pos - 1]
                    self.setColor(x, y, "blue")
                self.pos -= 1
        else:
            tk.messagebox.showinfo("Thông báo:", "Bắt đầu tìm đường!")
            self.searchPath()

    def startAction(self):
        if self.isSearched:
            while self.pos < len(self.openSearchPos):
                self.continueAction()
                self.update_idletasks()
                sleep(0.01)
            messagebox.showinfo("Thông báo:", "Đã mở rộng hết!")
            (x, y) = self.goal
            self.setColor(x, y, "green")
            for p in self.path:
                if p != self.goal and p != self.start:
                    (x, y) = p
                    self.setColor(x, y, "red")
        else:
            tk.messagebox.showinfo("Thông báo:", "Bắt đầu tìm đường!")
            self.searchPath()
            

    def continueAction(self):
        if self.isSearched:
            if self.pos == len(self.openSearchPos):
                messagebox.showinfo("Thông báo:", "Đã mở rộng hết!")
                (x, y) = self.goal
                self.setColor(x, y, "green")
                for p in self.path:
                    if p != self.goal and p != self.start:
                        (x, y) = p
                        self.setColor(x, y, "red")
            else:
                (x, y) = self.openSearchPos[self.pos]
                self.setColor(x, y, "white")
                self.pos += 1
        else:
            tk.messagebox.showinfo("Thông báo:", "Bắt đầu tìm đường!")
            self.searchPath()

    def createNewAction(self):
        for column in range(self.columns):
            for row in range(self.rows):
                self.setColor(column, row, "blue")
        self.isExistGoal = False
        self.isExistStart = False
        self.isDrawableCanvas = True
        self.isSearched = False
        self.openSearchPos = []
        self.start = None
        self.goal = None
        self.pos = None
        
        
    def searchPath(self):
        if self.isExistGoal and self.isExistStart:
            self.path = self.reconstruct_path(
                self.Astar_search(self.start, self.goal), self.start, self.goal)
            self.isSearched = True
            self.pos = 0
            self.isDrawableCanvas = False
        else:
            tk.messagebox.showerror(
                "Lỗi", "Chưa nhập vào điểm đầu và điểm cuối!")

    def getColor(self, x, y):
        xPos = (x + 0.5) * self.cellwidth
        yPos = (y + 0.5) * self.cellheight
        item = self.canvas.find_closest(xPos, yPos)
        return self.canvas.itemcget(item, 'fill')

    def setColor(self, x, y, colour):
        xPos = (x + 0.5) * self.cellwidth
        yPos = (y + 0.5) * self.cellheight
        item = self.canvas.find_closest(xPos, yPos)
        self.canvas.itemconfig(item, fill=colour)

    def h(self, a, b):  # euclid distance heuristic
        (x1, y1) = a
        (x2, y2) = b
        return math.sqrt((x2-x1)**2+(y2-y1)**2)

    def neighbor(self, robot):
        (x, y) = robot
        xplus = [-1, -1, -1, 0, 1, 1, 1, 0]
        yplus = [-1, 0, 1, 1, 1, 0, -1, -1]
        listNeighbor = []
        for i in range(8):
            xx = x+xplus[i]
            yy = y+yplus[i]
            if 0 <= xx < self.rows and 0 <= yy < self.columns and self.getColor(xx, yy) != 'grey':
                listNeighbor.append((xx, yy))
        return listNeighbor

    def Astar_search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        came_from[goal] = None  # neo lai
        cost_so_far[start] = 0
        while not frontier.emtpy():
            current = frontier.get()
            if current == goal:
                break
            for next in self.neighbor(current):
                # Dung list luu cac mo rong
                new_cost = cost_so_far[current] + 1  # chi tinh tren edges thoi
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    self.openSearchPos.append(next)
                    cost_so_far[next] = new_cost
                    value = new_cost + self.h(goal, next)
                    frontier.put(next, value)
                    came_from[next] = current
        return came_from  # cost_so_far

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        if came_from[goal] == None:
            return -1
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()  # optional
        return path


if __name__ == "__main__":
    app = AStar()
    app.mainloop()
