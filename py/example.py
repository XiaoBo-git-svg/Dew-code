import tkinter as tk
from tkinter import messagebox
import random

class GuessNumberGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🎯 猜数字游戏")
        self.window.geometry("500x600")
        self.window.configure(bg="#2C3E50")

        self.secret_number = random.randint(1, 100)
        self.attempts = 7
        self.current_attempt = 0
        self.guessed = False

        self.setup_ui()

    def setup_ui(self):
        # 标题
        title_label = tk.Label(
            self.window,
            text="🎯 猜数字游戏 🎯",
            font=("Arial", 24, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        title_label.pack(pady=20)

        # 游戏说明
        rules_frame = tk.Frame(self.window, bg="#34495E", relief=tk.RAISED, bd=2)
        rules_frame.pack(pady=10, padx=20, fill=tk.X)

        rules_text = """
        🎮 游戏规则：
        • 我想了一个 1-100 之间的数字
        • 你有 7 次机会猜中它
        • 每次猜测我会提示太大或太小
        • 还有温度提示哦！
        """
        rules_label = tk.Label(
            rules_frame,
            text=rules_text,
            font=("Arial", 11),
            bg="#34495E",
            fg="#ECF0F1",
            justify=tk.LEFT
        )
        rules_label.pack(pady=10, padx=10)

        # 输入区域
        input_frame = tk.Frame(self.window, bg="#2C3E50")
        input_frame.pack(pady=20)

        input_label = tk.Label(
            input_frame,
            text="👉 请输入你的猜测 (1-100):",
            font=("Arial", 12),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        input_label.pack()

        self.entry = tk.Entry(
            input_frame,
            font=("Arial", 16),
            width=10,
            justify=tk.CENTER
        )
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', lambda e: self.make_guess())

        # 猜测按钮
        self.guess_button = tk.Button(
            input_frame,
            text="🎯 猜测！",
            font=("Arial", 12, "bold"),
            bg="#E74C3C",
            fg="white",
            command=self.make_guess,
            width=10
        )
        self.guess_button.pack(pady=5)

        # 提示区域
        self.hint_frame = tk.Frame(self.window, bg="#34495E", relief=tk.SUNKEN, bd=2)
        self.hint_frame.pack(pady=10, padx=20, fill=tk.X)

        self.hint_label = tk.Label(
            self.hint_frame,
            text="🤔 等待你的第一次猜测...",
            font=("Arial", 14),
            bg="#34495E",
            fg="#F39C12",
            wraplength=400
        )
        self.hint_label.pack(pady=15)

        # 剩余次数
        self.attempts_label = tk.Label(
            self.window,
            text=f"🎯 剩余机会: {self.attempts} 次",
            font=("Arial", 12),
            bg="#2C3E50",
            fg="#E74C3C"
        )
        self.attempts_label.pack(pady=5)

        # 历史记录
        history_label = tk.Label(
            self.window,
            text="📜 猜测历史:",
            font=("Arial", 10),
            bg="#2C3E50",
            fg="#95A5A6"
        )
        history_label.pack(anchor=tk.W, padx=20)

        self.history_text = tk.Text(
            self.window,
            height=4,
            font=("Arial", 10),
            bg="#34495E",
            fg="#ECF0F1",
            state=tk.DISABLED
        )
        self.history_text.pack(pady=5, padx=20, fill=tk.X)

        # 重新开始按钮
        self.restart_button = tk.Button(
            self.window,
            text="🔄 重新开始",
            font=("Arial", 11),
            bg="#27AE60",
            fg="white",
            command=self.restart_game,
            state=tk.DISABLED
        )
        self.restart_button.pack(pady=10)

        # 状态栏
        self.status_label = tk.Label(
            self.window,
            text="🎮 游戏进行中...",
            font=("Arial", 10),
            bg="#2C3E50",
            fg="#1ABC9C"
        )
        self.status_label.pack(side=tk.BOTTOM, pady=10)

    def make_guess(self):
        if self.guessed:
            return

        try:
            guess = int(self.entry.get())
            if guess < 1 or guess > 100:
                messagebox.showwarning("⚠️ 警告", "请输入1-100之间的数字！")
                return

            self.current_attempt += 1
            remaining = self.attempts - self.current_attempt

            # 更新历史记录
            self.update_history(guess)

            if guess == self.secret_number:
                self.guessed = True
                self.show_win()
            else:
                # 显示提示
                diff = abs(guess - self.secret_number)
                if diff <= 5:
                    temperature = "🔥 非常接近了！"
                    color = "#E74C3C"
                elif diff <= 15:
                    temperature = "🌡️ 有点接近！"
                    color = "#F39C12"
                elif diff <= 30:
                    temperature = "❄️ 还差一点！"
                    color = "#3498DB"
                else:
                    temperature = "🥶 差得远呢！"
                    color = "#95A5A6"

                if guess < self.secret_number:
                    direction = "📈 太小了！"
                else:
                    direction = "📉 太大了！"

                hint_text = f"{direction}\n{temperature}"
                self.hint_label.config(text=hint_text, fg=color)
                self.attempts_label.config(text=f"🎯 剩余机会: {remaining} 次")

                if remaining == 0:
                    self.show_lose()

            self.entry.delete(0, tk.END)

        except ValueError:
            messagebox.showwarning("⚠️ 警告", "请输入有效的数字！")

    def update_history(self, guess):
        self.history_text.config(state=tk.NORMAL)
        diff = guess - self.secret_number
        if diff < 0:
            symbol = "⬆️"
        elif diff > 0:
            symbol = "⬇️"
        else:
            symbol = "✅"

        self.history_text.insert(tk.END, f"第{self.current_attempt}次: {guess} {symbol}\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)

    def show_win(self):
        self.guess_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)

        if self.current_attempt == 1:
            rating = "🌟 运气爆棚！一次命中！"
        elif self.current_attempt <= 3:
            rating = "💎 高手在民间！"
        elif self.current_attempt <= 5:
            rating = "🎯 不错不错！"
        else:
            rating = "👍 坚持就是胜利！"

        win_text = f"🎉 恭喜过关！\n答案就是 {self.secret_number}\n{rating}"
        self.hint_label.config(text=win_text, fg="#2ECC71")
        self.status_label.config(text="🏆 游戏胜利！")

        messagebox.showinfo("🎉 恭喜！", f"你猜对了！答案是 {self.secret_number}\n用了 {self.current_attempt} 次")

    def show_lose(self):
        self.guess_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)

        lose_text = f"😢 游戏结束！\n答案是 {self.secret_number}\n再接再厉！"
        self.hint_label.config(text=lose_text, fg="#E74C3C")
        self.status_label.config(text="💔 游戏失败")

        messagebox.showinfo("😢 游戏结束", f"很遗憾，答案是 {self.secret_number}\n下次再加油！")

    def restart_game(self):
        self.secret_number = random.randint(1, 100)
        self.current_attempt = 0
        self.guessed = False

        self.guess_button.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.DISABLED)
        self.hint_label.config(text="🤔 等待你的第一次猜测...", fg="#F39C12")
        self.attempts_label.config(text=f"🎯 剩余机会: {self.attempts} 次")
        self.status_label.config(text="🎮 游戏进行中...")
        self.entry.delete(0, tk.END)

        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = GuessNumberGame()
    game.run()
