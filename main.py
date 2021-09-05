# Password Manager App
# GUI made in tkinter

import random
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from generator import RandomPassword
import pyperclip
from datetime import datetime
import json

NAVY = '#0A043C'
GREY = '#bbbbbb'
BEIGE = '#ffe3d8'

def main():
  def createRandomPassword():
    length = random.randint(11, 27)
    createdPassword = RandomPassword(length).getPassword()
   
    password_entry.delete(0, END)
    password_entry.insert(0, createdPassword)

    pyperclip.copy(createdPassword)

    return createdPassword

  def savedEntries():
    website = website_entry.get()
    email = email_entry.get()
    pw = password_entry.get()

    newData = {
      website: {
        "email": email,
        "password": pw
      }
    }

    if len(website) and len(pw):
      try:
        with open('passwords.json', 'r') as pwFile:
          data = json.load(pwFile)
          data.update(newData)
      except FileNotFoundError:
        with open('passwords.json', 'w') as pwFile:
          json.dump(newData, pwFile, indent=4)
      else:
        confirmation = messagebox.askyesno(
          title=f"{website}",
          message=f"\n'email': {email}\n'password': {pw}\n\nConfirm?"
        )
        if confirmation:
          with open('passwords.json', 'w') as pwFile:
            json.dump(data, pwFile, indent=4)
            website_entry.delete(0, END)
            password_entry.delete(0, END)
    else:
      # if the entry box is blank
      messagebox.showwarning(title="Warning", message="One or more fields blank")

  def searchPasswords():
    website = website_entry.get()

    try:
      with open('passwords.json', 'r') as pwFile:
        data = json.load(pwFile)
        email = data[website]['email']
        pw = data[website]['password']

        email_entry.delete(0, END)
        email_entry.insert(0, email)
        password_entry.delete(0, END)
        password_entry.insert(0, pw)
    except KeyError as error:
      messagebox.showinfo(title="Key error", message=f"{error} password does not exist!")
    except FileNotFoundError as error:
      messagebox.showinfo(message="File does not exist")


  """ Tkinter User Interface """
  window = Tk()
  window.geometry("520x500+600+150")
  window.title("Password Manager by Keven Qiu")
  window.config(padx=50, pady=50, bg=NAVY)

  canvas = Canvas(height=200, width=200, bg=NAVY, highlightthickness=0)
  img = Image.open('lock.png')
  resizedImage = img.resize((70,70), Image.ANTIALIAS)
  newimg = ImageTk.PhotoImage(resizedImage)

  canvas.create_image(100, 100, image=newimg)
  canvas.grid(row=0, column=1)

  # ROW 1
  website_label = Label(text='Website:', bg=NAVY, fg=BEIGE)
  website_label.grid(row=1,column=0,sticky="W")
  website_entry = Entry()
  website_entry.grid(row=1,column=1, columnspan=2,sticky="EW")
  website_entry.focus()
  website_search = Button(text='Search', bg=GREY, command=searchPasswords)
  website_search.grid(row=1,column=2,sticky="EW")
  # ROW 2
  email_label = Label(text='Email/Username:', bg=NAVY, fg=BEIGE)
  email_label.grid(row=2,column=0,sticky="W")
  email_entry = Entry()
  email_entry.grid(row=2,column=1, columnspan=2,sticky="EW")
  email_entry.insert(0, 'myusername@gmail.com')
  # ROW 3
  password_label = Label(text='Password:', bg=NAVY, fg=BEIGE)
  password_label.grid(row=3,column=0,sticky="W")
  password_entry = Entry()
  password_entry.grid(row=3,column=1,sticky="EW")
  password_button = Button(text='Generate Password', bg=GREY, command=createRandomPassword)
  password_button.grid(row=3,column=2,sticky="EW")
  # ROW 4
  button = Button(text='Add', bg=GREY, command=savedEntries)
  button.grid(row=4,column=1,columnspan=2,sticky="EW")
  button.config(pady=2)

  window.mainloop()

if __name__ == "__main__":
  main()