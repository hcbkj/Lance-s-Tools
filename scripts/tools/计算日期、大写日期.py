# -*- coding: utf-8 -*-
# @Time    : 2023/3/9 16:08

import datetime


def count_date(date, count):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    new_date = (date + datetime.timedelta(days=count)).strftime("%Y-%m-%d")
    return new_date


def date_to_charater(word: str):
    lis = word.split('-')
    dic_year = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九', '0': '〇'}
    dic = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九', '0': ''}
    year, month, day = '', '', ''
    for _ in lis[0]:
        year += dic_year[_]
    for index, _ in enumerate(lis[1]):
        if _ == '1' and index == 0 and len(lis[1]) == 2:
            month += '十'
        else:
            month += dic[_]
    for index, _ in enumerate(lis[2]):
        if _ != '0' and index == 0 and len(lis[2]) == 2:
            if _ != '1':
                day += dic[_]
            day += '十'
        else:
            day += dic[_]

    return year + '年' + month + '月' + day + '日'

    # length = len(word)
    # if length == 3:
    #     if word[1] == '0':
    #         if word[2] == '0':
    #             return dic[word[0]] + '百'
    #         else:
    #             return dic[word[0]] + '百' + '零' + dic[word[2]]
    #     else:
    #         return dic[word[0]] + '百' + dic[word[1]] + '十' + dic[word[2]]
    # elif length == 2:
    #     if word[0] == '1':
    #         return '十' + dic[word[1]]
    #     else:
    #         return dic[word[0]] + '十' + dic[word[1]]
    # elif length == 1:
    #     return dic[word[0]]


if __name__ == '__main__':
    # for i in range(1949, 2030):
    #     start = f'{str(i)}-10-12'
    #     print(numToCharater(start))
    date = '2023-3-9'
    new_date = count_date(date, 15)
    charater_date = date_to_charater(new_date)
    print(charater_date)
