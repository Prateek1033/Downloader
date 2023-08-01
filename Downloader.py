import tkinter as tk
from tkinter import ttk, filedialog
import requests

class Downloader:
    def __init__(self):
        self.saveto = ""
        self.window = tk.Tk()
        self.window.title("Python GUI Downloader")
        self.url_label = tk.Label(text="Enter URL")
        self.url_label.pack()
        self.url_entry = tk.Entry()
        self.url_entry.pack()
        self.browse_button = tk.Button(text="Browse", command=self.browse_file)
        self.browse_button.pack()
        self.download_button = tk.Button(text="Download", command=self.download)
        self.download_button.pack()
        self.window.geometry("844x344")

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.window, orient="horizontal", maximum=100, length=300, mode="determinate", variable=self.progress_var)
        self.progress_bar.pack()

        # Label to display the percentage
        self.percentage_label = tk.Label(self.window, text="", width=10)
        self.percentage_label.pack()

    def browse_file(self):
        saveto = filedialog.asksaveasfilename(initialfile=self.url_entry.get().split("/")[-1].split("?")[0])
        self.saveto = saveto

    def download(self):
        url = self.url_entry.get()
        response = requests.get(url, stream=True)
        if response.headers.get("content-length"):
            total_size_in_bytes = int(response.headers.get("content-length"))
        
        block_size = 1024 * 1024
        self.progress_var.set(0)

        fileName = self.url_entry.get().split("/")[-1].split("?")[0]
        if not self.saveto:
            self.saveto = fileName
            
        with open(self.saveto, "wb") as f:
            for data in response.iter_content(block_size):
                f.write(data)
                self.progress_bar.step((100 * len(data)) / total_size_in_bytes)
                self.window.update()

                # Update the percentage label with the current progress
                percentage = self.progress_var.get()
                self.percentage_label.config(text=f"{percentage:.2f}%")

        print("Download complete!")

if __name__ == "__main__":
    downloader = Downloader()
    downloader.window.mainloop()