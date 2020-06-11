import csv

class IReader :
    listeners = []
    def __init__(self):
        pass
    
    def ReadLog(self, logs: list) -> str:
        pass

    def Attach(self, newListener: IReaderListener):
        listeners.append(newListener)

    def NotifyAll(self, input):
        for listener in listeners:
            listener.Update()
            

class IReaderListener :
    def Update(self, input):