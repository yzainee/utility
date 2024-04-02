import tkinter as tk
m=tk.Tk()
m.geometry("1500x750")
m.title("Trial Screen")
greeting = tk.Label(text="Welcome to Utils", width=30, height=10)
greeting.pack()
button = tk.Button(m, text="stop", width=25, command=m.destroy)
button.pack()
m.mainloop()