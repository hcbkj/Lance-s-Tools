# -*- coding: utf-8 -*-
# @Time    : 2022/8/30 10:49
# 中保国信-借款协议信息提取

import re
from flows.flow import ScriptDef, ListDataFlow, DirectoryItem
import pdfplumber
import fitz
import os
from rpalib.log import logger
from openpyxl import Workbook
import pandas as pd


class zbgx_jkxyxxtq(ListDataFlow):
    def __init__(self, file_path, saved_path):
        super().__init__()
        self.file_path = file_path
        self.saved_path = saved_path

    def pdf_xxtq(self):
        self.saved_excel()
        file_dir_list = os.listdir(self.file_path)

        # out_data = []
        for pdf_file in file_dir_list:
            result = []
            errmsg = []
            if pdf_file.endswith('.pdf'):
                logger.info(f"开始执行{pdf_file}")
                with pdfplumber.open(os.path.join(self.file_path, pdf_file)) as pdf:
                    texts = ""
                    for page in pdf.pages:
                        texts += page.extract_text() + "\n"
                    # print(texts)

                # 识别文件名称
                if pdf_file:
                    result.append(pdf_file)
                else:
                    result.append('')
                    errmsg.append('识别文件名称提取失败')

                # 合同抬头
                ht_name = re.search('(?P<taitou>.*?)\n', texts)
                if ht_name:
                    result.append(ht_name.group('taitou').strip())
                else:
                    result.append('')
                    errmsg.append('合同抬头提取失败')

                # 合同编号
                ht_num = re.search('合同编号：(?P<bianhao>.*?)\n', texts)
                if ht_num:
                    result.append(ht_num.group('bianhao').replace(' ', ''))
                else:
                    result.append('')
                    errmsg.append('合同编号提取失败')

                # 借款人姓名
                jkr_name = re.search('借款人：(?P<jkr_xingming>.*?)\n', texts)
                jkr_name = jkr_name.group('jkr_xingming').replace(' ', '')
                if jkr_name:
                    if jkr_name[0] == jkr_name[1]:
                        jkr_name = pdf_file.split('-')[-5]
                    result.append(jkr_name)
                else:
                    result.append('')
                    errmsg.append('借款人姓名提取失败')

                # 借款人证件号
                jkr_zjh = re.search('证件号码：(?P<jkr_zhengjianhao>.*?)\n', texts)
                if jkr_zjh:
                    jkr_zjh_str = jkr_zjh.group('jkr_zhengjianhao').strip().replace(' ', '')
                    if len(jkr_zjh_str) > 18:
                        jkr_zjh_str = self.quchong(jkr_zjh_str)
                    result.append(jkr_zjh_str)
                else:
                    result.append('')
                    errmsg.append('借款人证件号提取失败')

                # 借款人手机号
                jkr_sjh = re.search('手机号码：(?P<jkr_shoujihao>.*?)\n', texts)
                if jkr_sjh:
                    result.append(jkr_sjh.group('jkr_shoujihao').strip().replace(' ', ''))
                else:
                    result.append('')
                    errmsg.append('借款人手机号提取失败')

                # 借款金额
                jk_je = re.search('借款金额：(?P<jine>.*?)\n', texts)
                if jk_je:
                    result.append(jk_je.group('jine').strip().replace(' ', ''))
                else:
                    result.append('')
                    errmsg.append('借款金额提取失败')

                # 借款期限
                jk_qx = re.search('借款期限：(?P<qixian>.*?)，自', texts)
                if jk_qx:
                    jk_qx_str = jk_qx.group('qixian').replace(' ', '')
                    if '□' in jk_qx_str:
                        jk_qx_str = re.search('(\d.+天)|(\d.+?期)', jk_qx_str).group()
                    result.append(jk_qx_str)
                else:
                    result.append('')
                    errmsg.append('借款期限提取失败')

                # 借款起始日
                jk_start_date = re.search('，自(?P<start_date>.*?)起至', texts)
                if jk_start_date:
                    result.append(jk_start_date.group('start_date').replace(' ', ''))
                else:
                    result.append('')
                    errmsg.append('借款起始日提取失败')

                # 借款截至日
                jk_end_date = re.search('起至(?P<end_date>.*?)。如贷款', texts)
                if jk_end_date:
                    result.append(jk_end_date.group('end_date').replace(' ', ''))
                else:
                    result.append('')
                    errmsg.append('借款截至日提取失败')

                # 借款利率
                jk_rate = re.search('借款利率：(?P<rate>.*?)。', texts)
                if jk_rate:
                    jk_rate_str = jk_rate.group('rate').replace(' ', '')
                    if jk_rate_str == '':
                        # 该值本来正则取出不为空,经过replace()处理后为空,证明该值缺失
                        errmsg.append('借款利率值缺失')
                    if '□' in jk_rate_str:
                        jk_rate_str = re.search('(\d.+?/天)|(\d.+?/期)', jk_rate_str).group().replace('_', '')
                    result.append(jk_rate_str)
                else:
                    result.append('')
                    errmsg.append('借款利率提取失败')

                # 逾期利率
                jk_late_rate = re.search('借款人在借款届满期间支付的利息.*?率为(?P<late_rate>.*?)，本合同项下的借款年利率', texts, re.S)
                if jk_late_rate:
                    jk_late_rate_str = jk_late_rate.group('late_rate').replace(' ', '')
                    if jk_late_rate_str == '':
                        # 该值本来正则取出不为空,经过replace()处理后为空,证明该值缺失
                        print('逾期利率值缺失')
                        errmsg.append('逾期利率值缺失')
                    result.append(jk_late_rate_str)
                else:
                    # 第一种格式为空，判断是否是第二种格式
                    jk_late_rate = re.search('借款人在借款届满期间支付的利息.*?采用单利计算为(?P<late_rate>.*?)，本合同项下的借款年利率', texts, re.S)
                    if jk_late_rate:
                        jk_late_rate_str = jk_late_rate.group('late_rate').replace(' ', '')
                        if jk_late_rate_str == '':
                            # 该值本来正则取出不为空,经过replace()处理后为空,证明该值缺失
                            errmsg.append('逾期利率值缺失')
                        result.append(jk_late_rate_str)
                    else:
                        # 两种格式都为空
                        result.append('')
                        errmsg.append('逾期利率提取失败')

                # 还款方式
                repayment = re.search('还款方式：(?P<repay>.*?)\n', texts)
                if repayment:
                    result.append(repayment.group('repay').replace(' ', ''))
                else:
                    result.append('')
                    errmsg.append('还款方式提取失败')

                # 合同签署日期
                qs_date = re.search('合同签署日期：(?P<qianshuriqi>.*?)\n', texts)
                if qs_date:
                    qs_date_str = qs_date.group('qianshuriqi').replace(' ', '')
                    if len(qs_date_str) > 11:
                        qs_date_str = self.quchong(qs_date_str)
                    result.append(qs_date_str)
                else:
                    result.append('')
                    errmsg.append('合同签署日期提取失败')

                # 争议解决
                zyjj = re.search('第十五条 合同的适用法律及争议解决方式.*?。(?P<zhengyijiejue>.*?)三、为降低诉讼成本', texts, re.S)
                if zyjj:
                    result.append(zyjj.group('zhengyijiejue').replace(' ', '').replace('\n', ''))
                else:
                    result.append('')
                    errmsg.append('争议解决提取失败')

                logger.info(f'{pdf_file}提取完成')
                # print(result)
                out_data_list = result + [",".join(errmsg)]
                # out_data.append(out_data_list)
                self.ws.append(out_data_list)
                self.wb.save(os.path.join(self.saved_path, 'output2.xlsx'))
            else:
                logger.error(f"{pdf_file} 文件格式不匹配！")

            # self.ws.append(out_data)
            # self.wb.save(os.path.join(self.saved_path, 'output1.xlsx'))
            # self.saved_excel(out_data)

    def saved_excel(self):
        self.wb = Workbook()
        self.ws = self.wb.worksheets[0]
        header = ['识别文件名称路径', '合同抬头', '合同编号', '借款人姓名', '借款人证件号', '借款人手机号', '借款金额', '借款期限',
                  '借款起始日', '借款截至日', '借款利率', '逾期利率', '还款方式', '合同签署日期', '争议解决', '报错']
        self.ws.append(header)
        # df = pd.DataFrame(lst)
        # df.columns = header
        # df.to_csv(os.path.join(self.saved_path, 'output1.xlsx'))


    def quchong(self, strs):
        str_list = list(strs)
        n = len(str_list)
        list_res = []
        for i in range(0, n, 2):
            list_res.append(str_list[i])
        str1 = ''.join(list_res)
        return str1

    def run(self):
        self.pdf_xxtq()


export = ScriptDef(
    cls=zbgx_jkxyxxtq,
    group="其他",
    title="中保国信-借款协议信息提取",
    arguments=[
        DirectoryItem(title="pdf文件路径", name="file_path"),
        DirectoryItem(title="提取结果文件保存路径：", name="saved_path"),
    ]
)

if __name__ == '__main__':
    proj = zbgx_jkxyxxtq(r'D:\工作相关\需求\中保国信-借款协议信息提取\test', r'D:\工作相关\需求\中保国信-借款协议信息提取')
    proj.run()
