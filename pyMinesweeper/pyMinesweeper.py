#Python Minesweeper
import random
import tkinter as tk

size = int(input("Input board size: ")) 
gameBoard = [[0 for x in range(size)] for y in range(size)] # generate the board with the mines
playerBoard = [["X" for x in range(size)] for y in range(size)] # board the player sees
clearedBoard = [[0 for x in range(size)] for y in range(size)] # board that marks if spot has been checked to be cleared
numMines = size * size // 7
won = False

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
                          
def checkSpot(playerBoard, gameBoard, x, y): # add handling for already cleared spots later
    if playerBoard[y][x] == "X":
        playerBoard[y][x] = gameBoard[y][x]
        if gameBoard[y][x] == "M":
            print("You lost!")
            won = True # game over
            
        
printBoard(size, gameBoard) # print gameBoard befpre generation
generateBoard(gameBoard, numMines) # generate the board with the mines
addNums(gameBoard) # add numbers to the board
printBoard(size, gameBoard) # print gameBoard after generation and numbers

startBoard(playerBoard, gameBoard) # start the game by randomly picking spot and revealing clear space around it
printBoard(size, playerBoard) # print playerBoard so game can begin

while won == False:
    x = int(input("Input x coordinate: ")) -1
    y = int(input("Input y coordinate: ")) -1
    action = input("Input action (clear or flag): ")
    if action == "clear":
        checkSpot(playerBoard, gameBoard, x, y)
        if won == False: # only run these if spot wasnt mine
            if playerBoard == gameBoard:
                print("You won!")
                won = True # end game
            clearArea(playerBoard, gameBoard, x, y) # if area is clear, clear area around spot
            printBoard(size, playerBoard)
        
    if action == "flag":
        playerBoard[y][x] = "F"
        if gameBoard[y][x] == "M":
            gameBoard[y][x] = "F"
        printBoard(size, playerBoard)
        if playerBoard == gameBoard:
            print("You won!")
            won = True # end game
    elif action != "clear" and action != "flag":
        print("Invalid action")
        printBoard(size, playerBoard)
    
    if won == True:
        break
        
        
    
    