from tkinter import *


BLUE = '#0e1a64'


class Display:
    def __init__(self):
        self.tk = Tk()
        self.tk.attributes('-zoomed', True)
        self.is_fullscreen = True
        self.tk.attributes('-fullscreen', self.is_fullscreen)
        self.tk.configure(background=BLUE)
        self.frame = Frame(self.tk)
        self.frame.pack()
        self.message = StringVar()
        self.text = Label(self.frame,
                          fg='white',
                          bg='#0e1a64',
                          font=('Helvetica', 34),
                          height='9',
                          wraplength=self.tk.winfo_screenwidth() * 0.9,
                          textvariable=self.message)
        self.text.pack()
        self.tk.bind('<F11>', self.toggle_fullscreen)
        self.tk.bind('<Escape>', self.quit)

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.tk.attributes('-fullscreen', self.is_fullscreen)
        return 'break'

    def quit(self, event=None):
        self.tk.destroy()
        return 'break'
   
    def mainloop(self):
        self.tk.mainloop()

    def show(self, message):
        self.message.set(message)
