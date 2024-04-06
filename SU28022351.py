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

#IMPORTS================================================================================================================
import stdio
import sys
import stdarray
#=======================================================================================================================


#GLOBALS================================================================================================================
turn = 1 #keeps track of who's turn it is (odd = light and even = dark)
movesLeft = 2 #keeps track of the number of moves made in a turn
maxRowGlobal = None
maxColGlobal = None
guiModeGlobal = None
#=======================================================================================================================


#CHECKS=================================================================================================================
#WORKS
def checkArgs(maxRow, maxCol, guiMode):
    """
    Validates the arguements given for the board and gamemode.
    Returns a boolean value.
    If false, an error message is printed.
    
    Args:
        maxRow (int): The maximum number of rows on the board.
        maxCol (int): The maximum number of columns on the board.
        guiMode (str): The gamemode.
    """
    
    #converting into integers
    maxRow = int(maxRow)
    maxCol = int(maxCol)
    
    #checking if the board is valid
    if(not(maxRow > 7 and maxRow < 11) or not(maxCol > 7 and maxCol < 11)):
        stdio.writeln("ERROR: Illegal argument")
        return False
    
    #checking if the gamemode is one of two arguements (if it is neither then it is false)
    if(guiMode != "1" and guiMode != "0"):
        stdio.writeln("ERROR: Illegal argument")
        return False
    
    #if we get here then the arguements are valid
    return True
    
#-----------------------------------------------------------------------------------------------------------------------  
    
#WORKS
def checkNumArgs(numArgs):
    """
    Checks if the number of arguements is correct.
    Returns a boolean value.
    If false, an error message is printed.
    
    Args:
        numArgs (int): The number of arguements given.
    """
    
    if(numArgs != 3):
        if(numArgs < 3):
            stdio.writeln("ERROR: Too few arguements")
        else:
            stdio.writeln("ERROR: Too many arguements")
        return False
    
    #if we get here then the number of arguements is correct
    return True

#-----------------------------------------------------------------------------------------------------------------------  

#WORKS
def checkSinkRange(maxRow, maxCol, sinkRow, sinkCol):
    """
    Checks if a sink is in the correct position.
    Returns a boolean value.
    If false, an error message is printed.
    
    Args:
        maxRow (int): The maximum number of rows on the board.
        maxCol (int): The maximum number of columns on the board.
        sinkRow (int): The row of the sink.
        sinkCol (int): The column of the sink.
    """
    
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

#-----------------------------------------------------------------------------------------------------------------------  

#WORKS
def checkPieceRange(maxRow, maxCol, pieceRow, pieceCol):
    """
    Checks if a piece is in the correct position.
    Returns a boolean value.
    If false, an error message is printed.
    
    Args:
        maxRow (int): The maximum number of rows on the board.
        maxCol (int): The maximum number of columns on the board.
        pieceRow (int): The row of the piece.
        pieceCol (int): The column of the piece.
    """
    
    #piece is in the correct position if it is NOT in the first and last three columns and rows
    if((pieceRow < maxRow and pieceRow >= maxRow - 3) or (pieceRow < 3 and pieceRow >= 0) or (pieceCol < maxCol and pieceCol >= maxCol - 3) or (pieceCol < 3 and pieceCol >= 0)):
        stdio.writeln("ERROR: Piece in the wrong position for piece " + str(pieceRow) + " " + str(pieceCol))
        return False
    
    #if we get here, the piece is in the correct position
    return True

#-----------------------------------------------------------------------------------------------------------------------  

#WORKS
def checkPieceUpright(row, col, board):
    """
    Checks if the piece is upright or on its side.
    Returns a boolean value.
    
    Args:
        row (int): The row of the piece.
        col (int): The column of the piece.
        board (2D array of str): The game board.
    """
    
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

#-----------------------------------------------------------------------------------------------------------------------  

def checkMoveInput(row, col, direction, board):
    """
    Checks the move input.
    Returns a boolean value.
    If any part of the move is invalid, an error message is printed and the function returns False.
    NOTE: This function does not check if the move is possible or not. It only checks if the input is valid.
    
    Args:
        row (int): The row of the object to move
        col (int): The column of the object to move
        direction (str): The direction of the move
        board (2D array of str): The game board
    """
    
    #checking if the coordinates given are on the board
    if(row < 0 or col < 0 or row >= len(board) or col >= len(board[0])):
        stdio.writeln("ERROR: Field " + str(row) + " " + str(col) + " not on board")
        return False
    
    #checking if the direction is valid
    if(direction != "u" and direction != "d" and direction != "l" and direction != "r"):
        stdio.writeln("ERROR: Invalid direction")
        return False
    
    #checking if the field is empty
    if(board[row][col] == " "):
        stdio.writeln("ERROR: No piece on field " + str(row) + " " + str(col))
        return False
    
    #checking if the piece belongs to the player whose move it is
    if((turn % 2 == 1 and board[row][col].islower()) or (turn % 2 == 0 and board[row][col].isupper())):
        stdio.writeln("ERROR: Piece does not belong to the correct player")
        return False
    
    #checking if a 2x2x2 piece is being moved on the 2nd move of a player's turn
    if(movesLeft == 1 and (board[row][col] == "D" or board[row][col] == "d")):
        stdio.writeln("ERROR: Cannot move a 2x2x2 piece on the second move")
        return False
    
    
    #move input is valid
    return True
    
#-----------------------------------------------------------------------------------------------------------------------

#NO IDEA IF THIS WORKS OR NOT (I AM PRAYING OH MY GOSH)
def validateMove(row, col, direction, board):
    """
    Checks if the given move is possible or not.
    Returns a boolean value.
    If false, an error message is printed.
    
    Args:
        row (int): The row of the object to move
        col (int): The column of the object to move
        direction (str): The direction of the move
        board (2D array of str): The game board
    """
    
    #variables
    moveBeyondBoard = False
    fieldOccupied = False
    occupiedField = None
    
    #MOVING A 1X1 PIECE
    if(board[row][col] == "a" or board[row][col] == "A"):
        #checking if the space next to the piece is empty
        #moving up
        if(direction == "u"):
            #checking if the board border is reached or not
            if(row - 1 >= 0):
                if(board[row - 1][col] == " " or board[row - 1][col] == "s"):
                    return True
                else:
                    fieldOccupied = True
                    #getting the field that is occupied
                    occupiedField = (row - 1, col)
            else:
                moveBeyondBoard = True
        #moving down
        elif(direction == "d"):
            #checking if the board border is reached or not
            if(row + 1 <= len(board) - 1):
                if(board[row + 1][col] == " " or board[row + 1][col] == "s"):
                    return True
                else:
                    fieldOccupied = True
                    #getting the field that is occupied
                    occupiedField = (row + 1, col)
            else:
                moveBeyondBoard = True
        #moving left
        elif(direction == "l"):
            #checking if the board border is reached or not
            if(col - 1 >= 0):
                if(board[row][col - 1] == " " or board[row][col - 1] == "s"):
                    return True
                else:
                    fieldOccupied = True
                    #getting the field that is occupied
                    occupiedField = (row, col-1)
            else:
                moveBeyondBoard = True
        #moving right
        elif(direction == "r"):
            #checking if the board border is reached or not
            if(col + 1 <= len(board[0]) - 1):
                if(board[row][col + 1] == " " or board[row][col + 1] == "s"):
                    return True
                else:
                    fieldOccupied = True
                    #getting the field that is occupied
                    occupiedField = (row, col+1)
            else:
                moveBeyondBoard = True
            
            
    #MOVING A 1X2 PIECE
    elif(board[row][col] == "b" or board[row][col] == "B"):
        #checking if the piece is upright or not
        if(checkPieceUpright(row, col, board)):
            #checking if the 2 spaces next to the piece is empty
            #moving up
            if(direction == "u"):
                #checking if the board border is reached or not
                if(row - 2 >= 0): 
                    if((board[row - 1][col] == " " and board[row - 2][col] == " ") or (board[row - 1][col] == "s") and (board[row - 2][col] == "s")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the field that is occupied
                        for i in range(row-2, row):
                            if(board[i][col] != " " and board[i][col] != "s"):
                                occupiedField = (i, col)
                                break #only need to find the first field that is occupied
                else:
                    moveBeyondBoard = True                   
            #moving down
            elif(direction == "d"):
                #checking if the board border is reached or not
                if(row + 2 <= len(board) - 1):
                    if((board[row + 1][col] == " " and board[row + 2][col] == " ") or (board[row + 1][col] == "s") and (board[row + 2][col] == "s")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the field that is occupied
                        for i in range(row+1, row+3):
                            if(board[i][col] != " " and board[i][col] != "s"):
                                occupiedField = (i, col)
                                break #only need to find the first field that is occupied
                else:
                    moveBeyondBoard = True                    
            #moving left
            elif(direction == "l"):
                #checking if the board border is reached or not
                if(col - 2 >= 0):
                    if((board[row][col - 1] == " " and board[row][col - 2] == " ") or (board[row][col - 1] == "s") and (board[row][col - 2] == "s")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the field that is occupied
                        for i in range(col-2, col):
                            if(board[row][i] != " " and board[row][i] != "s"):
                                occupiedField = (row, i)
                                break #only need to find the first field that is occupied
                else:
                    moveBeyondBoard = True                    
            #moving right
            elif(direction == "r"):
                #checking if the board border is reached or not
                if(col + 2 <= len(board[0]) - 1):
                    if((board[row][col + 1] == " " and board[row][col + 2] == " ") or (board[row][col + 1] == "s") and (board[row][col + 2] == "s")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the field that is occupied
                        for i in range(col+1, col+3):
                            if(board[row][i] != " " and board[row][i] != "s"):
                                occupiedField = (row, i)
                                break #only need to find the first field that is occupied
                else:
                    moveBeyondBoard = True
        
        else: #piece is on its side
            #finding the direction the piece is lying in
            lyingDirection = None 
            value = (row*len(board[0][:])) + col 
            #the value associated with the piece will only ever be down or to the right of the coordinates given because the coordinates are the bottom left of the piece
            #down
            if(board[row+1][col] == str(value)):
                lyingDirection = "vertical"
            #right
            else:
                lyingDirection = "horizontal"
            
            
            #checking if the spaces required for the piece to move are empty
            #vertical piece
            if(lyingDirection == "vertical"):
                #moving up
                if(direction == "u"):
                    #checking if the board border is reached or not
                    if(row - 1 >= 0): #only need to check for one field because the piece will flip over into its upright position
                        if((board[row - 1][col] == " ") or (board[row - 1][col] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            occupiedField = (row-1, col)
                    else:
                        moveBeyondBoard = True
                #moving down
                elif(direction == "d"):
                    #checking if the board border is reached or not
                    if(row + 2 <= len(board) - 1): #only one field for the same reason as the up direction but needs to be +2 to account for the field the piece is in under its coords
                        if((board[row + 2][col] == " ") or (board[row + 2][col] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            occupiedField = (row+2, col)
                    else:
                        moveBeyondBoard = True                       
                #moving left
                elif(direction == "l"):
                    #checking if the board border is reached or not
                    if(col - 1 >= 0):
                        if((board[row][col - 1] == " " and board[row + 1][col - 1] == " ") or (board[row][col - 1] == "s" and board[row + 1][col - 1] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            for i in range(row, row+2):
                                if(board[i][col-1] != " " and board[i][col-1] != "s"):
                                    occupiedField = (i, col-1)
                                    break #only need to find the first field that is occupied
                    else:
                        moveBeyondBoard = True
                #moving right      
                elif(direction == "r"):
                    #checking if the board border is reached or not
                    if(col + 1 <= len(board[0]) - 1):
                        if((board[row][col + 1] == " " and board[row + 1][col + 1] == " ") or (board[row][col + 1] == "s" and board[row + 1][col + 1] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            for i in range(row, row+2):
                                if(board[i][col+1] != " " and board[i][col+1] != "s"):
                                    occupiedField = (i, col+1)
                                    break #only need to find the first field that is occupied
                    else:
                        moveBeyondBoard = True
              
            #horizontal piece          
            else: 
                #moving up
                if(direction == "u"):
                    #checking if the board border is reached or not
                    if(row - 1 >= 0):
                        if((board[row - 1][col] == " " and board[row - 1][col + 1] == " ") or (board[row - 1][col] == "s" and board[row - 1][col + 1] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            for i in range(col, col+2):
                                if(board[row-1][i] != " " and board[row-1][i] != "s"):
                                    occupiedField = (row-1, i)
                                    break #only need to find the first field that is occupied
                    else:
                        moveBeyondBoard = True                       
                #moving down
                elif(direction == "d"):
                    #checking if the board border is reached or not
                    if(row + 1 <= len(board) - 1):
                        if((board[row + 1][col] == " " and board[row + 1][col + 1] == " ") or (board[row + 1][col] == "s" and board[row + 1][col + 1] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            for i in range(col, col+2):
                                if(board[row+1][i] != " " and board[row+1][i] != "s"):
                                    occupiedField = (row+1, i)
                                    break #only need to find the first field that is occupied
                    else:
                        moveBeyondBoard = True                       
                #moving left
                elif(direction == "l"):
                    #checking if the board border is reached or not
                    if(col - 1 >= 0):
                        if((board[row][col - 1] == " ") or (board[row][col - 1] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            occupiedField = (row, col-1)
                    else:
                        moveBeyondBoard = True                        
                #moving right
                elif(direction == "r"):
                    #checking if the board border is reached or not
                    if(col + 2 <= len(board[0]) - 1):
                        if((board[row][col + 2] == " ") or (board[row][col + 2] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            occupiedField = (row, col+2)
                    else:
                        moveBeyondBoard = True
            
        
    #MOVING A 1X3 PIECE
    elif(board[row][col] == "c" or board[row][col] == "C"):
        #checking if the piece is upright or not
        if(checkPieceUpright(row, col, board)):
            #checking if the 3 spaces next to the piece is empty
            #moving up
            if(direction == "u"):
                #checking if the board border is reached or not
                if(row - 3 >= 0):
                    if((board[row - 1][col] == " " and board[row - 2][col] == " " and board[row - 3][col] == " ") or (board[row - 1][col] == "s" and board[row - 2][col] == "s" and board[row - 3][col] == "s")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the occupied field
                        for i in range(row-3, row):
                            if(board[i][col] != " " and board[i][col] != "s"):
                                occupiedField = (i, col)
                                break #only need to find the first field that is occupied
                else:
                    moveBeyondBoard = True                   
            #moving down
            elif(direction == "d"):
                #checking if the board border is reached or not
                if(row + 3 <= len(board) - 1):
                    if((board[row + 1][col] == " " and board[row + 2][col] == " " and board[row + 3][col] == " ") or (board[row + 1][col] == "s" and board[row + 2][col] == "s" and board[row + 3][col] == "s")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the occupied field
                        for i in range(row+1, row+4):
                            if(board[i][col] != " " and board[i][col] != "s"):
                                occupiedField = (i, col)
                                break #only need to find the first field that is occupied
                else:
                    moveBeyondBoard = True                   
            #moving left
            elif(direction == "l"):
                #checking if the board border is reached or not
                if(col - 3 >= 0):
                    if((board[row][col - 1] == " " and board[row][col - 2] == " " and board[row][col - 3] == " ") or (board[row][col - 1] == "s" and board[row][col - 2] == "s" and board[row][col - 3] == "s")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the occupied field
                        for i in range(col-3, col):
                            if(board[row][i] != " " and board[row][i] != "s"):
                                occupiedField = (row, i)
                                break #only need to find the first field that is occupied
                else:
                    moveBeyondBoard = True                   
            #moving right
            elif(direction == "r"):
                #checking if the board border is reached or not
                if(col + 3 <= len(board[0]) - 1):
                    if((board[row][col + 1] == " " and board[row][col + 2] == " " and board[row][col + 3] == " ") or (board[row][col + 1] == "s" and board[row][col + 2] == "s" and board[row][col + 3] == "s")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the occupied field
                        for i in range(col+1, col+4):
                            if(board[row][i] != " " and board[row][i] != "s"):
                                occupiedField = (row, i)
                                break #only need to find the first field that is occupied
                else:
                    moveBeyondBoard = True
                    
                    
        else: #piece is on its side
            #finding the direction the piece is lying in
            lyingDirection = None 
            value = (row*len(board[0][:])) + col 
            #the value associated with the piece will only ever be down or to the right of the coordinates given because the coordinates are the bottom left of the piece
            #down
            if(board[row+1][col] == str(value)):
                lyingDirection = "vertical"
            #right
            else:
                lyingDirection = "horizontal"
                
                
            #checking if the spaces required for the piece to move are empty
            #vertical piece
            if(lyingDirection == "vertical"):
                #moving up
                if(direction == "u"):
                    #checking if the board border is reached or not
                    if(row - 1 >= 0): #only need to check for one field because the piece will flip over into its upright position
                        if((board[row - 1][col] == " ") or (board[row - 1][col] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            occupiedField = (row-1, col)
                    else:
                        moveBeyondBoard = True                        
                #moving down
                elif(direction == "d"):
                    #checking if the board border is reached or not
                    if(row + 3 <= len(board) - 1): #only one field for the same reason as the up direction but needs to be +2 to account for the field the piece is in under its coords
                        if((board[row + 3][col] == " ") or (board[row + 3][col] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            occupiedField = (row+3, col)
                    else:
                        moveBeyondBoard = True
                #moving left
                elif(direction == "l"):
                    #checking if the board border is reached or not
                    if(col - 1 >= 0):
                        if((board[row][col - 1] == " " and board[row + 1][col - 1] == " " and board[row + 2][col - 1] == " ") or (board[row][col - 1] == "s" and board[row + 1][col - 1] == "s" and board[row + 2][col - 1] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the occupied field
                            for i in range(row, row+3):
                                if(board[i][col-1] != " " and board[i][col-1] != "s"):
                                    occupiedField = (i, col-1)
                                    break #only need to find the first field that is occupied
                    else:
                        moveBeyondBoard = True      
                #moving right
                elif(direction == "r"):
                    #checking if the board border is reached or not
                    if(col + 1 <= len(board[0]) - 1):
                        if((board[row][col + 1] == " " and board[row + 1][col + 1] == " " and board[row + 2][col + 1] == " ") or (board[row][col + 1] == "s" and board[row + 1][col + 1] == "s" and board[row + 2][col + 1] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the occupied field
                            for i in range(row, row+3):
                                if(board[i][col+1] != " " and board[i][col+1] != "s"):
                                    occupiedField = (i, col+1)
                                    break #only need to find the first field that is occupied
                    else:
                        moveBeyondBoard = True
                        
            #horizontal piece
            else:   
                #moving up
                if(direction == "u"):
                    #checking if the board border is reached or not
                    if(row - 1 >= 0):
                        if((board[row - 1][col] == " " and board[row - 1][col + 1] == " " and board[row - 1][col + 2] == " ") or (board[row - 1][col] == "s" and board[row - 1][col + 1] == "s"  and board[row - 1][col + 2] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the occupied field
                            for i in range(col, col+3):
                                if(board[row-1][i] != " " and board[row-1][i] != "s"):
                                    occupiedField = (row-1, i)
                                    break #only need to find the first field that is occupied
                    else:
                        moveBeyondBoard = True
                #moving down
                elif(direction == "d"):
                    #checking if the board border is reached or not
                    if(row + 1 <= len(board) - 1):
                        if((board[row + 1][col] == " " and board[row + 1][col + 1] == " " and board[row + 1][col + 2] == " ") or (board[row + 1][col] == "s" and board[row + 1][col + 1] == "s"  and board[row + 1][col + 2] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the occupied field
                            for i in range(col, col+3):
                                if(board[row+1][i] != " " and board[row+1][i] != "s"):
                                    occupiedField = (row+1, i)
                                    break #only need to find the first field that is occupied
                    else:
                        moveBeyondBoard = True
                #moving left
                elif(direction == "l"):
                    #checking if the board border is reached or not
                    if(col - 1 >= 0):
                        if((board[row][col - 1] == " ") and (board[row][col - 1] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            occupiedField = (row, col-1)
                    else:
                        moveBeyondBoard = True
                #moving right
                elif(direction == "r"):
                    #checking if the board border is reached or not
                    if(col + 3 <= len(board[0]) - 1):
                        if((board[row][col + 3] == " ") and (board[row][col + 3] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            occupiedField = (row, col+3)
                    else:
                        moveBeyondBoard = True
                        
        
    
    #MOVING A 2X2 PIECE          
    elif(board[row][col] == "d" or board[row][col] == "D"):
        #moving up
        if(direction == "u"):
            #checking if the board border is reached or not
            if(row - 2 >= 0):
                if((board[row - 1][col] == " " and board[row - 2][col] == " " and board[row - 1][col + 1] == " " and board[row - 2][col + 1] == " ") or (board[row - 1][col] == "s" and board[row - 2][col] == "s" and board[row - 1][col + 1] == "s" and board[row - 2][col + 1] == "s")):
                    return True
                else:
                    fieldOccupied = True
                    #getting the field that is occupied
                    for i in range(row-2, row):
                        for j in range(col, col+2):
                            if(board[i][j] != " " and board[i][j] != "s"):
                                occupiedField = (i,j)
                                break #only need to find the first field that is occupied
            else:
                moveBeyondBoard = True
        #moving down
        elif(direction == "d"):
            #checking if the board border is reached or not
            if(row + 3 <= len(board) - 1):
                if((board[row + 2][col] == " " and board[row + 3][col] == " " and board[row + 2][col + 1] == " " and board[row + 3][col + 1] == " ") or (board[row + 2][col] == "s" and board[row + 3][col] == "s" and board[row + 2][col + 1] == "s" and board[row + 3][col + 1] == "s")):
                    return True
                else:
                    fieldOccupied = True
                    #getting the field that is occupied
                    for i in range(row+2, row+4):
                        for j in range(col, col+2):
                            if(board[i][j] != " " and board[i][j] != "s"):
                                occupiedField = (i,j)
                                break #only need to find the first field that is occupied
            else:
                moveBeyondBoard = True
        #moving left
        elif(direction == "l"):
            #checking if the board border is reached or not
            if(col - 2 >= 0):
                if((board[row][col - 1] == " " and board[row][col - 2] == " " and board[row + 1][col - 1] == " " and board[row + 1][col - 2] == " ") or (board[row][col - 1] == "s" and board[row][col - 2] == "s" and board[row + 1][col - 1] == "s" and board[row + 1][col - 2] == "s")):
                    return True
                else:
                    fieldOccupied = True
                    #getting the field that is occupied
                    for i in range(row, row+2):
                        for j in range(col-2, col):
                            if(board[i][j] != " " and board[i][j] != "s"):
                                occupiedField = (i,j)
                                break #only need to find the first field that is occupied
            else:
                moveBeyondBoard = True
        #moving right
        elif(direction == "r"):
            #checking if the board border is reached or not
            if(col + 3 <= len(board[0]) - 1):
                if((board[row][col + 2] == " " and board[row][col + 3] == " " and board[row + 1][col + 2] == " " and board[row + 1][col + 3] == " ") or (board[row][col + 2] == "s" and board[row][col + 3] == "s" and board[row + 1][col + 2] == "s" and board[row + 1][col + 3] == "s")):
                    return True
                else:
                    fieldOccupied = True
                    #getting the field that is occupied
                    for i in range(row, row+2):
                        for j in range(col+2, col+4):
                            if(board[i][j] != " " and board[i][j] != "s"):
                                occupiedField = (i,j)
                                break #only need to find the first field that is occupied
                    
            else:
                moveBeyondBoard = True
                
                
    #move is invalid
    if(moveBeyondBoard):
        stdio.writeln("ERROR: Cannot move beyond the board")
    if(fieldOccupied):
        stdio.writeln("ERROR: Field " + str(occupiedField[0]) + " " + str(occupiedField[1]) + " not free")
#=======================================================================================================================


#MOVES=================================================================================================================
#NO IDEA IF THIS WORKS OR NOT BUT LETS GO WITH NO BUT HAVE HOPE
#MIGHT NOT NEED THIS
def getPieceFields(row, col, board):
    """
    Gets all the field coordinates that a piece occupies
    Returns a 2D array of numbers
    
    Args:
        row (int) : the row of the piece
        col (int): the col of the piece
        board (2D array of str): The game board
    """
    
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

#-----------------------------------------------------------------------------------------------------------------------  

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
    
    # This function may be useful for separating out the logic of doing a move.
    # remove the following line when you add something to this function:
    pass

#-----------------------------------------------------------------------------------------------------------------------  

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
#=======================================================================================================================


#BOARD=================================================================================================================
#WORKS BUT NEEDS ERROR CHECKS 
def readBoard(maxRow, maxCol):
    """
    Reads the arguements given on the first start of the game
    Returns an array, board, with all the given pieces
    
    Args:
        maxRow (int): The maximum number of rows in the board
        maxCol (int): The maximum number of columns in the board
    """
    
    #variables
    maxRow = int(maxRow)
    maxCol = int(maxCol)
    board = stdarray.create2D(maxRow,maxCol," ")
    
    #getting the line
    piece = stdio.readString()
    
    #running a loop until the next string gotten is #
    while(piece != "#"):
        #checks if the object type given is viable
        if(piece != "s" and piece != "l" and piece != "d" and piece != "x"):
            stdio.writeln("ERROR: Invalid object type " + piece)
        
        #gets the coordinates of a specific piece and adds it to the board
        elif(piece == "s"):
            #getting the size
            sinkSize = stdio.readInt()
            
            #getting the coordinates
            sinkRow = stdio.readInt()
            sinkCol = stdio.readInt()
            
            #checking if the size is valid
            if(sinkSize != 1 and sinkSize != 2):
                stdio.writeln("ERROR: Invalid piece type " + str(sinkSize))
            
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
            
            if(pieceType != "a" and pieceType != "b" and pieceType != "c" and pieceType != "d"):
                stdio.writeln("ERROR: Invalid piece type " + pieceType)
            
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
            
            if(pieceType != "a" and pieceType != "b" and pieceType != "c" and pieceType != "d"):
                stdio.writeln("ERROR: Invalid piece type " + pieceType)
            
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
                
    #returning the board with all the given pieces
    return board

#-----------------------------------------------------------------------------------------------------------------------  

#prints the board and everything in it in a grid-like model
#WORKS
def printBoard(board):
    """
    Prints the board and everything in it in a grid-like model
    
    Args:
        board (2D array of str): The game board
    """
    
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

#-----------------------------------------------------------------------------------------------------------------------  

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
#=======================================================================================================================


#GAME==================================================================================================================
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
#=======================================================================================================================


#MAIN==================================================================================================================
if __name__ == "__main__":
    # TODO: put logic here to check if the command-line arguments are correct,
    # and then call the game functions using these arguments. The following code
    # is a placeholder for this to give you an idea, and MUST be changed when
    # you start editing this file.
    
    #checking if there are enough arguements to begin the program
    #number of arguements is correct
    arguements = stdio.readLine().split(" ")
    numArgs = len(arguements)
    if(checkNumArgs(numArgs)): #error message is printed when this is run
        #getting the arguements for the board size and the gamemode
        maxRow = arguements[0]
        maxCol = arguements[1]
        guiMode = arguements[2]
        
        #setting the global variables
        maxRowGlobal = maxRow
        maxColGlobal = maxCol
        
        #performing error checks to ensure the arguements are valid
        if(checkArgs(maxRow, maxCol, guiMode)): #error message is printed when this is run
            board = readBoard(maxRow, maxCol)
            printBoard(board)
            #game_loop(board, gui_mode)
            
            #type setup_board_test.txt|python SU28022351.py 10 10 0  
#=======================================================================================================================       
