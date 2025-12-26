import tkinter as tk
from tkinter import filedialog,messagebox,ttk
import threading
import duplicate

class StorageApp:
    def __init__(self,root):
        self.root=root
        self.root.title("Storage Optimizer Pro")
        self.root.geometry("400x200")
        tk.Label(root,text="System Storage Optimizer").pack(pady=10)
        self.progress=ttk.Progressbar(root,orient="horizontal",length=300,mode="determinate")
        self.progress.pack(pady=10)
        self.status_var =tk.StringVar(value="Status: Ready")
        tk.Label(root,textvariable=self.status_var).pack()
        self.start_button=tk.Button(root,text="Select Floder",command=self.start_optimization,bg="#2196F3",fg="white",width=15)
        self.start_button.pack(pady=15)
    
    def update_progress(self,current,total):
        self.progress["maximum"]=total
        self.progress["value"]=current
        self.status_var.set(f"Processing file {current} of {total}...")
        self.root.update_idletasks()
    
    def run_in_background(self,folder):
        try:
            duplicates,space,compress = duplicate.process_files(folder,callback=self.update_progress)
            self.status_var.set("Status : Optimization Complete!")
            messagebox.showinfo("Sucess",f"Removed {duplicates} duplicates\nSpace {space} saved\nCompressed {compress} large files")
        except Exception as e:
            messagebox.showerror("Error",f"An error ocurred: {e}")
        finally:
            self.start_button.config(state="normal")

    def start_optimization(self):
        folder=filedialog.askdirectory()
        if folder:
            self.start_button.config(state="disabled")
            threading.Thread(target=self.run_in_background,args=(folder,),daemon=True).start()



if __name__=="__main__":
    root=tk.Tk()
    app=StorageApp(root)
    root.mainloop()