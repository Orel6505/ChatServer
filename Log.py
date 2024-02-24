import os, datetime

class Log:
    def __init__(self, filename: str):
        self.log = open(filename, 'a')
        self.log.write("\n")
        self.log.write("---------beginning of log\n")
    
    def Write_Logfile(self, logtype: str, message: str) -> None:
        self.log.write(f'{logtype}: {datetime.datetime.now()}: {message}\n')
        
    def Close_Logfile(self):
        self.log.close()