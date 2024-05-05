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
#setting game variables 
global movesLeft #number of moves left for the player
movesLeft = 2  
global turn #the player's turn (odd for light, even for dark)
turn = 1
global lightPoints
lightPoints = 0
global darkPoints
darkPoints = 0
global prevMove #the previous move made
prevMove = None
global gettingAllMoves #indicates whether the program is collecting all the possible moves for a player 
gettingAllMoves = False #will be used to stop error messages from being printed in validateMove (just want to get the moves)
#=======================================================================================================================


#CHECKS=================================================================================================================
#WORKS
def checkArgs(maxRow, maxCol, guiMode):
    """
    Validates the arguements given for the board and gamemode.
    Returns a boolean value.
    If false, an error message is printed
    
    Args:
        maxRow (int): The maximum number of rows on the board.
        maxCol (int): The maximum number of columns on the board.
        guiMode (str): The gamemode.
    """
    
    #checking if the arguements are integers
    if(not(maxRow.isdigit()) or not(maxCol.isdigit()) or not(guiMode.isdigit())):
        stdio.writeln("ERROR: Illegal argument")
        return False
    
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
    
    if(numArgs != 4):
        if(numArgs < 4):
            stdio.writeln("ERROR: Too few arguments")
        else:
            stdio.writeln("ERROR: Too many arguments")
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
    
    #field provided is a letter
    if(not sinkRow.isnumeric() or not sinkCol.isnumeric()):
        stdio.writeln("ERROR: Field " + str(sinkRow) + " " + str(sinkCol) + " not on board")
        sys.exit()
        
    #converting the sinkRow and sinkCol into integers
    sinkRow = int(sinkRow)
    sinkCol = int(sinkCol)
    
    #field provided is not on the board
    if(((sinkRow < 0) or (sinkCol < 0)) or ((sinkRow >= maxRow) or (sinkCol >= maxCol))):
        stdio.writeln("ERROR: Field " + str(sinkRow) + " " + str(sinkCol) + " not on board")
        sys.exit()
    
    #valid if it is in a correct row OR a correct column
    elif((sinkRow < maxRow and sinkRow >= maxRow - 3) or (sinkRow < 3 and sinkRow >= 0) or (sinkCol < maxCol and sinkCol >= maxCol - 3) or (sinkCol < 3 and sinkCol >= 0)):
        return True
            
    #if we get here, the sink is in the wrong position
    stdio.writeln("ERROR: Sink in the wrong position")
    sys.exit()

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
    #field provided is a letter
    if(not pieceRow.isnumeric() or not pieceCol.isnumeric()):
        stdio.writeln("ERROR: Field " + str(pieceRow) + " " + str(pieceCol) + " not on board")
        sys.exit()
        
    #converting the pieceRow and pieceCol into integers
    pieceRow = int(pieceRow)
    pieceCol = int(pieceCol)
    
    #field provided is not on the board
    if(((pieceRow < 0) or (pieceCol < 0)) or ((pieceRow >= maxRow) or (pieceCol >= maxCol))):
        stdio.writeln("ERROR: Field " + str(pieceRow) + " " + str(pieceCol) + " not on board")
        sys.exit()
    
    #piece is in the correct position if it is NOT in the first and last three columns and rows
    if((pieceRow < maxRow and pieceRow >= maxRow - 3) or (pieceRow < 3 and pieceRow >= 0) or (pieceCol < maxCol and pieceCol >= maxCol - 3) or (pieceCol < 3 and pieceCol >= 0)):
        stdio.writeln("ERROR: Piece in the wrong position")
        sys.exit()
    
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
    columnMax = len(board[0])
    rowMax = len(board)
    #getting the value from the piece
    value = (row*columnMax)+col
    isUpright = True
    
    # stdio.writeln(value)
    # printBoard(board)
    # stdio.writeln()
    
    # for i in range(0, rowMax):
    #     for j in range (0, columnMax):
    #         if(str(board[i][j]) == str(value)):
    #             isUpright = False
    # #if the code gets here then that means there is only one field occupied
    # return isUpright
    
    #making sure that it is not the big piece (D or d)
    if(board[row][col] == 'A' or board[row][col] == 'a'):
        #is technically always upright because it always is in one field
        return True
    elif(board[row][col] == 'D' or board[row][col] == 'd'):
        #can never be upright because it is always in 4 fields
        return False
        
    else:
        #running through all the fields to check if value is in any of them
        #means that the field is not upright if so
        for i in range(0, rowMax):
            for j in range (0, columnMax):
                if(str(board[i][j]) == str(value)):
                    return False
        #if the code gets here then that means there is only one field occuped
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
        sys.exit()
    
    #checking if the direction is valid
    if(direction != "u" and direction != "d" and direction != "l" and direction != "r" and direction != "b"):
        stdio.writeln("ERROR: Invalid direction " + direction)
        sys.exit()
    
    #checking if the field is empty
    if(board[row][col] == " " and direction != "b"):
        stdio.writeln("ERROR: No piece on field " + str(row) + " " + str(col))
        sys.exit()
    
    #checking if the piece belongs to the player whose move it is
    if((turn % 2 != 0 and board[row][col].isupper()) or (turn % 2 == 0 and board[row][col].islower())):
        stdio.writeln("ERROR: Piece does not belong to the correct player")
        sys.exit()
    
    #checking if a 2x2x2 piece is being moved on the 2nd move of a player's turn
    if(movesLeft == 1 and (board[row][col] == "D" or board[row][col] == "d")):
        stdio.writeln("ERROR: Cannot move a 2x2x2 piece on the second move")
        sys.exit()
    
    
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
        #moving down
        if(direction == "d"):
            #checking if the board border is reached or not
            if(row - 1 >= 0):
                if(board[row - 1][col] == " " or board[row - 1][col] == "s" or board[row - 1][col] == "o"):
                    return True
                else:
                    fieldOccupied = True
                    #getting the field that is occupied
                    occupiedField = (row - 1, col)
            else:
                moveBeyondBoard = True
        #moving up
        elif(direction == "u"):
            #checking if the board border is reached or not
            if(row + 1 <= len(board) - 1):
                if(board[row + 1][col] == " " or board[row + 1][col] == "s" or board[row + 1][col] == "o"):
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
                if(board[row][col - 1] == " " or board[row][col - 1] == "s" or board[row][col - 1] == "o"):
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
                if(board[row][col + 1] == " " or board[row][col + 1] == "s" or board[row][col + 1] == "o"):
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
            #moving down
            if(direction == "d"):
                #checking if the board border is reached or not
                if(row - 2 >= 0): 
                    if((board[row - 1][col] == " " and board[row - 2][col] == " ") or (board[row - 1][col] == "s") and (board[row - 2][col] == "s")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the field that is occupied
                        for i in range(row-1, row-3, -1):
                            if(board[i][col] != " "):
                                occupiedField = (i, col)
                                break #only need to find the first field that is occupied
                else:
                    moveBeyondBoard = True                   
            #moving up
            elif(direction == "u"):
                #checking if the board border is reached or not
                if(row + 2 <= len(board) - 1):
                    if((board[row + 1][col] == " " and board[row + 2][col] == " ") or (board[row + 1][col] == "s") and (board[row + 2][col] == "s")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the field that is occupied
                        for i in range(row+2, row, -1):
                            if(board[i][col] != " "):
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
                            if(board[row][i] != " "):
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
                            if(board[row][i] != " "):
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
            if(str(board[row+1][col]) == str(value)):
                lyingDirection = "vertical"
            #right
            else:
                lyingDirection = "horizontal"
                        
            #checking if the spaces required for the piece to move are empty
            #vertical piece
            if(lyingDirection == "vertical"):
                #moving down
                if(direction == "d"):
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
                #moving up
                elif(direction == "u"):
                    #checking if the board border is reached or not
                    if(row + 2 <= len(board) - 1): #only one field for the same reason as the up direction but needs to be +2 to account for the field the piece is in under its coords
                        if((board[row + 2][col] == " ") or (str(board[row + 2][col]) == "s")):
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
                            for i in range(row+2, row, -1):
                                if(board[i][col-1] != " "):
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
                                if(board[i][col+1] != " "):
                                    occupiedField = (i, col+1)
                                    break #only need to find the first field that is occupied
                    else:
                        moveBeyondBoard = True
              
            #horizontal piece          
            else: 
                #moving down
                if(direction == "d"):
                    #checking if the board border is reached or not
                    if(row - 1 >= 0):
                        if((board[row - 1][col] == " " and board[row - 1][col + 1] == " ") or (board[row - 1][col] == "s" and board[row - 1][col + 1] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            for i in range(col, col+2):
                                if(board[row-1][i] != " "):
                                    occupiedField = (row-1, i)
                                    break #only need to find the first field that is occupied
                    else:
                        moveBeyondBoard = True                       
                #moving up
                elif(direction == "u"):
                    #checking if the board border is reached or not
                    if(row + 1 <= len(board) - 1):
                        if((board[row + 1][col] == " " and board[row + 1][col + 1] == " ") or (board[row + 1][col] == "s" and board[row + 1][col + 1] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            for i in range(col, col+2):
                                if(board[row+1][i] != " "):
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
            #moving down
            if(direction == "d"):
                #checking if the board border is reached or not
                if(row - 3 >= 0):
                    if((board[row - 1][col] == " " and board[row - 2][col] == " " and board[row - 3][col] == " ") or (board[row - 1][col] == "s" and board[row - 2][col] == "s" and board[row - 3][col] == "s")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the occupied field
                        for i in range(row-1, row-4, -1):
                            if(board[i][col] != " "):
                                occupiedField = (i, col)
                                break #only need to find the first field that is occupied
                else:
                    moveBeyondBoard = True                   
            #moving up
            elif(direction == "u"):
                #checking if the board border is reached or not
                if(row + 3 <= len(board) - 1):
                    if((board[row + 1][col] == " " and board[row + 2][col] == " " and board[row + 3][col] == " ") or (board[row + 1][col] == "s" and board[row + 2][col] == "s" and board[row + 3][col] == "s")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the occupied field
                        for i in range(row+3, row, -1):
                            if(board[i][col] != " "):
                                occupiedField = (i, col)
                                break #only need to find the first field that is occupied
                else:
                    moveBeyondBoard = True                   
            #moving left
            elif(direction == "l"):
                #checking if the board border is reached or not
                if(col - 3 >= 0):
                    if((board[row][col - 1] == " " and board[row][col - 2] == " " and board[row][col - 3] == " ")):
                        return True
                    else:
                        fieldOccupied = True
                        #getting the occupied field
                        for i in range(col-3, col):
                            if(board[row][i] != " "):
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
                            if(board[row][i] != " "):
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
            if(str(board[row+1][col]) == str(value)):
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
                    if(row + 3 <= len(board) - 1): #only need to check for one field because the piece will flip over into its upright position
                        if((board[row + 3][col] == " ") or (board[row + 3][col] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            occupiedField = (row+3, col)
                    else:
                        moveBeyondBoard = True                        
                #moving down
                elif(direction == "d"):
                    #checking if the board border is reached or not
                    if(row - 1 >= 0): #only one field for the same reason as the up direction but needs to be +2 to account for the field the piece is in under its coords
                        if((board[row - 1][col] == " ") or (board[row - 1][col] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the field that is occupied
                            occupiedField = (row-1, col)
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
                            for i in range(row+2, row-1, -1):
                                if(board[i][col-1] != " "):
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
                            for i in range(row+2, row-1, -1):
                                if(board[i][col+1] != " "):
                                    occupiedField = (i, col+1)
                                    break #only need to find the first field that is occupied
                    else:
                        moveBeyondBoard = True
                        
            #horizontal piece
            else:   
                #moving down
                if(direction == "d"):
                    #checking if the board border is reached or not
                    if(row - 1 >= 0):
                        if((board[row - 1][col] == " " and board[row - 1][col + 1] == " " and board[row - 1][col + 2] == " ") or (board[row - 1][col] == "s" and board[row - 1][col + 1] == "s"  and board[row - 1][col + 2] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the occupied field
                            for i in range(col, col+3):
                                if(board[row-1][i] != " "):
                                    occupiedField = (row-1, i)
                                    break #only need to find the first field that is occupied
                    else:
                        moveBeyondBoard = True
                #moving up
                elif(direction == "u"):
                    #checking if the board border is reached or not
                    if(row + 1 <= len(board) - 1):
                        if((board[row + 1][col] == " " and board[row + 1][col + 1] == " " and board[row + 1][col + 2] == " ") or (board[row + 1][col] == "s" and board[row + 1][col + 1] == "s"  and board[row + 1][col + 2] == "s")):
                            return True
                        else:
                            fieldOccupied = True
                            #getting the occupied field
                            for i in range(col, col+3):
                                if(board[row+1][i] != " "):
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
                    if(col + 3 <= len(board[0]) - 1):
                        if((board[row][col + 3] == " ") or (board[row][col + 3] == "s")):
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
            if(row + 3 <= len(board) - 1):
                if((board[row + 2][col] == " " and board[row + 3][col] == " " and board[row + 2][col + 1] == " " and board[row + 3][col + 1] == " ") or (board[row + 2][col] == "s" and board[row + 3][col] == "s" and board[row + 2][col + 1] == "s" and board[row + 3][col + 1] == "s")):
                    return True
                else:
                    fieldOccupied = True
                    #getting the field that is occupied
                    for i in range(row+3, row+1, -1):
                        for j in range(col, col+2):
                            if(board[i][j] != " "):
                                occupiedField = (i,j)
                                break #only need to find the first field that is occupied
            else:
                moveBeyondBoard = True
        #moving down
        elif(direction == "d"):
            #checking if the board border is reached or not
            if(row - 2 >= 0):
                if((board[row - 1][col] == " " and board[row - 2][col] == " " and board[row - 1][col + 1] == " " and board[row - 2][col + 1] == " ") or (board[row - 1][col] == "s" and board[row - 2][col] == "s" and board[row - 1][col + 1] == "s" and board[row - 2][col + 1] == "s")):
                    return True
                else:
                    fieldOccupied = True
                    #getting the field that is occupied
                    for i in range(row-2, row):
                        for j in range(col, col+2):
                            if(board[i][j] != " "):
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
                    for i in range(row+1, row-1, -1):
                        for j in range(col-2, col):
                            if(board[i][j] != " "):
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
                    for i in range(row+1, row-1, -1):
                        for j in range(col+2, col+4):
                            if(board[i][j] != " "):
                                occupiedField = (i,j)
                                break #only need to find the first field that is occupied
                    
            else:
                moveBeyondBoard = True
                
                
    #move is invalid
    if(moveBeyondBoard and not gettingAllMoves):
        stdio.writeln("ERROR: Cannot move beyond the board")
        sys.exit()
    if(fieldOccupied and not gettingAllMoves):
        stdio.writeln("ERROR: Field " + str(occupiedField[0]) + " " + str(occupiedField[1]) + " not free")
        sys.exit()
        
#-----------------------------------------------------------------------------------------------------------------------

def continueGame(board):
    """"
    Checks if any of the conditions for the game to continue are met
    Returns a boolean value
    Will print a message depending on what condition is met
    """
    global lightPoints
    global darkPoints
    global gettingAllMoves
    global prevMove
        
    #a player has won with points
    if(lightPoints >= 4 or darkPoints >= 4):
        if(lightPoints >= 4):
            stdio.writeln("Light wins!")
            sys.exit()
        else:
            stdio.writeln("Dark wins!")
            sys.exit()
        
        return False
    
    #partial game -> no more moves left to be inputted
    gettingAllMoves = True
    if(stdio.isEmpty() and ((turn%2 > 0 and getAllMoves(board, "light") == [False]) or (turn%2 == 0 and getAllMoves(board, "dark") == [False]))):
        return False    
    
    #a player has lost by having no more moves
    if((turn%2 > 0 and getAllMoves(board, "light") == []) or (turn%2 == 0 and (getAllMoves(board, "dark") == []))):
        if(turn%2 > 0):
            stdio.writeln("Light loses")
            sys.exit()
        else:
            stdio.writeln("Dark loses")
            sys.exit()

    if(stdio.isEmpty()):
        return False
    
    gettingAllMoves = False  
    
    #game continues
    return True
    
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

def doMove(row, col, direction, board, guiMode):
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
    global turn
    global movesLeft
    global prevMove
    global lightPoints
    global darkPoints
    
    #player is adding a bomb
    if(direction == "b"):
        #checking if the player is on their first move
        if(movesLeft == 2):
            #checking if the field is free or being placed on another bomb
            if(board[row][col] == " "):
                board[row][col] = "o"
            elif(board[row][col] == "o"):
                board[row][col] = " " #bomb is being removed
            else:
                stdio.writeln("ERROR: Field " + str(row) + " " + str(col) + " not free")
                sys.exit()
            movesLeft -= 1
        else:
            stdio.writeln("ERROR: Cannot place bomb after move")
            sys.exit()
    
    #validating if the move is possible
    elif(validateMove(row, col, direction, board)):
        if(movesLeft > 0):           
            #getting the piece type
            pieceType = board[row][col]
            
            #moving a 1x1 piece
            if(pieceType == "a" or pieceType == "A"):
                if(direction == "d"):
                    #checking if the player is moving back to the same spot (will be the opposite to the move here)
                    if(prevMove != "u " + str(row-1) + " " + str(col)):
                        #moving the piece
                        if(board[row-1][col] != "s" and board[row-1][col] != "o"):
                            board[row][col] = " "
                            board[row-1][col] = pieceType
                            prevMove = "d " + str(row) + " " + str(col)
                        elif(board[row-1][col] == "o"): #field is a bomb
                            board[row][col] = " "
                            board[row-1][col] = " "
                            prevMove = ""
                        else: #field is a sink
                            board[row][col] = " "
                            if(turn%2 == 0): #dark scores
                                darkPoints += 1
                            else: #light scores
                                lightPoints += 1
                    else: #player is moving back to the same spot
                        stdio.writeln("ERROR: Piece cannot be returned to starting position")
                        sys.exit()
                elif(direction == "u"):
                    if(prevMove != "d " + str(row+1) + " " + str(col)):
                        #moving the piece
                        if(board[row+1][col] != "s" and board[row+1][col] != "o"):
                            board[row][col] = " "
                            board[row+1][col] = pieceType
                            prevMove = "u " + str(row) + " " + str(col)
                        elif(board[row+1][col] == "o"): #field is a bomb
                            board[row][col] = " "
                            board[row+1][col] = " "
                            prevMove = ""
                        else: #field is a sink
                            board[row][col] = " "
                            if(turn%2 == 0):
                                darkPoints += 1
                            else:
                                lightPoints += 1
                    else: #player is moving back to the same spot
                        stdio.writeln("ERROR: Piece cannot be returned to starting position")
                        sys.exit()
                elif(direction == "l"):
                    if(prevMove != "r " + str(row) + " " + str(col-1)):
                        if(board[row][col-1] != "s" and board[row][col-1] != "o"):
                            #moving the piece
                            board[row][col] = " "
                            board[row][col-1] = pieceType
                            prevMove = "l " + str(row) + " " + str(col)
                        elif(board[row][col-1] == "o"): #field is a bomb
                            board[row][col] = " "
                            board[row][col-1] = " "
                            prevMove = ""
                        else: #field is a sink
                            board[row][col] = " "
                            if(turn%2 == 0):
                                darkPoints += 1
                            else:
                                lightPoints += 1
                    else: #player is moving back to the same spot
                        stdio.writeln("ERROR: Piece cannot be returned to starting position")
                        sys.exit()
                elif(direction == "r"):
                    if(prevMove != "l " + str(row) + " " + str(col+1)):
                        #moving the piece
                        if(board[row][col+1] != "s" and board[row][col+1] != "o"):
                            board[row][col] = " "
                            board[row][col+1] = pieceType
                            prevMove = "r " + str(row) + " " + str(col)
                        elif(board[row][col+1] == "o"): #field is a bomb
                            board[row][col] = " "
                            board[row][col+1] = " "
                        else: #piece is a sink
                            board[row][col] = " "
                            if(turn%2 == 0):
                                darkPoints += 1
                            else:
                                lightPoints += 1
                    else: #player is moving back to the same spot
                        stdio.writeln("ERROR: Piece cannot be returned to starting position")
                        sys.exit()
                
                #decreasing the moves left
                movesLeft -= 1
            
            
            #moving a 1x2 piece
            elif(pieceType == "b" or pieceType == "B"):
                #checking if the piece is upright or not
                if(checkPieceUpright(row, col, board)):
                    #moving downwards
                    if(direction == "d"):
                        #checking if the player is moving back to the same spot (will be the opposite to the move here)
                        if(prevMove != "u " + str(row-1) + " " + str(col)):
                            #moving the piece
                            if(board[row-1][col] != "s"): #only need to check for one because this is checked in validateMove
                                value = ((row-2)*len(board[0][:])) + col
                                board[row][col] = " "
                                board[row-1][col] = str(value) 
                                board[row-2][col] = pieceType
                                prevMove = "d " + str(row) + " " + str(col)
                            else: #moving into a sink
                                board[row][col] = " "
                                if(turn%2 == 0): #dark scores
                                    darkPoints += 2
                                else: #light scores
                                    lightPoints += 2        
                        else: #player is moving back to the same spot
                            stdio.writeln("ERROR: Piece cannot be returned to starting position")
                            sys.exit()
                    elif(direction == "u"):
                        if(prevMove != "d " + str(row+2) + " " + str(col)):
                            #moving the piece
                            if(board[row+1][col] != "s"): #only need to check for one because this is checked in validateMove
                                value = ((row+1)*len(board[0][:])) + col
                                board[row][col] = " "
                                board[row+1][col] = pieceType
                                board[row+2][col] = str(value)
                                prevMove = "u " + str(row) + " " + str(col)
                            else: #moving into a sink
                                board[row][col] = " "
                                if(turn%2 == 0): #dark scores
                                    darkPoints += 2
                                else: #light scores
                                    lightPoints += 2
                        else: #player is moving back to the same spot
                            stdio.writeln("ERROR: Piece cannot be returned to starting position")
                            sys.exit()
                    elif(direction == "l"):
                        if(prevMove != "r " + str(row) + " " + str(col-1)):
                            #moving the piece
                            if(board[row][col-1] != "s"):
                                value = (row*len(board[0][:])) + col-2
                                board[row][col] = " "
                                board[row][col-2] = pieceType
                                board[row][col-1] = str(value)
                                prevMove = "l " + str(row) + " " + str(col)
                            else: #moving into a sink
                                board[row][col] = " "
                                if(turn%2 == 0): #dark scores
                                    darkPoints += 2
                                else: #light scores
                                    lightPoints += 2
                        else: #player is moving back to the same spot
                            stdio.writeln("ERROR: Piece cannot be returned to starting position")
                            sys.exit()
                    elif(direction == "r"):
                        if(prevMove != "l " + str(row) + " " + str(col+1)):
                            #moving the piece
                            if(board[row][col+1] != "s"):
                                value = (row*len(board[0][:])) + col+1
                                board[row][col] = " "
                                board[row][col+1] = pieceType
                                board[row][col+2] = str(value)
                                prevMove = "r " + str(row) + " " + str(col)
                            else: #moving into a sink
                                board[row][col] = " "
                                if(turn%2 == 0): #dark scores
                                    darkPoints += 2
                                else: #light scores
                                    lightPoints += 2
                        else: #player is moving back to the same spot
                            stdio.writeln("ERROR: Piece cannot be returned to starting position")
                            sys.exit()
                            
                else: #piece is on its side
                    #finding the direction the piece is lying in
                    lyingDirection = None
                    value = (row*len(board[0][:])) + col
                    #the value associated with the piece will only ever be down or to the right of the coordinates given because the coordinates are the bottom left of the piece
                    #down
                    if(str(board[row+1][col]) == str(value)):
                        lyingDirection = "vertical"
                    #right
                    else:
                        lyingDirection = "horizontal"
                        
                    #moving the piece
                    if(lyingDirection == "vertical"):
                        #moving up
                        if(direction == "u"):
                            if(prevMove != ("d " + str(row+2) + " " + str(col))):
                                #moving the piece
                                if(str(board[row+2][col]) != "s"):
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    board[row+2][col] = pieceType
                                    prevMove = "u " + str(row) + " " + str(col)
                                else: #piece is being sunk
                                    board[row][col] = " "
                                    if(turn%2 == 0):
                                        darkPoints += 2
                                    else:
                                        lightPoints += 2
                            else: #player is moving back to the same spot
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()  
                        #moving down
                        elif(direction == "d"):
                            if(prevMove != ("u " + str(row-1) + " " + str(col))):
                                #moving the piece
                                if(board[row-1][col] != "s"):
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    board[row-1][col] = pieceType
                                    prevMove = "d " + str(row) + " " + str(col)
                                else:
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    if(turn%2 == 0):
                                        darkPoints += 2
                                    else:
                                        lightPoints += 2
                            else: #player is moving back to the same spot
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                        #moving left
                        elif(direction == "l"):
                            if(prevMove != ("r " + str(row) + " " + str(col+1))):
                                #moving the piece
                                value = (row*len(board[0][:])) + col-1
                                if(board[row][col-1] != "s"):
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    board[row][col-1] = pieceType
                                    board[row+1][col-1] = str(value)
                                    prevMove = "l " + str(row) + " " + str(col)
                                else:
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    if(turn%2 == 0):
                                        darkPoints += 2
                                    else:
                                        lightPoints += 2
                            else:
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                        #moving right
                        elif(direction == "r"):
                            if(prevMove != ("l " + str(row) + " " + str(col+1))):
                                #moving the piece
                                value = (row*len(board[0][:])) + col+1
                                if(board[row][col+1] != "s"):
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    board[row][col+1] = pieceType
                                    board[row+1][col+1] = str(value)
                                    prevMove = "r " + str(row) + " " + str(col)
                                else:
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    if(turn%2 == 0):
                                        darkPoints += 2
                                    else:
                                        lightPoints += 2
                            else:
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                    else: #piece is horizontal
                        #moving down
                        if(direction == "d"):
                            if(prevMove != ("u " + str(row-1) + " " + str(col))):
                                #moving the piece
                                if(board[row-1][col] != "s"):
                                    value = ((row-1)*len(board[0][:])) + col
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    board[row-1][col] = pieceType
                                    board[row-1][col+1] = str(value)
                                    prevMove = "d " + str(row) + " " + str(col)
                                else:
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    if(turn%2 == 0):
                                        darkPoints += 2
                                    else:
                                        lightPoints += 2
                            else:
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                        #moving up
                        elif(direction == "u"):
                            if(prevMove != ("d " + str(row+1) + " " + str(col))):
                                #moving the piece
                                if(board[row+1][col] != "s"):
                                    value = ((row+1)*len(board[0][:])) + col
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    board[row+1][col] = pieceType
                                    board[row+1][col+1] = str(value)
                                    prevMove = "u " + str(row) + " " + str(col)
                                else:
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    if(turn%2 == 0):
                                        darkPoints += 2
                                    else:
                                        lightPoints += 2
                            else:
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                        #moving left
                        elif(direction == "l"):
                            if(prevMove != ("r " + str(row) + " " + str(col-1))):
                                #moving the piece
                                if(board[row][col-1] != "s"):
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    board[row][col-1] = pieceType
                                    prevMove = "l " + str(row) + " " + str(col)
                                else:
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    if(turn%2 == 0):
                                        darkPoints += 2
                                    else:
                                        lightPoints += 2
                            else:
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                        #moving right
                        elif(direction == "r"):
                            if(prevMove != ("l " + str(row) + " " + str(col+2))):
                                #moving the piece
                                if(board[row][col+2] != "s"):
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    board[row][col+2] = pieceType
                                    prevMove = "r " + str(row) + " " + str(col)
                                else:
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    if(turn%2 == 0):
                                        darkPoints += 2
                                    else:
                                        lightPoints += 2
                            else:
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                                
                #decreasing the moves left
                movesLeft -= 1
                
                
            #moving a 1x3 piece
            elif(pieceType == "c" or pieceType == "C"):
                #checking if the piece is upright or not
                if(checkPieceUpright(row, col, board)):
                    #moving downwards
                    if(direction == "d"):
                        #checking if the player is moving back to the same spot (will be the opposite to the move here)
                        if(prevMove != "u " + str(row-1) + " " + str(col)):
                            #moving the piece
                            if(board[row-1][col] != "s"): #remove this at some stage
                                value = ((row-3)*len(board[0][:])) + col
                                board[row][col] = " "
                                board[row-1][col] = str(value) 
                                board[row-2][col] = str(value) 
                                board[row-3][col] = pieceType
                                prevMove = "d " + str(row) + " " + str(col)
                            #will never move into a sink because the piece is 1x3
                        else: #player is moving back to the same spot
                            stdio.writeln("ERROR: Piece cannot be returned to starting position")
                            sys.exit()
                    #moving upwards
                    elif(direction == "u"):
                        if(prevMove != "d " + str(row-1) + " " + str(col)):
                            #moving the piece
                            if(board[row+1][col] != "s"): #remove this at some stage
                                value = ((row+1)*len(board[0][:])) + col
                                board[row][col] = " "
                                board[row+1][col] = pieceType
                                board[row+2][col] = str(value)
                                board[row+3][col] = str(value)
                                prevMove = "u " + str(row) + " " + str(col)
                            #will never move into a sink because the piece is 1x3
                        else: #player is moving back to the same spot
                            stdio.writeln("ERROR: Piece cannot be returned to starting position")
                            sys.exit()
                    #moving left
                    elif(direction == "l"):
                        if(prevMove != "r " + str(row) + " " + str(col-1)):
                            #moving the piece
                            if(board[row][col-1] != "s"): #remove this at some stage
                                value = (row*len(board[0][:])) + col-3
                                board[row][col] = " "
                                board[row][col-3] = pieceType
                                board[row][col-2] = str(value)
                                board[row][col-1] = str(value)
                                prevMove = "l " + str(row) + " " + str(col)
                            #will never move into a sink because the piece is 1x3
                        else: #player is moving back to the same spot
                            stdio.writeln("ERROR: Piece cannot be returned to starting position")
                            sys.exit()
                    #moving right
                    elif(direction == "r"):
                        if(prevMove != "l " + str(row) + " " + str(col+1)):
                            #moving the piece
                            if(board[row][col+1] != "s"): #remove this at some stage
                                value = (row*len(board[0][:])) + col+1
                                board[row][col] = " "
                                board[row][col+1] = pieceType
                                board[row][col+2] = str(value)
                                board[row][col+3] = str(value)
                                prevMove = "r " + str(row) + " " + str(col)
                            #will never move into a sink because the piece is 1x3
                        else: #player is moving back to the same spot
                            stdio.writeln("ERROR: Piece cannot be returned to starting position")
                            sys.exit()
                else: #piece is on its side
                    #finding the direction the piece is lying in
                    lyingDirection = None
                    value = (row*len(board[0][:])) + col
                    #the value associated with the piece will only ever be down or to the right of the coordinates given because the coordinates are the bottom left of the piece
                    #down
                    if(str(board[row+1][col]) == str(value)):
                        lyingDirection = "vertical"
                    #right
                    else:
                        lyingDirection = "horizontal"
                        
                    #moving the piece
                    if(lyingDirection == "vertical"):
                        #moving up
                        if(direction == "u"):
                            if(prevMove != ("d " + str(row+3) + " " + str(col))):
                                #moving the piece
                                if(str(board[row+3][col]) != "s"):
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    board[row+2][col] = " "
                                    board[row+3][col] = pieceType
                                    prevMove = "u " + str(row) + " " + str(col)
                                else: #piece is being sunk
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    board[row+2][col] = " "
                                    if(turn%2 == 0):
                                        darkPoints += 3
                                    else:
                                        lightPoints += 3
                            else:   #player is moving back to the same spot
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                        #moving down
                        elif(direction == "d"):
                            if(prevMove != ("u " + str(row-1) + " " + str(col))):
                                #moving the piece
                                if(board[row-1][col] != "s"):
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    board[row+2][col] = " "
                                    board[row-1][col] = pieceType
                                    prevMove = "d " + str(row) + " " + str(col)
                                else: #falls into a sink
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    board[row+2][col] = " "
                                    if(turn%2 == 0): #dark scores
                                        darkPoints += 3
                                    else: #light scores
                                        lightPoints += 3
                            else:   #player is moving back to the same spot
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                        #moving left
                        elif(direction == "l"):
                            if(prevMove != ("r " + str(row) + " " + str(col-1))):
                                #moving the piece
                                if(board[row][col-1] != "s"): #remove this at some stage
                                    value = (row*len(board[0][:])) + col-1
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    board[row+2][col] = " "
                                    board[row][col-1] = pieceType
                                    board[row+1][col-1] = str(value)
                                    board[row+2][col-1] = str(value)
                                    prevMove = "l " + str(row) + " " + str(col)
                                #will never move into a sink because the piece is 1x3
                            else: #player is moving back to the same spot
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                        #moving right
                        elif(direction == "r"):
                            if(prevMove != ("l " + str(row) + " " + str(col+1))):
                                #moving the piece
                                if(board[row][col+1] != "s"): #remove this at some stage
                                    value = (row*len(board[0][:])) + col+1
                                    board[row][col] = " "
                                    board[row+1][col] = " "
                                    board[row+2][col] = " "
                                    board[row][col+1] = pieceType
                                    board[row+1][col+1] = str(value)
                                    board[row+2][col+1] = str(value)
                                    prevMove = "r " + str(row) + " " + str(col)
                                #will never move into a sink because the piece is 1x3
                            else: #player is moving back to the same spot
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                                
                    else: #piece is horizontal
                        #moving down
                        if(direction == "d"):
                            if(prevMove != ("u " + str(row-1) + " " + str(col))):
                                #moving the piece
                                if(board[row+1][col] != "s"): #remove at some stage
                                    value = ((row-1)*len(board[0][:])) + col
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    board[row][col+2] = " "
                                    board[row-1][col] = pieceType
                                    board[row-1][col+1] = str(value)
                                    board[row-1][col+2] = str(value)
                                    prevMove = "d " + str(row) + " " + str(col)
                                #piece can never fall into a sink because it is 1x3
                            else: #player is moving back to the same spot
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                        #moving up
                        elif(direction == "u"):
                            if(prevMove != ("d " + str(row+1) + " " + str(col))):
                                #moving the piece
                                if(board[row-1][col] != "s"): #remove at some stage
                                    value = ((row+1)*len(board[0][:])) + col
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    board[row][col+2] = " "
                                    board[row+1][col] = pieceType
                                    board[row+1][col+1] = str(value)
                                    board[row+1][col+2] = str(value)
                                    prevMove = "u " + str(row) + " " + str(col)
                                #piece can never fall into a sink because it is 1x3
                            else: #player is moving back to the same spot
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                        #moving left
                        elif(direction == "l"):
                            if(prevMove != ("r " + str(row) + " " + str(col-1))):
                                #moving the piece
                                if(board[row][col-1] != "s"):
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    board[row][col+2] = " "
                                    board[row][col-1] = pieceType
                                    prevMove = "l " + str(row) + " " + str(col)
                                else: #falling into a sink
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    board[row][col+2] = " "
                                    if(turn%2 == 0):
                                        darkPoints += 3
                                    else:
                                        lightPoints += 3
                            else: #player is moving back to the same spot
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                        #moving right
                        elif(direction == "r"):
                            if(prevMove != ("l " + str(row) + " " + str(col-3))):
                                #moving the piece
                                if(board[row][col+3] != "s"):
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    board[row][col+2] = " "
                                    board[row][col+3] = pieceType
                                    prevMove = "r " + str(row) + " " + str(col)
                                else:
                                    board[row][col] = " "
                                    board[row][col+1] = " "
                                    board[row][col+2] = " "
                                    if(turn%2 == 0):
                                        darkPoints += 3
                                    else:
                                        lightPoints += 3
                            else:
                                stdio.writeln("ERROR: Piece cannot be returned to starting position")
                                sys.exit()
                
                #decreasing the moves left
                movesLeft -= 1            

            #moving a 2x2 piece
            elif(pieceType == "d" or pieceType == "D"):
                #moving up
                if(direction == "u"):
                    #moving the piece
                    if(board[row+2][col] != "s"):
                        value = ((row+2)*len(board[0][:])) + col
                        board[row][col] = " "
                        board[row+1][col] = " "
                        board[row][col+1] = " "
                        board[row+1][col+1] = " "
                        board[row+2][col] = pieceType
                        board[row+3][col+1] = str(value)
                        board[row+2][col+1] = str(value)
                        board[row+3][col] = str(value)
                        prevMove = "u " + str(row) + " " + str(col)
                    else: #field is a sink
                        board[row][col] = " "
                        board[row+1][col] = " "
                        board[row][col+1] = " "
                        board[row+1][col+1] = " "
                        if(turn%2 == 0):
                            darkPoints += 4
                        else:
                            lightPoints += 4
                #moving down
                elif(direction == "d"):
                    #moving the piece
                    if(board[row-2][col] != "s"):
                        value = ((row-1)*len(board[0][:])) + col
                        board[row][col] = " "
                        board[row+1][col] = " "
                        board[row][col+1] = " "
                        board[row+1][col+1] = " "
                        board[row-2][col] = pieceType
                        board[row-2][col+1] = str(value)
                        board[row-1][col+1] = str(value)
                        board[row-1][col] = str(value)
                        prevMove = "d " + str(row) + " " + str(col)
                    else: #field is a sink
                        board[row][col] = " "
                        board[row+1][col] = " "
                        board[row][col+1] = " "
                        board[row+1][col+1] = " "
                        if(turn%2 == 0):
                            darkPoints += 4
                        else:
                            lightPoints += 4
                #moving left
                elif(direction == "l"):
                    #moving the piece
                    if(board[row][col-1] != "s"):
                        value = (row*len(board[0][:])) + col-2
                        board[row][col] = " "
                        board[row+1][col] = " "
                        board[row][col+1] = " "
                        board[row+1][col+1] = " "
                        board[row][col-2] = pieceType
                        board[row+1][col-1] = str(value)
                        board[row+1][col-2] = str(value)
                        board[row][col-1] = str(value)
                        prevMove = "l " + str(row) + " " + str(col)
                    else:
                        board[row][col] = " "
                        board[row+1][col] = " "
                        board[row][col+1] = " "
                        board[row+1][col+1] = " "
                        if(turn%2 == 0):
                            darkPoints += 4
                        else:
                            lightPoints += 4
                #moving right
                elif(direction == "r"):
                    #moving the piece
                    if(board[row][col+2] != "s"):
                        value = (row*len(board[0][:])) + col+2
                        board[row][col] = " "
                        board[row+1][col] = " "
                        board[row][col+1] = " "
                        board[row+1][col+1] = " "
                        board[row][col+2] = pieceType
                        board[row+1][col+3] = str(value)
                        board[row+1][col+2] = str(value)
                        board[row][col+3] = str(value)
                        prevMove = "r " + str(row) + " " + str(col)
                    else:
                        board[row][col] = " "
                        board[row+1][col] = " "
                        board[row][col+1] = " "
                        board[row+1][col+1] = " "
                        if(turn%2 == 0):
                            darkPoints += 4
                        else:
                            lightPoints += 4    
                
                #decreasing the moves left
                movesLeft -= 2
                
            #piece is a blocked field
            elif(pieceType == "x"):
                stdio.writeln("No piece on field " + str(row) + " " + str(col))
                sys.exit()
                
            #piece is a sink
            #elif(pieceType == "s"):
                #MOVING SINK

        #changing the turn
        if(movesLeft == 0):
            #no more moves left for that player 
            turn += 1
            movesLeft += 2
            prevMove = None
        
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

def getAllMoves(board, player):
    """
    Generates a list of all moves (valid or invalid) that could potentially be
    played on the current board.

    Args:
        board (2D array of str): The game board
        player (str): The player whose moves are being generated

    Returns:
        array of moves: The moves that could be played on the given board
    """
    #variables
    moves = []
    pieceFound = False #can be used to indicate whether a player has moves left or not
    moves.append(pieceFound)
    
    #light player
    if(player == "light"):
        #looping through the array to find all the light pieces and check if they have any moves
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                #checking if the field contains an int
                if(not str(board[i][j]).isnumeric()):
                    if(board[i][j].islower() and board[i][j] != "s"):
                        if(not pieceFound): #a piece has been found
                            pieceFound = True
                            moves.remove(False)
                            
                        if(validateMove(i, j, "u", board)):
                            moves.append("u " + str(i) + " " + str(j))
                        if(validateMove(i, j, "d", board)):
                            moves.append("d " + str(i) + " " + str(j))
                        if(validateMove(i, j, "l", board)):
                            moves.append("l " + str(i) + " " + str(j))
                        if(validateMove(i, j, "r", board)):
                            moves.append("r " + str(i) + " " + str(j))
    else:
        #looping through the array to find all the dark pieces and check if they have any moves
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                #checking if the field contains an int
                if(not str(board[i][j]).isnumeric()):  
                    if(board[i][j].isupper()):
                        if(not pieceFound): #a piece has been found
                            pieceFound = True
                            moves.remove(False)
                            
                        if(validateMove(i, j, "u", board)):
                            moves.append("u " + str(i) + " " + str(j))
                        if(validateMove(i, j, "d", board)):
                            moves.append("d " + str(i) + " " + str(j))
                        if(validateMove(i, j, "l", board)):
                            moves.append("l " + str(i) + " " + str(j))
                        if(validateMove(i, j, "r", board)):
                            moves.append("r " + str(i) + " " + str(j))
                            
    #getting the opposite of the prevMove and removing it (means the player is moving back to the same spot)
    reverseMove = ""
    if(prevMove != None):
        if(prevMove[0] == "l"):
            reverseMove = "r " + str(int(prevMove[2])) + " " + str(int(prevMove[4]) - 1)
        elif(prevMove[0] == "r"):
            reverseMove = "l " + str(int(prevMove[2])) + " " + str(int(prevMove[4]) + 1)
        elif(prevMove[0] == "u"):
            reverseMove = "d " + str(int(prevMove[2]) + 1) + " " + str(int(prevMove[4]))
        elif(prevMove[0] == "d"):
            reverseMove = "u " + str(int(prevMove[2]) - 1) + " " + str(int(prevMove[4]))
            
        for i in range(0, len(moves)):
            if(moves[i] == reverseMove):
                moves.remove(reverseMove)
                break
            
                      
    return moves
#=======================================================================================================================


#BOARD=================================================================================================================
#WORKS
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
            sys.exit()
        
        #gets the coordinates of a specific piece and adds it to the board
        elif(piece == "s"):
            #getting the size
            sinkSize = stdio.readString()
            
            #getting the coordinates
            sinkRow = stdio.readString()
            sinkCol = stdio.readString()
            
            #checking if the sink is in the correct range for sink setup 
            if(checkSinkRange(maxRow, maxCol, sinkRow, sinkCol)): #error message is printed in the function
                #converting back to integers
                sinkRow = int(sinkRow)
                sinkCol = int(sinkCol)
                
                #checking if the field is occupied
                if(board[sinkRow][sinkCol] != " "):
                    stdio.writeln("ERROR: Field " + str(sinkRow) + " " + str(sinkCol) + " not free")
                    sys.exit()
                
                #checking if the size is valid
                if(sinkSize != "1" and sinkSize != "2"):
                    stdio.writeln("ERROR: Invalid piece type " + str(sinkSize))
                    sys.exit()
                
                #checking if the piece is 1x1 or 2x2
                if(sinkSize == "1"): #piece is 1x1
                    #checking if there are any sinks around this sink
                    #sink at the top
                    if(sinkRow == maxRow-1):
                        #top-left corner
                        if(sinkCol == 0 ):
                            if(board[sinkRow-1][sinkCol] == "s" or board[sinkRow][sinkCol+1] == "s"):
                                stdio.writeln("ERROR: Sink cannot be next to another sink")
                                sys.exit()
                        #top-right corner
                        elif(sinkCol == maxCol-1):
                            if(board[sinkRow-1][sinkCol] == "s" or board[sinkRow][sinkCol-1] == "s"):
                                stdio.writeln("ERROR: Sink cannot be next to another sink")
                                sys.exit()
                        #sink is just at the top
                        else:
                            if(board[sinkRow-1][sinkCol] == "s" or board[sinkRow][sinkCol-1] == "s" or board[sinkRow][sinkCol+1] == "s"):
                                stdio.writeln("ERROR: Sink cannot be next to another sink")
                                sys.exit()
                        
                    #sink at the bottom
                    elif(sinkRow == 0):
                        #bottom-right corner
                        if(sinkCol == maxCol-1):
                            if(board[sinkRow+1][sinkCol] == "s" or board[sinkRow][sinkCol-1] == "s" or board[sinkRow+1][sinkCol-1] == "s"):
                                stdio.writeln("ERROR: Sink cannot be next to another sink")
                                sys.exit()
                        #bottom-left corner
                        elif(sinkCol == 0):
                            if(board[sinkRow+1][sinkCol] == "s" or board[sinkRow][sinkCol+1] == "s" or board[sinkRow+1][sinkCol+1] == "s"):
                                stdio.writeln("ERROR: Sink cannot be next to another sink")
                                sys.exit()
                        #sink is just at the bottom
                        else:
                            if(board[sinkRow+1][sinkCol] == "s" or board[sinkRow][sinkCol-1] == "s" or board[sinkRow][sinkCol+1] == "s"):
                                stdio.writeln("ERROR: Sink cannot be next to another sink")
                                sys.exit()
                    #sink is on the left border
                    elif(sinkCol == 0):
                        if(board[sinkRow-1][sinkCol] == "s" or board[sinkRow+1][sinkCol] == "s" or board[sinkRow][sinkCol+1] == "s"):
                            stdio.writeln("ERROR: Sink cannot be next to another sink")
                            sys.exit()
                    #sink is on the right border
                    elif(sinkCol == maxCol-1):
                        if(board[sinkRow-1][sinkCol] == "s" or board[sinkRow+1][sinkCol] == "s" or board[sinkRow][sinkCol-1] == "s"):
                            stdio.writeln("ERROR: Sink cannot be next to another sink")
                            sys.exit()
                        
                    #sink isn't on any borders
                    else:
                        if(board[sinkRow-1][sinkCol] == "s" or board[sinkRow+1][sinkCol] == "s" or board[sinkRow][sinkCol-1] == "s" or board[sinkRow][sinkCol+1] == "s"):
                            stdio.writeln("ERROR: Sink cannot be next to another sink")
                            sys.exit()
                            
                    #no sinks around this sink
                    board[sinkRow][sinkCol] = "s"
                    
                else:  #piece is 2x2
                    #checking if the sink can fit on the board
                    if(sinkRow + 1 > maxRow - 1 or sinkCol + 1 > maxCol - 1):
                        stdio.writeln("ERROR: Sink in the wrong position")
                        sys.exit()
                        
                    #checking if the extra fields needed for this sink size are in the correct position
                    elif((sinkRow + 1 < 3 or sinkRow + 1 > maxRow - 3) or (sinkCol + 1 < 3 or sinkCol + 1 > maxCol - 3)):
                        #checking if there is a sink already in the extra fields
                        #there is
                        if(board[sinkRow][sinkCol + 1] != " " or board[sinkRow + 1][sinkCol] != " " or board[sinkRow + 1][sinkCol + 1] != " "):
                            #getting the field that is occupied
                            for i in range(sinkRow+1, sinkRow-1, -1):
                                for j in range(sinkCol, sinkCol+2):
                                    if(board[i][j] != " "):
                                        stdio.writeln("ERROR: Field " + str(i) + " " + str(j) + " not free")
                                        sys.exit()
                        #there isn't        
                        else:  
                            #checking if there are any sinks around this sink
                            #sink isn't on any borders
                            if(sinkRow + 1 < maxRow-1 and sinkCol + 1 < maxCol-1 and sinkRow > 0 and sinkCol > 0):
                                if(board[sinkRow+2][sinkCol] == "s" or board[sinkRow+2][sinkCol+1] == "s" or board[sinkRow+1][sinkCol-1] == "s" or board[sinkRow+1][sinkCol+2] == "s" or board[sinkRow][sinkCol-1] == "s" or board[sinkRow][sinkCol+2] == "s" or board[sinkRow-1][sinkCol] == "s" or board[sinkRow-1][sinkCol+1] == "s"):
                                    stdio.writeln("ERROR: Sink cannot be next to another sink")
                                    sys.exit()
                            #sink top-left corner
                            elif(sinkCol == 0 and sinkRow+1 == maxRow-1):
                                if(board[sinkRow-1][sinkCol] == "s" or board[sinkRow-1][sinkCol+1] == "s" or board[sinkRow][sinkCol+2] == "s" or board[sinkRow+1][sinkCol+2] == "s"):
                                    stdio.writeln("ERROR: Sink cannot be next to another sink")
                                    sys.exit()
                            #sink top-right corner
                            elif(sinkCol+1 == maxCol-1 and sinkRow+1 == maxRow-1):
                                if(board[sinkRow-1][sinkCol+1] == "s" or board[sinkRow-1][sinkCol] == "s" or board[sinkRow][sinkCol-1] == "s" or board[sinkRow+1][sinkCol-1] == "s"):
                                    stdio.writeln("ERROR: Sink cannot be next to another sink")
                                    sys.exit()
                            #sink bottom-right corner
                            elif(sinkCol+1 == maxCol-1 and sinkRow == 0):
                                if(board[sinkRow][sinkCol-1] == "s" or board[sinkRow+1][sinkCol-1] == "s" or board[sinkRow+2][sinkCol] == "s" or board[sinkRow+2][sinkCol+1] == "s"):
                                    stdio.writeln("ERROR: Sink cannot be next to another sink")
                                    sys.exit()
                            #sink bottom-left corner
                            elif(sinkCol == 0 and sinkRow == 0):
                                if(board[sinkRow+2][sinkCol] == "s" or board[sinkRow+2][sinkCol+1] == "s" or board[sinkRow+1][sinkCol+2] == "s" or board[sinkRow][sinkCol+2] == "s"):
                                    stdio.writeln("ERROR: Sink cannot be next to another sink")
                                    sys.exit()                                       
                            #sink on the top border
                            elif(sinkRow+1 == maxRow-1):
                                if(board[sinkRow+1][sinkCol-1] == "s" or board[sinkRow][sinkCol-1] == "s" or board[sinkRow-1][sinkCol] == "s" or board[sinkRow-1][sinkCol+1] == "s" or board[sinkRow][sinkCol+2] == "s" or board[sinkRow+1][sinkCol+2] == "s"):
                                    stdio.writeln("ERROR: Sink cannot be next to another sink")
                                    sys.exit()
                            #sink on the bottom border
                            elif(sinkRow == 0):
                                if(board[sinkRow][sinkCol-1] == "s" or board[sinkRow+1][sinkCol-1] == "s" or board[sinkRow+2][sinkCol] == "s" or board[sinkRow+2][sinkCol+1] == "s" or board[sinkRow+1][sinkCol+2] == "s" or board[sinkRow][sinkCol+2] == "s"):
                                    stdio.writeln("ERROR: Sink cannot be next to another sink")
                                    sys.exit()
                            #sink on the left border
                            elif(sinkCol == 0): 
                                if(board[sinkRow+2][sinkCol] == "s" or board[sinkRow+2][sinkCol+1] == "s" or board[sinkRow+1][sinkCol+2] == "s" or board[sinkRow][sinkCol+2] == "s" or board[sinkRow-1][sinkCol+1] == "s" or board[sinkRow-1][sinkCol] == "s"):
                                    stdio.writeln("ERROR: Sink cannot be next to another sink")
                                    sys.exit()
                            #sink on the right border
                            elif(sinkCol == maxCol-1): 
                                if(board[sinkRow-1][sinkCol+1] == "s" or board[sinkRow-1][sinkCol] == "s" or board[sinkRow][sinkCol-1] == "s" or board[sinkRow+1][sinkCol-1] == "s" or board[sinkRow+2][sinkCol] == "s" or board[sinkRow+2][sinkCol+1] == "s"):
                                    stdio.writeln("ERROR: Sink cannot be next to another sink")
                                    sys.exit()
                                
                            #no sinks around this sink                     
                            board[sinkRow][sinkCol] = "s"
                            board[sinkRow][sinkCol + 1] = "s"
                            board[sinkRow + 1][sinkCol] = "s"
                            board[sinkRow + 1][sinkCol + 1] = "s"
                    #sink in the wrong position
                    else:
                        stdio.writeln("ERROR: Sink in the wrong position")
                        sys.exit()
                
                
        elif(piece == "l"):
            #getting the piece type
            pieceType = stdio.readString()
            
            #getting the coordinates
            pieceRow = stdio.readString()
            pieceCol = stdio.readString()

            #checking that the field is in a valid position for piece setup
            if(checkPieceRange(maxRow, maxCol, pieceRow, pieceCol)): #error message is printed in the function
                #converting back to integers
                pieceRow = int(pieceRow)
                pieceCol = int(pieceCol)
                
                #checking if the field is occupied
                if(board[pieceRow][pieceCol] != " "):
                    stdio.writeln("ERROR: Field " + pieceRow + " " + pieceCol + " not free")
                    sys.exit()
                
                #checking if the piece type is valid
                if(pieceType != "a" and pieceType != "b" and pieceType != "c" and pieceType != "d"):
                    stdio.writeln("ERROR: Invalid piece type " + pieceType)  
                    sys.exit()  
                    
                if(pieceType == "d"): 
                    #checking if there is a piece already in the extra fields
                    if(board[pieceRow][pieceCol + 1] != " " or board[pieceRow + 1][pieceCol] != " " or board[pieceRow + 1][pieceCol + 1] != " "):
                        #getting the field that is occupied
                        for i in range(pieceRow+1, pieceRow-1, -1):
                            for j in range(pieceCol, pieceCol+2):
                                if(board[i][j] != " "):
                                    stdio.writeln("ERROR: Field " + str(i) + " " + str(j) + " not free")
                                    sys.exit() #only need to find the first field that is occupied
                                
                    #checking if the piece can fit according to the standards of setup
                    elif(pieceRow + 1 < maxRow - 3 and pieceCol + 1 <= maxCol - 3):
                        value = (pieceRow*maxCol)+pieceCol
                        board[pieceRow][pieceCol] = "d"
                        board[pieceRow][pieceCol + 1] = str(value)
                        board[pieceRow + 1][pieceCol] = str(value)
                        board[pieceRow + 1][pieceCol + 1] = str(value)
                    else:
                        stdio.writeln("ERROR: Piece in the wrong position")
                        sys.exit()
                        
                else: #all the other pieces will be upright anyways
                    board[pieceRow][pieceCol] = pieceType
                    
            
        elif(piece == "d"):
            #getting the piece type
            pieceType = stdio.readString()
            
            #getting the coordinates
            pieceRow = stdio.readString()
            pieceCol = stdio.readString()   
            
            #checking that the field is in a valid position for piece setup
            if(checkPieceRange(maxRow, maxCol, pieceRow, pieceCol)): #error message is printed in the function
                #converting back to integers
                pieceRow = int(pieceRow)
                pieceCol = int(pieceCol)
                
                #checking if the field is occupied
                if(board[pieceRow][pieceCol] != " "):
                    stdio.writeln("ERROR: Field " + str(pieceRow) + " " + str(pieceCol) + " not free")
                    sys.exit()
                
                #checking if the piece type is valid
                if(pieceType != "a" and pieceType != "b" and pieceType != "c" and pieceType != "d"):
                    stdio.writeln("ERROR: Invalid piece type " + pieceType)  
                    sys.exit()
                
                if(pieceType == "d"): 
                    #checking if there is a piece already in the extra fields
                    if(board[pieceRow][pieceCol + 1] != " " or board[pieceRow + 1][pieceCol] != " " or board[pieceRow + 1][pieceCol + 1] != " "):
                        #getting the field that is occupied
                        for i in range(pieceRow+1, pieceRow-1, -1):
                            for j in range(pieceCol, pieceCol+2):
                                if(board[i][j] != " "):
                                    stdio.writeln("ERROR: Field " + str(i) + " " + str(j) + " not free")
                                    sys.exit() #only need to find the first field that is occupied
                                
                    #checking if the piece can fit according to the standards of setup
                    elif(pieceRow + 1 < maxRow - 3 and pieceCol + 1 <= maxCol - 3):
                        value = (pieceRow*maxCol)+pieceCol
                        board[pieceRow][pieceCol] = "D"
                        board[pieceRow][pieceCol + 1] = str(value)
                        board[pieceRow + 1][pieceCol] = str(value)
                        board[pieceRow + 1][pieceCol + 1] = str(value)
                    else:
                        stdio.writeln("ERROR: Piece in the wrong position")
                        sys.exit()
                else: #all the other pieces will be upright anyways
                    board[pieceRow][pieceCol] = pieceType.upper()
                    
        elif(piece == "x"):
            #getting the coordinates
            pieceRow = stdio.readString()
            pieceCol = stdio.readString()
            
            #checking that the coordinates given are numbers
            if(not pieceRow.isnumeric() or not pieceCol.isnumeric()):
                stdio.writeln("ERROR: Field " + pieceRow + " " + pieceCol + " not on board")
                sys.exit()
                
            #converting back to integers
            pieceRow = int(pieceRow)
            pieceCol = int(pieceCol)
            
            #checking that the field is open
            if(board[pieceRow][pieceCol] == " "):
                board[pieceRow][pieceCol] = "x"
            else:
                stdio.writeln("ERROR: Field " + str(pieceRow) + " " + str(pieceCol) + " not free")
                sys.exit()
                    
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
    rowCount = len(board) - 1
    for i in range(rowCount, -1, -1):
        #writing out the divider between each row
        stdio.write("  +")
        for j in range(0, columnMax):
            stdio.write("--+")
        stdio.writeln()
        
        #writing out the row number
        stdio.write(str(rowCount) + " |")
        
        #writing out the values of the array into their respective places
        for j in range(0, len(board[i])):
            #ensuring that the board stays aligned according to the number of digits
            if(len(str(board[i][j])) == 1 and board[i][j] != "o"):
                stdio.write(" " + board[i][j] + "|")
            elif(board[i][j] == "o"):
                stdio.write("  |")
            else:
                stdio.write(str(board[i][j]) + "|")
        stdio.writeln()
        rowCount-=1
        
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
#WORKS
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
    
    #referencing game variables 
    global movesLeft
    global turn
    global lightPoints
    global darkPoints  
    
    #checking if the board is already empty --> means light loses
    if(board == [[" "]*int(maxCol)]*int(maxRow)):
        stdio.writeln("Light loses")
        sys.exit()
    
    #looping until game win/lose condition is met
    while(continueGame(board)):
        #reading in the move
        fieldRow = stdio.readInt()
        fieldCol = stdio.readInt()
        direction = stdio.readString()
        
        #checking if the move is valid
        if(checkMoveInput(fieldRow, fieldCol, direction, board)):
            #doing the move
            doMove(fieldRow, fieldCol, direction, board, guiMode)           
            #printing the board
            printBoard(board)
    #printing any possible wins that may have occured after the input stream has ended
    continueGame(board)
#=======================================================================================================================


#MAIN==================================================================================================================
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
        
        #setting the global variables
        maxRowGlobal = maxRow
        maxColGlobal = maxCol
        
        #performing error checks to ensure the arguements are valid
        if(checkArgs(maxRow, maxCol, guiMode)): #error message is printed when this is run
            if(not stdio.isEmpty()):
                #reading the board
                board = readBoard(maxRow, maxCol)
                printBoard(board)
                gameLoop(board, guiMode)
            else:
                stdio.writeln("Light loses")
            #type setup_board_test.txt|python SU28022351.py 10 10 0  
            #type problem.txt|python SU28022351.py 10 10 0
#=======================================================================================================================       
