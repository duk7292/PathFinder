import tkinter as tk

root = tk.Tk()

root.geometry("1200x750")
root.resizable(False, False)


text_widget = tk.Text(root)
text_widget.place(x = 0,y=0,height=750,width=200)

canvas = tk.Canvas(root, width=1000, height=750)
canvas.place(x=200)



root.mainloop()
