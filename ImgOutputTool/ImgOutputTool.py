import os
import json
import shutil
import datetime
import sys
import csv

from shutil import copyfile
sys.path.append('..') #let system can get the cxlib path 
from cxlib.anlog import Anlog, LineCounter

path = "."
logPath = path + "/logs"
blobPath = path + "/blob"
resultPath = path + "/Result"
tag_filter_ruid = 'run_teach'
tag_filter_result_cap = 'result_capture'
tag_filter_result_ins = 'result_inspection'

ruid = {}

class ResCollection:
    def __init__(self):
        self.logs = []
        self.dies = {}
        pass

def main():
    #rr = {}
    try:
        startDT, endDT = user_input()
        folder = run(startDT, endDT)
        open_folder(True, folder)
        os.system('pause')     
    except Exception as e:
        print('Run error! Please restart the program.\nError msg: ' + str(e))
        os.system('pause')
        sys.exit()

def print_rc(k, rc):
    print(k, len(rc.logs), rc.logs[0].dt)
    
    for k, die in rc.dies.items():
        print(k)
        for d in die:
            data = d.data()
            cp = data['call_path'].split(';')
            number = cp[3].replace(":", "_") # serial
            print('    ', number, data['capture_image_uid'])

#for k, rc in rr.items():
    #print_rc(k, rc)

def user_input():
    start = input('please input the start date time in YYYY-MM-DD HH:MM format or press enter to set no limit:\n')
    if start == '':
        startDT = datetime.datetime(1911, 1, 1, 0, 0)
    else:
        startDT = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M')

    end = input('please input the end date time in YYYY-MM-DD HH:MM format or press enter to set no limit:\n')
    if end == '':
        endDT = datetime.datetime.now()
    else:
        endDT = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M')

    print(f'Find the date between {startDT} ~ {endDT}.')
    return startDT, endDT

def run(startDT, endDT):
    logs = Anlog.read_dt_range_logs(logPath+"/v2k.log*", startDT, endDT)
    logs = filter(LineCounter.new(), logs)
    logs = filter(lambda l: l.dt >= startDT and l.dt <= endDT , logs)
    for log in logs:
        if log.data_log and tag_filter_ruid in log.tags():
            data = log.data()
            if data['run_uid'] != '' and data['run_uid'] not in ruid:
                ruid[data['run_uid']] = log.dt
                # print(data['run_uid'] + ': ' + str(ruid[data['run_uid']]))
     
        if log.data_log and (tag_filter_result_cap in log.tags() or tag_filter_result_ins in log.tags()):
            data = log.data()
            
            if data['run_uid'] not in ruid:
                continue
            
            uid = data['run_uid']
            cp = data['call_path'].split(';')
            loc = cp[1][cp[1].find('(')+1: cp[1].find(')')].replace(',', '_') # repeat index
            number = ''
            c = 0
            for n in cp:
                if c > 1:
                    number = number + n.replace(":", "_").replace("(", "_").replace(")", "_")
                    if c < len(cp)-1:
                        number = number + "_"
                c = c + 1
            # number = cp[len(cp)-1].replace(":", "_") # serial
            # print(data['capture_image_uid'], uid, loc, number)
            print(number)
            isExist = True
            imgFullPath = blobPath + "/" + log.dt.strftime('%Y') + "/" + log.dt.strftime('%Y%m%d') + "/pic/" + data['capture_image_uid'] + ".jpg"
            if not os.path.isfile(imgFullPath):
                isExist = False
                imgFullPath = imgFullPath + '_notfound'
                
            folderName = ruid[uid].strftime('%Y-%m-%d %H-%M-%S') 
            forlderPath = resultPath + "/" + folderName
            if not os.path.exists(resultPath):
                os.mkdir(resultPath)
            if not os.path.exists(forlderPath):
                os.mkdir(forlderPath)

            # if not os.path.isfile(forlderPath + '/result.csv'):
            #     with open(os.path.join(forlderPath, 'result.csv'), 'w', newline='') as resultFile:
            #         fieldnames = ['log_time', 'location', 'number', 'image_path']
            #         csvwriter = csv.DictWriter(resultFile, fieldnames=fieldnames)
            #         csvwriter.writeheader()

            entries = []
            entries.append(str(log.dt))
            entries.append(loc)
            entries.append(number)
            entries.append(imgFullPath)
            print("\t".join(entries))

            # with open(os.path.join(forlderPath, 'result.csv'), 'a', newline='') as resultFile:
            #     csvwriter = csv.writer(resultFile)
            #     csvwriter.writerow(entries)

            if not isExist:
                continue
            
            locPath = forlderPath+'/'+loc
            if not os.path.exists(locPath):
                os.mkdir(locPath)
            savePath = locPath + '/' + number + ".jpg"
            copyfile(imgFullPath, savePath)

            # Keep in rr
            """
            if not uid in rr:
                rr[uid] = ResCollection()

            rc = rr[uid]
            rc.logs.append(log)

            if not loc in rc.dies:
                rc.dies[loc] = []
            rc.dies[loc].append(log)
            """

    folder = os.getcwd() + resultPath.replace('/','\\')[1:]
    return folder    

def open_folder(open, folder):
    if not open:
        return
    #open the result folder
    print('Your result folder is ' + folder)
    os.system('explorer ' + folder)

main()