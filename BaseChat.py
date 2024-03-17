import json, base64
from Log import Log
from CryptoHelper import CryptoHelper

#
# Copyright (C) 2024 Orel6505
#
# SPDX-License-Identifier: GNU General Public License v3.0
#

class BaseChat():
    def __init__(self, ip: str, port: int, logName: str, cHelper: CryptoHelper) -> None:
        self.status = True
        self.ip = ip
        self.port = port
        self.cHelper = cHelper

        self.log = self.openLog(logName)
        self.buffer = 20000
        
    # My Own Implement of TLS
    def AddSecrets(self, cert, key):
        self.cert: bytes = cert
        self.key: bytes = key

    ## Manage Status
    def getStatus(self) -> bool:
        return self.status

    def setStatus(self, boolean: bool) -> None:
        self.status = boolean
        
    ## Manage Log class
    def openLog(self, logName: str) -> Log:
        return Log(logName, newFileLog=False)

    def closeLog(self) -> None:
        self.log.closeLog()
        
    def SerializeJson(self, Dictionary: dict) -> str:
        try:
            NewDict = Dictionary.copy()
            for key, value in NewDict.items():
                if isinstance(value, bytes):
                    NewDict[key] = base64.b64encode(value).decode('utf-8')
            return json.dumps(NewDict)
        except (TypeError, json.JSONDecodeError) as e:
            self.log.writePrintError(f"Error serializing data to JSON: {e}")
    
    def DeserializeJson(self, message) -> dict:
        try:
            NewDict = json.loads(message)
            for key, value in NewDict.items():
                if isinstance(value, bytes):
                    NewDict[key] = base64.b64decode(value).decode('utf-8')
            return NewDict
        except (TypeError, json.JSONDecodeError) as e:
            self.log.writePrintError(f"Error serializing data to JSON: {e}")
        return None