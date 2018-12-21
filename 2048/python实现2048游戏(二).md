上一篇文章中，我们梳理了实现简易版 2048 游戏的基本知识，这篇文章将介绍如何实现各个模块。换句话说，上一次我们确定了旅行的目的地，这一次就让我们自由畅行在山间田野。

![流程一](material/流程一.png)

游戏主程序，即 **game** 函数按部就班地向下执行，该判断就判断，然后执行相应函数。

首先读取用户输入，第一个判断：是否移动数字，显然要移动数字要满足以下条件：

- 用户输入小写的 w s a d 对应上下左右
- 该移动方向上允许移动

具体来说，移动方向最前面有空间或者有连续相同的数字。可以移动则执行 **move** 函数，并在棋盘上生成随机数字，否则原样输出。

其次判断：棋盘是否被填满。被填满时执行 **fail** 函数。

最后判断：是否胜利。如果获胜，打印获胜提示。

```python
def game(board, stdscr, rscore):
    global score
    global change
    
    # curses.noecho()
    # 屏幕不显示用户输入的字符
    curses.noecho()
    while 1:
       
        # stdscr.getch()
        # 读取用户输入的字符
        order = stdscr.getch()

        # move()对用户移动的响应
        current_board, change = move(order, board)
        # change 为 1 随机产生 2 或 4
        if change:
            current_board = choice(board)

        # 打印棋盘
        print_board(stdscr, current_board, rscore)

        # 当棋盘被填满，判断是否游戏结束
        if (current_board != 0).all():
            fail(current_board)

        # win 为 1 打印获胜提示
        if win:
            stdscr.addstr('You win')
```

以上便是游戏主程序的基本逻辑，接下来我们看具体的函数模块。

首先是移动模块：

**basic** 函数用来执行移动与碰撞的操作。**move_{up,down,right,left}** 函数用来实现各个方向上的 **basic** 函数操作。**move** 函数用来响应用户指令，实现各个方向上的移动。

棋盘由矩阵组成，0 代表该位置上没有数字。basic 函数就是基于矩阵的运算，且以右移为基础移动。

**4 $\times $ 4 矩阵**：
$$
\left[
\begin{matrix}
&2&2&0&4&\\
&2&4&2&0&\\
&4&8&0&2&\\
&8&4&0&4&\\
\end{matrix}
\right]
$$


向右滑动：

每一周期分为 4 轮，每一轮操作一行（共 4 行），从最左面的元素开始执行。设置 flag 用于提示这一轮是否发生了改变，如果发生了改变，这一轮就再进行一次循环，直到 flag 保持为 0 不变。对于循环的每一个元素，如果该元素不为 0 ，若下个元素为 0，就交换当前值与下个元素的值。若下个元素与当前元素相同，则当前元素置 0 ，且下一个元素增加一倍，分数还要增加 100 分。

举个例子：对于第一行 [2 2 0 4]

第一轮：

- 4 与 0 不交换   [2 2 0 4]
- 0 与 2 交换     [2 0 2 4]
- 0 与 2 交换     [0 2 2 4]
- flag = 1 且 score + = 0  

第二轮：

- 4 与 2 不交换              [0 2 2 4]
- a13 双倍 a12 置 0          [0 0 4 4]
- 0 不变                     [0 0 4 4]
- flag = 1 且 score += 100

第三轮：

- a14 双倍 a13 置 0          [0 0 0 8]
- 不变                       [0 0 0 8]
- 不变                       [0 0 0 8]
- flag = 1 且 score += 100

第四轮：

- 不变
- 不变
- 不变
- flag = 0 且 score += 0

即第一轮最后输出结果 [0 0 0 8]。

以上就是向右移动的操作，而对于其他方向上的移动其实就是在此基础上进行矩阵的转置与逆置操作。

```python
# A 为 4*4 的矩阵
# 转置操作
A.T
# 逆置操作
A[::-1,::-1]
```

下图为原矩阵：
$$
\left[
\begin{matrix}
&a_{11}&a_{12}&a_{13}&a_{14}& \\
&a_{21}&a_{22}&a_{23}&a_{24}& \\
&a_{31}&a_{32}&a_{33}&a_{34}& \\
&a_{41}&a_{42}&a_{43}&a_{44}& \\
\end{matrix}
\right]
$$

向下滑动：

将原矩阵转置得到新矩阵，新矩阵向右滑动，相当于原矩阵向下滑动，再转置变回原矩阵。

$$
\left[
\begin{matrix}
&a_{11}&a_{21}&a_{31}&a_{41}& \\
&a_{12}&a_{22}&a_{32}&a_{42}& \\
&a_{13}&a_{23}&a_{33}&a_{43}& \\
&a_{14}&a_{24}&a_{34}&a_{44}& \\
\end{matrix}
\right]
$$

向左滑动：

将原矩阵逆置得到新矩阵，新矩阵向右滑动，相当于原矩阵向左滑动，再逆置变回原矩阵。

$$
\left[
\begin{matrix}
&a_{44}&a_{43}&a_{42}&a_{41}& \\
&a_{34}&a_{33}&a_{32}&a_{31}& \\
&a_{24}&a_{23}&a_{22}&a_{21}& \\
&a_{14}&a_{13}&a_{12}&a_{11}& \\
\end{matrix}
\right]
$$

向上滑动：

将原矩阵转置加逆置得到新矩阵，新矩阵向右滑动，相当于原矩阵向上滑动，再通过转置加逆置变回原矩阵。

$$
\left[
\begin{matrix}
&a_{44}&a_{34}&a_{24}&a_{14}& \\
&a_{43}&a_{33}&a_{23}&a_{13}& \\
&a_{42}&a_{32}&a_{22}&a_{12}& \\
&a_{41}&a_{31}&a_{21}&a_{11}& \\
\end{matrix}
\right]
$$


```python
# 基础移动
def basic(board):
    global score
    global win
    # 以右移为基础移动

    for i in range(4):
        flag = 1
        while flag:
            flag = 0
            j = 2
            while j >= 0:
                if board[i, j] != 0:
                    if board[i, j + 1] == board[i, j]:
                        board[i, j + 1] = 2 * board[i, j]
                        if board[i, j + 1] == 2048:
                            win = 1
                        board[i, j] = 0
                        score += 100
                        flag = 1

                    elif board[i, j + 1] == 0:
                        temp = board[i, j]
                        board[i, j] = board[i, j + 1]
                        board[i, j + 1] = temp
                        flag = 1

                j -= 1
    return board


# 右移
def move_right(board):
    return basic(board)


# 上移
def move_up(board):
    # 逆置 + 转置
    board = board[::-1, ::-1].T
    board = basic(board)
    board = board[::-1, ::-1].T
    return board


# 左移
def move_left(board):
    # 逆置
    board = board[::-1, ::-1]
    board = basic(board)
    board = board[::-1, ::-1]
    return board


# 下移
def move_down(board):
    # 转置
    board = board.T
    board = basic(board)
    board = board.T
    return board


# 移动
def move(order, board):
    # ord 求码值
    global score
    global win
    change = 1
    tempboard = copy.deepcopy(board)

    # 退出游戏
    if order == ord('q'):
        save_score(score)
        exit()
    # 重置游戏
    elif order == ord('r'):
        win = 0
        save_score(score)
        score = 0
        stdscr.clear()
        wrapper(main)
    # 胜利后，只有退出和重置游戏
    elif win:
        change = 0
        newboard = tempboard
        return newboard, change
    # 上下左右移动
    elif order == ord('w'):
        newboard = move_up(board)
    elif order == ord('s'):
        newboard = move_down(board)
    elif order == ord('a'):
        newboard = move_left(board)
    elif order == ord('d'):
        newboard = move_right(board)

    # 按其他键程序不响应
    else:
        newboard = board

    if (newboard == tempboard).all():
        change = 0

    return newboard, change
```

接下来，我们讲 **choice** 模块：首先获取值为 0 的矩阵元素的位置，并储存在字典里，以序号（ 最大值为 count ） 为索引。其次产生 [0,count) 范围内的随机数（随机抽取值为 0 的元素），并且产生随机数 2 或 4 (概率为 75% 与 25%)。最后将随机抽取的元素更改为生成的随机数（2 或 4）。

```python
# 随机产生 2 或 4
def choice(board):
    udict = {}
    # 统计0的个数
    count = 0
    for i in range(4):
        for j in range(4):
            # board[i,j] 为 0
            # eg. {0:(1,3),1:(2,1),3:(3,2)}
            # 根据 key 可以获得元素 0 在棋盘上的位置
            if not board[i, j]:
                udict[count] = (i, j)
                count += 1
    # np.random.randint(0, count)
    # 产生 [0,count) 范围内的随机数
    random_number = np.random.randint(0, count)
    # np.random.choice([2,2,2,4])
    # 随机选取列表 [2,2,2,4] 中的元素
    two_or_four = np.random.choice([2, 2, 2, 4])
    # 更改棋盘上 0 元素为随机数
    board[udict[random_number]] = two_or_four
    return board
```

然后是生成分数：

首先游戏开始时加载一次分数（历史最高分），游戏结束时保存最高分。每次打印棋盘前，都比较当前分数与当前最高分，并更改当前最高分数。

```python
# 加载最高分
def load_score():
    rank_score = np.load(FILENAME)
    return rank_score


# 保存最高分
def save_score(score):
    rscore = load_score()
    if score > rscore:
        np.save(FILENAME, score)

# 比较当前分数与当前最高分
def compare_score(score, rscore):
    if score > rscore:
        rscore = score
    return rscore
```

其次是打印模块：

只打印非零值。

```python
# 打印棋盘
def print_board(stdscr, board, rscore):
    global score
    rscore = compare_score(score, rscore)
    
# stdscr.clear()
# 清除屏幕
# stdsscr.addstr()
# 打印字符串
    stdscr.clear()
    stdscr.addstr('得分：' + str(score) + '\n')
    stdscr.addstr('历史最高：' + str(rscore) + '\n')
    for i in range(4):
        stdscr.addstr('-' * 22 + '\n')
        for j in range(4):
            stdscr.addstr('|')
            if board[i, j]:
                stdscr.addstr('{:^4d}'.format(board[i, j]))
            else:
                stdscr.addstr('    '.format())
        stdscr.addstr('|')
        stdscr.addstr('\n')
    stdscr.addstr('-' * 22 + '\n')
```

最后是一些零碎的知识点：

首先我们要初始化程序，初次运行游戏会在当前目录生成 ‘out.npy’ 文件，并且储存 0 在文本中。其次初始化棋盘，最后就可以愉快地开始游戏了。

```python
import numpy as np
import curses
import copy
import os
from curses import wrapper

stdscr = curses.initscr()
# 分数
score = 0
# 判断是否获胜
win = 0
#
FILENAME = 'out.npy'


# 初始化
def init():
    # 初始化棋盘
    # 初始棋盘 2 或 4 的随机数字
    if FILENAME not in os.listdir():
    	np.save(FILENAME, 0)
    init_board = choice(np.zeros((4, 4), dtype=np.int))
    return init_board


# 主程序
def main(stdscr):
    # 初始化程序
    init_board = init()
    rscore = load_score()
    # 打印棋盘
    print_board(stdscr, init_board, rscore)
    # 游戏主进程
    game(init_board, stdscr, rscore)


if __name__ == "__main__":
    wrapper(main)
```

以上便是 python 实现 2048 游戏的完结版，如果想获取源代码，在微信后台回复 2048 ，或者点击阅读原文即可。

**想了解更多请关注：**

![img](https://mmbiz.qpic.cn/mmbiz_jpg/MnCc8lk8Gyv2n5rxvFGML9PqF5Oh91wIMOXInU0L4eYVauRJEP9qaJkHLQs3FmaPrALUzVN9I9pug08IeS1ic6w/640)















