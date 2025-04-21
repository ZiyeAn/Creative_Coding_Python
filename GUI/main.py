import tkinter as tk

def increase():
    current = slider.get()
    if current < 100:
        slider.set(current + 1)

def decrease():
    current = slider.get()
    if current > 0:
        slider.set(current - 1)

def block_slider(event):
    return "break"  

root = tk.Tk()
root.title("Button-Controlled Slider")

slider = tk.Scale(root, from_=0, to=100, orient="horizontal", showvalue=True)
slider.pack(pady=10)


slider.bind("<Button-1>", block_slider)
slider.bind("<B1-Motion>", block_slider)


btn_frame = tk.Frame(root)
btn_frame.pack()

btn_decrease = tk.Button(btn_frame, text="–", width=5, command=decrease)
btn_decrease.pack(side="left", padx=5)

btn_increase = tk.Button(btn_frame, text="+", width=5, command=increase)
btn_increase.pack(side="left", padx=5)

root.mainloop()