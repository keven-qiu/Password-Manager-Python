# Password Manager App
# GUI made in tkinter

import random
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from generator import RandomPassword
import pyperclip
import json

GREENBLUE = '#164d5e'
GREY = '#bbbbbb'
BEIGE = '#ffe3d8'
BLACK = '#000000'

def main():
  def createRandomPassword():
    """
    Create a random password
    """
    length = random.randint(11, 27)
    createdPassword = RandomPassword(length).getPassword()
   
    password_entry.delete(0, END)
    password_entry.insert(0, createdPassword)

    pyperclip.copy(createdPassword)

    return createdPassword

  def saveEntries():
    """
    Save entries entered by user to
    "passwords.json"
    """
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
    """
    Search through passwords.json file and
    add to the entry widget
    Add both email/username and password
    """
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


  def copyEmail():
    """ Copy email from entry box"""
    pyperclip.copy(email_entry.get())

  def copyPassword():
    """ Copy password from entry box"""
    pyperclip.copy(password_entry.get())


  """ Tkinter User Interface """
  window = Tk()
  window.geometry("520x500+600+150")
  window.title("Password Manager by Keven Qiu")
  window.config(padx=50, pady=50, bg=GREENBLUE)

  canvas = Canvas(height=200, width=200, bg=GREENBLUE, highlightthickness=0)
  img = Image.open('lock.png')
  resizedImage = img.resize((70,70), Image.ANTIALIAS)
  newimg = ImageTk.PhotoImage(resizedImage)

  canvas.create_image(100, 100, image=newimg)
  canvas.grid(row=0, column=1)

  # website label and entry widget
  website_label = Label(text='Website:', bg=GREENBLUE, fg=BEIGE)
  website_label.grid(row=1,column=0,sticky="W")
  website_entry = Entry()
  website_entry.grid(row=1,column=1, columnspan=1,sticky="EW")
  website_entry.focus()
  website_search = Button(text='Search', bg=BLACK, command=searchPasswords)
  website_search.grid(row=1,column=2,sticky="EW")

  # email/username label and entry widget
  email_label = Label(text='Email/Username:', bg=GREENBLUE, fg=BEIGE)
  email_label.grid(row=2,column=0,sticky="W")
  email_entry = Entry()
  email_entry.grid(row=2,column=1, columnspan=1,sticky="EW")
  email_entry.insert(0, 'myusername@gmail.com')

  # password label and entry widget
  password_label = Label(text='Password:', bg=GREENBLUE, fg=BEIGE)
  password_label.grid(row=3,column=0,sticky="W")
  password_entry = Entry()
  password_entry.grid(row=3,column=1,sticky="EW")
  password_button = Button(text='Generate Password', bg=GREY, command=createRandomPassword)
  password_button.grid(row=3,column=2,sticky="EW")

  # save/add button
  button = Button(text='Add', bg=BLACK, command=saveEntries)
  button.grid(row=4,column=0,columnspan=1,sticky="EW")
  button.config(pady=2)

  copyEmail = Button(text='Copy user', bg=BLACK, command=copyEmail)
  copyEmail.grid(row=4, column=1, columnspan=1, sticky="EW")
  copyEmail.config(pady=2)

  copyPassword = Button(text='Copy password', bg=BLACK, command=copyPassword)
  copyPassword.grid(row=4, column=2, columnspan=1, sticky="EW")
  copyPassword.config(pady=2)

  window.mainloop()

if __name__ == "__main__":
  main()