# -*- coding: utf-8 -*-
# @Time    : 2022/8/30 14:30

L = []


def quchong(str):
    str_list = list(str)
    n = len(str_list)
    list_res = L
    for i in range(0, n, 2):
        list_res.append(str_list[i])
    str1 = ''.join(list_res)
    print(str1)
    return str1


def run():
    # str = input()
    strnum = '33440044005511998833112222990022229'
    quchong(strnum)


if __name__ == '__main__':
    run()
