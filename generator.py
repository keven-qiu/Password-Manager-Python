from random import choice

# constants
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTYVWXYZ0123456789"
special = "(,._-*~\"<>/|!@\#$%^&)+='"

class RandomPassword:
  def __init__(self, length):
    self.password = ""
    self.length = length
    #self.specialChar = spec 

  def create(self):
    self.password = ""
    for i in range(self.length):
      #if self.specialChar:
        #self.password += choice(special+characters)
      #else:
      self.password += choice(special+characters)

  def getPassword(self):
    self.create()
    return self.password