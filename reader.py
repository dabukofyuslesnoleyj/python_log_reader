import csv
import cxlib.anlog

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