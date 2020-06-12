import csv

class IReaderListener :
    def Update(self, input):
        pass

class IReader :
    def __init__(self):
        self.listeners = []
    def ReadLog(self, logs: list) -> str:
        pass
    def Attach(self, newListener: IReaderListener):
        self.listeners.append(newListener)
    def NotifyAll(self, input):
        for listener in self.listeners:
            listener.Update()
            