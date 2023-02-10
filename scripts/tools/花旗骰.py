"""
说明: CRAPS又称花旗骰，是美国拉斯维加斯非常受欢迎的一种的桌上赌博游戏。
该游戏使用两粒骰子，玩家通过摇两粒骰子得出的点数进行游戏。
简化后的规则是:
玩家第一次摇骰子如果 摇出了7点或11点，玩家胜;
玩家第一次如果摇出2点、3点或12点，庄家胜;
玩家如果摇出其他点数则玩家继续摇骰子，如果玩家摇出了7点，庄家胜;
如果玩家摇出了第一次摇的点数，玩家胜;
摇出其他点数则玩家继续摇骰子，直到分出胜负。
"""
import random  # 导入python 提供的工具 random

money = 100000  # 玩家的赌注  100000
flag = 0

# 如果资产为0 游戏结束
while money > 0:
    # print('玩家的总资产为{money}'.format(money=money))
    print(f'玩家的总资产为{money}')  # 打印玩家的余额
    go_on = False
    while True:  # 这个循环主要是让玩家下注  并且保证下注的范围正确
        debt = int(input('请下注:'))
        if debt <= money:
            break
        print('您的赌资不足！请重新下注')
    if debt < 0:
        print('玩家主动离开赌桌！')
        break
    flag += 1
    # 玩家第一次下注
    first = random.randint(1, 6) + random.randint(1, 6)
    print(f'\n玩家第{flag}次摇出了{first}点')
    if first == 7 or first == 11:
        print('玩家胜\n')
        money += debt
    elif first == 2 or first == 3 or first == 12:
        print('庄家胜\n')
        money -= debt
    else:
        go_on = True  # 没分出胜负  继续摇色子
    while go_on:  # 如果没有分出胜负  继续摇
        flag += 1
        go_on = False  # 默认这一次能出结果
        current = random.randint(1, 6) + random.randint(1, 6)
        print(f'\n玩家第{flag}次摇出了{current}点')
        if current == 7:
            print('庄家胜\n')
            money -= debt
        elif current == first:
            print('玩家胜\n')
            money += debt
        else:
            go_on = True
if money <= 0:
    print('玩家破产了')
print('游戏结束')
