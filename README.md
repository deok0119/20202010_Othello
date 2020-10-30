# 20202010_Othello

## 봇 알고리즘
  1. stone_onMouseAction() 끝마다 봇 턴 인지 체크 후 bot_play() 진입
  ```python
  if turn == bot_turn:
    bot_play()
  ```
  2. 이중포문을 이용하여 board[y][x] 각각의 state가 POSSIBLE인지 체크 후 True라면 해당 칸에서 얻을 수 있는 score를 알아보기 위해 bot_xy()진입
  ```python
  for y in range(8):
        for x in range(8):
            object = board[y][x]
            if object.state==State.POSSIBLE:
                score=0
                bot_xy(x, y)
  ```
  3. bot_xy()에서 bot_xy_dir()로 8방향 체크
  ```python
  def bot_xy(x, y):
    bot_xy_dir(x, y, 0, 1)
    bot_xy_dir(x, y, 1, 1)
    bot_xy_dir(x, y, 1, 0)
    bot_xy_dir(x, y, 1, -1)
    bot_xy_dir(x, y, 0, -1)
    bot_xy_dir(x, y, -1, -1)
    bot_xy_dir(x, y, -1, 0)
    bot_xy_dir(x, y, -1, 1)
  ```
  4. bot_xy_dir()에서 한칸씩 이동하며 other이면 possible(해당 라인에서 얻을 수 있는 점수) 1증가 후 계속이동, mine이면 possible값을 score에 더한 후 반복문 탈출한다.
  ```python
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
  ```
  5. 8방향 모두 체크하고 score가 best_score보다 크다면 best_score, best_x, best_y 갱신
  ```python
  if best_score<score:
    best_score=score
    best_x=x
    best_y=y
  ```
  6. 모든 칸에 대하여 2~5 반복
  7. 최종 best를 가지고 setState(), reverse() 처리 (착수)
  ```python
  setState(best_x, best_y, mine)
  reverse_xy(best_x, best_y)
  setScore()
  ```
  8. 턴 바꾸고 setPossible(), 이후 stone_onMouseAction()과 동일
  ```python
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
  ```
  9. 마지막으로 만약 다시 봇 턴인지 체크
  ```python
  if turn == bot_turn:
    bot_play()
  ```
