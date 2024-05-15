import tkinter as tk

root = tk.Tk()
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

def on_closing():
    pass

label = tk.Label(root, text="Se asteapta inceperea urmatorului eveniment.")
label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, anchor=tk.CENTER)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()



