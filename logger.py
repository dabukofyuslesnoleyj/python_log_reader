import csv

class ILoggerListener:
    def Update(self, input: str):
        pass

class ILogger:
    def __init__(self):
        self.listeners = []
    def Log(self):
        pass
    def Attach(self, newListener: ILoggerListener):
        self.listeners.append(newListener)
    def NotifyAll(self, input: str):
        for listener in self.listeners:
            listener.Update(input)
