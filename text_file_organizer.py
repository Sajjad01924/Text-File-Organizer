import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)
        list_files()

def list_files():
    folder = folder_path.get()
    if not os.path.isdir(folder):
        messagebox.showerror("Error", "Invalid folder path.")
        return
    
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    file_list.delete(*file_list.get_children())
    for file in files:
        full_path = os.path.join(folder, file)
        size = os.path.getsize(full_path)
        modified = os.path.getmtime(full_path)
        file_list.insert("", "end", values=(file, size, modified))

def sort_files(column, reverse):
    files = [(file_list.set(k, column), k) for k in file_list.get_children("")]
    files.sort(reverse=reverse)
    for index, (_, k) in enumerate(files):
        file_list.move(k, "", index)
    file_list.heading(column, command=lambda: sort_files(column, not reverse))

def organize_files():
    folder = folder_path.get()
    if not os.path.isdir(folder):
        messagebox.showerror("Error", "Invalid folder path.")
        return
    
    organized_folder = os.path.join(folder, "Organized")
    os.makedirs(organized_folder, exist_ok=True)
    
    for item in file_list.get_children():
        file_name = file_list.item(item)['values'][0]
        source_path = os.path.join(folder, file_name)
        dest_path = os.path.join(organized_folder, file_name)
        os.rename(source_path, dest_path)
    
    messagebox.showinfo("Success", f"Files organized in {organized_folder}.")
    list_files()

# GUI Setup
root = tk.Tk()
root.title("Text File Organizer")
root.geometry("600x400")

folder_path = tk.StringVar()

# Folder Selection
frame = tk.Frame(root)
frame.pack(pady=10, fill="x")
tk.Label(frame, text="Folder:").pack(side="left", padx=5)
folder_entry = tk.Entry(frame, textvariable=folder_path, width=50)
folder_entry.pack(side="left", padx=5, fill="x", expand=True)
tk.Button(frame, text="Browse", command=browse_folder).pack(side="left", padx=5)

# File List
columns = ("Name", "Size (Bytes)", "Last Modified")
file_list = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    file_list.heading(col, text=col, command=lambda c=col: sort_files(c, False))
    file_list.column(col, width=150, anchor="center")
file_list.pack(fill="both", expand=True, padx=10, pady=10)

# Organize Button
organize_button = tk.Button(root, text="Organize Files", command=organize_files)
organize_button.pack(pady=10)

root.mainloop()
