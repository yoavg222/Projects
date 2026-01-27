import tkinter as tk
from tkinter import filedialog
import anti_virus
from anti_virus import scan_full_path, to_list, counter


def upload_action():
    filename = filedialog.askdirectory()
    print("selected",filename)
    path_user.set(filename)


root = tk.Tk()
root.title("anti virus")

btn = tk.Button(root,text = "upload files/dic",command=upload_action)
path_user = tk.StringVar()
print(path_user)
anti_virus.counter = 0
anti_virus_btn =tk.Button(root,text = "scan_full_path",command=lambda:scan_full_path(to_list(path_user.get())))
btn.pack()
anti_virus_btn.pack()
to_see = tk.Button(root,text = "to_print",command=lambda:to_print(counter))
to_see.pack()

def to_print(num):
    see = tk.StringVar()
    see.set(f"you have{num}")

    label = tk.Label(root,textvariable=see,
                     anchor=tk.CENTER,
                     bg="lightblue",
                     height=3,
                     width=30,
                     bd=3,
                     font=("Arial", 16, "bold"),
                     cursor="hand2",
                     fg="red",
                     padx=15,
                     pady=15,
                     justify=tk.CENTER,
                     relief=tk.RAISED,
                     underline=0,
                     wraplength=250
                    )
    label.pack(pady=20)


print(anti_virus_btn)
root.mainloop()


