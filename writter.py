import csv
import json

class IWriterListener :
    def Update(self, input: str):
        pass

class IWriter :
    def __init__(self):
        self.listeners = []
    def WriteLog(self):
        pass
    def Attach(self, newListener):
        self.listeners.append(newListener)
    def NotifyAll(self, input: str):
        for listener in self.listeners:
            listener.Update(input)

class JSONLogUpdater (IWriterListener):
    def Update(self, input:str):
       with open('data.txt', 'w') as outfile:
           json.dump(input, outfile)
