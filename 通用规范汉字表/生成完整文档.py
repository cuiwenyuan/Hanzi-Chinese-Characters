#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完整的通用规范汉字表Markdown文档
"""

import os

def parse_line(line):
    """解析一行数据"""
    parts = line.strip().split('\t')
    result = {'num': '', 'char': '', 'pinyin': '', 'traditional': '', 'variant': ''}
    
    # 正确解析各字段
    if len(parts) > 0:
        result['num'] = parts[0]
    if len(parts) > 1:
        result['char'] = parts[1]
    if len(parts) > 2:
        result['pinyin'] = parts[2]
    if len(parts) > 3:
        result['traditional'] = parts[3]
    if len(parts) > 4:
        result['variant'] = parts[4]
    
    return result

def get_level(num):
    """根据编号返回级别"""
    n = int(num)
    if n <= 3500:
        return 1, "一级字表（常用字）"
    elif n <= 6500:
        return 2, "二级字表"
    else:
        return 3, "三级字表"

def generate_full_document(input_file, output_file):
    """生成完整的markdown文档"""
    
    # 读取数据
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 解析数据
    data = []
    for line in lines:
        if line.strip():
            data.append(parse_line(line))
    
    # 生成markdown
    md_lines = []
    md_lines.append('# 通用规范汉字表')
    md_lines.append('')
    md_lines.append('本表收录汉字8105个，分为三级：')
    md_lines.append('- **一级字表**（1-3500）：常用字，覆盖99.48%的使用频率')
    md_lines.append('- **二级字表**（3501-6500）：次常用字')
    md_lines.append('- **三级字表**（6501-8105）：通用字')
    md_lines.append('')
    md_lines.append('---')
    md_lines.append('')
    
    current_level = 0
    table_rows = []
    current_level_name = ''
    
    for i, item in enumerate(data):
        level, level_name = get_level(item['num'])
        
        # 如果级别变化
        if level != current_level:
            # 保存之前的表格
            if table_rows:
                md_lines.append('| 编号 | 汉字 | 拼音 | 繁体 | 异体 |')
                md_lines.append('|------|------|------|------|------|')
                md_lines.extend(table_rows)
                md_lines.append('')
                md_lines.append('---')
                md_lines.append('')
            
            # 写入新级别的标题
            md_lines.append(f'## {level_name}')
            md_lines.append('')
            
            # 重置
            table_rows = []
            current_level = level
            current_level_name = level_name
        
        # 添加行到表格
        num = item['num']
        char = item['char']
        pinyin = item['pinyin'] if item['pinyin'] else ' '
        traditional = item['traditional'] if item['traditional'] else ' '
        variant = item['variant'] if item['variant'] else ' '
        
        row = f'| {num} | {char} | {pinyin} | {traditional} | {variant} |'
        table_rows.append(row)
    
    # 保存最后一个表格
    if table_rows:
        md_lines.append('| 编号 | 汉字 | 拼音 | 繁体 | 异体 |')
        md_lines.append('|------|------|------|------|------|')
        md_lines.extend(table_rows)
        md_lines.append('')
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    
    print(f'✅ 完整文档已生成: {output_file}')
    print(f'📊 总字数: {len(data)}')

if __name__ == '__main__':
    input_file = '通用规范汉字表_文本.txt'
    output_file = '通用规范汉字表_完整版.md'
    
    generate_full_document(input_file, output_file)
