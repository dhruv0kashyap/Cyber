import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, VERTICAL, RIGHT, Y
from tkinter.ttk import Progressbar
import os
import time  # Import the time module

class VirusScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virus Scanner")
        self.root.geometry("800x600")
        self.root.config(bg="#2c3e50")
        
        self.loading_text = None
        self.loading = False
        
        self.create_widgets()

    def create_widgets(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg="#34495e", width=200, height=600)
        self.sidebar.pack(side="left", fill="y")

        self.logo_label = tk.Label(self.sidebar, text="Virus Scanner", font=("Arial", 18, "bold"), bg="#34495e", fg="white")
        self.logo_label.pack(pady=20)

        self.scan_button = tk.Button(self.sidebar, text="Scan Directory", command=self.directory_open, bg="#2980b9", fg="white", activebackground="#1abc9c", activeforeground="white", font=("Arial", 14, "bold"), relief="flat")
        self.scan_button.pack(pady=10, padx=20, fill="x")
        
        self.progress_label = tk.Label(self.sidebar, text="Scan Progress", font=("Arial", 12), bg="#34495e", fg="white")
        self.progress_label.pack(pady=10)
        
        self.progress_bar = Progressbar(self.sidebar, orient="horizontal", length=180, mode="determinate")
        self.progress_bar.pack(pady=10, padx=20)

        # Main area
        self.main_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.text_frame = tk.Frame(self.main_frame, bg="#ecf0f1")
        self.text_frame.pack(pady=20)

        self.scrollbar = Scrollbar(self.text_frame, orient=VERTICAL)
        self.text_area = Text(self.text_frame, height=25, width=80, yscrollcommand=self.scrollbar.set, wrap="none", bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12))
        self.scrollbar.config(command=self.text_area.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text_area.pack(padx=10, pady=10)

        # Configure tags for colored text
        self.text_area.tag_config("virus_found", foreground="red")
        self.text_area.tag_config("no_virus_found", foreground="green")

    def directory_open(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.loading = True
            self.loading_text = tk.Label(self.main_frame, text="Scanning, please wait...", font=("Arial", 14), bg="#ecf0f1", fg="#2c3e50")
            self.loading_text.pack(pady=10)
            self.root.after(100, self.animate_loading)
            self.root.after(500, lambda: self.scan_directory(directory_path))
        
    def animate_loading(self):
        if self.loading:
            current_text = self.loading_text.cget("text")
            if current_text.endswith("..."):
                new_text = "Scanning, please wait"
            else:
                new_text = current_text + "."
            self.loading_text.config(text=new_text)
            self.root.after(500, self.animate_loading)
        
    def scan_directory(self, directory_path):
        self.progress_bar["value"] = 0
        self.text_area.delete(1.0, tk.END)
        total_files = sum(len(files) for _, _, files in os.walk(directory_path))
        scanned_files = 0
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.scan_file(file_path)
                scanned_files += 1
                self.update_progress(scanned_files, total_files)
        
        self.loading = False
        self.loading_text.destroy()
    
    def scan_file(self, file_path):
        time.sleep(3)  # Add delay of 3 seconds
        with open(file_path, "rb") as f:
            file_content = f.read()
            virus_signature = b"X0/2132fkiubwjn9we8phffjffiywhnwo;inv0w8hgfnwekp"
            if virus_signature in file_content:
                self.display_result(f"Virus found in file: {file_path}\n", "virus_found")
            else:
                self.display_result(f"No virus found in file: {file_path}\n", "no_virus_found")
    
    def update_progress(self, scanned_files, total_files):
        progress = (scanned_files / total_files) * 100
        self.progress_bar["value"] = progress
        self.root.update_idletasks()
    
    def display_result(self, result, tag):
        self.text_area.insert(tk.END, result, tag)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirusScannerApp(root)
    root.mainloop()
