import os
import pypdf
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import time
import uuid
import threading


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("PDF Splitter")
        self.geometry("400x200")

        self.folder_path = None

        self.select_folder_button = ttk.Button(self, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(pady=10)

        self.status = tk.StringVar()
        self.status_label = ttk.Label(self, textvariable=self.status)
        self.status_label.pack(pady=10)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.status.set(f"Selected Folder: {self.folder_path}")
        self.detect_pdf_files()

    def detect_pdf_files(self):
        if self.folder_path is None:
            messagebox.showerror("Error", "Please select a folder first.")
            return

        while True:
            for filename in os.listdir(self.folder_path):
                if not filename.endswith('_done.pdf') and filename.endswith('.pdf'):
                    self.split_pdf_file(os.path.join(self.folder_path, filename))
            time.sleep(1)

    def get_filename_from_path(file_path):
        return os.path.basename(file_path)

    def split_pdf_file(self, pdf_file_path):
        file_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
        print(f"Splitting {file_name}")
        pdf = pypdf.PdfReader(pdf_file_path)
        for page in range(len(pdf.pages)):
            pdf_writer = pypdf.PdfWriter()
            pdf_writer.add_page(pdf.pages[page])

            output_filename = f"{file_name}_{page}_done.pdf"
            with open(os.path.join(self.folder_path, output_filename), 'wb') as output_file:
                pdf_writer.write(output_file)

        os.remove(pdf_file_path) 


if __name__ == '__main__':
    app = Application()
    
    thread1 = threading.Thread(target=app.mainloop())
    #thread2 = threading.Thread(target=worker2)

    thread1.start()
    #thread2.start()

    thread1.join()
    #thread2.join()
