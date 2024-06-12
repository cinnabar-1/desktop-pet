from tkinter import HIDDEN, NORMAL, Tk, Canvas


class CanvasContainer:

    def __init__(self, tk: Tk):
        self.root = tk
        self.c = Canvas(self.root, width=400, height=400)
        self.c.configure(bg='dark blue', highlightthickness=0)
        self.body_color = 'SkyBlue1'

        self.body = self.c.create_oval(35, 20, 365, 350, outline=self.body_color, fill=self.body_color)
        self.ear_left = self.c.create_polygon(75, 80, 75, 10, 165, 70, outline=self.body_color,
                                              fill=self.body_color)
        self.ear_right = self.c.create_polygon(255, 45, 325, 10, 320, 70, outline=self.body_color,
                                               fill=self.body_color)
        self.foot_left = self.c.create_oval(65, 320, 145, 360, outline=self.body_color, fill=self.body_color)
        self.foot_right = self.c.create_oval(250, 320, 330, 360, outline=self.body_color, fill=self.body_color)

        self.eye_left = self.c.create_oval(130, 110, 160, 170, outline='black', fill='white')
        self.pupil_left = self.c.create_oval(140, 145, 150, 155, outline='black', fill='black')
        self.eye_right = self.c.create_oval(230, 110, 260, 170, outline='black', fill='white')
        self.pupil_right = self.c.create_oval(240, 145, 250, 155, outline='black', fill='black')

        self.mouth_normal = self.c.create_line(170, 250, 200, 272, 230, 250, smooth=1, width=2, state=NORMAL)
        self.mouth_happy = self.c.create_line(170, 250, 200, 282, 230, 250, smooth=1, width=2, state=HIDDEN)
        self.mouth_sad = self.c.create_line(170, 250, 200, 232, 230, 250, smooth=1, width=2, state=HIDDEN)
        self.tongue_main = self.c.create_rectangle(170, 250, 230, 290, outline='red', fill='red', state=HIDDEN)
        self.tongue_tip = self.c.create_oval(170, 285, 230, 300, outline='red', fill='red', state=HIDDEN)

        self.cheek_left = self.c.create_oval(70, 180, 120, 230, outline='pink', fill='pink', state=HIDDEN)
        self.cheek_right = self.c.create_oval(280, 180, 330, 230, outline='pink', fill='pink', state=HIDDEN)

        self.c.pack()
        self.c.bind('<Motion>', self.show_happy)
        self.c.bind('<Leave>', self.hide_happy)
        self.c.bind('<Double-1>', self.cheeky)

        self.happy_level = 10
        self.eyes_crossed = False
        self.tongue_out = False

        self.root.after(1000, self.blink)
        self.root.after(5000, self.sad)
        self.root.overrideredirect(True)

    def toggle_eyes(self):
        current_color = self.c.itemcget(self.eye_left, 'fill')
        new_color = self.body_color if current_color == 'white' else 'white'
        current_state = self.c.itemcget(self.pupil_left, 'state')
        new_state = NORMAL if current_state == HIDDEN else HIDDEN
        self.c.itemconfigure(self.pupil_left, state=new_state)
        self.c.itemconfigure(self.pupil_right, state=new_state)
        self.c.itemconfigure(self.eye_left, fill=new_color)
        self.c.itemconfigure(self.eye_right, fill=new_color)

    def blink(self):
        self.toggle_eyes()
        self.root.after(250, self.toggle_eyes)
        self.root.after(3000, self.blink)

    def toggle_pupils(self):
        if not self.eyes_crossed:
            self.c.move(self.pupil_left, 10, -5)
            self.c.move(self.pupil_right, -10, -5)
            self.eyes_crossed = True
        else:
            self.c.move(self.pupil_left, -10, 5)
            self.c.move(self.pupil_right, 10, 5)
            self.eyes_crossed = False

    def toggle_tongue(self):
        if not self.tongue_out:
            self.c.itemconfigure(self.tongue_tip, state=NORMAL)
            self.c.itemconfigure(self.tongue_main, state=NORMAL)
            self.tongue_out = True
        else:
            self.c.itemconfigure(self.tongue_tip, state=HIDDEN)
            self.c.itemconfigure(self.tongue_main, state=HIDDEN)
            self.tongue_out = False

    def cheeky(self, event):
        self.toggle_tongue()
        self.toggle_pupils()
        self.hide_happy(event)
        self.root.after(1000, self.toggle_tongue)
        self.root.after(1000, self.toggle_pupils)
        return

    def show_happy(self, event):
        if (20 <= event.x <= 350) and (20 <= event.y <= 350):
            self.c.itemconfigure(self.cheek_left, state=NORMAL)
            self.c.itemconfigure(self.cheek_right, state=NORMAL)
            self.c.itemconfigure(self.mouth_happy, state=NORMAL)
            self.c.itemconfigure(self.mouth_normal, state=HIDDEN)
            self.c.itemconfigure(self.mouth_sad, state=HIDDEN)
            self.c.happy_level = 10
        return

    def hide_happy(self, event):
        self.c.itemconfigure(self.cheek_left, state=HIDDEN)
        self.c.itemconfigure(self.cheek_right, state=HIDDEN)
        self.c.itemconfigure(self.mouth_happy, state=HIDDEN)
        self.c.itemconfigure(self.mouth_normal, state=NORMAL)
        self.c.itemconfigure(self.mouth_sad, state=HIDDEN)
        return

    def sad(self):
        if self.happy_level == 0:
            self.c.itemconfigure(self.mouth_happy, state=HIDDEN)
            self.c.itemconfigure(self.mouth_normal, state=HIDDEN)
            self.c.itemconfigure(self.mouth_sad, state=NORMAL)
        else:
            self.happy_level -= 1
        self.root.after(5000, self.sad)


if __name__ == '__main__':
    root = Tk()
    container = CanvasContainer(root)
    root.attributes('-topmost', True)
    root.mainloop()
