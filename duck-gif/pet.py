import os.path
import sys
import tkinter as tk
import time


def get_path(relative_path):
    try:
        # _MEIPASS will be added only when .exe file created
        base_path = sys._MEIPASS
    except AttributeError:
        # so if exception that is in ide or something
        base_path = os.path.abspath(".")
    return os.path.normpath(os.path.join(base_path, relative_path))


class pet:
    def __init__(self):
        self.window = tk.Tk()
        # code below generates string for each frame in gif
        self.moveleft = [tk.PhotoImage(file=get_path('assets/duck-left.gif'), format='gif -index %i' % (i)) for i in
                         range(10)]
        self.moveright = [tk.PhotoImage(file=get_path('assets/duck-right.gif'), format='gif -index %i' % (i)) for i in
                          range(10)]
        self.frame_index = 0  # setting starting frame
        self.img = self.moveleft[self.frame_index]  # starting direction gif
        self.timestamp = time.time()
        self.window.config(background='black')
        self.window.wm_attributes('-transparentcolor', 'black')
        self.window.overrideredirect(True)  # makes window frameless
        self.window.attributes('-topmost', True)  # puts window on top
        self.label = tk.Label(self.window, bd=0, bg='black')  # creates a label as a container for a gif
        # starting points
        # get screen width and height to decide to where to start
        self.x = width = self.window.winfo_screenwidth() - 200
        self.y = height = self.window.winfo_screenheight() - 100
        self.window.geometry('128x128+{}+{}'.format(str(self.x), str(self.y)))
        self.label.configure(image=self.img)
        self.label.pack()
        self.stop_flag = False
        self.window.after(0, self.update)
        self.dir = -1  # starting direction
        self.window.bind('<Motion>', self.stop)
        self.window.bind('<Double-1>', self.run)
        self.window.mainloop()

    def changetime(self, direction):
        if time.time() > self.timestamp + 0.05:
            self.timestamp = time.time()
            self.frame_index = (self.frame_index + 1) % 5  # speed of frames change
            self.img = direction[self.frame_index]

    def changedir(self):
        self.dir = -self.dir

    def go(self):
        self.x = self.x + self.dir
        if self.dir < 0:
            direction = self.moveleft
        else:
            direction = self.moveright
        self.changetime(direction)

    def stop(self, event):
        # print('stop', self.stop_flag)
        self.stop_flag = True

    def run(self, event):
        # print('run', self.stop_flag)
        self.stop_flag = False
        self.update()

    def update(self):
        # print('update', self.stop_flag)
        if self.stop_flag is False:
            self.go()
            if self.x == 0 or self.x == self.window.winfo_screenwidth() - 200:
                self.changedir()

            self.window.geometry('128x128+{}+{}'.format(str(self.x), str(self.y)))
            self.label.configure(image=self.img)
            self.label.pack()
            self.window.after(1, self.update)  # 10 is frames number for my gif
            self.window.lift()


if __name__ == '__main__':
    pet()
