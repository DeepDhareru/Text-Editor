import tkinter as tk
from tkinter import filedialog, messagebox, font
from tkinter.simpledialog import askstring

# Initialize main window
root = tk.Tk()
root.title("Enhanced Text Editor")
root.geometry("800x600")

# Global variables
file_path = None
is_dark_mode = False
font_name = tk.StringVar(value="Helvetica")
font_size = tk.IntVar(value=14)

# Create Text Widget
text_area = tk.Text(root, wrap="word", undo=True, font=(font_name.get(), font_size.get()))
text_area.pack(expand=1, fill="both")

# Function to update font
def update_font(*args):
    text_area.config(font=(font_name.get(), font_size.get()))

font_name.trace("w", update_font)
font_size.trace("w", update_font)

# Function for Dark Mode
def toggle_dark_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    bg_color, fg_color = ("#333333", "#ffffff") if is_dark_mode else ("#ffffff", "#000000")
    text_area.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
    status_bar.config(bg=bg_color, fg=fg_color)

# Functions for File Operations
def new_file():
    global file_path
    file_path = None
    text_area.delete(1.0, tk.END)
    update_status_bar()

def open_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())
            root.title(f"Text Editor - {file_path}")
        update_status_bar()

def save_file():
    global file_path
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))
    else:
        save_as_file()

def save_as_file():
    global file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))
        root.title(f"Text Editor - {file_path}")

# Functions for Edit Operations
def cut_text():
    text_area.event_generate("<<Cut>>")

def copy_text():
    text_area.event_generate("<<Copy>>")

def paste_text():
    text_area.event_generate("<<Paste>>")

# Text Formatting Functions
def toggle_bold():
    current_tags = text_area.tag_names("sel.first")
    if "bold" in current_tags:
        text_area.tag_remove("bold", "sel.first", "sel.last")
    else:
        text_area.tag_add("bold", "sel.first", "sel.last")
    text_area.tag_configure("bold", font=(font_name.get(), font_size.get(), "bold"))

def toggle_italic():
    current_tags = text_area.tag_names("sel.first")
    if "italic" in current_tags:
        text_area.tag_remove("italic", "sel.first", "sel.last")
    else:
        text_area.tag_add("italic", "sel.first", "sel.last")
    text_area.tag_configure("italic", font=(font_name.get(), font_size.get(), "italic"))

def toggle_underline():
    current_tags = text_area.tag_names("sel.first")
    if "underline" in current_tags:
        text_area.tag_remove("underline", "sel.first", "sel.last")
    else:
        text_area.tag_add("underline", "sel.first", "sel.last")
    text_area.tag_configure("underline", font=(font_name.get(), font_size.get(), "underline"))

# Find and Replace Function
def find_and_replace():
    find_text = askstring("Find", "Enter the text to find:")
    replace_text = askstring("Replace", "Enter the text to replace with:")
    content = text_area.get(1.0, tk.END)
    new_content = content.replace(find_text, replace_text)
    text_area.delete(1.0, tk.END)
    text_area.insert(1.0, new_content)

# Word and Character Count
def update_status_bar(event=None):
    text = text_area.get(1.0, tk.END)
    word_count = len(text.split())
    char_count = len(text) - 1  # Exclude the trailing newline character
    status_bar.config(text=f"Words: {word_count}  Characters: {char_count}")

text_area.bind("<KeyRelease>", update_status_bar)

# Creating Menu
menu_bar = tk.Menu(root)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label="Find and Replace", command=find_and_replace)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Format Menu
format_menu = tk.Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Bold", command=toggle_bold)
format_menu.add_command(label="Italic", command=toggle_italic)
format_menu.add_command(label="Underline", command=toggle_underline)
menu_bar.add_cascade(label="Format", menu=format_menu)

# Options Menu
options_menu = tk.Menu(menu_bar, tearoff=0)

# Font Name Menu
font_menu = tk.Menu(options_menu, tearoff=0)
for font_name_option in font.families():
    font_menu.add_radiobutton(label=font_name_option, variable=font_name, value=font_name_option)
options_menu.add_cascade(label="Font", menu=font_menu)

# Font Size Menu
size_menu = tk.Menu(options_menu, tearoff=0)
for size in range(8, 32, 2):
    size_menu.add_radiobutton(label=str(size), variable=font_size, value=size)
options_menu.add_cascade(label="Font Size", menu=size_menu)

# Dark Mode Toggle
options_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)
menu_bar.add_cascade(label="Options", menu=options_menu)

# Adding Shortcuts
root.bind("<Control-n>", lambda e: new_file())
root.bind("<Control-o>", lambda e: open_file())
root.bind("<Control-s>", lambda e: save_file())
root.bind("<Control-Shift-S>", lambda e: save_as_file())
root.bind("<Control-x>", lambda e: cut_text())
root.bind("<Control-c>", lambda e: copy_text())
root.bind("<Control-v>", lambda e: paste_text())

# Configure menu
root.config(menu=menu_bar)

# Status Bar for Word Count
status_bar = tk.Label(root, text="Words: 0  Characters: 0", anchor="e")
status_bar.pack(fill="x", side="bottom")
update_status_bar()

# Start main loop
root.mainloop()
