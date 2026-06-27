---
title: PromptBuilder 代码示例
category: 提示词技巧与方法
difficulty: 进阶
tags:
  - prompt
  - 代码
  - Python
  - API
created: 2026-06-23
source: "[[02.Prompt 提示词  菜鸟教程]]"
---

# PromptBuilder 代码示例

> 除了在聊天界面输入提示词，你也可以通过代码来调用 AI API。下面是一个结构化构建提示词的 Python 工具。

---

## Prompt 模板

用 Builder 模式结构化地组织提示词的各个部分：

```python
import json
from typing import Dict, Optional


class PromptBuilder:
    """提示词构建器，帮助你结构化地组织提示词"""

    def __init__(self):
        self.role = None        # 角色设定
        self.task = None        # 任务描述
        self.context = None     # 背景信息
        self.format = None      # 输出格式
        self.examples = []      # 示例
        self.constraints = []   # 约束条件

    def set_role(self, role: str) -> "PromptBuilder":
        """设定 AI 的角色"""
        self.role = role
        return self

    def set_task(self, task: str) -> "PromptBuilder":
        """设定任务"""
        self.task = task
        return self

    def set_context(self, context: str) -> "PromptBuilder":
        """设定背景信息"""
        self.context = context
        return self

    def set_format(self, format_spec: str) -> "PromptBuilder":
        """设定输出格式"""
        self.format = format_spec
        return self

    def add_example(self, input_example: str, output_example: str) -> "PromptBuilder":
        """添加示例"""
        self.examples.append({"input": input_example, "output": output_example})
        return self

    def add_constraint(self, constraint: str) -> "PromptBuilder":
        """添加约束条件"""
        self.constraints.append(constraint)
        return self

    def build(self) -> str:
        """构建最终的提示词"""
        parts = []

        if self.role:
            parts.append(f"角色：{self.role}")
        if self.context:
            parts.append(f"背景：{self.context}")
        if self.task:
            parts.append(f"任务：{self.task}")
        if self.examples:
            parts.append("示例：")
            for i, example in enumerate(self.examples, 1):
                parts.append(f"  输入{i}：{example['input']}")
                parts.append(f"  输出{i}：{example['output']}")
        if self.format:
            parts.append(f"输出格式：{self.format}")
        if self.constraints:
            parts.append("约束条件：")
            for constraint in self.constraints:
                parts.append(f"  - {constraint}")

        return "\n".join(parts)
```

---

## 使用示例

### 示例 1：写邮件

```python
prompt = (PromptBuilder()
    .set_role("你是一名专业的商务写作助手，擅长英文邮件写作")
    .set_context("我是公司的市场经理，需要给客户写一封跟进邮件")
    .set_task("写一封邮件，询问客户对产品方案的反馈，并预约下周的会议")
    .set_format("邮件格式，包含：主题、称呼、正文、落款")
    .add_constraint("语气友好但专业")
    .add_constraint("不超过 200 词")
    .build())

print(prompt)
```

**输出：**
```
角色：你是一名专业的商务写作助手，擅长英文邮件写作
背景：我是公司的市场经理，需要给客户写一封跟进邮件
任务：写一封邮件，询问客户对产品方案的反馈，并预约下周的会议
输出格式：邮件格式，包含：主题、称呼、正文、落款
约束条件：
  - 语气友好但专业
  - 不超过 200 词
```

### 示例 2：代码优化

```python
prompt = (PromptBuilder()
    .set_role("你是一位经验丰富的 Python 高级工程师，擅长代码审查")
    .set_task("优化下面的代码，使其更高效、可读性更好")
    .set_context("这是一段处理学生成绩数据的代码，运行速度有点慢")
    .set_format("输出优化后的代码，并用注释说明改动原因")
    .add_constraint("保持原有功能不变")
    .add_constraint("兼容 Python 3.8+")
    .build())
```

---

## 技巧

PromptBuilder 把提示词的四要素（角色、任务、上下文、格式）拆分成独立的方法，通过链式调用组装。

实际项目中，将 `build()` 的结果传给 AI API（如 OpenAI、Anthropic 等）即可：

```python
# 实际调用时替换为真实 API
# from openai import OpenAI
# client = OpenAI(api_key="your-key")
# response = client.chat.completions.create(
#     model="gpt-4",
#     messages=[{"role": "user", "content": prompt}]
# )
```

---

## 相关模板

- [[Prompt/07-提示词技巧与方法/01-提示词基础结构|提示词基础结构]]
- [[Prompt/Prompt-MOC|Prompt 模板库]]
