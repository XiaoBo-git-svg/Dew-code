<%*
// ============================================
// Templater 脚本：为代码块添加 Python 语言标识
// 使用方法：Ctrl+P → Templater: Replace templates in active file
// ============================================

// 获取当前笔记内容
let content = tp.file.content;

// 正则匹配没有语言标识的代码块
// 匹配 ``` 后面直接换行的情况（排除已有语言标识的）
const regex = /```(\s*)\n/g;

// 替换为 ```python\n
const newContent = content.replace(regex, '```python\n');

// 统计替换数量
const matches = content.match(regex);
const count = matches ? matches.length : 0;

// 写回笔记
if (count > 0) {
    await tp.file.content(newContent);
    tR += `✅ 已为 ${count} 个代码块添加 python 标识\n`;
} else {
    tR += `ℹ️ 未找到需要处理的代码块\n`;
}
%>
