# -*- coding: utf-8 -*-
# @Time    : 2023/3/9 17:39

def merge_dict(dic1, dic2):
    result_dic = {}
    '''
    核心思路：
            1：遍历字典1和字典2的每一个键
            2：如果两个字典的键是一样的，就给新字典的该键赋值为空列表
                然后空列表依次添加字典1和字典2 的值，然后将最后的值赋值给原字典
            3：如果两个字典的键不同，则分别将键值对加到新列表中
    '''
    for k, v in dic1.items():
        for m, n in dic2.items():
            if k == m:
                result_dic[k] = []
                result_dic[k].append(dic1[k])
                result_dic[k].append(dic2[k])
                dic1[k] = result_dic[k]
                dic2[k] = result_dic[k]
            else:
                result_dic[k] = dic1[k]
                result_dic[m] = dic2[m]
        # if k in dic_b.keys():

    return result_dic


if __name__ == '__main__':
    dic_a = {"key1": 1, "key4": 4}
    dic_b = {"key1": 3, "key4": 4}
    # print("合并前的字典1是{}".format(dic_a))
    # print("合并前的字典2是{}".format(dic_b))
    result_dic = merge_dict(dic_a, dic_b)
    print(result_dic)
    print(list(result_dic.values()))
