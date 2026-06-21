<%*
// ============================================
// Templater 脚本：修复菜鸟教程剪藏笔记中的代码块
//
// 问题：菜鸟教程代码用 <div class="example_code"> + <span>
//       没有 <pre><code>，Web Clipper 无法识别为代码块
//
// 效果：将 "## 实例" 后的纯文本代码包裹到代码块中
//       移除 Web Clipper 的转义符号，自动添加语言标识
//
// 使用方法：
//   1. 打开需要修复的剪藏笔记
//   2. Ctrl+P → "Templater: Replace templates in active file"
//   3. 选择此模板
// ============================================

const content = tp.file.content;
const lines = content.split('\n');
const result = [];
let i = 0;
let fixCount = 0;

while (i < lines.length) {
  const line = lines[i];

  // 检测 "## 实例" 标题
  if (line.trim() === '## 实例') {
    result.push(line);
    i++;

    // 跳过标题后的空行
    while (i < lines.length && lines[i].trim() === '') {
      result.push(lines[i]);
      i++;
    }

    // 收集代码行（直到遇到非代码内容）
    // 代码行特征：\# 开头、def/import/class/for/if 等关键字、
    //             赋值语句、pip 命令、函数调用
    const codeLines = [];
    while (i < lines.length) {
      const cl = lines[i];
      const trimmed = cl.trim();

      // 遇到这些就停止收集
      if (trimmed === '---' ||
          trimmed.startsWith('## ') ||
          trimmed.startsWith('### ') ||
          trimmed.startsWith('> ')) {
        break;
      }

      // 空行后如果下一行是普通段落文本，也停止
      if (trimmed === '') {
        // 预看下一行
        const nextLine = (i + 1 < lines.length) ? lines[i + 1].trim() : '';
        const isCodeNext = nextLine.startsWith('\\#') ||
                           nextLine.startsWith('def ') ||
                           nextLine.startsWith('import ') ||
                           nextLine.startsWith('class ') ||
                           nextLine.startsWith('from ') ||
                           nextLine.startsWith('pip ') ||
                           nextLine.startsWith('whisper ') ||
                           nextLine.startsWith('for ') ||
                           nextLine.startsWith('if ') ||
                           nextLine.startsWith('elif ') ||
                           nextLine.startsWith('else:') ||
                           nextLine.startsWith('print(') ||
                           nextLine.startsWith('return ') ||
                           nextLine.startsWith('async ') ||
                           nextLine.startsWith('const ') ||
                           nextLine.startsWith('let ') ||
                           nextLine.startsWith('var ') ||
                           nextLine.startsWith('function ') ||
                           nextLine.match(/^\w+\s*=\s/) ||
                           nextLine.match(/^\w+\(/) ||
                           nextLine === '';

        if (!isCodeNext && nextLine.length > 0) {
          break;
        }
        codeLines.push(cl);
        i++;
        continue;
      }

      // 普通代码行
      codeLines.push(cl);
      i++;
    }

    // 只有收集到足够多的代码行才处理（至少 2 行非空）
    const nonEmpty = codeLines.filter(l => l.trim().length > 0);
    if (nonEmpty.length >= 2) {
      // 清理代码内容
      let cleaned = codeLines.join('\n')
        .replace(/\\\#/g, '#')        // \# → #
        .replace(/\\_/g, '_')         // \_ → _
        .replace(/\\\[/g, '[')        // \[ → [
        .replace(/\\\]/g, ']')        // \] → ]
        .replace(/  $/gm, '')         // 行尾两空格 → 删除
        .replace(/\n{3,}/g, '\n\n')   // 多余空行
        .trim();

      // 检测语言
      let lang = 'python';
      const firstCode = nonEmpty[0].replace(/^  $/, '').trim();
      if (firstCode.includes('//') && !firstCode.includes('def ')) {
        lang = 'javascript';
      } else if (firstCode.startsWith('$') || firstCode.startsWith('sudo ')) {
        lang = 'bash';
      }

      result.push('```' + lang);
      result.push(cleaned);
      result.push('```');
      result.push('');
      fixCount++;
    } else {
      // 代码行太少，原样保留
      codeLines.forEach(l => result.push(l));
    }

    continue;
  }

  // 第二步：修复已有 ``` 但没有语言标识的代码块
  if (line.match(/^```\s*$/) && !line.match(/^```\w/)) {
    result.push('```python');
    fixCount++;
    i++;
    continue;
  }

  result.push(line);
  i++;
}

if (fixCount > 0) {
  await tp.file.content(result.join('\n'));
  tR += `✅ 已修复 ${fixCount} 个代码块\n\n`;
  tR += `修复内容：\n`;
  tR += `- 将 "## 实例" 后的纯文本代码包裹到代码块中\n`;
  tR += `- 移除 Web Clipper 转义符号（\\# \\_ \\[ \\]）\n`;
  tR += `- 自动检测并添加语言标识（python/javascript/bash）\n`;
} else {
  tR += `ℹ️ 未找到需要修复的代码块\n`;
}
%>
