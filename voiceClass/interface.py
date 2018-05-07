from tkinter import *
import time
from random import random as random
import voiceid

recs = []

def close():
    voiceid.saveDB(recs)
    root.destroy()
    root.quit()

def button1_clicked():                                  #load DB
    recs.extend(voiceid.loadDB())
    for i in range(len(recs)):
        recList.insert(END, "record No %r" % recs[i].id)
    print(recs)

def button2_clicked():                                  #save DB
    voiceid.saveDB(recs)

def button3_clicked():                                  #add record 
    recs.append(voiceid.voiceRec())
    recList.insert(END, "record No %r" % recs[-1].id)
    print(recs)

def button4_clicked():                                  #plot Signal
    print('var get for graph =', var.get())
    i = int(var.get())
    recs[i].plotSignal()

def button5_clicked():                                  #record wav
    print('var get for rec =', var.get())
    i = int(var.get())
    recs[i].createWav()
    recs[i].rec_done = True

def button7_clicked():                                  #play wav
    print('var get for play =', var.get())
    i = int(var.get())
    recs[i].playRam()

def button9_clicked():                                  #fourier
    print('var get for fur =', var.get())
    i = int(var.get())
    recs[i].plotFFT()

def onSelect(event):                                    #list selection actions
    curPos = event.widget.curselection()
    print(curPos, type(curPos))
    pos = curPos[0]
    var.set(pos)
    var_param.set("Record No " + str(recs[pos].id) 
                  + " | is recorded - " + str(recs[pos].rec_done) 
                  + " | is analised - " + str(recs[pos].analyse_done))
    i = int(var.get())
    recs[i].wavToRam()                                  #usable?


root = Tk()                                             #
root.title("Voice IDs")
root.geometry('800x350')


var = StringVar()
var.set('0')
var_param = StringVar()

############################# image #################
grafImg = Canvas(root, width=200, height = 200)
grafImg.pack()
img = PhotoImage(file='res/kitty.gif')
grafImg.create_image(0, 0, image=img, anchor='nw')
####################################################

button1 = Button(root, text="Load DB", command=button1_clicked)

button2 = Button(root, text="Save DB", command=button2_clicked)

button3 = Button(root, text="Создать\nзапись", command=button3_clicked)

button4 = Button(text="Показать\nграфик", command=button4_clicked)

button5 = Button(text="Rec", command=button5_clicked)

button6 = Button(text="Anls")

button7 = Button(text="Play", command=button7_clicked)

button8 = Button(text="Del")

button9 = Button(text="Fur\nFur", command=button9_clicked)


# РЕКЛИСТ
recList = Listbox(root)
recList.bind('<<ListboxSelect>>', onSelect)

label = Label(root, text="null", textvariable=var, anchor=W, bg = '#ccc')     #виджет
label_params = Label(root, text = "222", textvariable=var_param, anchor=W, bg = "#9cc")


################### РАЗМЕЩЕНИЕ ВИДЖЕТОВ ##############################

grafImg.place(x=10, y=10, width=200, height=200, anchor='nw')
button1.place(x=15, y=220, width=90, height=50, anchor='nw')
button2.place(x=115, y=220, width=90, height=50, anchor='nw')
button3.place(x=15, y=280, width=90, height=50, anchor='nw')
button4.place(x=115, y=280, width=90, height=50, anchor='nw')
recList.place(x=220, y=10, width=300, height=200, anchor='nw')
label.place(x=220, y=220, width=300, height=50, anchor='nw')
label_params.place(x=220, y=270, width=300, height=50, anchor='nw')

button5.place(x=540, y=10, width=50, height=30, anchor='nw')
button6.place(x=600, y=10, width=50, height=30, anchor='nw')
button7.place(x=660, y=10, width=50, height=30, anchor='nw')
button8.place(x=720, y=10, width=50, height=30, anchor='nw')
button9.place(x=720, y=110, width=50, height=30, anchor='nw')

######################################################################
button1_clicked()
root.protocol('WM_DELETE_WINDOW', close)

root.mainloop()

