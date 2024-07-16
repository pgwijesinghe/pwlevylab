import os
import glob
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class FileNavigator(tk.Tk):
    def __init__(self, input_folder):
        super().__init__()
        self.input_folder = input_folder
        self.files = sorted(glob.glob(os.path.join(input_folder, '*.txt')))
        self.file_index = 0
        
        if not self.files:
            print(f"No files found in directory: {input_folder}")
            self.destroy()
            return
        
        self.title("File Navigator")
        self.geometry("800x700")
        
        self.create_widgets()
        self.plot_file(self.files[self.file_index])
        
    def create_widgets(self):
        self.label = ttk.Label(self, text="File:")
        self.label.pack(pady=10)
        
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)
        
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(pady=10)
        
        self.prev_button = ttk.Button(self.control_frame, text="Previous", command=self.prev_file)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        self.next_button = ttk.Button(self.control_frame, text="Next", command=self.next_file)
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        self.slider = ttk.Scale(self.control_frame, from_=0, to=len(self.files)-1, orient=tk.HORIZONTAL, command=self.slider_moved)
        self.slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.file_entry = ttk.Entry(self.control_frame, width=5)
        self.file_entry.pack(side=tk.LEFT, padx=5)
        
        self.go_button = ttk.Button(self.control_frame, text="Go", command=self.go_to_file)
        self.go_button.pack(side=tk.LEFT, padx=5)
        
    def plot_file(self, file_path):
        self.label.config(text=f"File: {os.path.basename(file_path)}")
        
        try:
            data = pd.read_csv(file_path, header=None, names=['Wavelength', 'Intensity'])
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return
        
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        
        ax.plot(data['Wavelength'].values, data['Intensity'].values)
        ax.set_xlabel('Wavelength')
        ax.set_ylabel('Summed Intensity')
        ax.set_title('Wavelength vs Summed Intensity')
        
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def prev_file(self):
        if self.file_index > 0:
            self.file_index -= 1
            self.plot_file(self.files[self.file_index])
            self.update_slider_and_entry()
    
    def next_file(self):
        if self.file_index < len(self.files) - 1:
            self.file_index += 1
            self.plot_file(self.files[self.file_index])
            self.update_slider_and_entry()
    
    def slider_moved(self, event):
        self.file_index = int(self.slider.get())
        self.plot_file(self.files[self.file_index])
        self.update_entry()
    
    def go_to_file(self):
        try:
            file_index = int(self.file_entry.get())
            if 0 <= file_index < len(self.files):
                self.file_index = file_index
                self.plot_file(self.files[self.file_index])
                self.update_slider()
            else:
                print("Invalid file index.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def update_slider_and_entry(self):
        self.slider.set(self.file_index)
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, str(self.file_index))
    
    def update_slider(self):
        self.slider.set(self.file_index)
    
    def update_entry(self):
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, str(self.file_index))

def main():
    input_folder = r"C:\Users\Pubudu Wijesinghe\Desktop\output"
    app = FileNavigator(input_folder)
    app.mainloop()

if __name__ == "__main__":
    main()
