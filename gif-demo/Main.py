import tkinter as tk
import time
import random
from tkinter import ttk


class pet:
    def __init__(self):
        # create a window
        self.window = tk.Tk()
        self.img_len = 23
        self.img_size_format = '500x500+{x}+0'
        # pla ceholder image
        self.walking_right = [tk.PhotoImage(file='giphy.gif', format='gif -index %i' % i) for i in range(self.img_len)]
        self.frame_index = 0
        self.img = self.walking_right[self.frame_index]

        # timestamp to check whether to advance frame
        self.timestamp = time.time()

        # set focushighlight to black when the window does not have focus
        self.window.config(highlightbackground='black')

        # make window frameless
        self.window.overrideredirect(True)

        # make window draw over all others
        self.window.attributes('-topmost', True)

        # turn black into transparency
        self.window.wm_attributes('-transparentcolor', 'black')

        # create a label as a container for our image
        self.label = tk.Label(self.window, bd=0, bg='black')

        # create a window of size 128x128 pixels, at coordinates 0,0
        self.x = 0
        self.window.geometry(self.img_size_format.format(x=str(self.x)))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()

    def update(self):
        # move right by one pixel
        self.x += 1

        # advance frame if 50ms have passed
        if time.time() > self.timestamp + 0.1:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % int(self.img_len/2+1)
            self.img = self.walking_right[self.frame_index]

        # create the window
        self.window.geometry(self.img_size_format.format(x=str(self.x)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()

        # call update after 10ms
        self.window.after(10, self.update)


def tk_window():
    root = tk.Tk()
    label = tk.Label(root, bd=0, bg='black')
    root.attributes('-topmost', True)
    root.overrideredirect(True)
    root.config(highlightbackground='black')
    img = [tk.PhotoImage(file='giphy.gif', format='gif -index %i' % i) for i in range(4)]
    label.configure(image=img[0])
    label.pack()
    root.mainloop()


def ttk_window():
    root = tk.Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    img = [tk.PhotoImage(file='giphy.gif', format='gif -index %i' % i) for i in range(4)]
    lable = frm
    label = tk.Label(root, bd=0, bg='black')
    label = ttk.Label
    label.configure(image=img[0])
    # label.pack()
    root.attributes('-topmost', True)
    # set focushighlight to black when the window does not have focus
    root.config(highlightbackground='black')
    root.mainloop()


if __name__ == '__main__':
    # ttk_window()
    height = tk.Tk().winfo_screenheight()
    print(height)
    weight = tk.Tk().winfo_screenwidth()
    print(weight)
    # pet()
