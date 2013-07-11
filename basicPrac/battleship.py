#need to back for it,only enhanced to support multi ships now,should support two players also

from random import randint

ships=[]
usedrowindex=[]
usedcolindex=[]
boardSize = 5
board = [["O"] * boardSize for x in range(boardSize)]

##for x in range(boardSize):
##    board.append(["O"] * boardSize)

def print_board(board):
    for row in board:
        print " ".join(row)

def random_row(board):
    ship_row = randint(0, len(board) - 1)
    for i in usedrowindex:
        if i==ship_row:
            return random_row(board)
    usedrowindex.append(ship_row)
    return ship_row

def random_col(board):
    ship_col = randint(0, len(board[0]) - 1)
    for i in usedcolindex:
        if i==ship_col:
            return random_col(board)
    usedcolindex.append(ship_col)
    return ship_col

def generatemultiships(totalships):
    total=[]
    for i in range(totalships):
        ship_row = random_row(board)
        ship_col = random_col(board)
        total.append([ship_row,ship_col])
    return total

def oneshipguess(board,ship,shipid):
    ship_row=ship[0]
    ship_col=ship[1]
    for turn in range(4):
        guess_row = input("Guess Row:")
        guess_col = input("Guess Col:")
        print "ship "+str(shipid)+" turn %d" % (turn + 1)
        if guess_row == ship_row and guess_col == ship_col:
            print "Congratulations! You sunk my battleship!"
            break;
        else:
            if (guess_row < 0 or guess_row > boardSize-1) or (guess_col < 0 or guess_col > boardSize-1):
                print "Oops, that's not even in the ocean."
            elif(board[guess_row][guess_col] == "X"):
                print "You guessed that one already."
            else:
                print "You missed my battleship!"
                board[guess_row][guess_col] = "X"
            print_board(board)
            if turn==3:
                print "Game Over for ship %d" % shipid


print "Let's play Battleship!"
ships = generatemultiships(2)#must be lese than or eqaul to the size of board
print "there are two ships be placed,u have 4 turns for each"
print_board(board)
for i in range(2):
    oneshipguess(board,ships[i],i+1)
