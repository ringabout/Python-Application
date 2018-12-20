# python实现 2048

## 理清游戏逻辑

### 规则

2048 游戏是一款即时休闲游戏。

游戏规则：玩家通过 w s a d 控制数字移动方向，达成 2048 这个数字即获胜。

每次可以选择一个方向移动，数字便会朝这个方向移动，如果遇到相同数字就相加，遇到不同数字或者边界就停止

移动。同时会在空白的地方生成 2 或者 4 的随机数字。通过不断相撞、相加，最后达成 2048 这个数字。

### 实现逻辑

#### 方向控制

python 借用 C 语言的输入字符控制

```python
import curses
stdscr = curses.initscr()
# stdscr.getchar() 返回的是输入的单个字符的 ascii 码值
# 假如输入'p',返回 112
stdscr.getch()
```

stdscr = 

getch:读取字符

w: UP

s: DOWN

a:LEFT

d:RIGHT
$$
\left[
\begin{matrix}
2& & & &\\
& & & &\\
& & & &\\
& & & &\\
\end{matrix}
\right]
$$
4 $\times $ 4 矩阵

$$
\left[
\begin{matrix}
2& & 2& &\\
& & & &\\
& & & &\\
& & & &\\
\end{matrix}
\right]
$$

向右滑动：

每一周期分为 4 轮：

每一轮操作一行（共 4 行），设置 flag 用于提示这一轮是否发生了改变，初始值设为 0，如果这一轮进行了操作，flag 

```python
flag = 1
for i in range(4):
    flag = 1
    while flag:
        flag = 0
        j = 2
        
        while j >= 0:
            if a[i,j]!= 0:
                if  a[i,j+1]==a[i,j]:
                    a[i,j+1] = 2 * a[i,j]
                    a[i,j] = 0 
                    flag = 1
            
                elif a[i,j+1] == 0:
                    temp = a[i,j]
                    a[i,j] = a[i,j+1]
                    a[i,j+1] = temp
                    flag = 1
                
            j -= 1
        
             
```

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










可能简化的做法:
$$
\left[
\begin{matrix}
&4&0&0&0& \\
&2&4&0&0& \\
&4&4&0&4& \\
&0&4&0&2& \\
\end{matrix}
\right]
$$
整体思路：将所有为零的值插到第一个位置上。

先将为零的值插到第一个位置，然后再删除这个值。

```python
for num1,i in enumerate(b):
    for num2,j in enumerate(i[1:]):
        if j == 0:
            b[num1].insert(0,j)
            b[num1].pop(num2+1)
```



优化：

```python
# 第一个位置上的零不需要考虑
for num1,i in enumerate(b):
    for num2,j in enumerate(i[1:]):
        if j == 0:
            b[num1].insert(0,j)
            b[num1].pop(num2+2)
```

转换后的结果：
$$
\left[
\begin{matrix}
&0&0&0&4& \\
&0&0&2&4& \\
&0&4&4&4& \\
&0&0&4&2& \\
\end{matrix}
\right]
$$
下一步

#### 随机生成 2 或 4

```python
udict = {}
count = 0
for i in range(4):
    for j in range(4):
        if(a[i,j]==0):
            udict[count] = (i,j)
            count += 1
random_number = np.random.randint(0,count)

two_or_four = np.random.choice([2,4])

a[udict[random_number]] = two_or_four
```

