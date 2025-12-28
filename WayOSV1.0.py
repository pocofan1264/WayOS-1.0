# WayOS v1.o - Shitty mini-OS made by 2 teenagers with soul and a lot of free time :D
# Made by TheWayOSTeam, hope u enjoy <3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import time
import random
import os
import datetime

# Colors for style
BG_COLOR = "#0d1117"
FG_COLOR = "#c9d1d9"
ACCENT = "#00bfff"
DARK_ACCENT = "#005f99"

# Real filesystem folder
FS_DIR = os.path.expanduser("~/WayOS_Files")
os.makedirs(FS_DIR, exist_ok=True)

class WayOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WayOS v1.0 - Vanilla Cream edition")
        self.root.geometry("1000x700")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(True, True)

        # Top bar
        top_frame = tk.Frame(root, bg=ACCENT, height=60)
        top_frame.pack(fill="x")
        tk.Label(top_frame, text="WayOS v1.0, STABLE.", 
                 fg="white", bg=ACCENT, font=("Arial", 16, "bold")).pack(pady=15)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.configure("Custom.TNotebook.Tab", background=DARK_ACCENT, foreground="white")
        style.map("Custom.TNotebook.Tab", background=[("selected", ACCENT)], foreground=[("selected", "white")])

        # Terminal tab with input
        terminal_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(terminal_tab, text="Terminal")

        self.terminal_text = scrolledtext.ScrolledText(terminal_tab, bg="#000000", fg=FG_COLOR, font=("Courier", 12), insertbackground="white")
        self.terminal_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.terminal_text.tag_config("green", foreground="#98c379")
        self.terminal_text.tag_config("red", foreground="#e06c75")
        self.terminal_text.tag_config("yellow", foreground="#e5c07b")
        self.terminal_text.tag_config("blue", foreground="#61afef")
        self.terminal_text.tag_config("cyan", foreground="#56b6c2")
        self.terminal_text.tag_config("purple", foreground="#c678dd")

        cmd_frame = tk.Frame(terminal_tab, bg=BG_COLOR)
        cmd_frame.pack(fill="x", pady=5)
        self.cmd_entry = tk.Entry(cmd_frame, bg="#000000", fg=FG_COLOR, font=("Courier", 12), insertbackground="white")
        self.cmd_entry.pack(fill="x", padx=10)
        self.cmd_entry.bind("<Return>", self.handle_cmd)

        # Booting up text
        self.log("WayOS Vanilla Cream edition booting up... Welcome to visual chaos!", "purple")

        # Nautilus Light tab
        nautilus_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(nautilus_tab, text="Nautilus Light")

        self.file_list = tk.Listbox(nautilus_tab, bg="#000000", fg=FG_COLOR, font=("Courier", 12), selectbackground=ACCENT)
        self.file_list.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(nautilus_tab, bg=BG_COLOR)
        btn_frame.pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Create File", command=self.create_file, bg=ACCENT, fg="white", width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_file, bg="#e06c75", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Open/Edit", command=self.edit_file, bg="#98c379", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.update_file_list, bg="#61afef", fg="white", width=15).pack(side="left", padx=5)

        self.update_file_list()

        # Shitty Games tab
        games_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(games_tab, text="Shitty Games")

        tk.Label(games_tab, text="Simple games to kill time", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 16, "bold")).pack(pady=20)

        for text, cmd in [
            ("Snake", self.start_snake),
            ("Guess the Number", self.start_guess_game),
            ("Basic Calculator", self.start_calc),
            ("Pong", self.start_pong),
            ("Tic-Tac-Toe", self.start_tictactoe),
            ("Memory Match", self.start_memory)
        ]:
            tk.Button(games_tab, text=text, command=cmd, bg=ACCENT, fg="white", width=25, height=2).pack(pady=10)

        # MOTD at startup
        self.handle_motd()

    def log(self, message, color="green"):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.terminal_text.insert(tk.END, f"[{timestamp}] {message}\n", color)
        self.terminal_text.see(tk.END)

    def handle_cmd(self, event):
        cmd = self.cmd_entry.get().strip()
        if cmd:
            self.log(f"> {cmd}", "yellow")
            self.cmd_entry.delete(0, tk.END)
            if cmd == "help":
                help_text = "Commands:\nhelp - this list\nmotd - message of the day\njoke - random joke\ninsult - random insult\nclear - clear screen\nshutdown - quit"
                self.log(help_text, "cyan")
            elif cmd == "motd":
                self.handle_motd()
            elif cmd == "joke":
                jokes = ["Why do programmers prefer dark mode? Because light attracts bugs!", "My code is so bad, even Python is ashamed"]
                self.log(random.choice(jokes), "yellow")
            elif cmd == "insult":
                insults = ["Your code is so slow, it's got a speed ticket from a snail", "You're so lazy, your laziness has laziness"]
                self.log(random.choice(insults), "red")
            elif cmd == "clear":
                self.terminal_text.delete("1.0", tk.END)
            elif cmd == "shutdown":
                self.root.quit()
            else:
                self.log(f"Command '{cmd}' not found. Type 'help'", "red")
        self.terminal_text.see(tk.END)

    def handle_motd(self):
        motds = ["Today is a good day to code something shitty!", "Remember: Code lost is code that never existed..."]
        self.log(random.choice(motds), "purple")

    def update_file_list(self):
        self.file_list.delete(0, tk.END)
        try:
            files = os.listdir(FS_DIR)
            if not files:
                self.file_list.insert(tk.END, "Folder empty... create something, bro :D")
            else:
                for f in sorted(files):
                    size = os.path.getsize(os.path.join(FS_DIR, f))
                    self.file_list.insert(tk.END, f"{f} ({size} bytes)")
        except Exception as e:
            self.log(f"Error reading folder: {e}", "red")

    def create_file(self):
        name = filedialog.asksaveasfilename(initialdir=FS_DIR, defaultextension=".txt")
        if name:
            try:
                open(name, 'w').close()
                self.log(f"File created: {os.path.basename(name)}", "green")
                self.update_file_list()
            except Exception as e:
                self.log(f"Error creating file: {e}", "red")

    def delete_file(self):
        sel = self.file_list.curselection()
        if not sel:
            messagebox.showwarning("Nothing selected", "Select a file first")
            return
        filename = self.file_list.get(sel[0]).split(" (")[0]
        path = os.path.join(FS_DIR, filename)
        if messagebox.askyesno("Delete", f"Delete {filename}? (no recycle bin)"):
            try:
                os.remove(path)
                self.log(f"File deleted: {filename} 💔", "red")
                self.update_file_list()
            except Exception as e:
                self.log(f"Error deleting: {e}", "red")

    def edit_file(self):
        sel = self.file_list.curselection()
        if not sel:
            messagebox.showwarning("Nothing selected", "Select a file first")
            return
        filename = self.file_list.get(sel[0]).split(" (")[0]
        path = os.path.join(FS_DIR, filename)
        try:
            with open(path, 'r') as f:
                content = f.read()
            edit_win = tk.Toplevel(self.root)
            edit_win.title(f"Editing {filename}")
            edit_win.geometry("600x400")
            text = scrolledtext.ScrolledText(edit_win, bg="#000000", fg=FG_COLOR, font=("Courier", 12))
            text.pack(fill="both", expand=True)
            text.insert(tk.END, content)
            tk.Button(edit_win, text="Save Changes", command=lambda: self.save_edit(path, text.get("1.0", tk.END), edit_win)).pack(pady=5)
        except Exception as e:
            self.log(f"Error opening file: {e}", "red")

    def save_edit(self, path, content, window):
        try:
            with open(path, 'w') as f:
                f.write(content)
            self.log(f"File saved: {os.path.basename(path)}", "green")
            window.destroy()
            self.update_file_list()
        except Exception as e:
            self.log(f"Error saving: {e}", "red")

    # Snake
    def start_snake(self):
        snake_win = tk.Toplevel(self.root)
        snake_win.title("Snake - WayOS Edition")
        snake_win.geometry("450x500")

        canvas = tk.Canvas(snake_win, width=400, height=400, bg="black")
        canvas.pack(pady=10)

        score_label = tk.Label(snake_win, text="Score: 0", font=("Arial", 14), bg=BG_COLOR, fg=FG_COLOR)
        score_label.pack()

        snake = [(200, 200), (190, 200), (180, 200)]
        direction = "Right"
        score = 0
        game_over = False

        food = random.randint(0, 39) * 10, random.randint(0, 39) * 10
        canvas.create_oval(food[0], food[1], food[0]+10, food[1]+10, fill="red", tags="food")

        # Initial snake
        for segment in snake:
            canvas.create_rectangle(segment[0], segment[1], segment[0]+10, segment[1]+10, fill="green", tags="snake")

        def move_snake():
            nonlocal direction, score, game_over, food
            if game_over:
                return

            head = snake[0]
            if direction == "Right":
                new_head = (head[0] + 10, head[1])
            elif direction == "Left":
                new_head = (head[0] - 10, head[1])
            elif direction == "Up":
                new_head = (head[0], head[1] - 10)
            elif direction == "Down":
                new_head = (head[0], head[1] + 10)

            if new_head in snake or not (0 <= new_head[0] < 400 and 0 <= new_head[1] < 400):
                game_over = True
                messagebox.showinfo("Game Over", f"Final score: {score}")
                snake_win.destroy()
                return

            snake.insert(0, new_head)

            if new_head == food:
                score += 1
                score_label.config(text=f"Score: {score}")
                canvas.delete("food")
                food = random.randint(0, 39) * 10, random.randint(0, 39) * 10
                canvas.create_oval(food[0], food[1], food[0]+10, food[1]+10, fill="red", tags="food")
            else:
                tail = snake.pop()
                canvas.delete("snake_tail")

            canvas.create_rectangle(new_head[0], new_head[1], new_head[0]+10, new_head[1]+10, fill="green", tags="snake")

            snake_win.after(100, move_snake)

        def change_direction(event):
            nonlocal direction
            if event.keysym == "Right" and direction != "Left":
                direction = "Right"
            elif event.keysym == "Left" and direction != "Right":
                direction = "Left"
            elif event.keysym == "Up" and direction != "Down":
                direction = "Up"
            elif event.keysym == "Down" and direction != "Up":
                direction = "Down"

        snake_win.bind("<Key>", change_direction)
        snake_win.focus_set()
        move_snake()

    # Guess the Number
    def start_guess_game(self):
        guess_win = tk.Toplevel(self.root)
        guess_win.title("Guess the Number")
        guess_win.geometry("400x300")

        number = random.randint(1, 100)
        attempts = 0

        tk.Label(guess_win, text="Guess a number between 1 and 100", font=("Arial", 14)).pack(pady=20)

        entry = tk.Entry(guess_win, font=("Arial", 12))
        entry.pack(pady=10)

        result_label = tk.Label(guess_win, text="", font=("Arial", 12))
        result_label.pack(pady=10)

        def check_guess():
            nonlocal attempts
            try:
                guess = int(entry.get())
                attempts += 1
                if guess < number:
                    result_label.config(text="Too low!", fg="blue")
                elif guess > number:
                    result_label.config(text="Too high!", fg="red")
                else:
                    result_label.config(text=f"You got it in {attempts} tries!", fg="green")
                    messagebox.showinfo("You Win", f"You got it in {attempts} tries!")
                    guess_win.destroy()
            except ValueError:
                result_label.config(text="Enter a valid number!", fg="orange")

        tk.Button(guess_win, text="Guess", command=check_guess, bg=ACCENT, fg="white").pack(pady=10)

    # Basic Calculator
    def start_calc(self):
        calc_win = tk.Toplevel(self.root)
        calc_win.title("Basic Calculator")
        calc_win.geometry("300x400")

        entry = tk.Entry(calc_win, font=("Arial", 18), justify="right")
        entry.pack(fill="x", padx=10, pady=10)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0)
        ]

        for (text, row, col) in buttons:
            cmd = lambda x=text: self.calc_click(entry, x)
            tk.Button(calc_win, text=text, font=("Arial", 14), width=5, height=2, command=cmd).grid(row=row, column=col, padx=5, pady=5)

    def calc_click(self, entry, value):
        if value == 'C':
            entry.delete(0, tk.END)
        elif value == '=':
            try:
                result = eval(entry.get())
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error")
        else:
            entry.insert(tk.END, value)

    # Pong
    def start_pong(self):
        pong_win = tk.Toplevel(self.root)
        pong_win.title("Pong - WayOS Edition")
        pong_win.geometry("600x500")

        canvas = tk.Canvas(pong_win, width=600, height=400, bg="black")
        canvas.pack(pady=10)

        paddle = canvas.create_rectangle(280, 380, 320, 390, fill="white")

        ball = canvas.create_oval(295, 195, 305, 205, fill="white")
        ball_speed = [5, -5]

        def move_ball():
            canvas.move(ball, ball_speed[0], ball_speed[1])
            x1, y1, x2, y2 = canvas.coords(ball)
            if x1 <= 0 or x2 >= 600:
                ball_speed[0] = -ball_speed[0]
            if y1 <= 0:
                ball_speed[1] = -ball_speed[1]
            if y2 >= 400:
                messagebox.showinfo("Game Over", "Ball lost!")
                pong_win.destroy()
                return
            if canvas.coords(paddle)[1] <= y2 <= canvas.coords(paddle)[3] and canvas.coords(paddle)[0] <= x1 <= canvas.coords(paddle)[2]:
                ball_speed[1] = -ball_speed[1]
            pong_win.after(20, move_ball)

        def move_paddle(event):
            x = event.x
            canvas.coords(paddle, x-40, 380, x+40, 390)

        pong_win.bind("<Motion>", move_paddle)
        move_ball()

    # Tic-Tac-Toe
    def start_tictactoe(self):
        ttt_win = tk.Toplevel(self.root)
        ttt_win.title("Tic-Tac-Toe")
        ttt_win.geometry("300x350")

        board = [[" " for _ in range(3)] for _ in range(3)]
        player = "X"

        def click(row, col):
            nonlocal player
            if board[row][col] == " ":
                board[row][col] = player
                buttons[row][col].config(text=player)
                if self.check_win(board, player):
                    messagebox.showinfo("Winner!", f"{player} wins!")
                    ttt_win.destroy()
                elif all(cell != " " for row in board for cell in row):
                    messagebox.showinfo("Tie", "It's a tie!")
                    ttt_win.destroy()
                else:
                    player = "O" if player == "X" else "X"

        buttons = []
        for row in range(3):
            row_buttons = []
            for col in range(3):
                btn = tk.Button(ttt_win, text=" ", font=("Arial", 40), width=5, height=2, command=lambda r=row, c=col: click(r, c))
                btn.grid(row=row, column=col)
                row_buttons.append(btn)
            buttons.append(row_buttons)

    def check_win(self, board, player):
        # Rows
        for row in board:
            if all(cell == player for cell in row):
                return True
        # Columns
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        # Diagonals
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return True
        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            return True
        return False

    # Memory Match
    def start_memory(self):
        memory_win = tk.Toplevel(self.root)
        memory_win.title("Memory Match")
        memory_win.geometry("400x400")

        cards = list(range(8)) * 2
        random.shuffle(cards)
        buttons = []
        flipped = []

        def flip(btn, idx):
            if len(flipped) == 2 or btn["text"] != "?":
                return
            btn["text"] = cards[idx]
            flipped.append((btn, cards[idx]))
            if len(flipped) == 2:
                if flipped[0][1] == flipped[1][1]:
                    flipped.clear()
                else:
                    memory_win.after(1000, lambda: [b.config(text="?") for b, _ in flipped])
                    flipped.clear()

        for i in range(16):
            btn = tk.Button(memory_win, text="?", font=("Arial", 30), width=5, height=2, command=lambda idx=i: flip(btn, idx))
            btn.grid(row=i//4, column=i%4)
            buttons.append(btn)

if __name__ == "__main__":
    root = tk.Tk()
    app = WayOSApp(root)
    root.mainloop()