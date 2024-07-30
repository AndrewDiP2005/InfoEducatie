import tkinter as tk
from tkinter import ttk, messagebox
from game_logic import GameLogic
import random
import math

class WordleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Language Learning App")
        self.center_window()
        self.current_screen = None
        self.dark_mode = False
        self.main_menu()

    def center_window(self):
        self.window_width = 800
        self.window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.window_width // 2)
        y = (screen_height // 2) - (self.window_height // 2)
        self.root.geometry(f'{self.window_width}x{self.window_height}+{x}+{y}')

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = tk.Frame(self.root)
        self.current_screen.pack(fill=tk.BOTH, expand=True)

    def main_menu(self):
        self.clear_screen()
        tk.Label(self.current_screen, text="Wordle Language Learning App", font=("Arial", 24)).pack(pady=20)
        tk.Button(self.current_screen, text="Play", font=("Arial", 16), command=self.setup_game).pack(pady=10)
        tk.Button(self.current_screen, text="Settings", font=("Arial", 16), command=self.settings_menu).pack(pady=10)
        tk.Button(self.current_screen, text="Toggle Dark Mode", font=("Arial", 16), command=self.toggle_dark_mode).pack(pady=10)

    def settings_menu(self):
        self.clear_screen()
        tk.Label(self.current_screen, text="Settings", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.current_screen, text="Select Window Width:", font=("Arial", 16)).pack(pady=10)
        self.width_var = tk.IntVar(value=self.window_width)
        width_combo = ttk.Combobox(self.current_screen, textvariable=self.width_var, font=("Arial", 14))
        width_combo['values'] = (600, 800, 1000, 1200)
        width_combo.pack(pady=10)

        tk.Label(self.current_screen, text="Select Window Height:", font=("Arial", 16)).pack(pady=10)
        self.height_var = tk.IntVar(value=self.window_height)
        height_combo = ttk.Combobox(self.current_screen, textvariable=self.height_var, font=("Arial", 14))
        height_combo['values'] = (400, 600, 800, 1000)
        height_combo.pack(pady=10)

        tk.Button(self.current_screen, text="Save", font=("Arial", 16), command=self.save_settings).pack(pady=20)
        tk.Button(self.current_screen, text="Back", font=("Arial", 16), command=self.main_menu).pack(pady=10)

    def save_settings(self):
        self.window_width = self.width_var.get()
        self.window_height = self.height_var.get()
        self.center_window()
        messagebox.showinfo("Settings Saved", "Window size updated successfully!")

    def setup_game(self):
        self.clear_screen()
        tk.Label(self.current_screen, text="Select Language:", font=("Arial", 16)).pack(pady=10)
        self.language_var = tk.StringVar()
        language_combo = ttk.Combobox(self.current_screen, textvariable=self.language_var, font=("Arial", 14))
        language_combo['values'] = ('English', 'Spanish', 'French')
        language_combo.pack(pady=10)

        tk.Label(self.current_screen, text="Select Word Length:", font=("Arial", 16)).pack(pady=10)
        self.length_var = tk.IntVar()
        length_combo = ttk.Combobox(self.current_screen, textvariable=self.length_var, font=("Arial", 14))
        length_combo['values'] = (4, 5, 6, 7, 8)
        length_combo.pack(pady=10)

        tk.Button(self.current_screen, text="Start Game", font=("Arial", 16), command=self.start_game).pack(pady=20)

    def start_game(self):
        selected_language = self.language_var.get().lower()
        selected_length = self.length_var.get()
        if not selected_language or not selected_length:
            messagebox.showerror("Error", "Please select both a language and a word length.")
            return

        words = GameLogic.load_words(selected_language)
        self.words_list = GameLogic.get_words_by_length(words, selected_length)
        if not self.words_list:
            messagebox.showerror("Error", f"No words of length {selected_length} found in {selected_language}.")
            return

        self.target_word = random.choice(self.words_list)
        print(self.target_word)
        self.target_word_length = selected_length
        self.attempts_left = max(6, math.ceil(selected_length * 1.2))  # At least 6 attempts

        self.create_game_widgets()

    def create_game_widgets(self):
        self.clear_screen()
        tk.Label(self.current_screen, text=f"Guess the {self.target_word_length}-letter word:", font=("Arial", 16)).pack(pady=10)
        
        input_frame = tk.Frame(self.current_screen, padx=10, pady=10)
        input_frame.pack(pady=10)
        input_frame.config(borderwidth=2, relief="solid")

        self.guess_var = tk.StringVar()
        self.guess_entry = tk.Entry(input_frame, textvariable=self.guess_var, font=("Arial", 16))
        self.guess_entry.pack(padx=10, pady=10)
        self.guess_entry.bind("<Return>", self.submit_guess)

        tk.Button(self.current_screen, text="Submit Guess", font=("Arial", 16), command=self.submit_guess).pack(pady=10)
        self.result_label = tk.Label(self.current_screen, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)

        self.definition_label = tk.Label(self.current_screen, text="", font=("Arial", 16), wraplength=600)
        self.definition_label.pack(pady=10)

        self.create_scrollable_grid()

    def create_scrollable_grid(self):
        self.scroll_canvas = tk.Canvas(self.current_screen)
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.current_screen, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.grid_frame = tk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.grid_frame.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))

        self.grid_squares = []
        for row in range(self.attempts_left):
            grid_row = []
            for col in range(self.target_word_length):
                cell = tk.Label(self.grid_frame, text="", font=("Arial", 20), width=2, height=1, borderwidth=2, relief="solid")
                cell.grid(row=row, column=col, padx=2, pady=2)
                grid_row.append(cell)
            self.grid_squares.append(grid_row)

        self.center_grid()

    def center_grid(self):
        self.scroll_canvas.update_idletasks()
        width = self.grid_frame.winfo_width()
        height = self.grid_frame.winfo_height()
        canvas_width = self.scroll_canvas.winfo_width()
        canvas_height = self.scroll_canvas.winfo_height()
        self.scroll_canvas.config(scrollregion=(0, 0, width, height))
        self.scroll_canvas.xview_moveto(0.5 - canvas_width / width / 2)
        self.scroll_canvas.yview_moveto(0.5 - canvas_height / height / 2)

    def submit_guess(self, event=None):
        guess = self.guess_var.get().lower()
        if GameLogic.is_valid_word(guess, self.target_word_length):
            self.update_grid(guess)
            feedback = GameLogic.get_feedback(guess, self.target_word)
            colors = self.color_code(feedback)
            self.animate_letter_colors(colors)
            self.guess_var.set("")
            self.attempts_left -= 1
            definition = GameLogic.fetch_definition(guess)
            self.definition_label.config(text=f"Definition: {definition}")
            if feedback == 'G' * self.target_word_length:
                self.end_game("Congratulations! You've guessed the word!")
            elif self.attempts_left == 0:
                self.end_game(f"Out of attempts! The word was {self.target_word}.")
        else:
            self.result_label.config(text="Invalid word. Ensure it is the correct length and contains no digits.")
            self.clear_current_row()

    def clear_current_row(self):
        row = self.find_empty_row()
        if row is not None:
            for col in range(self.target_word_length):
                if self.grid_squares[row][col] is not None:
                    self.grid_squares[row][col].config(text="")

    def update_grid(self, guess):
        self.current_row = self.find_empty_row()
        if self.current_row is not None:
            for col in range(self.target_word_length):
                if self.grid_squares[self.current_row][col] is not None:
                    self.grid_squares[self.current_row][col].config(text=guess[col])

    def find_empty_row(self):
        for i, row in enumerate(self.grid_squares):
            if row[0] is not None and row[0].cget("text") == "":
                return i
        return None

    def animate_letter_colors(self, colors):
        for col in range(self.target_word_length):
            self.root.after(col * 500, self.color_cell, self.current_row, col, colors[col])

    def color_cell(self, row, col, color):
        if self.grid_squares[row][col] is not None:
            self.grid_squares[row][col].config(bg=color)

    def color_code(self, feedback):
        color_map = {
            'G': 'darkgreen' if self.dark_mode else 'green',
            'Y': 'darkgoldenrod' if self.dark_mode else 'yellow',
            'B': 'darkgray' if self.dark_mode else 'gray'
        }
        return [color_map[char] for char in feedback]

    def end_game(self, message):
        definition = GameLogic.fetch_definition(self.target_word)
        full_message = f"{message}\nDefinition: {definition}"
        messagebox.showinfo("Game Over", full_message)
        self.result_label.config(text=full_message)
        self.guess_entry.config(state='disabled')
        tk.Button(self.current_screen, text="New Game", font=("Arial", 16), command=self.setup_game).pack(pady=10)
        tk.Button(self.current_screen, text="Main Menu", font=("Arial", 16), command=self.main_menu).pack(pady=10)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg_color = 'darkgray' if self.dark_mode else 'white'
        fg_color = 'white' if self.dark_mode else 'black'
        self.root.config(bg=bg_color)
        self.current_screen.config(bg=bg_color)
        for widget in self.current_screen.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                widget.config(bg=bg_color, fg=fg_color)
        if hasattr(self, 'scroll_canvas'):
            self.scroll_canvas.config(bg=bg_color)
            for row in self.grid_squares:
                for cell in row:
                    cell.config(bg=bg_color, fg=fg_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleApp(root)
    root.mainloop()
