import datetime, time, traceback
from shutil import move

class Log:
    __instance = None
    
    def getInstance(cls):
        if cls.__instance is None:
            return None
        return cls.__instance
    
    def __init__(self, filename: str, newFileLog: bool=True) -> None:
        instance = self.getInstance()
        if instance is None: 
            self.filename = filename
            header = "---------beginning of log"
            if newFileLog:
                moveResult = self.__moveOldLog()
            else:
                header = "\n" + header
                moveResult = f'Opening {filename}.log'
            self.log = open(f'{filename}.log', "a")                
            self.__write(header)
            self.writeInfo(moveResult)
            Log.__instance = self
        self = Log.__instance
    
    def __moveOldLog(self) -> str:
        try:
            move(f'{self.filename}.log',f'{self.filename}.{int(time.time())}.log')
            return f'Moved {self.filename}.log to {self.filename}.{int(time.time())}.log'
        except FileNotFoundError:
            return "File doesn't exist, Creating it..."

    def __write(self, Message: str) -> None:
        try:
            self.log.write(f'{Message}\n')
        except Exception:
            raise OSError(f'Can\'t write to {self.filename}')
    
    def __writeLogEntry(self, LogEntry: str, Message: str) -> None:
        self.__write(f'{LogEntry}: {datetime.datetime.now().replace(microsecond=0)}: {Message}')
        
    def writeInfo(self, Message: str) -> None:
        self.__writeLogEntry("I", Message)
    
    def writeWarning(self, Message: str) -> None:
        self.__writeLogEntry("W", Message)
        
    def writeError(self, Message: str) -> None:
        self.__writeLogEntry("E", Message)

    def writeFatal(self) -> None:
        self.__write("---------Fatal Error---------")
        self.__writeLogEntry("F", f'{traceback.format_exc().strip()}')
        self.__write("---------Fatal Error---------")

    def isActive(self) -> bool:
        return False if self.log.closed else True
        
    def closeLog(self) -> None:
        self.log.close()
        self.__instance = None