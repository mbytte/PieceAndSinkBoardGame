"""
Skeleton code for CS114 project 2024: A 3D board game.

This skeleton code for the project is intended as a starting point for students
to get an idea of how they can begin to code the project. You are not required
to use any of the functions in this skeleton code, however you may find some of
the ideas useful. You are however required to have the line:

if __name__ == "__main__":

but you are free to and should modify the lines following this.

None of the functions are implemented yet, so if you would like to
use a particular function, you need to implement it yourself. If you decide not
to use any of the functions, you are free to leave them empty or remove them
from this file. You are also free to alter the function signatures (the name of
the function and its arguments), so if you need to pass more arguments to the
function, or do not need a particular argument, you are also free to add and
remove arguments as you see fit. We provide the function signatures only as a
guide for how we think you can start to approach the project.
"""

#imports
import stdio
import sys
import stdarray


#global variables
turn = 1 #keeps track of who's turn it is (odd = light and even = dark)


#validates if the variables given for the board and gamemode are viable
#returns false if arguements are not viable
#WORKS
def checkArgs(maxRow, maxCol, guiMode):
    #checking if the board is valid
    if(not(int(maxRow) > 7 and int(maxRow) < 11) or not(int(maxCol) > 7 and int(maxCol) < 11)):
        stdio.writeln("ERROR: Illegal argument")
        return False
    
    #checking if the gamemode is one of two arguements (if it is neither then it is false)
    if(guiMode != "1" and guiMode != "0"):
        stdio.writeln("ERROR: Illegal argument")
        return False
    
    #if we get here then the arguements are valid
    return True
    
    
    
#checking if there are either too few or too many arguements
#WORKS
def checkNumArgs(numArgs):
    if(numArgs != 4):
        if(numArgs < 4):
            stdio.writeln("ERROR: Too few arguements")
        else:
            stdio.writeln("ERROR: Too many arguements")
        return False
    
    #if we get here then the number of arguements is correct
    return True


#checks if a sink is in a valid position
#WORKS
def checkSinkRange(maxRow, maxCol, sinkRow, sinkCol):
    #a sink is valid if it is in the outer 3 rows/columns in the table
    #field provided is not on the board
    if((maxRow == sinkRow or maxCol == sinkCol) or ((sinkRow < 0) or (sinkCol < 0)) or ((sinkRow >= maxRow) or (sinkCol >= maxCol))):
        stdio.writeln("ERROR: Field " + str(sinkRow) + " " + str(sinkCol) + " not on board")
        return False
    
    #valid if it is in a correct row OR a correct column
    elif((sinkRow < maxRow and sinkRow >= maxRow - 3) or (sinkRow < 3 and sinkRow >= 0) or (sinkCol < maxCol and sinkCol >= maxCol - 3) or (sinkCol < 3 and sinkCol >= 0)):
        return True
            
    #if we get here, the sink is in the wrong position
    stdio.writeln("ERROR: Sink in the wrong position")
    return False



#checks if a piece is in the correct position
#WORKS
def checkPieceRange(maxRow, maxCol, pieceRow, pieceCol):
    #piece is in the correct position if it is NOT in the first and last three columns and rows
    if((pieceRow < maxRow and pieceRow >= maxRow - 3) or (pieceRow < 3 and pieceRow >= 0) or (pieceCol < maxCol and pieceCol >= maxCol - 3) or (pieceCol < 3 and pieceCol >= 0)):
        stdio.writeln("ERROR: Piece in the wrong position for piece " + str(pieceRow) + " " + str(pieceCol))
        return False
    
    #if we get here, the piece is in the correct position
    return True



#checks if the piece is upright or on its side
#WORKS
def checkPieceUpright(row, col, board):
    #the piece is upright if it occupies one field on the board
    #getting the number of columns and rows on the board
    columnMax = len(board[0][:])
    rowMax = len(board[:][0])
    #getting the value from the piece
    value = (row*columnMax)+col
    
    #making sure that it is not the big piece (D or d)
    if(board[row][col] == 'A' or board[row][col] == 'a'):
        stdio.writeln("True") #is technically always upright because it always is in one field
        return True
    elif(board[row][col] == 'D' or board[row][col] == 'd'):
        stdio.writeln("False") #can never be upright because it is always in 4 fields
        return False
        
    else:
        #running through all the fields to check if value is in any of them
        #means that the field is not upright if so
        for i in range(0, rowMax):
            for j in range (0, columnMax):
                if(board[i][j] == str(value)):
                    stdio.writeln("False")
                    return False
        #if the code gets here then that means there is only one field occuped
        stdio.writeln("True")
        return True



#gets all the field coordinates that a piece occupies
#NO IDEA IF THIS WORKS OR NOT BUT LETS GO WITH NO BUT HAVE HOPE
def getPieceFields(row, col, board):
    #variables
    coords = []
    value = (row*len(board[0][:]))+col
    
    #adding the coords given to the array
    coords.append((row, col))
    
    #getting the coordinates by searching through the board array for any fields that have the same value as the piece
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if(board[i][j] == value):
                coords.append((i,j))    
    
    
    #returning the array of coordinates
    return coords



def validateMove(row, col, direction, board):
    """
    Checks whether the given move is valid by checking that all aspects of the
    move are legal.

    Args:
        row (int): The row of the object to move
        col (int): The column of the object to move
        direction (str): The direction of the move
        board (2D array of str): The game board

    Returns:
        bool: True if the move is valid, False otherwise
    """
    # This function is important for checking whether a move given by a player
    # is valid and can be played, however it may also be useful for determining
    # if a player has valid moves left or not.
    # TODO: implement this function.
    # remove the following line when you add something to this function:
    pass



def doMove(row, col, direction, board, scores, guiMode):
    """
    Executes the given move on the board.

    Args:
        row (int): The row of the object to move
        col (int): The column of the object to move
        direction (str): The direction of the move
        board (2D array of str): The game board
        scores (array of int): The current scores for each player
        gui_mode (bool): The mode of the game, True if gui_mode, False if terminal mode
    """
    # This function may be useful for separating out the logic of doing a move.
    # remove the following line when you add something to this function:
    pass



def generateAllMoves(board):
    """
    Generates a list of all moves (valid or invalid) that could potentially be
    played on the current board.

    Args:
        board (2D array of str): The game board

    Returns:
        array of moves: The moves that could be played on the given board
    """
    # When used with the validate_move function, this function is useful for
    # checking whether a player has a valid move left to play.
    # remove the following line when you add something to this function:
    pass



#reads the arguements given on the first start up of the game and returns them as an array
#WORKS BUT NEEDS ERROR CHECKS 
def readBoard(maxRow, maxCol):
    #variables
    maxRow = int(maxRow)
    maxCol = int(maxCol)
    board = stdarray.create2D(maxRow,maxCol," ")
    
    #getting the line
    piece = stdio.readString()
    
    #running a loop until the next string gotten is #
    while(piece != "#"):
        #gets the coordinates of a specific piece and adds it to the board
        if(piece == "s"):
            #getting the size
            sinkSize = stdio.readInt()
            
            #getting the coordinates
            sinkRow = stdio.readInt()
            sinkCol = stdio.readInt()
            
            #checking if the sink is in the correct position
            if(checkSinkRange(maxRow, maxCol, sinkRow, sinkCol)): #error message is printed in the function
                #checking if the piece is 1x1 or 2x2
                if(sinkSize == 1): #piece is 1x1
                    board[sinkRow][sinkCol] = "s"
                else:  #piece is 2x2
                    #NEED TO VALIDATE IF A SINK OF THIS SIZE CAN FIT IN THE BOARD
                    board[sinkRow][sinkCol] = "s"
                    board[sinkRow][sinkCol + 1] = "s"
                    board[sinkRow + 1][sinkCol] = "s"
                    board[sinkRow + 1][sinkCol + 1] = "s"
                
                
        elif(piece == "l"):
            #getting the piece type
            pieceType = stdio.readString()
            
            #getting the coordinates
            pieceRow = stdio.readInt()
            pieceCol = stdio.readInt()
            
            if(checkPieceRange(maxRow, maxCol, pieceRow, pieceCol)): #error message is printed in the function
                if(pieceType == "d"): #NEED TO VALIDATE IF A PIECE OF THIS SIZE CAN FIT WITHIN THESE COORDINATES
                    #ADD CHECK TO CHECK IF THERE IS ANOTHER PIECE OCCUPYING THE FIELD OR NOT ALREADY
                    value = (pieceRow*maxCol)+pieceCol
                    board[pieceRow][pieceCol] = "d"
                    board[pieceRow][pieceCol + 1] = str(value)
                    board[pieceRow + 1][pieceCol] = str(value)
                    board[pieceRow + 1][pieceCol + 1] = str(value)
                else: #all the other pieces will be upright anyways
                    #ADD CHECK TO CHECK IF THERE IS ANOTHER PIECE OCCUPYING THE FIELD OR NOT ALREADY
                    board[pieceRow][pieceCol] = pieceType
                    
            
        elif(piece == "d"):
            #getting the piece type
            pieceType = stdio.readString()
            
            #getting the coordinates
            pieceRow = stdio.readInt()
            pieceCol = stdio.readInt()
            
            if(checkPieceRange(maxRow, maxCol, pieceRow, pieceCol)): #error message is printed in the function
                if(pieceType == "d"): #NEED TO VALIDATE IF A PIECE OF THIS SIZE CAN FIT WITHIN THESE COORDINATES
                    #ADD CHECK TO CHECK IF THERE IS ANOTHER PIECE OCCUPYING THE FIELD OR NOT ALREADY
                    value = (pieceRow*maxCol)+pieceCol
                    board[pieceRow][pieceCol] = "D"
                    board[pieceRow][pieceCol + 1] = str(value)
                    board[pieceRow + 1][pieceCol] = str(value)
                    board[pieceRow + 1][pieceCol + 1] = str(value)
                else: #all the other pieces will be upright anyways
                    #ADD CHECK TO CHECK IF THERE IS ANOTHER PIECE OCCUPYING THE FIELD OR NOT ALREADY
                    board[pieceRow][pieceCol] = pieceType.upper()
                    
        #getting the value of the next piece
        piece = stdio.readString()
                
        #direction
        #getting the direction it lies in
        #NEEDED FOR MOVE FUNCTION AND NOT FOR THIS FUNCTION 
        # else:
        #     moveDirection = string[len(string) - 1]
                
        #     if(moveDirection == "l"):
        #         stdio.writeln("left")
        #     elif(moveDirection == "r"):
        #         stdio.writeln("right")
        #     elif(moveDirection == "u"):
        #         stdio.writeln("up")
        #     elif(moveDirection == "d"):
        #         stdio.writeln("down")  
                
    #returning the board with all the given pieces
    return board



#prints the board and everything in it in a grid-like model
#WORKS
def printBoard(board):
    #getting the number of columns and rows in the board
    columnMax = len(board[0][:])
    
    #writing out the column nums at the top
    stdio.write(" ")
    for i in range(0, columnMax):
        stdio.write("  " + str(i))
    stdio.writeln() #to get it onto the next line       
    
    #running through the array of the board and printing its values
    rowCount = 0
    for i in range(0, len(board)):
        #writing out the divider between each row
        stdio.write("  +")
        for j in range(0, columnMax):
            stdio.write("--+")
        stdio.writeln()
        
        #writing out the row number
        stdio.write(str(rowCount) + " |")
        
        #writing out the values of the array into their respective places
        for j in range(0, len(board[i])):
            stdio.write(" " + board[i][j] + "|")
        stdio.writeln()
        rowCount+=1
        
    #writing out the last divider
    stdio.write("  +")
    for j in range(0, columnMax):
        stdio.write("--+")
    stdio.writeln()



def drawGame(board):
    """
    Draws the given board using standard draw.

    Args:
        board (2D array of str): The game board
    """
    # When implemented correctly, this function can be called after each move to
    # re-draw the game for the GUI.
    # remove the following line when you add something to this function:
    pass



def gameLoop(board, guiMode):
    """
    Executes the main game loop including
        * reading in a move
        * checking if the move is valid
        * if it is, doing the move
        * printing (or displaying) the board
        * and repeating.

    Args:
        board (2D array of str): The game board
        gui_mode (bool): The mode of the game, True if gui_mode, False if terminal mode
    """
    # If implemented well, this function can be used for both terminal and GUI mode.
    # TODO: implement this function.
    # remove the following line when you add something to this function:
    pass



if __name__ == "__main__":
    # TODO: put logic here to check if the command-line arguments are correct,
    # and then call the game functions using these arguments. The following code
    # is a placeholder for this to give you an idea, and MUST be changed when
    # you start editing this file.
    
    #checking if there are enough arguements to begin the program
    #number of arguements is correct
    if(checkNumArgs(len(sys.argv))): #error message is printed when this is run
        #getting the arguements for the board size and the gamemode
        maxRow = sys.argv[1]
        maxCol = sys.argv[2]
        guiMode = sys.argv[3]
        
        #performing error checks to ensure the arguements are valid
        if(checkArgs(maxRow, maxCol, guiMode)): #error message is printed when this is run
            board = readBoard(maxRow, maxCol)
            printBoard(board)
            #game_loop(board, gui_mode)
        
