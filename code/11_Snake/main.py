from turtle import *
from random import randint

gz = 22  # Cell size
bc = gz * 8  # Half of board cize

screen = Screen()
screen.bgcolor("darkblue")

food = Turtle()
food.color("red")
food.shape("square")
food.up()
food.speed(0)
food.goto(randint(-bc+gz, bc-gz) // gz * gz, 
          randint(-bc+gz, bc-gz) // gz * gz)

liner = Turtle()
liner.speed(0)
liner.up()
liner.goto(-bc, bc)
liner.color("white")
liner.pensize(5)
liner.down()
for i in range(4):
    liner.fd(bc*2)
    liner.rt(90)
liner.ht()

score = 0
judge = Turtle()
judge.speed(0)
judge.up()
judge.goto(0, bc+20)
judge.color("white")
judge.write("得分:{}".format(score), align="center", font=("Kai", 20, "bold"))
judge.ht()

head = Turtle()
head.speed(0)
head.up()
head.color("cyan")
head.shape("square")

snake = []
snake.append(head)
for i in range(2):
    body = head.clone()
    body.color("white")
    body.goto(head.xcor()+(i+1)*gz, head.ycor())
    snake.append(body)

d: list[int] = [-1, 0]
next_d = d.copy()

def move():
    global d, next_d
    d = next_d
    last = snake.pop()
    first = snake[0]
    first.color("white")
    last.goto(first.xcor() + d[0] * gz, first.ycor() + d[1] * gz)
    last.color("cyan")
    snake.insert(0, last)
    
    if snake[0].xcor() == food.xcor() and snake[0].ycor() == food.ycor():
        food.ht()
        food.goto(randint(-bc+gz, bc-gz)//gz*gz, randint(-bc+gz, bc-gz)//gz*gz)
        food.st()
        body = snake[-1].clone()
        snake.append(body)
        global score
        score += 1
        judge.clear()
        judge.write("得分:{}".format(score), align="center", font=("Kai", 20, "bold"))
    
    head = snake[0]
    for segment in snake[1:]:
        if head.xcor() == segment.xcor() and head.ycor() == segment.ycor():
            judge.goto(0, 0)
            judge.write("GAME OVER", align="center", font=("Kai", 30, "bold"))
            screen.ontimer(reset_game, 2000)
            return
    
    if (snake[0].xcor() > -bc and snake[0].xcor() < bc) and \
       (snake[0].ycor() > -bc and snake[0].ycor() < bc):
        screen.ontimer(move, 500)
    else:
        judge.goto(0, 0)
        judge.write("GAME OVER", align="center", font=("Kai", 30, "bold"))
        screen.ontimer(reset_game, 2000)
        return

def reset_game():
    global snake, score, d

    for segment in snake:
        segment.hideturtle()

    snake.clear()

    head = Turtle()
    head.speed(0)
    head.up()
    head.color("cyan")
    head.shape("square")
    snake.append(head)

    for i in range(2):
        body = head.clone()
        body.color("white")
        body.goto(head.xcor() + (i+1)*gz, head.ycor())
        snake.append(body)

    d = [-1, 0]

    score = 0
    judge.clear()
    judge.goto(0, bc+20)
    judge.write("得分:{}".format(score), align="center", font=("Kai", 20, "bold"))

    food.goto(randint(-bc+gz, bc-gz)//gz*gz,
              randint(-bc+gz, bc-gz)//gz*gz)

    move()

def up():
    global next_d
    if d[1] != -1:
        next_d = [0, 1]
def down():
    global next_d
    if d[1] != 1:
        next_d = [0, -1]
def left():
    global next_d
    if d[0] != 1:
        next_d = [-1, 0]
def right():
    global next_d
    if d[0] != -1:
        next_d = [1, 0]

screen.onkey(up, "Up")
screen.onkey(down, "Down")
screen.onkey(left, "Left")
screen.onkey(right, "Right")

screen.listen()

move()
screen.mainloop()
