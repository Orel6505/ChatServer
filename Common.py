import json, base64
from Log import Log
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

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
        self.buffer = 20000

    def GenerateMasterKey(self, ServerRandom: bytes,ClientRandom,ServerSecret,ClientSecret):
        MainSecret = ServerRandom + ClientRandom + ServerSecret + ClientSecret
        hkdf = HKDF(algorithm=self.hash, length=256, backend=default_backend())
    
        # Derive the master key
        return hkdf.derive(MainSecret)
        
    def encrypt(self, data, key):
        # Create a Cipher object
        cipher = Cipher(algorithms.AES(key), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Encrypt the data
        return encryptor.update(data) + encryptor.finalize()

    def decrypt(self, ciphertext, key):
        # Create a Cipher object
        cipher = Cipher(algorithms.AES(key), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decrypt the data
        return decryptor.update(ciphertext) + decryptor.finalize()

    def ChooseKeyType(self, SupportedKeys: list):
        # Supported key types
        keyTypes = ['RSA','DSA','EC']
        if 'RSA' in SupportedKeys:
            return 'RSA'
                
        for key in SupportedKeys:
            if key in keyTypes:
                return key
        return None

    def ChooseHashType(self, SupportedHashes: list) -> str:
        # Supported Hash type
        hashAlgorithms = ['SHA-384', 'SHA-512','SHA3-256','SHA3-384','SHA3-512']
        hashObject = {
            'SHA-384': hashes.SHA384, 
            'SHA-512': hashes.SHA512,
            'SHA3-256': hashes.SHA3_256,
            'SHA3-384': hashes.SHA3_384,
            'SHA3-512': hashes.SHA3_512,
        }
        
        if 'SHA-256' in SupportedHashes:
            self.hash = hashes.SHA256
            return 'SHA-256'

        for hash in SupportedHashes:
            if hash in hashAlgorithms:
                self.hash = hashObject[hash]
                return hash

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
    
    def SerializeJson(self, Dictionary: dict) -> bytes:
        try:
            return json.dumps(Dictionary)
        except (TypeError, json.JSONDecodeError) as e:
            self.logAndPrintError(f"Error serializing data to JSON: {e}")
            return None
    
    def DeserializeJson(self, message) -> dict:
        try:
            return json.loads(message)
        except (TypeError, json.JSONDecodeError) as e:
            self.logAndPrintError(f"Error serializing data to JSON: {e}")
        return None
            
        
        