import random
import tkinter as tk

# 颜色配置：背景色, 文字色
COLORS = {
    0:    ("#cdc1b4", "#cdc1b4"),
    2:    ("#eee4da", "#776e65"),
    4:    ("#ede0c8", "#776e65"),
    8:    ("#f2b179", "#f9f6f2"),
    16:   ("#f59563", "#f9f6f2"),
    32:   ("#f67c5f", "#f9f6f2"),
    64:   ("#f65e3b", "#f9f6f2"),
    128:  ("#edcf72", "#f9f6f2"),
    256:  ("#edcc61", "#f9f6f2"),
    512:  ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}

CELL_SIZE = 120    # 每个格子的大小（像素）
GAP = 10           # 格子之间的间距
MARGIN = 15        # 棋盘边缘留白
BOARD_SIZE = CELL_SIZE * 4 + GAP * 5 + MARGIN * 2  # 棋盘总尺寸


def move_left(row):
    new = [i for i in row if i != 0]
    for i in range(len(new) - 1):
        if new[i] == new[i + 1]:
            new[i] *= 2
            new[i + 1] = 0
    new = [i for i in new if i != 0]
    while len(new) < 4:
        new.append(0)
    return new


class Game2048:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.best = 0
        self.game_over = False
        self.won = False
        self.spawn_num = 2

        self.root = tk.Tk()
        self.root.title("2048")
        self.root.resizable(False, False)
        self.root.configure(bg="#faf8ef")

        self.canvas = tk.Canvas(
            self.root, width=BOARD_SIZE, height=BOARD_SIZE + 60,
            bg="#faf8ef", highlightthickness=0
        )
        self.canvas.pack()

        self.root.bind("<Key>", self.on_key)

        self.spawn()
        self.spawn()
        self.draw()

    def spawn(self):
        # 生成数字为棋盘最大数字/4，最小为2
        max_val = max(val for row in self.board for val in row)
        self.spawn_num = max(max_val // 4, 2)
        empty = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty:
            x, y = random.choice(empty)
            self.board[x][y] = self.spawn_num

    def move(self, direction):
        old = [r.copy() for r in self.board]

        if direction == "left":
            for i in range(4):
                self.board[i] = move_left(self.board[i])
        elif direction == "right":
            for i in range(4):
                self.board[i] = move_left(self.board[i][::-1])[::-1]
        elif direction == "up":
            for j in range(4):
                col = [self.board[i][j] for i in range(4)]
                new_col = move_left(col)
                for i in range(4):
                    self.board[i][j] = new_col[i]
        elif direction == "down":
            for j in range(4):
                col = [self.board[i][j] for i in range(4)][::-1]
                new_col = move_left(col)[::-1]
                for i in range(4):
                    self.board[i][j] = new_col[i]

        if self.board != old:
            # 计算得分：合并产生的分数
            for i in range(4):
                for j in range(4):
                    if self.board[i][j] != old[i][j] and self.board[i][j] != 0:
                        self.score += self.board[i][j]
            self.spawn()
            self.check_state()

    def check_state(self):
        for row in self.board:
            if 128 in row and not self.won:
                self.won = True

        for row in self.board:
            if 0 in row:
                return
        for i in range(4):
            for j in range(3):
                if self.board[i][j] == self.board[i][j + 1]:
                    return
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == self.board[i + 1][j]:
                    return
        self.game_over = True

    def on_key(self, event):
        key_map = {
            "w": "up", "W": "up", "Up": "up",
            "s": "down", "S": "down", "Down": "down",
            "a": "left", "A": "left", "Left": "left",
            "d": "right", "D": "right", "Right": "right",
        }
        key = event.keysym
        if key in ("q", "Q"):
            self.root.destroy()
            return
        if key in ("r", "R"):
            self.restart()
            return
        if key == "space":
            self.clear_small()
            return
        if key in key_map and not self.game_over:
            self.move(key_map[key])
            self.draw()

    def clear_small(self):
        """清除所有低于生成数字的格子"""
        changed = False
        for i in range(4):
            for j in range(4):
                if 0 < self.board[i][j] < self.spawn_num:
                    self.board[i][j] = 0
                    changed = True
        if changed:
            self.check_state()
            self.draw()

    def restart(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.spawn()
        self.spawn()
        self.draw()

    def draw(self):
        self.canvas.delete("all")

        # 标题和分数
        self.canvas.create_text(
            MARGIN, MARGIN, anchor="nw", text="2048",
            font=("Helvetica", 36, "bold"), fill="#776e65"
        )
        self.canvas.create_text(
            BOARD_SIZE - MARGIN, MARGIN, anchor="ne",
            text=f"分数: {self.score}",
            font=("Helvetica", 18, "bold"), fill="#776e65"
        )
        if self.best < self.score:
            self.best = self.score
        self.canvas.create_text(
            BOARD_SIZE - MARGIN, MARGIN + 30, anchor="ne",
            text=f"最高: {self.best}",
            font=("Helvetica", 12), fill="#776e65"
        )

        # 棋盘背景
        board_top = 60
        self.canvas.create_rectangle(
            MARGIN, board_top, BOARD_SIZE - MARGIN, board_top + CELL_SIZE * 4 + GAP * 5,
            fill="#bbada0", outline="#bbada0", width=0
        )

        # 格子
        for i in range(4):
            for j in range(4):
                val = self.board[i][j]
                bg, fg = COLORS.get(val, ("#3c3a32", "#f9f6f2"))
                x1 = MARGIN + GAP + j * (CELL_SIZE + GAP)
                y1 = board_top + GAP + i * (CELL_SIZE + GAP)
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=bg, outline=bg, width=0
                )
                if val:
                    font_size = 36 if val < 100 else (28 if val < 1000 else 22)
                    self.canvas.create_text(
                        (x1 + x2) / 2, (y1 + y2) / 2,
                        text=str(val), fill=fg,
                        font=("Helvetica", font_size, "bold")
                    )

        # 提示文字
        hint_y = board_top + CELL_SIZE * 4 + GAP * 5 + 15
        hint = f"R 重新开始  Q 退出  空格清除<{self.spawn_num}的格子"
        self.canvas.create_text(
            BOARD_SIZE // 2, hint_y, text=hint,
            font=("Helvetica", 11), fill="#776e65"
        )

        # 游戏结束 / 胜利遮罩
        if self.game_over:
            self.canvas.create_rectangle(
                MARGIN, board_top, BOARD_SIZE - MARGIN, board_top + CELL_SIZE * 4 + GAP * 5,
                fill="#eee4da", stipple="gray50"
            )
            self.canvas.create_text(
                BOARD_SIZE // 2, board_top + (CELL_SIZE * 4 + GAP * 5) // 2,
                text="游戏结束!", fill="#776e65",
                font=("Helvetica", 48, "bold")
            )
        elif self.won:
            self.canvas.create_text(
                BOARD_SIZE // 2, board_top + (CELL_SIZE * 4 + GAP * 5) // 2,
                text="恭喜! 128!", fill="#f9f6f2",
                font=("Helvetica", 40, "bold")
            )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Game2048().run()
