# Obsidian Templater 脚本：自动为代码块添加 Python 高亮

## 使用方法

### 1. 安装 Templater 插件
- Obsidian → 设置 → 第三方插件 → 浏览 → 搜索 "Templater" → 安装并启用

### 2. 配置 Templater
- 设置 → Templater：
  - **Template folder location**: `Templates`（或你的模板文件夹路径）
  - **Enable System Command**: 开启（可选）

### 3. 创建模板文件
在你的模板文件夹中创建以下文件：

---

## 脚本一：为当前笔记添加 Python 高亮

文件名：`add-python-highlight.md`

````markdown
<%*
// ============================================
// Templater 脚本：为代码块添加 Python 语言标识
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
````

---

## 脚本二：为代码块添加指定语言（交互式）

文件名：`add-language-highlight.md`

````markdown
<%*
// ============================================
// Templater 脚本：为代码块添加指定语言标识
// ============================================

// 弹出输入框让用户选择语言
const language = await tp.system.prompt("请输入代码语言（如 python, javascript, bash, sql）：", "python");

if (!language) {
    tR += "❌ 已取消操作\n";
    return;
}

// 获取当前笔记内容
let content = tp.file.content;

// 正则匹配没有语言标识的代码块
const regex = /```(\s*)\n/g;

// 替换为指定语言
const newContent = content.replace(regex, '```' + language + '\n');

// 统计替换数量
const matches = content.match(regex);
const count = matches ? matches.length : 0;

// 写回笔记
if (count > 0) {
    await tp.file.content(newContent);
    tR += `✅ 已为 ${count} 个代码块添加 ${language} 标识\n`;
} else {
    tR += `ℹ️ 未找到需要处理的代码块\n`;
}
%>
````

---

## 脚本三：批量处理文件夹中所有剪藏笔记

文件名：`batch-add-python-highlight.md`

````markdown
<%*
// ============================================
// Templater 脚本：批量为文件夹中所有笔记添加 Python 高亮
// ============================================

// 设置目标文件夹（修改为你的剪藏文件夹路径）
const targetFolder = "Clippings";

// 获取文件夹中所有 md 文件
const files = tp.vault.getMarkdownFiles().filter(f => f.path.startsWith(targetFolder));

if (files.length === 0) {
    tR += `❌ 未找到文件夹 "${targetFolder}" 中的笔记\n`;
    return;
}

let totalProcessed = 0;
let totalReplaced = 0;

for (const file of files) {
    // 读取文件内容
    let content = await tp.vault.read(file);

    // 正则匹配没有语言标识的代码块
    const regex = /```(\s*)\n/g;
    const matches = content.match(regex);
    const count = matches ? matches.length : 0;

    if (count > 0) {
        // 替换为 ```python\n
        const newContent = content.replace(regex, '```python\n');
        await tp.vault.modify(file, newContent);
        totalReplaced += count;
        totalProcessed++;
    }
}

tR += `✅ 处理完成！\n`;
tR += `- 扫描文件数: ${files.length}\n`;
tR += `- 处理文件数: ${totalProcessed}\n`;
tR += `- 替换代码块数: ${totalReplaced}\n`;
%>
````

---

## 脚本四：剪藏时自动触发（配合 Web Clipper）

文件名：`auto-clipper-python.md`

````markdown
<%*
// ============================================
// Templater 脚本：Web Clipper 剪藏后自动处理
// 配合 QuickAdd 或 Obsidian URI 使用
// ============================================

// 获取当前笔记内容
let content = tp.file.content;

// 检查是否是剪藏笔记（通过 frontmatter 判断）
if (!content.includes("tags:") || !content.includes("clipping")) {
    tR += "ℹ️ 当前笔记不是剪藏笔记，跳过处理\n";
    return;
}

// 正则匹配没有语言标识的代码块
const regex = /```(\s*)\n/g;
const matches = content.match(regex);
const count = matches ? matches.length : 0;

if (count > 0) {
    // 替换为 ```python\n
    const newContent = content.replace(regex, '```python\n');
    await tp.file.content(newContent);
    tR += `✅ 剪藏笔记已处理，添加了 ${count} 个 python 标识\n`;
} else {
    tR += `ℹ️ 剪藏笔记中未找到需要处理的代码块\n`;
}
%>
````

---

## 快捷键配置

在 Obsidian 中为模板设置快捷键：

1. **设置** → **快捷键**
2. 搜索 "Templater"
3. 为以下命令设置快捷键：
   - `Templater: Insert template` → `Ctrl + Shift + T`
   - 或者使用 `Templater: Replace templates in active file` → `Ctrl + Shift + R`

### 推荐快捷键方案

| 功能 | 快捷键 |
|------|--------|
| 为当前笔记添加 Python 高亮 | `Ctrl + Shift + P` |
| 选择语言添加高亮 | `Ctrl + Shift + L` |
| 批量处理剪藏文件夹 | `Ctrl + Shift + B` |

---

## 高级用法：智能识别语言

如果你希望脚本能自动识别代码块的语言（而不是统一设置为 python），可以使用以下增强版：

````markdown
<%*
// ============================================
// Templater 脚本：智能识别代码语言
// ============================================

// 获取当前笔记内容
let content = tp.file.content;

// 语言识别规则（基于代码特征）
const languagePatterns = [
    { pattern: /\bdef\s+\w+\s*\(.*\):/, lang: 'python' },
    { pattern: /\bimport\s+(?:os|sys|json|re)\b/, lang: 'python' },
    { pattern: /\bprint\s*\(/, lang: 'python' },
    { pattern: /\bfunction\s+\w+\s*\(/, lang: 'javascript' },
    { pattern: /\bconst\s+|let\s+|var\s+/, lang: 'javascript' },
    { pattern: /\bconsole\.log\s*\(/, lang: 'javascript' },
    { pattern: /\bpublic\s+class\s+/, lang: 'java' },
    { pattern: /\bSystem\.out\.print/, lang: 'java' },
    { pattern: /\bfn\s+\w+\s*\(/, lang: 'rust' },
    { pattern: /\blet\s+mut\s+/, lang: 'rust' },
    { pattern: /\bfunc\s+\w+\s*\(/, lang: 'go' },
    { pattern: /\bfmt\.Print/, lang: 'go' },
    { pattern: /\bSELECT\s+.*\bFROM\b/i, lang: 'sql' },
    { pattern: /\bINSERT\s+INTO\b/i, lang: 'sql' },
    { pattern: /\b<!DOCTYPE\s+html>/i, lang: 'html' },
    { pattern: /\b\{[\s\S]*?[\w-]+\s*:.*;\s*\}/, lang: 'css' },
    { pattern: /\bsudo\s+|apt\s+|yum\s+/, lang: 'bash' },
    { pattern: /\becho\s+/, lang: 'bash' },
];

// 正则匹配代码块（包括内容）
const codeBlockRegex = /```(\s*)\n([\s\S]*?)```/g;

let processedContent = content;
let count = 0;

// 遍历所有代码块
let match;
while ((match = codeBlockRegex.exec(content)) !== null) {
    const [fullMatch, space, codeContent] = match;

    // 如果已经有语言标识，跳过
    if (space && space.trim() !== '') continue;

    // 尝试识别语言
    let detectedLang = 'python'; // 默认 python
    for (const { pattern, lang } of languagePatterns) {
        if (pattern.test(codeContent)) {
            detectedLang = lang;
            break;
        }
    }

    // 替换代码块
    const newBlock = '```' + detectedLang + '\n' + codeContent + '```';
    processedContent = processedContent.replace(fullMatch, newBlock);
    count++;
}

if (count > 0) {
    await tp.file.content(processedContent);
    tR += `✅ 智能处理完成，识别并标记了 ${count} 个代码块\n`;
} else {
    tR += `ℹ️ 未找到需要处理的代码块\n`;
}
%>
````

---

## 故障排除

### 问题 1：脚本不生效
- 确认 Templater 插件已启用
- 确认模板文件放在正确的模板文件夹中
- 检查 Obsidian 控制台是否有错误（`Ctrl + Shift + I`）

### 问题 2：替换后格式错乱
- 检查原代码块是否使用了四个反引号（``````）而不是三个
- 脚本目前只处理三个反引号的情况

### 问题 3：想恢复原始内容
- 使用 `Ctrl + Z` 撤销
- 或者从 Obsidian 的版本历史中恢复

---

## 相关资源

- [Templater 官方文档](https://silentvoid13.github.io/Templater/)
- [Obsidian 论坛 - Templater 板块](https://forum.obsidian.md/c/share-showcase/9)
- [Obsidian Web Clipper](https://obsidian.md/clipper)
