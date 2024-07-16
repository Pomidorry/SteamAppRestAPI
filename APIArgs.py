from abc import ABC, abstractmethod

class APIArgs(ABC):
    def __init__(self, apiKey=None):
        self.key = apiKey
    
    @abstractmethod
    def to_dict(self):
        pass

class APIPlayerSummariesArgs(APIArgs):
    def __init__(self, apiKey=None, Ids=None):
        super().__init__(apiKey)
        self.steamids = Ids
    
    def to_dict(self):
        return self.__dict__
    
class APIFriendListFriends(APIArgs):
    def __init__(self, apiKey=None, Id=None):
        super().__init__(apiKey)
        self.steamid = Id
        self.relationship = 'friend'
    
    def to_dict(self):
        return self.__dict__    