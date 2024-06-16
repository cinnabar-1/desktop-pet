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
        gif_frame = 10
        self.moveleft = [tk.PhotoImage(file=get_path('assets/duck-left.gif'), format='gif -index %i' % (i)) for i in
                         range(gif_frame)]
        self.moveright = [tk.PhotoImage(file=get_path('assets/duck-right.gif'), format='gif -index %i' % (i)) for i in
                          range(gif_frame)]
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
        self.jumping = False
        self.jump_level = 100
        self.window.after(0, self.update)
        self.dir = -1  # starting direction
        self.y_dir = -5
        self.window.bind('<Motion>', self.stop)
        self.window.bind('<Leave>', self.run)
        self.window.bind('<Double-1>', self.jump)
        self.window.mainloop()

    def changetime(self, direction):
        if time.time() > self.timestamp + 0.2:
            self.timestamp = time.time()
            self.frame_index = (self.frame_index + 1) % 8  # speed of frames change
            self.img = direction[self.frame_index]

    def changedir(self, dir_type):
        if dir_type == 'x':
            self.dir = -self.dir
        if dir_type == 'y':
            self.y_dir = -self.y_dir

    def go(self, dir_type):
        if dir_type == 'x':
            self.x = self.x + self.dir
            if self.dir < 0:
                direction = self.moveleft
            else:
                direction = self.moveright
            self.changetime(direction)
        if dir_type == 'y':
            self.y = self.y + self.y_dir
            if self.dir < 0:
                direction = self.moveleft
            else:
                direction = self.moveright
            self.changetime(direction)
        if dir_type == 'jump_y':
            if self.y_dir < 0:
                # when start jump speed is fast
                self.y = self.y + (self.y_dir + 1)
            else:
                self.y = self.y + (self.y_dir - 1)
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
        if not self.jumping:
            self.update()

    def update(self):
        # stop or go
        print('jumping', self.jumping)
        if not self.jumping:
            if self.stop_flag is False:
                self.go('x')
                if self.x == 0 or self.x == self.window.winfo_screenwidth() - 200:
                    self.changedir('x')
                self.window.geometry('128x128+{}+{}'.format(str(self.x), str(self.y)))
                self.label.configure(image=self.img)
                self.label.pack()
                self.window.after(20, self.update)  # 10 is frames number for my gif
                self.window.lift()
        # jump
        else:
            self.go('y')
            self.go('x')
            if self.y <= self.window.winfo_screenheight() - 100 - self.jump_level:
                self.changedir('y')  # when jump to top
            elif self.y >= self.window.winfo_screenheight() - 100:
                # when fall to floor
                self.jumping = False
                self.y = self.window.winfo_screenheight() - 100
                self.changedir('y')
            self.window.geometry('128x128+{}+{}'.format(str(self.x), str(self.y)))
            self.label.configure(image=self.img)
            self.label.pack()
            self.window.after(20, self.update)  # 10 is frames number for my gif
            self.window.lift()

    def jump(self, event):
        self.stop(event)
        self.jumping = True
        self.update()


if __name__ == '__main__':
    pet()
