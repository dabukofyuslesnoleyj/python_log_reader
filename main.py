from reader import LogFileReader, LogReader
from writter import JSONLogUpdater

def main():
    filePath = ""
    logReader = LogReader()
    logFileReader = LogFileReader()
    jsonLogUpdater = JSONLogUpdater()
    
    logReader.Attach(jsonLogUpdater)
    logs = logReader.ReadLog(logFileReader.ReadFile(filePath))
    
    

main()