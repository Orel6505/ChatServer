import os, datetime

class Log:
    def __init__(self, filename: str):
        self.log = open(filename, 'a')
        self.log.write("\n")
        self.log.write("---------beginning of log\n")
    
    def Write_Logfile(self, LogLevel: str, Message: str) -> None:
        self.log.write(f'{LogLevel}: {datetime.datetime.now().replace(microsecond=0)}: {Message}\n')
        
    def Close_Logfile(self):
        self.log.close()