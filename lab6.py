import re
import logging
import json
import sys
import keyboard
from ipaddress import IPv4Address
from config import configName as confName

logger = logging.getLogger(__name__)

configurations = { 
    'logName' :'file.txt',
    'myIpAddress' : '192.168.0.0',
    'loggingLevel' : 10,
    'linesAtOnce' : 10,
    'maxSize' : 2137 
}

class entryLog:

    def __init__(self, ip, clientID, userID, time, request, statusCode, size, referer, userAgent):
        self.ip = ip
        self.clientID = clientID
        self.userID = userID
        self.time = time
        self.request = request
        self.statusCode = statusCode
        self.size = size
        self.referer = referer
        self.userAgent = userAgent
    
    def __str__(self):
        return f"{self.ip} {self.clientID} {self.userID} {self.time} {self.request} {self.statusCode} {self.size} {self.referer} {self.userAgent}"


def splitLog(line: str):
    logElements = re.split("( |\".*?\"|\[.*?\])",line)
    logElements = filter(lambda e: e.strip(), logElements)

    return list(map(lambda e: e.replace('"','').replace("[","").replace("]",""), logElements))

def readLog():
    try:
        logFile = open(configurations['logName'], 'r')
    except FileNotFoundError:
        print("File", configurations['logName'],"doesn't exist. Exiting program now.")
        sys.exit()
    logDict = {}
    index = 0
    for line in logFile.readlines():
        entry = entryLog(*splitLog(line))
        logDict[index] = entry
        index+=1
    logFile.close()
    return logDict

def ipRequestsNumber(entries):
    rqCountDict = {}
    for item in entries.values():
        rqCountDict[item.ip] = rqCountDict.get(item.ip, 0) + 1
    return rqCountDict

def ipFind(entries ,mostActive = True):
    ipDict = ipRequestsNumber(entries)
    targetOcc = max(ipDict.values()) if mostActive else min(ipDict.values())
    return [ip for ip, value in ipDict.items() if value == targetOcc]

def longestRequest(entries):
    longestReq, corIp  = "",""
    for entry in entries.values():
        if len(entry.request) > len(longestReq):
            longestReq, corIp = entry.request, entry.ip
    return (longestReq, corIp)

def nonExistent(entries):
    return {entry.request for entry in entries.values() if entry.statusCode == "404"}


def loadConfig():
    tempConfigs = {}
    try:
        configFile = open(confName, 'r')
        tempConfigs = json.load(configFile)
        configFile.close()
    except FileNotFoundError:
        print('No config file found. Using default values instead.')
        return
    except json.JSONDecodeError:
        print('Wrongly formatted config file. Exiting program.')
        sys.exit()

    try:
        configurations['logName'] = tempConfigs['logName']
        configurations['myIpAddress'] = tempConfigs['ipAddress']
        configurations['loggingLevel'] = tempConfigs['loggingLevel']
        configurations['linesAtOnce'] = tempConfigs['linesAtOnce']
        configurations['maxSize'] = tempConfigs['maxSize']
        print("Config File loaded without errors!")
    except KeyError:
        print("Missing value in configs. Using defaults from now on.")
    logging.basicConfig(level=configurations['loggingLevel'])


def printLogsFromMyIp(entries):
    print(*(entry for entry in entries.values() if entry.ip == configurations['myIpAddress']), sep = '\n')


def printLogsInParts(entries):
    try:
        assert configurations['linesAtOnce'] > 1
    except AssertionError:
        logging.error("Value of lines at once must be greater or equal to 1.")
    index = 0
    logs = list(entries.values())
    while index < len(logs):
        endIndex = min(index+configurations['linesAtOnce'], len(logs))
        print(*logs[index:endIndex], sep = '\n')
        index+=configurations['linesAtOnce']
        keyboard.read_key()

def printBelowMaxSize(entries):
    print(*(entry for entry in entries.values() if entry.size.isdecimal() and int(entry.size) <= configurations['maxSize']), sep = '\n')

def run():
    print()
    loadConfig()
    logDict = readLog()
    printLogsFromMyIp(logDict)
    #printLogsInParts(logDict)
    #printBelowMaxSize(logDict)

if __name__ == "__main__":
    run()

