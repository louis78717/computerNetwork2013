# from Tkinter import *
# from time import *


# class test(Frame):
#     def __init__(self, parent):
#         self.root = parent;
#         self.listbox = Listbox(parent)
#         self.listbox.pack()
#         self.listbox.insert(END, "a list entry")
#         self.CurrentTime = int(time())
#         self.update()
#         parent.mainloop()    

#     def update(self):
#         if int(time())!=self.CurrentTime:
#             self.listbox.insert(END, int(time()))
#             self.CurrentTime = int(time())
#             self.root.after(1000, self.update) 

# def main():
#     root = Tk()
#     ex = test(root)
#     root.mainloop()  


# if __name__ == '__main__':
#     main()

from Tkinter import *
from time import *

class App():
    def __init__(self):
        self.root = Tk()
        self.root.geometry("300x150+300+300")
        self.listbox = Listbox(self.root)
        self.listbox.config(width=300, font=('Consolas',12))
        self.listbox.insert(0, "Message".rjust(10)+"Time".rjust(20))
        self.listbox.pack()
        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        message='asdf'
        totalStr=message.rjust(10)+(strftime('%X %x').rjust(20))
        self.listbox.insert(1, totalStr)
        self.root.after(1000, self.update_clock)

app=App()
app.mainloop()