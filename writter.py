import csv

class IWriter :
    listeners = []
    def WriteLog(self):
        pass
    def Attach(self, newListener: IWriterListener):
        listeners.append(newListener)
    def NotifyAll(self, input: str):
        for listener in listeners:
            listener.Update(input)

class IWriterListener :
    def Update(self, input: string)
        pass