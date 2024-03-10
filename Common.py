from Log import Log
from Security.RSAKeyManager import RSAKeyManager
from Security.CertificateManager import CertificateManager

#
# Copyright (C) 2024 Orel6505
#
# SPDX-License-Identifier: GNU General Public License v3.0
#

class Common():
    def __init__(self, ip: str, port: int, logName: str) -> None:
        self.status = True
        self.ip = ip
        self.port = port
        self.log = self.openLog(logName)
        
    # My own implementation of TLS
    def ChangeChiperSpec(self):
        pass
    
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
    
    def logAndPrintInfo(self, message: str)-> None:
        self.log.writeInfo(message)
        self.Print(message)
        
    def logAndPrintWarning(self, message: str) -> None:
        self.log.writeWarning(message)
        self.Print(message)

    def logAndPrintError(self, message: str) -> None:
        self.log.writeError(message)
        self.Print(message)
        
    def Print(self, message: str) -> None:
        print(message)
    