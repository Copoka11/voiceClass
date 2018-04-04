

from tkinter import *
import time
from random import random as random
import voiceid

recs = []



"""
#rec1 = voiceid.voiceRec()
#rec2 = voiceid.voiceRec()
#rec3 = voiceid.voiceRec()

#rec1.createWav()

#rec2.createWav(2)
#rec3.createWav(3)
#print (id(rec1.byteData))
#print (id(rec2.byteData))
"""

def close():
    root.destroy()
    root.quit()

def button1_clicked():
    recs.append(voiceid.voiceRec())
    recList.insert(END, "record No %r" % recs[len(recs)-1].id)

def button2_clicked():
    button2['text'] = time.strftime('%H:%M:%S')

def button3_clicked():
    bg = '#%0x%0x%0x' % (int(random()*16), int(random()*16), int(random()*16))
    print(bg)
    button3['bg'] = bg
    button3['text'] = button3['bg'] # показываем предыдущий цвет кнопки
    button3['activebackground'] = bg

def onSelect(event):
    curPos = event.widget.curselection()
    print(curPos, type(curPos))
    pos = curPos[0]
    var.set(pos)
    var_param.set("Record No " + str(recs[pos].id) 
                  + " | is recorded - " + str(recs[pos].rec_done) 
                  + " | is analised - " + str(recs[pos].analyse_done))

#test
    

root = Tk()
root.title("Voice IDs")
root.geometry('800x350')

var = StringVar()
var_param = StringVar()

############################# image #################
grafImg = Canvas(root, width=200, height = 200)
grafImg.pack()
img = PhotoImage(file='res/kitty.gif')
grafImg.create_image(0, 0, image=img, anchor='nw')
####################################################



button1 = Button(root, text="Создать\nзапись", command=button1_clicked)

button2 = Button(root, text=" ")
button2.configure(text=time.strftime('%H:%M:%S'), command=button2_clicked)

button3 = Button(root, text="color change", command=button3_clicked)

button4 = Button(text="Емпту")

recList = Listbox(root)
label = Label(root, text="null", textvariable=var, anchor=W, bg = '#ccc')     #виджет
label_params = Label(root, text = "222", textvariable=var_param, anchor=W, bg = "#9cc")

recList.bind('<<ListboxSelect>>', onSelect)



################### РАЗМЕЩЕНИЕ ВИДЖЕТОВ ##############################

grafImg.place(x=10, y=10, width=200, height=200, anchor='nw')
button1.place(x=15, y=220, width=90, height=50, anchor='nw')
button2.place(x=115, y=220, width=90, height=50, anchor='nw')
button3.place(x=15, y=280, width=90, height=50, anchor='nw')
button4.place(x=115, y=280, width=90, height=50, anchor='nw')
recList.place(x=220, y=10, width=300, height=200, anchor='nw')
label.place(x=220, y=220, width=300, height=50, anchor='nw')
label_params.place(x=220, y=270, width=300, height=50, anchor='nw')

######################################################################


root.protocol('WM_DELETE_WINDOW', close)
root.mainloop()

