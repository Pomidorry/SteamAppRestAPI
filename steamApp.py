from tkinter import *
import tkinter as tk
from restClient import *
from currentFrame import *
from tkinter import messagebox

class steamApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Steam App')
        self.geometry('400x500')
        self.initializeIdInput()
        self.initializeIdGetterButton()

        self.container = tk.Frame(self)
        self.initializeContainer()
        self.showFrame()

    def showFrame(self):
        self.frame = currentFrame(self.container, self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.tkraise()

    def initializeContainer(self):
        self.container.grid(row=1, column=0, columnspan=5, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def initializeIdInput(self):
        Label(self, text='User ID').grid(row=0)
        self.idField = Entry(self)
        self.idField.grid(row=0, column=1)

    def initializeIdGetterButton(self):
        self.IdGetterButton = Button(self, text= "Get Profile Info", command=self.setIdGetterButtonCommand)
        self.IdGetterButton.grid(row=0, column=2)
    
    def setIdGetterButtonCommand(self):
        self.setCurrentId()
        if self.createRestClient():
            self.updateLabelFromApi(self.frame.username, self.RestApiClient.getPersonaname)
            self.updateLabelFromApi(self.frame.profileurl, self.RestApiClient.getProfileUrl)
            self.updateLabelFromApi(self.frame.personastate, self.RestApiClient.getPersonaState)
            self.updateAvatarfull()
            self.updateFriendsList()

    def createRestClient(self):
        try:
            self.RestApiClient = restClient(self.currentId)
            return True
        except ValueError as e:
            logging.error("Can't create client: %s", e)
            messagebox.showerror("Error", f"Invalid Steam ID: {e}")
        except Exception as e:
            logging.error("Failed to create client: %s", e)
            messagebox.showerror("Error", f"Failed to create client: {e}")
        return False
        
    def setCurrentId(self):
        self.currentId = self.idField.get()

    def updateLabelFromApi(self, label, apiMethod):
        newValue = apiMethod()
        self.frame.updateLabel(label, newValue)       

    def updateAvatarfull(self):
        self.currentAvatarfull = self.RestApiClient.getAvatarfull()
        self.frame.updateAvatarfull(self.currentAvatarfull)    

    def updateFriendsList(self):
        self.currentFriendsList = self.RestApiClient.getFriends10Names()
        self.frame.updateFriendsList(self.currentFriendsList)