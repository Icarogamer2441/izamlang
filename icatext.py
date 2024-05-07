import tkinter as tk
from tkinter import filedialog

class IcaTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("icaText - for izamlang")
        self.root.configure(background="black")

        self.text_area = tk.Text(self.root, bg="black", fg="white", insertbackground="white", wrap="word")
        self.text_area.pack(fill="both", expand=True)

        self.root.bind('<Control-o>', self.open_file)
        self.root.bind('<Control-s>', self.save_file)
        self.text_area.bind('<KeyRelease>', self.highlight_keywords)

    def open_file(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Izam files", "*.izam"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, file.read())
                self.highlight_keywords()

    def save_file(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".izam", filetypes=[("Izam files", "*.izam"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get('1.0', tk.END))

    def highlight_keywords(self, event=None):
        keyword_colors = {
            "Output": "orange",
            "PrintMsg": "orange",
            "PrintVar": "orange",
            "Input": "orange",
            "nifs": "blue",
            "uifs": "blue",
            "func": "green",
            "pyfunc": "green",
            "start": "pink",
            "Main": "gray",
            "run": "pink",
            "system": "green",
            "callfunc": "red",
            "callpyfunc": "red",
            ">>": "green",
            "<<": "green",
            "int": "blue",
            "float": "blue",
            "string": "blue",
            "boolean": "blue",
            "endvar": "blue",
            "codend": "orange",
            "unicline": "blue",
            "newline": "blue",
            "import": "yellow",
            "wait": "yellow",
            "File": "orange",
            "Read": "orange",
            "ReadPrint": "orange",
            "Write": "orange",
            "Append": "orange",
            "pyimport": "yellow",
            "repeat": "green",
        }

        self.text_area.tag_remove("keyword", "1.0", tk.END)

        for keyword, color in keyword_colors.items():
            start_index = "1.0"
            while True:
                start_index = self.text_area.search(keyword, start_index, stopindex=tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(keyword)}c"
                self.text_area.tag_add(keyword, start_index, end_index)
                self.text_area.tag_config(keyword, foreground=color)
                start_index = end_index

if __name__ == "__main__":
    root = tk.Tk()
    editor = IcaTextEditor(root)
    root.mainloop()
