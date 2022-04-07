import tkinter as Tk

import pyttsx3

# the campas preparation

root = Tk.Tk()
root.geometry("400x350")
root.configure(bg="Pink")
root.title("Nisome")  # nisome means let me read  ..yap

# area for typing plus  label
label = Tk.Label
button = Tk.Button
ujumbe = Tk.StringVar()  # ujumbe is swahili word means message
label(root, text="Ingiza Maneno", font="Algerian", bg="Pink").pack()
entry = Tk.Entry
uwanja = entry(root, textvariable=ujumbe, width=50)  # uwanja is swahili word means canvans(Area)
uwanja.place(x=50, y=40)


# functions to perform tasks

def Twendekazi():  # twende kaazi means lets go/lets do it hahahah
    kazi = pyttsx3.init()
    text = ujumbe.get()
    kazi.say(text)
    kazi.runAndWait()


def Toka():  # toka is swahili word means exit(out)
    root.destroy()


def Futa():  # futa is swahili word means delete(clear)
    ujumbe.set("")


# buttons

button(root, text='Sikiliza', font="Magneto", bg="Cyan", width=9, command=Twendekazi).place(x=135, y=95)
button(root, text='Futa', font="Magneto", bg="Red", width=9, command=Futa).place(x=135, y=140)
button(root, text='TOKA', font="Magneto", bg="Cyan", width=9, command=Toka).place(x=135, y=185)
root.mainloop()
