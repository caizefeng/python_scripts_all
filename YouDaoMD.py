#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : YouDaoMD.py
# Author            : frostime <https://me.csdn.net/frostime>
# Date              : 04/09/2020
# Last Modified Date: 04/09/2020
# Last Modified By  : Zefeng Cai <czf17@mails.tsinghua.edu.cn>

import argparse
import re

import pyperclip

parser = argparse.ArgumentParser(
    description='将有道云笔记Markdown和正常Markdown的进行互相转换（数学公式的格式）')
parser.add_argument('--type', default='m2y', choices=['y2m', 'm2y'],
                    help='转换类型, m2y: md -> youdao; y2m: youdao -> md')
parser.add_argument(
    '--in', dest='input', help='转换后的 markdown 的输入文件；不填则自动读取剪贴板')
parser.add_argument(
    '--out', dest='output', help='转换后的 markdown 的输出文件；不填则自动写入剪贴板')
args = parser.parse_args()


def main():
    y2m_pat_block = r'```math((.|\n)*?)```'
    y2m_pat_inline = r'`\$(.*?)\$`'
    m2y_pat_block = r'\$\$((.|\n)*?)\$\$'
    m2y_pat_inline = r'(?<!`)\$(.*?)\$(?!`)'
    src_content = ''
    if args.input:
        with open(args.input, encoding='utf-8') as f:
            src_content = f.read()
    else:
        src_content = pyperclip.paste()

    if args.type == 'y2m':
        des_content = re.sub(y2m_pat_block, r'$$\1$$', src_content)
        des_content = re.sub(y2m_pat_inline, r'$\1$', des_content)
    else:
        des_content = re.sub(m2y_pat_block, r'```math\1```', src_content)
        des_content = re.sub(m2y_pat_inline, r'`$\1$`', des_content)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(des_content)
    else:
        pyperclip.copy(des_content)


if __name__ == '__main__':
    main()
