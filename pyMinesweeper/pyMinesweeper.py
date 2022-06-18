#Python Minesweeper
from multiprocessing import get_all_start_methods
import random

size = int(input("Input board size: ")) 
gameBoard = [[0 for x in range(size)] for y in range(size)] # generate the board with the mines
playerBoard = [[0 for x in range(size)] for y in range(size)] # board the player sees
numMines = size * size // 6

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

printBoard(size, gameBoard)

def generateBoard(gameBoard, numMines): # randomly place the mines in the board
    for i in range(numMines):
        gameBoard[random.randint(0, size-1)][random.randint(0, size-1)] = "M"

def checkSurround(gameBoard, x, y): #check if there is mine in area around spot
      for i in range((y-1), (y+2)):
          for j in range((x-1), (x+2)):
              if (i >= 0 and i < size and j >= 0 and j < size and (i != y or j != x)):
                if gameBoard[i][j] == "M":
                      print("yes")
                else:
                      print("no") 

def addNums(gameBoard):
    for i in range(size):
        for j in range(size):
            
#def startBoard(playerBoard, GameBoard): # pick random spot and clear 
    
generateBoard(gameBoard, numMines)
printBoard(size, gameBoard)

#checkSurround(gameBoard, int(input("x")) -1, int(input("y")) -1)
