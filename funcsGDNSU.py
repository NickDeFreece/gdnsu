import os
import time
import datetime
import requests

def getTimestamp(delta=None,mode='add'): #Ex. delta = datetime.timedelta(seconds=69)
    t = datetime.datetime.utcnow()
    st = str(t.strftime('%Y-%m-%dT%H.%M.%S.%f'))
    if delta != None:
        if mode == 'add':
            dt = t + delta
        elif mode == 'sub':
            dt = t - delta
        return {'now': st, 'atdelta': str(dt.strftime('%Y-%m-%dT%H.%M.%S.%f'))}
    else:
        return st

def writeLog(msg, path=None, timestamp=None, prnt=False, useLocalTZ=False):
    if timestamp == None:
        #if useLocalTZ == True:
            #delta = datetime.timedelta(hours=7) #hours = Get local TZ's offset from system
            #ts = getTimestamp(delta)
            #timestamp = ts['atdelta']
        #else:
        timestamp = getTimestamp() #Nest this if i figure out using local TZ
    msg = f'\n[{timestamp}] {msg}'
    if path == None:
        path = os.getcwd() + "\\gdnsu.log"
    with open(path, 'a') as f:
        f.write(msg)
    if prnt == True:
        print(msg)

def pw(msg, path=None, timestamp=None):
    print(msg)
    writeLog(msg, path, timestamp)

def csvToDictList(csvpath):
    dicts = []
    t = getTimestamp()
    #print("\n===Importing CSV to dict at", t, "...")
    with open(csvpath, 'r') as f:
        header = f.readline()
        lines = f.readlines()
    header = header.rstrip("\n")
    header = header.split(",")
    #print("\nColumns: ", header)
    index = 0
    for l in lines:
        csvdict = {}
        _l = l.rstrip('\n')
        _l = _l.split(",")
        #print("Line: ", _l)
        headerlen = len(header)
        llen = len(_l)
        if headerlen != llen:
            msg = "Line " + str(index) + " has the wrong number of fields! (" + str(llen) + "/" + str(headerlen) + ")\nLine: " + str(l)
            raise RuntimeError(msg)
        for h in header:
            csvdict.update({h: _l[header.index(h)]})
        index += 1
        dicts.append(csvdict)
    #print("\nPost-Import CSVDict list:")
    #for d in dicts:
    #    print(d)
    return dicts

def dictlistToCSV(dictlist, outpath):
    header = ""
    lines = ""
    t = getTimestamp()
    #print("\n=Exporting dict to CSV at", t, "!=")
    for dl in dictlist:
        if header == "": #Should branch here only on the first loop. Will handle header line and first data line of output CSV
            #print("headerDict: ", dl)
            headerlen = len(dl)
            #print("headerlen: ", headerlen)
            line1 = ""
            for d in dl:
                header += d + ","
                line1 += dl[d] + ","
            header = header[:-1] + "\n"
            line1 = line1[:-1] + "\n"
            lines = header + line1
            #print("OutHeader: ", header)

        else:
            _line = ""
            #print("\nlineDict: ", dl)
            _llen = len(dl)
            #print("linelen: ", _llen)
            if _llen != headerlen:
                msg = "Element at index " + str(dictlist.index(dl)) + " is the wrong length (" + str(_llen) + "/" + str(headerlen) + ")\nElement: " + str(dl)
                raise RuntimeError(msg)
            for d in dl:
                _line += dl[d] + ","
            _line = _line[:-1] + "\n"
            lines += _line
            #print("OutLine: ", _line)

    with open(outpath, 'w') as f:
        f.write(lines)

def doGet(uri, headers, retries=None):
    #if retries == None:
    #    retries = getSetting('retries')
    #retries = int(retries)
    retries = 3
    attempt = 0
    wait = 1
    response = requests.get(uri, headers=headers)
    while (response == None or (response.status_code < 200 or response.status_code >= 400)) and attempt < retries:
        attempt += 1
        time.sleep(wait)
        wait *= 2
        response = requests.get(uri, headers=headers)
    if response == None or (response.status_code < 200 or response.status_code >= 400):
        msg = f'\n==========GET request failed after {attempt}/{retries} attempts! '
        if response != None:
            msg += f'\nHeaders: {response.headers}'
            msg += f'\nBody: {response.content}'
        else:
            msg += "No response from endpoint!=========\n"
    return response

def doPost(uri, headers, data=None, retries=None):
    #if retries == None:
    #    retries = getSetting('retries')
    #retries = int(retries)
    retries = 3
    attempt = 0
    wait = 1
    response = requests.post(uri, headers=headers, data=data)
    while (response == None or (response.status_code < 200 or response.status_code >= 400)) and attempt < retries:
        if data != None:
            response = requests.post(uri, headers=headers, data=data)
        else:
            response = requests.post(uri, headers=headers)
        time.sleep(wait)
        wait *= 2
        attempt += 1
    if response == None or (response.status_code < 200 or response.status_code >= 400):
        msg = f'\n==========POST request failed after {attempt}/{retries} attempts! '
        if response != None:
            msg += f'\nHeaders: {response.headers}'
            msg += f'\nBody: {response.content}'
        else:
            msg += "No response from endpoint!=========\n"
    return response

def doPut(uri, headers, data, retries=None):
    #if retries == None:
    #    retries = getSetting('retries')
    #retries = int(retries)
    retries = 3
    attempt = 0
    wait = 1
    response = requests.put(uri, headers=headers, data=data)
    while (response == None or (response.status_code < 200 or response.status_code >= 400)) and attempt < retries:
        response = requests.put(uri, headers=headers, data=data)
        time.sleep(wait)
        wait *= 2
        attempt += 1
    if response == None or (response.status_code < 200 or response.status_code >= 400):
        msg = f'\n==========PUT request failed after {attempt}/{retries} attempts! '
        if response != None:
            msg += f'\nHeaders: {response.headers}'
            msg += f'\nBody: {response.content}'
        else:
            msg += "No response from endpoint!=========\n"
    return response
