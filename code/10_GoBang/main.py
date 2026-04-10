from turtle import *

win = False

speed(0)
bgcolor("lightgreen")
screen = Screen()
screen.setup(width=1.0, height=1.0)  # full screen
yanse="black"  # Current player. Black move first.
cell_size=40

judge = Turtle()
judge.up()
judge.goto(-480, 330)
judge.write("Next", font=("Arial", 40, "bold"))
judge.color(yanse)
judge.goto(-420, 300)
judge.dot(30)

# Draw horisontal lines.
for i in range(19):
    up()
    goto(-cell_size*9, cell_size*(9-i))
    down()
    fd(cell_size*18)
    bk(cell_size*18)

rt(90)

# Draw vertical lines.
for i in range(19):
    up()
    goto(-cell_size*(9-i), cell_size*9)
    down()
    fd(cell_size*18)
    bk(cell_size*18)

# Draw borders
pensize(5)
for i in range(4):
    fd(cell_size*18)
    rt(90)

# board = [[0] * 19 for i in range(19)]
board =[
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

def check(row, col):
    """
    Gomoku (Five-in-a-row) win check
    """
    global win
    counts = [0] * 8
    # →  ↘  ↓  ↙  ←  ↖  ↑  ↗
    directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))

    for index in range(8):
        direction = directions[index]
        next_row = row + direction[0]
        next_col = col + direction[1]
        while next_row in range(19) and next_col in range(19) and board[next_row][next_col] == board[row][col]:
            counts[index] = counts[index] + 1
            next_row = next_row + direction[0]
            next_col = next_col + direction[1]

    for index in range(4):
        if counts[index] + counts[index + 4] + 1 >= 5:
            win = True
            goto(0, 0)
            if yanse == "black":
                write('Black Win', font=('Arial', 100, ''), align='center')
            else:
                write('White Win', font=('Arial', 100, ''), align='center')
            break

def play(x, y):
    """
    Check click (x,y) coordinates calculate board position 
    draw rock in position and add it to board matrix.
    """
    if not win:
        global yanse
        global cell_size
        color(yanse)
        up()
        x = round(x/cell_size)*cell_size
        y = round(y/cell_size)*cell_size
        row = int(9 - y / cell_size)
        col = int(x / cell_size + 9)

        if row >= 0 and row <= 18 and col >=0 and col<=18:
            if board[row][col] == 0:  # 1-black, 2-white, 0-empty
                goto(x, y)
                dot(30)

                if yanse == "black":
                    board[row][col] = 1
                    check(row, col)
                    yanse="white"
                else:
                    board[row][col] = 2
                    check(row, col)
                    yanse="black"

                judge.color(yanse)
                judge.dot(30)

onscreenclick(play, 1)
done()
