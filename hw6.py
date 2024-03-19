#################################################
# hw6.py
#
# Your name: Natalie Hutner
# Your andrew id: nhutner
# This assignment is SOLO!
#################################################

import cs112_f22_week6_linter
import math, copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Tetris
#################################################

#HELPER FUNCTIONS 
def playTetris():
    # gameDimensions() calculates the correct width and height values 
    # from rows, cols, cellSize, and margin
    rows, cols, cellSize, margin = gameDimensions()
    width = (cellSize * cols) + (margin*2)
    height = (cellSize * rows) + (margin*2)
    runApp(width=width, height=height)

def gameDimensions():
    # These values are set to the writeup defaults
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

def newFallingPiece(app):
    import random
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    randomColor = random.randint(0, len(app.tetrisPieceColors)-1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomColor]
    app.fallingPieceRow = 0
    app.fallingPieceCol = (app.cols//2)- (len(app.fallingPiece[0])//2)

def moveFallingPiece(app, drow, dcol):
    app.fallingPieceRow = app.fallingPieceRow + drow
    app.fallingPieceCol = app.fallingPieceCol + dcol
    if fallingPieceIsLegal(app) == False:
        app.fallingPieceRow = app.fallingPieceRow - drow
        app.fallingPieceCol = app.fallingPieceCol - dcol
        return False
    return True

def fallingPieceIsLegal(app):
    rows, cols = len(app.fallingPiece), len(app.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if app.fallingPiece[row][col] == True:
                cellRow = app.fallingPieceRow + row
                cellCol = app.fallingPieceCol + col
                if ((cellRow >= app.rows) or (cellCol < 0) or 
                (cellCol >= app.cols)):
                    return False
                if app.board[cellRow][cellCol] != app.emptyColor:
                    return False
    return True

def rotateFallingPiece(app):
    piece = app.fallingPiece
    pieceR = app.fallingPieceRow    #save old row position
    pieceC = app.fallingPieceCol    #save old col position
    pieceRows = len(app.fallingPiece)
    pieceCols = len(app.fallingPiece[0])
    newRows = pieceCols
    newCols = pieceRows
    rotatedPiece = []
    for row in range(newRows):
        rotatedPiece.append([None]*newCols)
    for row in range(pieceRows):
        for col in range(pieceCols):
            rotatedPiece[(pieceCols-1)-col][row] = app.fallingPiece[row][col]
    app.fallingPiece = rotatedPiece
    app.fallingPieceRow = pieceR + (len(piece)//2) - (newRows//2)
    app.fallingPieceCol = pieceC + (len(piece[0])//2) - (newCols//2)
    if fallingPieceIsLegal(app) == False:
        app.fallingPiece = piece
        #revert position:
        app.fallingPieceRow = pieceR
        app.fallingPieceCol = pieceC

def removeFullRows(app):
    fullRows = 0
    boardRows = app.rows
    newBoard = []
    for row in range(len(app.board)):
        if app.emptyColor not in app.board[row]:
            fullRows += 1
            continue
        else:
            newBoard.append(app.board[row])
    emptyRows = boardRows - len(newBoard)   
    for i in range(emptyRows):
        newBoard.insert(0, [app.emptyColor]*len(app.board[0]))
    app.board = newBoard
    app.score += fullRows**2
    
#haven't debugged this function yet
def hardDrop(app):
    #find lowest place app.fallingPiece can fit
    #update app.fallingPieceRow w the new position
    #call placeFallingPiece(app)
    dRow = 1
    while moveFallingPiece(app, dRow, 0) == True:
        dRow += 1 
    placeFallingPiece(app)

#CONTROLLER FUNCTIONS

#model
def appStarted(app):
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.board = []
    app.emptyColor = "blue"
    for row in range(app.rows):
        app.board.append([app.emptyColor]*app.cols)
    app.tetrisPieces = [
    [
        [  True,  True,  True,  True ]     #i piece
    ],
    [
        [  True, False, False ],            #j piece
        [  True,  True,  True ]
    ],
    [
        [ False, False,  True ],            #l piece
        [  True,  True,  True ]
    ],
    [
        [  True,  True ],               #o piece
        [  True,  True ]
    ],
    [
        [ False,  True,  True ],        #s piece
        [  True,  True, False ]
    ],
    [
        [ False,  True, False ],        #t piece
        [  True,  True,  True ]
    ],
    [
        [  True,  True, False ],        #z piece
        [ False,  True,  True ]
    ] ]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", 
    "cyan", "green", "orange" ]
    newFallingPiece(app)    
    app.isGameOver = False
    app.score = 0
    app.timerDelay = 500

def keyPressed(app, event):
    if event.key == 'r':
        appStarted(app)
    if app.isGameOver: return 
    if event.key == 'Down':
        drow = 1
        dcol = 0
        moveFallingPiece(app, drow, dcol)
    elif event.key == 'Right':
        drow = 0
        dcol = 1
        moveFallingPiece(app, drow, dcol)
    elif event.key == 'Left':
        drow = 0
        dcol = -1
        moveFallingPiece(app, drow, dcol)
    elif event.key == 'Up':
        rotateFallingPiece(app)
    elif event.key == 'Space':  
        hardDrop(app)   #this function still has a bug

def timerFired(app):
    if app.isGameOver: 
        return
    if not moveFallingPiece(app, +1, 0):
        placeFallingPiece(app) 
        newFallingPiece(app)
        if not fallingPieceIsLegal(app):
            app.isGameOver = True
            


#VIEW FUNCTIONS 

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, (app.cellSize * app.cols) + (app.margin*2), 
    (app.cellSize * app.rows) + (app.margin*2), fill='orange')
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)
    drawGameOver(app, canvas)
    drawScore(app, canvas)

def drawBoard(app, canvas):
    rows, cols, cellSize, margin = gameDimensions()
    for row in range(rows):
        for col in range(cols):
            color = app.board[row][col]
            drawCell(app, canvas, row, col, color)

def drawCell(app, canvas, row, col, color):
    x0 = app.margin + app.cellSize*col
    y0 = app.margin + app.cellSize*row
    x1 = x0 + app.cellSize
    y1 = y0 + app.cellSize
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, 
    outline = "black", width = 3)

def drawFallingPiece(app, canvas):
    rows, cols = len(app.fallingPiece), len(app.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if app.fallingPiece[row][col] == True:
                drawCell(app, canvas, row + app.fallingPieceRow, 
                col + app.fallingPieceCol, app.fallingPieceColor)
 
#we load the corresponding cells of the fallingPiece
#onto the board with the fallingPieceColor
def placeFallingPiece(app):
    rows, cols = len(app.fallingPiece), len(app.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if app.fallingPiece[row][col] == True:
                rowIndex = app.fallingPieceRow+row
                colIndex = app.fallingPieceCol+col
                app.board[rowIndex][colIndex] = app.fallingPieceColor
    removeFullRows(app)

def drawGameOver(app, canvas):
    if (app.isGameOver):
        canvas.create_rectangle(0, app.height/3, app.width, (app.height/3)*2, 
        fill='black')
        canvas.create_text(app.width/2, app.height/2, text='Game Over!',
                           font='Arial 26 bold italic', fill='lime green')

def drawScore(app, canvas):
    canvas.create_text(app.width/2, app.margin/2, text= f'SCORE: {app.score}',
                           font='Arial 16 bold', fill='blue')

#################################################
# Test Functions
#################################################

# None!  Though... you may wish to (optionally) add some test 
#        functions of your own for any functions that do not 
#        involve graphics


#################################################
# main
#################################################

def main():
    cs112_f22_week6_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()
