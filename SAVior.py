import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
from savParser import savParser
#from PIL import Image, ImageTk
import sys

#Funksjoner


def select_file():
    filetypes = (
        ('SPSS filer', '*.sav'),
        ('Alle filer', '*.*')
    )

    filename = fd.askopenfilename(
        title='Åpne fil',
        initialdir=os.getcwd(),
        filetypes=filetypes)

    pb.pack()
    spacing()
    open_button.config(text= "Vennligst vent")
    loadingTextLabel.config(text="Spør respondentene...")
    root.update_idletasks() 
    
    parseFile = savParser(filename)

    pb['value'] = 20
    loadingTextLabel.config(text="...skriver ned svar")
    root.update_idletasks() 
    parseFile.getRespondents()


    pb['value'] = 75
    loadingTextLabel.config(text="Betaler for store regninger til IBM")
    root.update_idletasks() 

    parseFile.getQuestions()

    pb['value'] = 80
    loadingTextLabel.config(text="Finner på tall")
    root.update_idletasks() 

    parseFile.getQuestionLabels()
    pb['value'] = 90
    loadingTextLabel.config(text="Oppretter regneark")
    root.update_idletasks() 

    parseFile.getValueLabels()
    pb['value'] = 100
    loadingTextLabel.config(text="Ferdig! Filene ligger i "+os.getcwd())

    on_close()
    open_button.config(text= buttonText)




def on_close():
    response=messagebox.askyesno('SAV filen er parset','Vil du avslutte?')
    if response:
        root.destroy()


def spacing():
    spacing = ttk.Label(root, text="", background="#0A2343")
    spacing.pack()


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


#initialisere

root = tk.Tk()
root.title("SAVior")
root.configure(background="#0A2343")
root.minsize(500,300)
root.maxsize(500,300)
root.geometry("500x300+200+200")

#Fluff
versioning = ttk.Label(root, text="v1.0 Snø", background="#0A2343", foreground="white")
versioning.pack(side=tk.TOP, anchor=tk.NE)
spacing()

#image=Image.open(resource_path('nrk-logo.png'))
#image=Image.open(fd)

#img=image.resize((125, 50))
#my_img=ImageTk.PhotoImage(img)

#img = ttk.Label(root, image=my_img, background="#0A2343")
#img.pack()

spacing()

text = ttk.Label(root, text="Velkommen til SAVior", background="#0A2343", foreground="white")
text.pack()
text2 = ttk.Label(root, text="Konverterer en .SAV fil fire .csv filer du kan importere til PowerBI", background="#0A2343", foreground="white")
text2.pack()

buttonText = "Last inn fil"

open_button = ttk.Button(
    root,
    text=buttonText,
    command=select_file
)

open_button.pack(expand=True)

spacing()

pb = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=100
)

pb.pack()
pb.pack_forget()

spacing()

loadingText = ""
loadingTextLabel = ttk.Label(root, text="", background="#0A2343", foreground="white")
loadingTextLabel.pack()


spacing()

root.mainloop()