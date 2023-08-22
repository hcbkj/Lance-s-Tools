# -*- coding: utf-8 -*-
# @Time    : 2023/4/15 10:31

import pandas as pd

# 读取 t1 和 t2 表格
# t1 = pd.read_excel(r"D:\工作相关\需求\法院侧需求\浙江温州龙湾\0411\t1.xlsx")
# t2 = pd.read_excel(r"D:\工作相关\需求\法院侧需求\浙江温州龙湾\0411\t2.xlsx", header=0, skiprows=2)
t1 = pd.read_excel(r"D:\工作相关\需求\法院侧需求\浙江温州龙湾\0411\test.xlsx", sheet_name='诉调立对接表')
t2 = pd.read_excel(r"D:\工作相关\需求\法院侧需求\浙江温州龙湾\0411\test.xlsx", sheet_name='源4-2023前调集约送达信息', header=0, skiprows=2)


# 按照 民调案号 和 案号 进行合并
merged = pd.merge(t1, t2, left_on='（法院内网端）民诉前调案件案号', right_on='案号', how='left')
# 按照 被申请人 和 被告名称 进行二次合并
merged = pd.merge(merged, t2[['案号', '当事人', '可联系号码(调解员匹配源所在列，一案号一组数据，多被告CONCATENATE公式合并在第一被告行）']],
                  left_on=['被申请人\n(被申请人代理人，取值ODR外网端)', '当事人'],
                  right_on=['案号', '当事人'],
                  how='left', suffixes=('_t1', '_t2'))
for index, row in merged.iterrows():
    row = dict(row)
    if ',' in str(row['被申请人\n(被申请人代理人，取值ODR外网端)']):
        # print(row)
        lst = merged.loc[row['（法院内网端）民诉前调案件案号'] == merged['案号_t1'], '可联系号码(调解员匹配源所在列，一案号一组数据，多被告CONCATENATE公式合并在第一被告行）_t1'].to_list()
        phones = ''
        for index, phone in enumerate(lst):
            try:
                # phones += fr'{str(row["被申请人\\n1"]).split(",")[index]}:' + str(phone) + ';'
                phones += str(row["被申请人\n(被申请人代理人，取值ODR外网端)"]).split(",")[index] + ":" + str(phone) + ';'
            except:
                # print(f"民调案号:{str(row['民调案号'])}, 被申请人:{str(row['被申请人\n1'])}")
                print("error")
        # print(phones)
        merged.loc[merged["（法院内网端）民诉前调案件案号"] == row["案号_t1"], "被告联系方式（取值内法院端）"] = phones

# 选择需要的列并重新排序
merged = merged[t1.columns.tolist()]
merged = merged.drop_duplicates()

# 多被告不填写，需要改进
merged.to_excel(r'D:\工作相关\需求\法院侧需求\浙江温州龙湾\0411\merged.xlsx', index=False)
