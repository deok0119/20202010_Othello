from bangtal import *
from enum import Enum

setGameOption(GameOption.ROOM_TITLE, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)

scene1=Scene("othello", "Images/background.png")

class State(Enum):
    BLANK=0
    POSSIBLE=1
    BLACK=2
    WHITE=3

class Turn(Enum):
    BLACK=1
    WHITE=2
turn=Turn.BLACK
bot_turn=Turn.WHITE                 ##_________________________________bot turn 설정

def setState(x, y, s):
    object=board[y][x]
    object.state=s

    if s==State.BLANK:
        object.setImage("Images/blank.png")
    elif s==State.BLACK:
        object.setImage("Images/black.png")
    elif s==State.WHITE:
        object.setImage("Images/white.png")
    elif turn==Turn.BLACK:
        object.setImage("Images/black possible.png")
    else:
        object.setImage("Images/white possible.png")

black_score=0
white_score=0
number=["Images/L0.png", "Images/L1.png", "Images/L2.png", "Images/L3.png", "Images/L4.png","Images/L5.png", "Images/L6.png","Images/L7.png","Images/L8.png","Images/L9.png"]
black_scoreboard_L1=Object(number[0])
black_scoreboard_L2=Object(number[0])
white_scoreboard_L1=Object(number[0])
white_scoreboard_L2=Object(number[0])

black_scoreboard_L1.locate(scene1, 750, 220)
black_scoreboard_L2.locate(scene1, 830, 220)
white_scoreboard_L2.locate(scene1, 1070, 220)

def setScoreBoard():
    black_score_L1=int(black_score/10)
    black_score_L2=black_score%10
    white_score_L1=int(white_score/10)
    white_score_L2=white_score%10

    black_scoreboard_L1.setImage(number[black_score_L1])
    black_scoreboard_L2.setImage(number[black_score_L2])
    white_scoreboard_L1.setImage(number[white_score_L1])
    white_scoreboard_L2.setImage(number[white_score_L2])

    if black_score_L1==0: black_scoreboard_L1.hide()
    else: black_scoreboard_L1.show()
    
    if white_score_L1==0:
        white_scoreboard_L1.hide()
        white_scoreboard_L2.locate(scene1, 1070, 220)
    else:
        white_scoreboard_L1.locate(scene1, 1070, 220)
        white_scoreboard_L2.locate(scene1, 1150, 220)
        white_scoreboard_L1.show()

    black_scoreboard_L2.show()
    white_scoreboard_L2.show()

def setScore():
    global black_score
    global white_score
    black_score=0
    white_score=0
    for y in range(8):
        for x in range(8):
            object=board[y][x]
            if object.state==State.BLACK: black_score+=1
            elif object.state==State.WHITE: white_score+=1
    setScoreBoard()

score=0
def bot_xy_dir(x, y, dx, dy):
    global score
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK

    possible=0
    while True:
        x = x + dx
        y = y + dy

        if x<0 or x>7: break
        if y<0 or y>7: break 

        object = board[y][x]
        if object.state == other:
            possible+=1
        elif object.state == mine:
            score+=possible
            break
        else: break

def bot_xy(x, y):
    bot_xy_dir(x, y, 0, 1)
    bot_xy_dir(x, y, 1, 1)
    bot_xy_dir(x, y, 1, 0)
    bot_xy_dir(x, y, 1, -1)
    bot_xy_dir(x, y, 0, -1)
    bot_xy_dir(x, y, -1, -1)
    bot_xy_dir(x, y, -1, 0)
    bot_xy_dir(x, y, -1, 1)

def bot_play():
    global turn
    global score
    best_score=0
    best_x=0
    best_y=0

    if turn == Turn.BLACK:
        mine = State.BLACK
        other = Turn.WHITE
    else:
        mine = State.WHITE
        other = Turn.BLACK

    for y in range(8):
        for x in range(8):
            object = board[y][x]
            if object.state==State.POSSIBLE:
                score=0
                bot_xy(x, y)
                if best_score<score:
                    best_score=score
                    best_x=x
                    best_y=y

    setState(best_x, best_y, mine)
    reverse_xy(best_x, best_y)
    setScore()

    turn = other      
    if not setPossible():
        if turn == Turn.BLACK: turn=Turn.WHITE
        else: turn = Turn.BLACK

        if not setPossible():
            if black_score>white_score: winner="흑돌 승!"
            elif black_score<white_score: winner= "백돌 승!"
            else: winner="무승부"
            showMessage("게임이 종료되었습니다.\n"+winner)
            return

    if turn == bot_turn:
        bot_play()
    
    


def stone_onMouseAction(x, y):
    global turn

    object = board[y][x]
    if object.state==State.POSSIBLE:
        if turn==Turn.BLACK:
            setState(x, y, State.BLACK)
            reverse_xy(x, y)
            turn=Turn.WHITE
        else:
            setState(x, y, State.WHITE)
            reverse_xy(x, y)
            turn=Turn.BLACK

        if not setPossible():
            if turn == Turn.BLACK: turn=Turn.WHITE
            else: turn = Turn.BLACK

            if not setPossible():
                if black_score>white_score: winner="흑돌 승!"
                elif black_score<white_score: winner= "백돌 승!"
                else: winner="무승부"
                showMessage("게임이 종료되었습니다.\n"+winner)
        
        setScore()
        if turn == bot_turn:
            bot_play()


def setPossible_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK

    possible=False
    while True:
        x = x + dx
        y = y + dy

        if x<0 or x>7: return False
        if y<0 or y>7: return False

        object = board[y][x]
        if object.state == other:
            possible=True
        elif object.state == mine:
            return possible
        else: return False

def reverse_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK

    possible=False
    while True:
        x = x + dx
        y = y + dy

        if x<0 or x>7: return
        if y<0 or y>7: return

        object = board[y][x]
        if object.state == other:
            possible=True
        elif object.state == mine:
            if possible:
                while True:
                    x = x - dx
                    y = y - dy

                    object = board[y][x]
                    if object.state ==other:
                        setState(x, y, mine)
                    else: return
        else: return

def setPossible_xy(x, y):
    object = board[y][x]
    if object.state == State.BLACK: return False
    if object.state == State.WHITE: return False
    setState(x, y, State.BLANK)

    if(setPossible_xy_dir(x, y, 0, 1)): return True
    if(setPossible_xy_dir(x, y, 1, 1)): return True
    if(setPossible_xy_dir(x, y, 1, 0)): return True
    if(setPossible_xy_dir(x, y, 1, -1)): return True
    if(setPossible_xy_dir(x, y, 0, -1)): return True
    if(setPossible_xy_dir(x, y, -1, -1)): return True
    if(setPossible_xy_dir(x, y, -1, 0)): return True
    if(setPossible_xy_dir(x, y, -1, 1)): return True
    return False

def reverse_xy(x, y):
    if(reverse_xy_dir(x, y, 0, 1)): return True
    if(reverse_xy_dir(x, y, 1, 1)): return True
    if(reverse_xy_dir(x, y, 1, 0)): return True
    if(reverse_xy_dir(x, y, 1, -1)): return True
    if(reverse_xy_dir(x, y, 0, -1)): return True
    if(reverse_xy_dir(x, y, -1, -1)): return True
    if(reverse_xy_dir(x, y, -1, 0)): return True
    if(reverse_xy_dir(x, y, -1, 1)): return True
    return False


def setPossible():
    possible = False
    for y in range(8):
        for x in range(8):
            if setPossible_xy(x, y):
                setState(x, y, State.POSSIBLE)
                possible=True
    return possible

board=[]
for y in range(8):
    board.append([])
    for x in range(8):
        object=Object("Images/blank.png")
        object.locate(scene1, 40+80*x, 40+80*y)
        object.show()
        object.onMouseAction=lambda mx, my, action, ix=x, iy=y: stone_onMouseAction(ix, iy)
        object.state=State.BLANK

        board[y].append(object)

setState(3, 3, State.BLACK)
setState(4, 4, State.BLACK)
setState(3, 4, State.WHITE)
setState(4, 3, State.WHITE)

setPossible()
setScoreBoard()

startGame(scene1)
