import tkinter as tk
import math

# Main window
root = tk.Tk()
root.title("Advanced Calculator")
root.geometry("390x420")
root.resizable(False, False)

# Themes
light_theme = {"bg": "#2c3e50", "fg": "#000000", "btn": "#e0e0e0"}
dark_theme = {"bg": "#2e2e2e", "fg": "#ffffff", "btn": "#444"}

current_theme = light_theme

# Expression storage
expression = ""

# Entry field
entry = tk.Entry(root, font=("Arial", 20), borderwidth=4, relief="solid", justify="right")
entry.pack(pady=15, ipady=10, fill="x", padx=10)

# Change theme
def toggle_theme():
    global current_theme
    current_theme = dark_theme if current_theme == light_theme else light_theme
    apply_theme()

def apply_theme():
    root.config(bg=current_theme["bg"])
    entry.config(bg=current_theme["bg"], fg=current_theme["fg"])
    for button in buttons.values():
        button.config(bg=current_theme["btn"], fg=current_theme["fg"])

# Handle button press
def button_click(value):
    global expression
    expression += str(value)
    entry.delete(0, tk.END)
    entry.insert(tk.END, expression)

def clear():
    global expression
    expression = ""
    entry.delete(0, tk.END)

def evaluate():
    global expression
    try:
        # Replace special symbols with math equivalents
        expr = expression.replace('π', str(math.pi)).replace('^', '**')
        #Auto-wrap sqrt argument
        while '√' in expr:
            idx = expr.index('√')
            #Get number after √
            num = ''
            i = idx + 1
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            if num :
                expr = expr.replace(f'√{num}', f'math.sqrt({num})')
            else:
                expr = expr.replace('√','math.sqrt')
        expr = expr.replace('sin', 'math.sin')
        expr = expr.replace('cos', 'math.cos')
        expr = expr.replace('tan', 'math.tan')
        expr = expr.replace('log', 'math.log10')
        result = eval(expr)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        expression = str(result)
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")
        expression = ""

# Button layout
buttons = {}

button_texts = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "π", "+"],
    ["C", "^", "√", "="],
    ["sin", "cos", "tan", "log"],
    ["Theme"]
]

button_frame = tk.Frame(root)
button_frame.pack()

for r, row in enumerate(button_texts):
    for c, char in enumerate(row):
        if char == "Theme":
            btn = tk.Button(button_frame, text="Switch Theme", font=("Arial", 10),
                            width=35, height=1, command=toggle_theme)
            btn.grid(row=r, column=0, columnspan=4, pady=6)
            buttons[char] = btn
        else:
            btn = tk.Button(button_frame, text=char, font=("Arial", 14),
                            width=7, height=1,
                            command=lambda ch=char: evaluate() if ch == "=" else clear() if ch == "C" else button_click(ch))
            btn.grid(row=r, column=c, padx=2, pady=2)
            buttons[char] = btn

apply_theme()

# Launch app
root.mainloop()
