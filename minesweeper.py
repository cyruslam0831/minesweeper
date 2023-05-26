from tkinter import *
from random import *
from tkinter import messagebox


def gameStart():
    global gameStarted, numBomb, gameOver, gameVictory, bombRemaining, realBombRemaining, numRevealed
    setting.destroy()
    main = Tk()
    main.title("Minesweeper Game")
    main.resizable(FALSE, FALSE)  
    #print(mapWidth)
    #print(mapHeight)
    gameStarted = False
    gameOver = False
    gameVictory = False
    realBombRemaining = numBomb
    bombRemaining = numBomb
    numRevealed = 0
    
    def checkVictory():
        global gameOver, gameVictory, mapWidth, mapHeight
        if ((numRevealed + numBomb == mapHeight * mapWidth) or (bombRemaining == realBombRemaining == 0)) and not gameOver:
            gameOver = True
            gameVictory = True
            gameWon()
    
    def genBomb(pressedx, pressedy): # Generate bombs on the map, excluding the first grid and those nearby
        global mapHeight, mapWidth, numBomb, bomb
        safe = [i for i in range(mapWidth * mapHeight)]
        bomb = []
        
        # Exclude first grid and those nearby
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= pressedx + i and pressedx + i <= mapHeight - 1 and 0 <= pressedy + j and pressedy + j <= mapWidth - 1:
                    print((pressedx + i), (pressedy + j))
                    safe.remove((pressedx + i) * mapWidth + (pressedy + j))
                    
        # Generate bombs randomly from the safe list, removing them from the safe list while doing so
        for i in range(numBomb):
            selected = int(random() * (mapWidth * mapHeight - i - 9))
            #print(i, safe[selected] // mapWidth, safe[selected] % mapWidth)
            gameGrid[safe[selected] // mapWidth][safe[selected] % mapWidth].isBomb = True
            #gameGrid[safe[selected] // mapWidth][safe[selected] % mapWidth].interact.config(bg="red")
            bomb.append(safe[selected])
            safe.remove(safe[selected])
            
    # Popup message for winning, reveal all grids
    def gameWon():
        for i in range(mapHeight):
            for j in range(mapWidth):
                gameGrid[i][j].revealGrid()
        response = messagebox.askyesno("CONGRATULATIONS!", "You win! Play again?")
        main.destroy()
        if response == 1:
            gameSetting()
            
    
    def showBomb(): # Show all bombs in about 1.25 sec one by one
        global bomb, mapWidth, realBombRemaining
        bombShow = bomb.pop()
        delay = int(random() * 2500 / realBombRemaining)
        gameGrid[bombShow // mapWidth][bombShow % mapWidth].interact.config(text="💥", fg="red")
        gameGrid[bombShow // mapWidth][bombShow % mapWidth].isRevealed = True
        if len(bomb) > 0:
            main.after(delay, showBomb)
        else:
            for i in range(mapHeight):
                for j in range(mapWidth):
                    gameGrid[i][j].revealGrid()
            response = messagebox.askyesno("GAME OVER!", "You lose! Play again?")
            main.destroy()
            if response == 1:
                gameSetting()
            
        
    def gameLost():
        global gameOver, mapWidth
        gameOver = True
        showBomb()
        
    def calBomb(): # Calculate the number of nearby bombs for all grids
        global mapHeight, mapWidth
        for i in range(mapHeight):
            for j in range(mapWidth):
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if i + k >= 0 and i + k <= mapHeight - 1 and j + l >= 0 and j + l <= mapWidth - 1 and (k != 0 or l != 0) and gameGrid[i + k][j + l].isBomb:
                            gameGrid[i][j].nearbyBomb += 1
                          
                #print(gameGrid[i][j].nearbyBomb)
                #gameGrid[i][j].interact.config(text=gameGrid[i][j].nearbyBomb)
                                    

    def drawMap():
        global mapHeight, mapWidth, numBomb, lbl6
        for i in range(mapHeight):
            for j in range(mapWidth):
                gameGrid[i][j].interact.grid(row=i, column=j)
                
        lbl6 = Label(main, text="Bombs Remaining: " + str(bombRemaining), anchor=E, font=("Courier New", 11))
        lbl6.grid(row=mapHeight+1, column=0, columnspan=mapWidth, sticky=E)
        #lbl6.bind("<Button-3>", lambda event: print("!"))

    class gridStat():
        row = 0
        column = 0
        isFlagged = False
        isBomb = False
        isRevealed = False
        nearbyBomb = 0
        interact = Button()
        
        def pressed(self):
            global gameStarted, gameOver
            #print(self.row, self.column)
            if not gameOver:
                if not gameStarted:
                    genBomb(self.row, self.column)
                    calBomb()
                    gameStarted = True
                self.revealGrid()
            if self.isRevealed:
                #print(self.nearFlag())
                if self.nearbyBomb == self.nearFlag():
                    self.revealNear()
                
            elif self.nearFlag() == self.nearbyBomb and not self.isFlagged:
                self.revealNear()
                
        
        def revealNear(self):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (self.row + i >= 0 and 
                        self.row + i <= mapHeight - 1 and 
                        self.column + j >= 0 and 
                        self.column + j <= mapWidth - 1 and
                        (i != 0 or j != 0)):
                            gameGrid[self.row + i][self.column + j].revealGrid()
        
        def nearFlag(self):
            temp = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (self.row + i >= 0 and 
                        self.row + i <= mapHeight - 1 and 
                        self.column + j >= 0 and 
                        self.column + j <= mapWidth - 1 and 
                        gameGrid[self.row + i][self.column + j].isFlagged):
                            temp += 1
            return temp
            
        def flag(self):
            global bombRemaining, lbl6, realBombRemaining, mapWidth, gameVictory
            if (gameVictory or not self.isRevealed) and gameStarted: 
                self.isFlagged = not self.isFlagged
                if self.isFlagged:
                    self.interact.config(text="🚩",fg="red")
                    bombRemaining -= 1
                    if self.isBomb:
                        realBombRemaining -= 1
                        bomb.remove(self.row * mapWidth + self.column)
                else:
                    self.interact.config(text="", fg="black")
                    bombRemaining += 1
                    if self.isBomb:
                        realBombRemaining += 1
                        bomb.insert(int(random()*len(bomb)), self.row * mapWidth + self.column)
            lbl6.config(text="Bombs Remaining: " + str(bombRemaining))
            checkVictory()
        
        def bombColor(self):
            color = [None, "#0000AA", "#00AA00", "#CC0000", "#000088", "#008800", "#000088", "#004400", "#440000"]
            self.interact.config(fg=color[self.nearbyBomb])
        
        def revealGrid(self):
            global gameOver, gameVictory, bomb, numRevealed
            if (gameOver and not self.isRevealed) or (not self.isFlagged and not self.isRevealed):
                self.isRevealed = True
                numRevealed += 1
                if self.isBomb and not self.isFlagged and not gameOver:
                    self.interact.config(text="💥", fg="black", bg="red")
                    #print(bomb)
                    #print(self.row * mapWidth + self.column)
                    bomb.remove(self.row * mapWidth + self.column)
                    gameLost()
                elif gameVictory and not self.isFlagged and self.isBomb:
                    self.flag()
                elif not self.isFlagged and self.nearbyBomb == 0 and (gameVictory or not gameOver):
                    self.interact.config(bg="#dddddd")
                    self.revealNear()
                elif gameOver and self.isFlagged and not self.isBomb:
                    self.interact.config(fg="#888888")
                elif not self.isFlagged and (gameVictory or not gameOver) and not self.isBomb:
                    self.interact.config(text=self.nearbyBomb, bg="#dddddd")
                    self.bombColor()
                checkVictory()
        
        def __init__(self, r, c):
            self.row = r
            self.column = c
            self.interact = Button(main, width=2, height=1, font=("Courier New Bold",  11), command=self.pressed)
            self.interact.bind("<Button-3>", lambda event: self.flag())
        
    gameGrid = [[gridStat(i, j) for j in range(mapWidth)] for i in range(mapHeight)]

    drawMap()
    
    main.mainloop()
    
# Game Setting Window
def gameSetting():
    global mapHeightSlider, mapWidthSlider, bombDensitySlider, setting, btn2
    setting = Tk()
    setting.title("Game Settings")
    setting.resizable(FALSE, FALSE)
    lbl1 = Label(setting, width=36, font=("Courier New",20), text="Minesweeper", anchor=CENTER)
    lbl1.grid(row=0, column=0, columnspan=4, sticky=N+E)
    lbl2 = Label(setting, text="Map Width: ", anchor=E, width=4)
    lbl2.grid(row=1, column=0, sticky=E+W)
    lbl3 = Label(setting, text="Map Height: ", anchor=E, width=4)
    lbl3.grid(row=2, column=0, sticky=E+W)
    lbl5 = Label(setting, text="Bomb Desnity (%): ", anchor=E, width=4)
    lbl5.grid(row=3, column=0, sticky=E+W)
    mapWidthSlider = Scale(setting, from_=8, to=50, orient=HORIZONTAL) # Slider for choosing the map width (8 - 50)
    mapHeightSlider = Scale(setting, from_=8, to=24, orient=HORIZONTAL) # Slider for choosing the map height (8 - 24)
    bombDensitySlider = Scale(setting, from_=15, to=30, orient=HORIZONTAL) # Slider for choosing the bomb density (15% - 30%)
    mapWidthSlider.grid(row=1, column=1, columnspan=3, sticky=E+W, padx=10)
    mapHeightSlider.grid(row=2, column=1, columnspan=3, sticky=E+W, padx=10)
    bombDensitySlider.grid(row=3, column=1, columnspan=3, sticky=E+W, padx=10)
    btn1 = Button(setting, text="Confirm Map Settings", command=mapSize) # Confirm Map Settings button
    btn1.grid(row=4, column=1, columnspan=2, sticky=E+W, pady=20)
    btn2 = Button(setting, text="< Start Game! >", command=lambda: gameStart()) # Game Start button, destroys the setting screen
    setting.mainloop()

def mapSize(): # Confirm the map size, and determine the number of bombs
    global mapHeight, mapWidth, numBomb
    mapHeight = mapHeightSlider.get()
    mapWidth = mapWidthSlider.get()
    bombDensity = bombDensitySlider.get()
    numBomb = int(mapHeight * mapWidth * bombDensity / 500) * 5 # No. of bombs must be multiples of 5
    lbl4 = Label(setting, text= "No. of Bombs: ", anchor=E, width=4)
    lbl5 = Label(setting, text=numBomb, anchor=W)
    lbl4.grid(row=5, column=0, sticky=E+W, pady=10)
    lbl5.grid(row=5, column=1, columnspan=3, sticky=E+W, padx=10, pady=10)
    btn2.grid(row=6, column=1, columnspan=2, sticky=E+W, pady=20)

gameSetting()
