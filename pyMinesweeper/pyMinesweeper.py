#Python Minesweeper
import random
import tkinter as tk
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring
from turtle import color



def printBoard(size, playerBoard):
    print("\t ", end="")
    for i in range (size):
        print(i+1, end=" ")
    print("\n\n")
    for i in range(size):
        print(i+1, end="\t|") # row numbers
        for j in range(size):
            print(playerBoard[i][j], end=" ")
        print()
    print()
    
def generateBoard(gameBoard, numMines): # randomly place the mines in the board
    for i in range(numMines):
        gameBoard[random.randint(0, size-1)][random.randint(0, size-1)] = "M"

def checkSurround(gameBoard, x, y): #check if there is mine in area around spot
    mines = 0
    for i in range((y-1), (y+2)):
          for j in range((x-1), (x+2)):
              if (i >= 0 and i < size and j >= 0 and j < size and (i != y or j != x)):
                if gameBoard[i][j] == "M":
                      mines += 1
    return mines

def addNums(gameBoard):
    for i in range(size):
        for j in range(size):
            if (checkSurround(gameBoard, i, j) > 0 and gameBoard[j][i] != "M"):
                gameBoard[j][i] = checkSurround(gameBoard, i, j)
            
            
def startBoard(playerBoard, gameBoard): # pick random spot and clear 
    x = random.randint(1, size-2) # random spot but not on the edge
    y = random.randint(1, size-2)
    while gameBoard[y][x] == "M": # make sure spot picked isnt a mine
        x = random.randint(1, size-2)
        y = random.randint(1, size-2)
    clearArea(playerBoard, gameBoard, x, y)
                      
def clearArea(playerBoard, gameBoard, x, y):
    playerBoard[y][x] = gameBoard[y][x]
    for i in range((y-1), (y+2)):
        for j in range((x-1), (x+2)):
              if (i >= 0 and i < size and j >= 0 and j < size and (i != y or j != x)):
                if gameBoard[i][j] != "M":
                      if gameBoard[i][j] == 0 and playerBoard[i][j] == "X" and clearedBoard[i][j] == 0:
                          clearedBoard[i][j] = 1 # mark spot as cleared
                          clearArea(playerBoard, gameBoard, j, i) # recursively clear area since there are no mines around
                          playerBoard[i][j] = gameBoard[i][j]
                      elif gameBoard[i][j] != 0 and playerBoard[i][j] == "X" and clearedBoard[i][j] == 0:
                          playerBoard[i][j] = gameBoard[i][j] # if there is a number, place it in the board
                          # dont recursively clear area since there are mines around
                          clearedBoard[i][j] = 1 # mark spot as cleared
                          
def checkSpot(playerBoard, gameBoard, x, y):
    if playerBoard[y][x] == "X":
        playerBoard[y][x] = gameBoard[y][x]
        if gameBoard[y][x] == "M":
            print("You lost!")
            global won
            won = True # game over
            global lost
            lost = True
            
def clearSpot(playerBoard, gameBoard, x, y):
    checkSpot(playerBoard, gameBoard, x, y)
    global won
    if won == False: # only run these if spot wasnt mine
        clearArea(playerBoard, gameBoard, x, y) # if area is clear, clear area around spot
    if playerBoard == gameBoard:
        print("You won!")
        won = True # end game

def flagSpot(playerBoard, gameBoard, x, y):
    global won
    if playerBoard[y][x] == "X":
        playerBoard[y][x] = "F"
        if gameBoard[y][x] == "M":
            gameBoard[y][x] = "F"
    elif playerBoard[y][x] == "F":
        playerBoard[y][x] = "X"
        if gameBoard[y][x] == "F":
            gameBoard[y][x] = "M"
    
    if playerBoard == gameBoard:
        print("You won!")
        won = True # end game

def click(playerBoard, gameBoard, x, y, callback):
    print("x: ", x, "y: ", y)
    if mode == 1:
        flagSpot(playerBoard, gameBoard, x, y)
    elif mode == 0:
        clearSpot(playerBoard, gameBoard, x, y)
     
    printBoard(size, playerBoard)
    printBoard(size, gameBoard)
    callback(playerBoard, gameBoard, size) # update board after click
    
def revealMines(playerBoard, gameBoard, size):
    for i in range(size):
        for j in range(size):
            if gameBoard[i][j] == "M" and playerBoard[i][j] != "F":
                playerBoard[i][j] = "M"
    updateBoard(playerBoard, gameBoard, size)



window = tk.Tk()
window.title("Minesweeper")
window.aspect(1, 1, 1, 1)
window.resizable = (False,False)

size = 0

def changeMode(m):
    global mode
    mode = m
    print("Mode: ", mode)
 
def numberColor(num): 
    # blue for 1, green for 2, red for 3, purple for 4
    color="black"
    if num == 1:
        color="blue"
    elif num == 2:
        color="green"
    elif num == 3:
        color="red"
    elif num == 4:
        color="purple"
    return color
        
def updateBoard(playerBoard, gameBoard, size):
    global mode
    flag = tk.Button(window, width=2, text="Flag", command=lambda: changeMode(1))
    flag.grid(row=0, column=int((size/2) - 2))
    check = tk.Button(window, width=2, text="Check", command=lambda: changeMode(0))
    check.grid(row=0, column=int((size/2) + 2))
    # create grid of buttons 
    for x in range(size):
        for y in range(size):
            if playerBoard[y][x] == "X":
                btn = tk.Button(window, text=" ", width=2, command=lambda x=x, y=y: click(playerBoard, gameBoard, x, y, updateBoard))
                btn.grid(row=y+2, column=x)
            elif playerBoard[y][x] == "F":
                btn = tk.Button(window, text=playerBoard[y][x], width=2, command=lambda x=x, y=y: click(playerBoard, gameBoard, x, y, updateBoard))
                btn.grid(row=y+2, column=x)
            elif playerBoard[y][x] in range(9):
                btn = tk.Button(window, text=playerBoard[y][x], width=2, relief="flat", state="disabled", disabledforeground=numberColor(playerBoard[y][x]))
                if playerBoard[y][x] == 0:
                    btn.config(text=" ")
                btn.grid(row=y+2, column=x)
            elif playerBoard[y][x] == "M":
                btn = tk.Button(window, text=playerBoard[y][x], width=2, relief="flat", state="disabled", disabledforeground="red")
                btn.grid(row=y+2, column=x)
  
gameBoard = [[0 for x in range(size)] for y in range(size)] # generate the board with the mines
playerBoard = [["X" for x in range(size)] for y in range(size)] # board the player sees
clearedBoard = [[0 for x in range(size)] for y in range(size)] # board that marks if spot has been checked to be cleared
numMines = size * size // 7
won = False
lost = False
mode = 0 # whether to check or flag spot, 0 is check, 1 is flag   

def isInt(i):
    try:
        int(i)
        return True
    except ValueError:
        return False
def getSize():
    size = askstring("Board Size", "Enter board size",parent=window)
    while isInt(size) == False or int(size) < 6 or int(size) > 25:
        tk.messagebox.showerror("Error", "Please enter a number between 5 and 25")
        size = askstring("Board Size", "Enter board size",parent=window)
    return int(size)

def initGame():
    global playerBoard
    global gameBoard
    global clearedBoard
    global won
    global lost
    global size
    won = False
    lost = False
    window.update_idletasks()
    size = getSize()
    gameBoard = [[0 for x in range(size)] for y in range(size)] # generate the board with the mines
    playerBoard = [["X" for x in range(size)] for y in range(size)] # board the player sees
    clearedBoard = [[0 for x in range(size)] for y in range(size)] # board that marks if spot has been checked to be cleared
    numMines = size * size // 7
    generateBoard(gameBoard, numMines)  # place mines
    addNums(gameBoard) # add the numbers
    startBoard(playerBoard, gameBoard) # make the board the player sees
    for widget in window.winfo_children():
        widget.destroy()
    updateBoard(playerBoard, gameBoard, size) # make the window with the board
                
initGame()
while won == False:
    
    window.update_idletasks()
    window.update()
    if lost == True:
        revealMines(playerBoard, gameBoard, size)
    if (won == True and lost == True):
        window.update_idletasks()
        answer = askyesno("Game Over", "You lost! Play again?",parent=window)
        if answer == True:
            initGame()
        else:
            break
    elif (won == True and lost == False):
        window.update_idletasks()
        answer = askyesno("Game Over", "You won! Play again?",parent=window)
        if answer == True:
            initGame()
        else:
            break
                
    
        
        
    
    