# from tkinter import *
# from gtts import gTTS
# from playsound import playsound
import tkinter as Tk
import gtts as gTTS
import playsound as playsound


root = Tk.Tk()
root.geometry("500x500")
root.configure(bg='ghost white')
root.title("Sikiliza maneno")
Label=Tk.Label
StringVar=Tk.StringVar
Label(root, text = "ANDIKA HAPA", font = "arial 20 bold", bg='white smoke').pack()
Label(text ="Erick App", font = 'arial 15 bold', bg ='white smoke' , width = '20').pack(side = 'bottom')

Msg = StringVar()
Label(root,text ="Enter Text", font = 'arial 15 bold', bg ='white smoke').place(x=20,y=60)
Entry=Tk.Entry
entry_field = Entry(root, textvariable = Msg ,width ='70')
entry_field.place(x=20,y=100)

def Text_to_speech():
    Message = entry_field.get()
    speech = gTTS(text = Message)
    speech.save('erickvoice.mp3')
    playsound('erickvoice.mp3')

def Exit():
    root.destroy()

def Reset():
    Msg.set("")
Button=Tk.Button
Button(root, text = "PLAY", font = 'arial 15 bold' , command = Text_to_speech ,width = '4',bg = 'Pink').place(x=25,y=140)

Button(root, font = 'arial 15 bold',text = 'EXIT', width = '4' , command = Exit, bg = 'Cyan').place(x=100 , y = 140)

Button(root, font = 'arial 15 bold',text = 'RESET', width = '6' , command = Reset,bg = 'Orange').place(x=175 , y = 140)

root.mainloop()