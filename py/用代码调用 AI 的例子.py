# ============================================
# 使用 Python 调用 AI API 发送提示词
# 这个示例展示如何结构化你的提示词
# ============================================
#
# 教学目标：
# 1. 学习如何用 Python 构建结构化的 AI 提示词
# 2. 理解提示词的组成部分（角色、任务、上下文等）
# 3. 掌握链式调用（Fluent API）的设计模式
#
# 使用场景：
# - 需要向 AI 发送复杂、结构化的请求
# - 希望代码可读性强、易于维护
# - 需要复用提示词模板
#
# 注意：本示例使用模拟调用，实际项目中需替换为真实 API
# ============================================

import json
from typing import Dict, Optional


class PromptBuilder:
    """
    提示词构建器，帮助你结构化地组织提示词

    使用 Builder 设计模式，支持链式调用（Fluent API），
    使代码读起来像自然语言一样流畅。

    示例用法：
        prompt = (PromptBuilder()
                  .set_role("你是一名翻译")
                  .set_task("翻译以下文本")
                  .set_format("中文")
                  .build())
    """

    def __init__(self):
        # 提示词的各个组成部分，初始值为 None 或空列表
        self.role = None          # 角色设定：告诉 AI 它扮演什么身份
        self.task = None          # 任务描述：具体要 AI 做什么
        self.context = None       # 背景信息：提供必要的上下文
        self.format = None        # 输出格式：期望的回复格式
        self.examples = []        # 示例：输入/输出的范例（Few-shot 学习）
        self.constraints = []     # 约束条件：对输出的限制要求

    def set_role(self, role: str) -> "PromptBuilder":
        """
        设定 AI 的角色

        好的角色设定能让 AI 更好地理解任务背景，生成更符合期望的回答。

        参数:
            role: 角色描述，例如 "你是一名专业的翻译"

        返回:
            self，支持链式调用
        """
        self.role = role
        return self

    def set_task(self, task: str) -> "PromptBuilder":
        """
        设定任务

        任务描述应该清晰、具体，避免模糊不清的表述。

        参数:
            task: 任务描述，例如 "将以下英文翻译成中文"

        返回:
            self，支持链式调用
        """
        self.task = task
        return self

    def set_context(self, context: str) -> "PromptBuilder":
        """
        设定背景信息

        提供上下文能帮助 AI 更好地理解任务场景，
        生成更贴合实际需求的回答。

        参数:
            context: 背景信息，例如 "这是一封商务邮件"

        返回:
            self，支持链式调用
        """
        self.context = context
        return self

    def set_format(self, format_spec: str) -> "PromptBuilder":
        """
        设定输出格式

        指定期望的输出格式，可以使 AI 的回答更规范、易于使用。

        参数:
            format_spec: 格式要求，例如 "JSON 格式" 或 "邮件格式"

        返回:
            self，支持链式调用
        """
        self.format = format_spec
        return self

    def add_example(self, input_example: str, output_example: str) -> "PromptBuilder":
        """
        添加示例（Few-shot 学习）

        通过提供输入/输出示例，可以让 AI 更好地理解期望的回答模式。
        这种技术称为 "Few-shot Learning"。

        参数:
            input_example: 输入示例
            output_example: 期望的输出示例

        返回:
            self，支持链式调用
        """
        self.examples.append({"input": input_example, "output": output_example})
        return self

    def add_constraint(self, constraint: str) -> "PromptBuilder":
        """
        添加约束条件

        约束条件用于限制 AI 的输出，确保回答符合特定要求。
        例如：字数限制、语气要求、格式规范等。

        参数:
            constraint: 约束条件描述

        返回:
            self，支持链式调用
        """
        self.constraints.append(constraint)
        return self

    def build(self) -> str:
        """
        构建最终的提示词

        将所有设置的组件组合成一个完整的提示词字符串。
        组合顺序：角色 → 背景 → 任务 → 示例 → 输出格式 → 约束条件

        返回:
            完整的提示词字符串
        """
        parts = []  # 存储提示词的各个部分

        # 按照逻辑顺序组合各部分
        if self.role:
            parts.append(f"角色：{self.role}")

        if self.context:
            parts.append(f"背景：{self.context}")

        if self.task:
            parts.append(f"任务：{self.task}")

        # 示例部分可能有多个，需要遍历
        if self.examples:
            parts.append("示例：")
            for i, example in enumerate(self.examples, 1):
                parts.append(f"  输入{i}：{example['input']}")
                parts.append(f"  输出{i}：{example['output']}")

        if self.format:
            parts.append(f"输出格式：{self.format}")

        # 约束条件可能有多个，需要遍历
        if self.constraints:
            parts.append("约束条件：")
            for constraint in self.constraints:
                parts.append(f"  - {constraint}")

        # 用换行符连接所有部分
        return "\n".join(parts)


def simulate_ai_call(prompt: str, api_key: Optional[str] = None) -> Dict:
    """
    模拟 AI API 调用

    注意：这是一个模拟函数，仅用于演示提示词的结构化方式。
    实际项目中，你需要替换为真实的 API 调用，例如：
    - OpenAI API: https://platform.openai.com/docs
    - Anthropic API: https://docs.anthropic.com/

    参数:
        prompt: 构建好的提示词字符串
        api_key: API 密钥（本示例中未使用）

    返回:
        包含调用结果的字典
    """
    # 打印提示词，方便调试和学习
    print("=" * 60)
    print("发送给 AI 的提示词：")
    print("-" * 60)
    print(prompt)
    print("=" * 60)

    # 这里仅做演示，实际项目中会调用真实的 API
    # 例如：OpenAI API、Anthropic API 等
    # 真实调用示例（伪代码）：
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[{"role": "user", "content": prompt}]
    # )

    # 返回模拟的响应结果
    return {
        "status": "success",  # 调用状态
        "prompt_sent": prompt,  # 发送的提示词（用于调试）
        "message": "这是 AI 的模拟回复（实际使用时会替换为真实 API 响应）",
        "tips": "在实际项目中，请配置你的 API Key 并调用真实 API"
    }


# ============================================
# 使用示例 1：写邮件
# ============================================
# 场景：需要 AI 帮忙写一封商务邮件
# 特点：角色明确、格式规范、有约束条件

print("\n【示例 1：写邮件】")

# 使用链式调用构建提示词，代码读起来像自然语言
prompt1 = (PromptBuilder()
           .set_role("你是一名专业的商务写作助手，擅长英文邮件写作")  # 角色：商务写作专家
           .set_context("我是 runoob 公司的市场经理，需要给客户写一封跟进邮件")  # 背景：商务场景
           .set_task("写一封邮件，询问客户对我们产品方案的反馈，并预约下周的会议")  # 任务：写跟进邮件
           .set_format("邮件格式，包含：主题、称呼、正文、落款")  # 格式：标准邮件结构
           .add_constraint("语气友好但专业")  # 约束：语气要求
           .add_constraint("不超过 200 词")  # 约束：字数限制
           .build())

# 调用（模拟）AI API
result1 = simulate_ai_call(prompt1)
print(f"API 状态：{result1['status']}")


# ============================================
# 使用示例 2：代码优化
# ============================================
# 场景：需要 AI 帮忙优化代码
# 特点：技术角色、有兼容性要求

print("\n【示例 2：代码优化】")

# 构建代码优化的提示词
prompt2 = (PromptBuilder()
           .set_role("你是一位经验丰富的 Python 高级工程师，擅长代码审查")  # 角色：Python 专家
           .set_task("优化下面的代码，使其更高效、可读性更好")  # 任务：优化代码
           .set_context("这是一段处理学生成绩数据的代码，运行速度有点慢")  # 背景：性能问题
           .set_format("输出优化后的代码，并用注释说明改动原因")  # 格式：代码 + 注释
           .add_constraint("保持原有功能不变")  # 约束：功能不变
           .add_constraint("兼容 Python 3.8+")  # 约束：版本兼容
           .build())

# 调用（模拟）AI API
result2 = simulate_ai_call(prompt2)
print(f"API 状态：{result2['status']}")


# ============================================
# 学习提示
# ============================================
#
# 1. 提示词的结构很重要：
#    - 角色：让 AI 进入特定身份，回答更专业
#    - 任务：明确告诉 AI 要做什么
#    - 上下文：提供背景信息，帮助 AI 理解场景
#    - 格式：指定期望的输出格式，使结果更规范
#    - 约束：限制输出范围，避免回答过于宽泛
#
# 2. 链式调用（Fluent API）的优点：
#    - 代码可读性强
#    - 使用方式灵活
#    - 易于维护和扩展
#
# 3. 实际使用时，替换 simulate_ai_call 为真实 API 调用：
#    - OpenAI: pip install openai
#    - Anthropic: pip install anthropic
#    - 其他 AI 服务提供商的 SDK