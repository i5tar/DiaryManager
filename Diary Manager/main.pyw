import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Directory to store the entries
script_path = os.path.dirname(os.path.abspath(__file__))
directory = os.path.join(script_path, "entries")

# Function to save an entry to a file
def save_entry(title, content):
    with open(os.path.join(directory, title + ".txt"), "w") as file:
        file.write(content)

# Function to create a new entry
def create_entry():
    title = title_entry.get()
    content = content_text.get("1.0", tk.END)
    if title and content.strip():
        save_entry(title, content)
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)
        update_listbox()
    else:
        messagebox.showwarning("Missing Data", "Title and content are required.")

# Function to read an entry
def read_entry(event=None):
    title = listbox.get(tk.ACTIVE)
    if title:
        with open(os.path.join(directory, title + ".txt"), "r") as file:
            content = file.read()
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)
        title_entry.insert(0, title)
        content_text.insert(tk.INSERT, content)

# Function to delete an entry
def delete_entry():
    title = listbox.get(tk.ACTIVE)
    if title:
        os.remove(os.path.join(directory, title + ".txt"))
        update_listbox()

# Function to update listbox
def update_listbox():
    listbox.delete(0, tk.END)
    for filename in os.listdir(directory):
        title, _ = os.path.splitext(filename)
        listbox.insert(tk.END, title)

# Check if the directory exists, if not, create it
if not os.path.exists(directory):
    os.makedirs(directory)

root = tk.Tk()
root.title("Diary Manager")
root.geometry("800x600")

style = ttk.Style(root)
style.theme_use("clam")

canvas = tk.Canvas(root, bd=0, highlightthickness=0)
canvas.grid(sticky=tk.NSEW, row=0, rowspan=6, column=0, columnspan=3)

grey_color = "#999999"  # Grey color
canvas.create_rectangle(0, 0, 8000, 6000, fill=grey_color, tags=("bg",))

# Entry styling with grey color
style.configure("TEntry", background="#323232", foreground="#FFFFFF", fieldbackground="#323232", font=('Arial', 12))

# Button styling with grey color
style.configure("TButton", background="#323232", foreground="#FFFFFF", borderwidth=0, padding=10)
style.map("TButton", background=[("active", "#CCCCCC")])

# Grid configuration
for i in range(3):
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(5, weight=1)

# Title label and entry
title_label = ttk.Label(root, text="Title:", font=('Arial', 14, 'bold'), background=grey_color)
title_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="nw")
title_entry = ttk.Entry(root, font=('Arial', 12))
title_entry.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="ew")

# Content label and text widget
content_label = ttk.Label(root, text="Content:", font=('Arial', 14, 'bold'), background=grey_color)
content_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="nw")
content_text = tk.Text(root, height=10, width=40, wrap=tk.WORD, bg="#323232", fg="#FFFFFF", insertbackground="#FFFFFF", font=('Arial', 12), padx=10, pady=10)
content_text.grid(row=3, column=0, padx=5, pady=5, columnspan=3, sticky="nsew")

create_button = ttk.Button(root, text="Create Entry", command=create_entry)
create_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
read_button = ttk.Button(root, text="Read Entry", command=read_entry)
read_button.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
delete_button = ttk.Button(root, text="Delete Entry", command=delete_entry)
delete_button.grid(row=4, column=2, padx=5, pady=5, sticky="ew")

listbox = tk.Listbox(root, bg="#323232", fg="#FFFFFF", selectbackground="#CCCCCC", selectforeground="#000000")
listbox.grid(row=5, column=0, padx=5, pady=5, columnspan=3, sticky="nsew")
listbox.bind("<Double-Button-1>", read_entry)

update_listbox()

root.mainloop()
