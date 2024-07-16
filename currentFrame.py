from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class currentFrame(tk.Frame):
    def __init__(self, parent, steam_app):
        self.steam_app = steam_app
        tk.Frame.__init__(self, parent)

        self.username = self.initializeLabel("Start Username", 0, 0)
        self.profileurl = self.initializeLabel("Start URL", 1, 0)
        self.personastate = self.initializeLabel("Start State", 2, 0)

        self.photo = self.initializeAvatarfullPhoto()
        self.initializeAvatarfullPhotoLabel()
        self.initializeFriendsList()

    def initializeFriendsList(self):
        self.friendsListLabel = Label(self, text = "List Of Frinds")  
        self.friendsList = Listbox(self)  
        self.friendsList.insert(1,"Names") 
        self.friendsList.grid(row=1, column=7) 

    def updateFriendsList(self, newFriendsList):
        self.friendsList.delete(0,END)
        for friend in newFriendsList:
            self.friendsList.insert(END, friend)  

    def updateAvatarfull(self, newAvatarfull):
        self.photo = self.initializeAvatarfullPhoto(newAvatarfull)
        self.label.config(image=self.photo)  

    def initializeAvatarfullPhotoLabel(self):
        self.label = Label(self, image=self.photo)
        self.label.grid(row=3, column=0)   

    def initializeAvatarfullPhoto(self, link="https://dealersupport.co.uk/wp-content/uploads/2023/08/iStock-1124532572.jpg"):
        imageUrl = link
        response = requests.get(imageUrl)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((250, 250), Image.Resampling.LANCZOS)  
        photo = ImageTk.PhotoImage(img)
        return photo 
    
    def updateLabel(self, label, newValue):
        label.config(text=newValue) 
    
    def initializeLabel(self, labelText, rowPos, colPos):    
        label = Label(self, text=labelText)
        label.grid(row=rowPos, column=colPos)  
        return label
    