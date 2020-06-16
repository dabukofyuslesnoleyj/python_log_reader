import csv
from cxlib.anlog import Anlog

class IReaderListener :
    def Update(self, input):
        pass

class IReader :
    def __init__(self):
        self.listeners = []
    def ReadLog(self, logs: list) -> list:
        pass
    def Attach(self, newListener: IReaderListener):
        self.listeners.append(newListener)
    def NotifyAll(self, input):
        for listener in self.listeners:
            listener.Update()
            
class LogReader(IReader) :
    def ReadLog(self, logs: list) -> list:
        log_list = []
        for log in logs:
            log_list.append(Anlog.parse_log(log))

class LogFileReader :
    def ReadFile(self, filePath: str) -> list:
        file = open(filePath, "r")
        
        return file.readlines()