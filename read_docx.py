#!/usr/bin/env python3
"""
读取DOCX文件内容
"""

import docx
import sys
import io

# 设置默认编码为utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    doc = docx.Document('操作系统安装用户关键词研究报告.docx')
    text = '\n'.join([para.text for para in doc.paragraphs])
    print(text[:5000])
except Exception as e:
    print(f"错误: {e}")
