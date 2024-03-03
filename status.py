class ServerStatus:
    def __init__(self):
        self.status = True
    
    def GetServerStatus(self):
        return self.status

    def SetServerStatus(self, boolean: bool):
        self.status = boolean