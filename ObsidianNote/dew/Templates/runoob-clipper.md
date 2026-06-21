---
clipper: true
name: "菜鸟教程 - 代码高亮"
note: "Obsidian Web Clipper 模板配置指南"
---

## Web Clipper 模板配置步骤

### 1. 打开 Web Clipper 设置

Firefox 中点击 Obsidian Web Clipper 图标 → 齿轮图标 → **Templates**

### 2. 创建新模板

点击 **+ New template**，填写：

| 字段 | 值 |
|------|-----|
| Template name | `菜鸟教程` |
| Note name | `{{title}}` |
| Note location | `Clippings` |

### 3. 配置 Content（关键步骤）

在 **Content** 区域，点击 **Show page content** 下方的 **Edit** 按钮，粘贴以下内容：

```
{{selectorHtml}}
```

然后在 **Content Transform** 或 **Post-processor** 中添加 JavaScript：

```javascript
// ============================================
// 菜鸟教程 Web Clipper 内容转换脚本
// 将 .example_code div 转为 Markdown 代码块
// ============================================

// 等待 DOM 就绪
document.querySelectorAll('.example_code').forEach((block, index) => {
  // 获取纯文本，保留换行
  let codeText = block.innerText
    .replace(/ /g, ' ')    // &nbsp; → 空格
    .trim();

  // 检测语言（简单启发式）
  let lang = 'python';  // 默认 Python
  const firstLine = codeText.split('\n')[0];
  if (firstLine.includes('//') && !firstLine.includes('#')) {
    lang = 'javascript';
  } else if (firstLine.includes('pip ') || firstLine.includes('import ') ||
             firstLine.includes('def ') || firstLine.includes('print(')) {
    lang = 'python';
  } else if (firstLine.includes('$') || firstLine.includes('#!')) {
    lang = 'bash';
  }

  // 构造 markdown 代码块
  const fenced = '```' + lang + '\n' + codeText + '\n```';

  // 替换原 div 内容（用临时标记）
  const marker = document.createElement('div');
  marker.setAttribute('data-code-block', index);
  marker.textContent = fenced;
  block.parentNode.replaceChild(marker, block);
});
```

### 4. 配置 Frontmatter（可选）

在 **Frontmatter** 区域添加：

```yaml
source: "{{url}}"
author: "{{author}}"
created: "{{date}}"
tags:
  - "clippings"
  - "runoob"
```

### 5. 保存并测试

1. 打开任意菜鸟教程页面（如 https://www.runoob.com/ai/ai-tools.html）
2. 点击 Web Clipper 图标
3. 选择刚创建的 **菜鸟教程** 模板
4. 预览确认代码块被正确识别
5. 保存

---

## 备注

如果 Web Clipper 不支持 Content Transform（某些版本），可以改用方案：

1. 只配置基本模板，不加 JS 转换
2. 剪藏后立即运行 Templater 脚本修复（方案二）

详见 [[Templates/fix-runoob-code|修复菜鸟教程代码块]]
