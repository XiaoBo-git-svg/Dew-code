#!/usr/bin/env python3
"""
修复 Web Clipper 剪切的菜鸟教程笔记
用法: python fix_clipper.py <文件路径>
      python fix_clipper.py --batch Clippings/  # 批量修复目录
"""
import re
import sys
import os
from pathlib import Path


def detect_language(code_lines: list[str]) -> str:
    """根据代码内容自动检测语言"""
    text = "\n".join(code_lines)
    if re.search(r'\b(def |import |from |print\(|class )\b', text):
        return "python"
    if re.search(r'\b(const |let |var |function |=>|console\.)\b', text):
        return "javascript"
    if re.search(r'\b(curl |#!/bin|echo |grep |sudo )\b', text):
        return "bash"
    if text.strip().startswith('{') or '"messages"' in text:
        return "json"
    if '<html' in text.lower() or '<div' in text.lower():
        return "html"
    return ""


def fix_escapes_in_code(text: str) -> str:
    """还原代码块内的转义字符"""
    text = text.replace('\\[', '[')
    text = text.replace('\\]', ']')
    text = text.replace('\\_', '_')
    text = text.replace('\\#', '#')
    # \* 还原，但不还原 \*\*（Markdown 粗体）
    text = re.sub(r'(?<!\*)\\\*(?!\*)', '*', text)
    return text


def fix_escapes_in_tables(text: str) -> str:
    """还原 Markdown 表格单元格中的转义（仅 \_ → _）"""
    lines = text.split('\n')
    result = []
    for line in lines:
        if line.strip().startswith('|') and '|' in line[1:]:
            line = line.replace('\\_', '_')
        result.append(line)
    return '\n'.join(result)


def fix_clipper_note(filepath: str) -> bool:
    """修复单个笔记文件，返回是否做了修改"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    result = []
    i = 0
    modified = False

    while i < len(lines):
        line = lines[i]

        # 检测 ## 实例 标记（菜鸟教程代码块起始）
        if line.strip() == '## 实例':
            modified = True
            # 跳过实例标题，开始收集代码行
            i += 1
            # 跳过空行
            while i < len(lines) and lines[i].strip() == '':
                i += 1

            # 收集代码块内容（直到遇到下一个标题或明显的正文段落）
            code_lines = []
            while i < len(lines):
                current = lines[i]
                # 遇到下一个标题 → 代码块结束
                if current.startswith('## ') or current.startswith('### '):
                    break
                # 遇到已有围栏 → 说明是情况 A，不需要处理
                if current.strip().startswith('```'):
                    # 把已有的围栏和内容原样保留
                    result.append(line)  # ## 实例
                    result.append('')    # 空行
                    while i < len(lines):
                        result.append(lines[i])
                        i += 1
                    code_lines = None  # 标记：无需处理
                    break
                # 遇到纯中文正文段落（非代码）→ 代码块结束
                if (current.strip() and
                    not current.startswith(' ') and
                    not current.startswith('\t') and
                    not current.startswith('|') and
                    not current.startswith('-') and
                    not current.startswith('>') and
                    not current.startswith('#') and
                    not current.startswith('```') and
                    re.match(r'^[一-鿿]', current.strip()) and
                    '(' not in current and '=' not in current and
                    ':' not in current[:20]):
                    break
                code_lines.append(current)
                i += 1

            if code_lines is None:
                continue  # 已有围栏，跳过

            if code_lines:
                # 去除首尾空行
                while code_lines and code_lines[0].strip() == '':
                    code_lines.pop(0)
                while code_lines and code_lines[-1].strip() == '':
                    code_lines.pop()

                if code_lines:
                    # 还原转义
                    code_lines = [fix_escapes_in_code(l) for l in code_lines]
                    # 检测语言
                    lang = detect_language(code_lines)
                    # 输出围栏
                    result.append(f'```{lang}')
                    result.extend(code_lines)
                    result.append('```')
        else:
            result.append(line)
            i += 1

    new_content = '\n'.join(result)

    # 对整个文件的表格进行转义还原
    new_content = fix_escapes_in_tables(new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    if len(sys.argv) < 2:
        print("用法: python fix_clipper.py <文件路径>")
        print("      python fix_clipper.py --batch <目录>")
        sys.exit(1)

    if sys.argv[1] == '--batch':
        directory = sys.argv[2] if len(sys.argv) > 2 else 'Clippings'
        fixed = 0
        for f in sorted(Path(directory).glob('*.md')):
            if fix_clipper_note(str(f)):
                print(f"✅ 已修复: {f.name}")
                fixed += 1
            else:
                print(f"⬜ 无需修复: {f.name}")
        print(f"\n共修复 {fixed} 个文件")
    else:
        filepath = sys.argv[1]
        if fix_clipper_note(filepath):
            print(f"✅ 已修复: {filepath}")
        else:
            print(f"⬜ 无需修复: {filepath}")


if __name__ == '__main__':
    main()
