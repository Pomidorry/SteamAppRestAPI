import requests
from personaState import *
import json
import logging
from APIArgs import *

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
class restClient:
    def __init__(self, profileId):
        if not self.isValidSteamId(profileId):
            raise ValueError("Invalid Steam ID")
        
        self.Id = profileId  

        self.apiKey = self.loadApiKey('credentials.json')

        self.GetPlayerSummariesUrl ='http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002'
        self.GetPlayerSummariesArgs = APIPlayerSummariesArgs(self.apiKey, self.Id).to_dict()

        self.GetFriendListUrl ='http://api.steampowered.com/ISteamUser/GetFriendList/v0001'
        self.GetFriendListArgs = APIFriendListFriends(self.apiKey, self.Id).to_dict()

        self.playerSummariesJson = self.tryToGetJson(self.GetPlayerSummariesArgs, self.GetPlayerSummariesUrl)

        if not self.playerSummariesJson['response']['players']:
            raise ValueError("No player summaries found for the given ID")
        
        try:
            self.friendListJson = self.tryToGetJson(self.GetFriendListArgs, self.GetFriendListUrl)
        except requests.exceptions.RequestException as e:    
            logging.error("Can't get friend list: %s", e)
            self.friendListJson = None
        
    @staticmethod
    def isValidSteamId(steam_id):
        return steam_id.isdigit() and len(steam_id) == 17 
    
    def loadApiKey(self, fileName):
        try:
            with open(fileName) as credentialsJsonFile:
                credentialsJsonData = json.load(credentialsJsonFile)
            return credentialsJsonData['APIkey']
        except FileNotFoundError:
            logging.error("credentials.json file not found")
            raise
        except json.JSONDecodeError:
            logging.error("Error decoding JSON from credentials.json")
            raise

    def getAvatarfull(self):
        avatarfull=((((self.playerSummariesJson['response'])['players'])[0])['avatarfull'])
        return avatarfull
    
    def getPersonaState(self):
        presonastateFromJson=((((self.playerSummariesJson['response'])['players'])[0])['personastate'])
        presonastate=personaState(presonastateFromJson).name
        return presonastate

    def getPersonaname(self):
        presonaname=((((self.playerSummariesJson['response'])['players'])[0])['personaname'])
        return presonaname
   
    def getProfileUrl(self):
        profileurl=((((self.playerSummariesJson['response'])['players'])[0])['profileurl'])
        return profileurl
    
    def getFriends10Names(self):
        if self.friendListJson:
            friendsList = self.friendsSummariesList()
            namesList = [friend['personaname'] for friend in friendsList]
            return namesList
        else:
            return ['PrivateInfo']
    
    def friendsSummariesList(self):
        friendsIdsString = self.getFriends10Ids()
        GetFriendsSummariesArgs = APIPlayerSummariesArgs(self.apiKey, friendsIdsString).to_dict()
        friendsSummariesJson = self.tryToGetJson(GetFriendsSummariesArgs, self.GetPlayerSummariesUrl)
        friendsList = ((friendsSummariesJson)['response'])['players']
        return friendsList
    
    def getFriends10Ids(self):
        friends10InJson = (((self.friendListJson)['friendslist'])['friends'])[:10]
        friends10IdsList = [entry['steamid'] for entry in friends10InJson]
        idsString = ','.join(friends10IdsList)
        return idsString

    def tryToGetJson(self, GetArgs, GetURL):
        try:
            response = requests.get(GetURL, params=GetArgs)
            response.raise_for_status()
            jsonData = response.json()
            return jsonData
        except requests.exceptions.RequestException as e:
            logging.error("HTTP Request failed: %s", e)
            raise e
        except ValueError as e:
            logging.error("JSON decoding failed: %s", e)
            raise e
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)
            raise e 