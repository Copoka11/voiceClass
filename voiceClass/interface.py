
from tkinter import *
import time
from random import random as random
import voiceid

rec1 = voiceid.voiceRec()
rec2 = voiceid.voiceRec()
rec3 = voiceid.voiceRec()

rec1.createWav()
#rec2.createWav(2)
#rec3.createWav(3)



"""
def close():
    root.destroy()
    root.quit()

def button1_clicked():
    print("Hello World")

def button2_clicked():
    button2['text'] = time.strftime('%H:%M:%S')

def button3_clicked():
    bg = '#%0x%0x%0x' % (int(random()*16), int(random()*16), int(random()*16))
    print(bg)
    button3['bg'] = bg
    button3['text'] = button3['bg'] # показываем предыдущий цвет кнопки
    button3['activebackground'] = bg

root = Tk()
root.title("Voice IDs")
root.geometry('800x350')

grafImg = Canvas(root, width=200, height = 200)
grafImg.pack()
img = PhotoImage(file='d:/VoiceID/kitty.gif')
grafImg.create_image(0, 0, image=img, anchor='nw')
button1 = Button(root, text="press me", command=button1_clicked)
button2 = Button(root, text="Lol")
button2.configure(text=time.strftime('%H:%M:%S'), command=button2_clicked)
button3 = Button(root, text="color change", command=button3_clicked)
button4 = Button(text="Спрятать/показать надпись ниже")
label = Label(text='Я здесь!')

recList = Listbox(root)
for i in range(20):
    recList.insert(END, i)

var = StringVar()
label = Label(root, text=0, textvariable=var, anchor=W)     

def onSelect(event):
    curPos = recList.curselection()
    var.set(curPos)
   
recList.bind('<<ListboxSelect>>', onSelect)   

grafImg.place(x=10, y=10, width=200, height=200, anchor='nw')
button1.place(x=15, y=220, width=90, height=50, anchor='nw')
button2.place(x=115, y=220, width=90, height=50, anchor='nw')
button3.place(x=15, y=280, width=90, height=50, anchor='nw')
button4.place(x=115, y=280, width=90, height=50, anchor='nw')
recList.place(x=220, y=10, width=300, height=200, anchor='nw')
label.place(x=220, y=220, width=300, height=100, anchor='nw')

root.protocol('WM_DELETE_WINDOW', close)
root.mainloop()
"""


