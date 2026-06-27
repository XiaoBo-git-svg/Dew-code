---
title: Obsidian Web Clipper 代码块修复指南
created: 2026-06-24
updated: 2026-06-27
tags:
  - obsidian
  - webclipper
  - 工具
---

## 问题

Web Clipper 转 Markdown 时产生两类错误：

1. 代码没有 ` ``` ` 围栏
2. 代码中的 `[` `_` `#` `*` 被加了 `\` 转义（如 `\_tokens` → 应为 `_tokens`）

---

## 约束

- **执行流程：读文件 → 读指南 → 按 Step 1-5 顺序执行。** 不要想别的，照着做。
- **转义还原用 Edit replace_all，围栏操作优先用 Python 脚本。** 转义还原（5 次 replace_all）用 Edit；围栏操作用 Python 脚本一次性处理（sed 中的反引号会被 bash 解释，需额外处理）。围栏数量多时，Python 脚本是最可靠选择。**注意：** `\]` 的 Edit replace_all 可能失效，Step 2 完成后必须验证，若 `\]` 残留则用 Python 兜底。
- **先读完，再动手。** 通读全篇后一次性规划所有 Edit，不要读一次改一次。
- **old_string 越短越好，但必须唯一。** 匹配首行 + 紧邻的 1-2 行即可，不要把整个代码块塞进 old_string。old_string 越长，转义字符导致匹配失败的概率越高。若首行在文件中出现多次（如 `# ========== `），向下多取 1-2 行直到唯一。
- **禁止在思考中反复推演。** 读完文件、列出修复清单后，下一步就是发出工具调用。不要在内部推理中讨论策略、分析可能性、自我质疑——这些不会产生任何输出，只是浪费时间。**发出第一个工具调用前的思考时间不得超过 30 秒。** 指南已写明每步操作，照着执行即可，无需额外分析。失败了再处理。
- **严格按 Step 顺序执行，不跳步、不合并。** 每个 Step 做完再进下一个，不要试图"优化"流程。

## 执行纪律

1. **严格按 Step 顺序执行。** 不跳步、不合并、不省略。每个 Step 做完再进下一个。
2. **禁止自由发挥。** 指南写什么就做什么，不要"聪明地"优化流程。没有写在指南里的操作不做。
3. **Edit 失败立即降级。** 第一次 Edit 失败后，缩小 old_string 为 2-3 行重试，不要重复同样的大片段。围栏操作已用 Python 脚本，不会遇到此问题。
4. **清单项必须实际执行。** 打勾 = 已完成，不是 = 计划完成。没做的不许打勾。
5. **加完围栏必须防空检查。** Step 3 完成后，用 Python 检查围栏是否有 `\` 前缀，并验证开闭数量相等，有问题立即修复，不等到 Step 4。

---

## 流程

### Step 1：扫描

读完整篇笔记，记录每个需要修复的位置。菜鸟教程以 `## 实例` 标记代码块，检查其下方是否有围栏。

三种情况：
- 已有 ` ``` ` 围栏且无转义 → 跳过
- 无围栏、有转义 → Step 2 + Step 3
- 有围栏、表格中有转义 → 仅 Step 2

### Step 2：还原转义

对全篇执行 5 次 `replace_all`（并行发出）：

| 找到 | 替换为 |
|------|--------|
| `\[` | `[` |
| `\]` | `]` |
| `\_` | `_` |
| `\#` | `#` |
| `\*` | `*` |

**例外（不还原）：**
- 正文中的 `\[产品类型\]`（模板占位符，保留反斜杠防止 Obsidian 解析为链接）
- 表格中的 `\>`（`>` 在表格中会触发引用块，必须保留转义）

**\] 兜底：** Edit replace_all 对 `\]` 可能失效。Step 2 完成后验证：若代码中仍有 `\]`，用 Python 一行修复：
```python
python3 -c "f='文件路径';c=open(f).read().replace('\\\\]',']');open(f,'w').write(c)"
```

### Step 3：加围栏

用 Python 脚本一次性插入开围栏和闭围栏。

**语言标记：**

| 代码特征 | 标记 |
|----------|------|
| `import`、`def`、`print(`、4 空格缩进 | `python` |
| `curl`、`#!/bin/bash`、`$` 提示符 | `bash` |
| `const`、`let`、`function` | `javascript` |
| `<html>`、`<div>` | `html` |
| 提示词模板、自然语言描述 | 不加标记，用 ` ``` ` |

**操作方式（Python 脚本）：**

1. 先移除文件中所有已有的 ` ``` ` 和 ` ```python ` 行（清理残留）
2. 用正则找到所有 `## 实例` 的行号
3. 对每个代码块：
   - **开围栏**：插入在 `## 实例` 之后、第一个非空行之前（即 `## 实例` + 空行 + ` ```python ` + 代码首行）
   - **闭围栏**：插入在**代码最后一行之后**（不是下一个 `## 实例` 之前！）
4. 代码结束位置检测：逐行扫描，找最后一个匹配 Python 代码模式的行
5. **最后一行检查**：确认文件末尾的闭围栏没有与代码行粘连（如 `print(...)```` `），有则拆分

> **注意：** 不要把闭围栏放在下一个 `## 实例` 之前——那会导致闭围栏跑到散文段落中间。闭围栏必须紧跟代码最后一行。

**防空检查：** Step 3 完成后，用 Python 检查围栏是否有 `\` 前缀，并验证开闭数量相等。

**代码结束位置检测要点：**

- `is_likely_code()` 中**空行返回 False**（不是 True），否则闭围栏会插到空行后面而非代码末行后面
- **中文散文误识别为代码的常见陷阱**：
  - `class token 是一个可学习的向量` — `class` 前缀匹配，但含 `是` `的` `，` 所以是散文
  - `CLIP 可以用任意文字描述` — `clip` 前缀匹配，但含 `可以` `，` 所以是散文
  - `负例：A="我喜欢吃苹果"` — 含 `=` 和 `"` 被当成赋值，但含 `：` `，` 是散文
  - 规则：**中文标点（`，` `。` `：` `！` `？` `；`）是散文的最强信号**，非 `#` 开头、非缩进行、非 `print` → 判定为散文
- **散文标记**（绝对不是代码）：`###` 标题、`## ` 标题、`| ` 表格行、`>` 引用块、`- ` 列表项、`\d+\.` 有序列表、`---` 水平线

**经过验证的脚本骨架：**

```python
import re

with open("文件路径", "r") as f:
    lines = f.readlines()

# 1. 移除所有已有围栏
clean = [l for l in lines if l.strip() not in ("```", "```python")]

# 2. 找 ## 实例 位置
instances = [i for i, l in enumerate(clean) if l.strip() == "## 实例"]

# 3. 对每个代码块找代码最后一行
def is_code_line(s):
    """空行返回 False（不是代码）。中文标点是最强散文信号。"""
    if not s: return False
    # === 散文标记（绝对不是代码） ===
    if s.startswith(('###', '## ', '| ', '> ', '- ', '---')): return False
    if re.match(r'^\d+\\\.', s): return False
    # 中文标点 → 散文（覆盖任何代码模式匹配）
    if re.search(r'[。，：！？；]', s) and not s.startswith('#') and not s.startswith('    '):
        return False
    # === 代码标记 ===
    code_p = ('#', 'import ', 'from ', 'def ', 'class ', 'return ', 'print',
              'for ', 'if ', 'elif ', 'else:', 'self.', '    ')
    if any(s.startswith(p) for p in code_p): return True
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*[\s]*[=\(]', s): return True
    if s.startswith((')', ']', '}', '),', '],')): return True
    if '"' in s and '=' in s: return True
    if s.startswith(('f"', "f'", '"', "'")): return True
    return False

# 4. 从后往前插入围栏
for idx in reversed(range(len(instances))):
    start = instances[idx]
    end = instances[idx + 1] if idx + 1 < len(instances) else len(clean)
    last_code = start
    for j in range(start, end):
        if is_code_line(clean[j].strip()):
            last_code = j
    clean.insert(last_code + 1, "```\n")
    ins = start + 1
    while ins < len(clean) and not clean[ins].strip(): ins += 1
    clean.insert(ins, "```python\n")

# 5. 末行检查：确保闭围栏未与代码粘连
if clean and clean[-1].strip().endswith("```") and len(clean[-1].strip()) > 3:
    code_part = clean[-1].rstrip().rstrip('`').rstrip()
    clean[-1] = code_part + "\n"
    clean.append("```\n")

with open("文件路径", "w") as f:
    f.writelines(clean)
```

### Step 4：验证

逐项检查：

- [ ] 每段代码都有 ` ``` ` 围栏，开闭配对
- [ ] 围栏有正确的语言标记
- [ ] 代码内无 `\` 前缀（`_` `#` `[` `]` `*` 均为正常字符）
- [ ] 表格中技术参数名正确（`max_tokens` 而非 `max\_tokens`）
- [ ] 每个 ` ``` ` 独占一行，未与正文粘连
- [ ] 代码块内无中文正文混入
- [ ] 模板占位符 `\[...\]` 保留了反斜杠

> **注意：** Read 工具可能对 `*` 做额外转义显示。Edit 匹配失败时，重新 Read 确认文件真实内容。若仍无法匹配，用 `sed -n '起始行,结束行p' 文件 | cat -A` 查看原始字节，确认是真实内容还是转义显示。

### Step 5：回看指南

完成 Step 4 后，立即回看本指南，逐项自检：

- 本指南是否有新的坑未覆盖？
- 经验是否过时？
- 执行耗时集中在哪个阶段？该阶段是否可以优化？
- 发现需要改进的步骤，**立即更新本指南**。
