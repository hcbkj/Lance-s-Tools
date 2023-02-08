# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 11:03
# @Author  : SYH
# @File    : 迷宫算法.py
# @Software: PyCharm

# from queue import Queue
# from collections import deque

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


# 判断当前这个点，上下左右是0还是1
# 上: r - 1 , c
# 下: r + 1 , c
# 左: r , c - 1
# 右: r , c + 1

# DFS 深度优先,找到出路但不是最短路径
def dfs(startPoint, endPoint, maps):
    # # 用栈来记录已经走过的路
    # # list 就是一个栈
    # lst = []
    # lst.append(1)
    # lst.append(2)
    # lst.append(3)
    # lst.append(4)
    # print(lst.pop())

    lst = [startPoint]  # lst中记录着我每一次走过的点的坐标    (r,c)

    while lst:
        # 只有当列表不为空的时候才能继续走
        now = lst[-1]  # 当前走到的节点坐标
        # print(now)    # 实时路径
        if now == endPoint:
            # 迷宫出口
            break
        x, y = now  # 解构 解包
        maps[x][y] = 2  # 标记已经走过的点
        # 判断是否可以以走
        dfs_next_step(x, y, lst)

    if lst:
        # lst里面还有东西,那就是出去的路径
        print('成功走出迷宫!')
    else:
        print('无法走通!')
    return lst  # 输出路径


def dfs_next_step(row, col, lst):
    # 判断是否可以以走
    if maze[row - 1][col] == 0:
        # 上面可以走
        lst.append((row - 1, col))
        return lst
    elif maze[row + 1][col] == 0:
        # 下方可以走
        lst.append((row + 1, col))
        return lst
    elif maze[row][col - 1] == 0:
        # 左方可以走
        lst.append((row, col - 1))
        return lst
    elif maze[row][col + 1] == 0:
        # 右方可以走
        lst.append((row, col + 1))
        return lst
    else:
        # 往回走
        lst.pop()


# BFS 广度优先,查找最短路径
# 打印路径的话其实在每个点上记录它的前驱结点就够了，这样从终点能一步步回溯到起点，得到一条完整路径。
def bfs(startPoint, endPoint, maps):
    # queue, 队列
    queue = [startPoint]
    flag = []
    lst = []
    while queue:
        now = queue[0]
        if now == endPoint:
            # return queue
            break
        x, y = now  # 解构 解包
        maps[x][y] = 2  # 标记已经走过的点

        # 与DFS不同的是,判断下一个可以走的路径的时候应该全部判断,把所有能往下走的节点坐标全部入队
        lst.append(bfs_next_step(x, y, queue)[0])
        # print(bfs_next_step(x, y, queue)[0])
    print(lst)
    # print(lst)


def bfs_next_step(row, col, queue):
    if maze[row - 1][col] == 0:
        # 上面能走,直接入队
        queue.append((row - 1, col))
        if queue[0] == (row, col):
            queue.pop(0)
    if maze[row + 1][col] == 0:
        # 下面能走,直接入队
        queue.append((row + 1, col))
        if queue[0] == (row, col):
            queue.pop(0)
    if maze[row][col - 1] == 0:
        # 左面能走,直接入队
        queue.append((row, col - 1))
        if queue[0] == (row, col):
            queue.pop(0)
    if maze[row][col + 1] == 0:
        # 右面能走,直接入队
        queue.append((row, col + 1))
        if queue[0] == (row, col):
            queue.pop(0)
    if maze[row - 1][col] != 0 and maze[row + 1][col] != 0 and maze[row][col - 1] != 0 and maze[row][col + 1] != 0:
        # 都走不通就出队
        queue.pop(0)
    return queue


if __name__ == '__main__':
    # 设置起点
    # 设置终点
    start = (1, 1)
    end = (8, 8)

    # path = dfs(start, end, maze)

    bfs(start, end, maze)

    # print(path)
