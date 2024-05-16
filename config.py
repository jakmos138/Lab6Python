import json
import sys

configName = 'config.json'

configDict = {
    'logName' : '',
    'ipAddress' : '',
    'loggingLevel' : 0,
    'linesAtOnce' : 0,
    'maxSize' : 0
}

if __name__ == '__main__':
    try:
        f = open(configName, 'r')
        configDict = json.load(f)
        print("Current config values:")
        for name, value in configDict.items():
            print("\t{}: {}".format(name, value))
        f.close()

        decision = input("Do you wanna change config file?[Y/N]")
        if decision.lower() not in ['y','yes']:
            sys.exit()

    except FileNotFoundError:
        print("You don't have config file yet!")
    
    for name in configDict.keys():
        typeOfInput = type(configDict[name])
        newValue = input("Input new value of {}. Press Enter to continue. (Expected input:{}) ".format(name, typeOfInput))
        if not newValue:
            continue
        try:
            newValue = typeOfInput(newValue)
            configDict[name] = newValue
        except:
            print("Invalid Input")
        
    configFile = open(configName, 'w')
    json.dump(configDict, configFile)
    configFile.close()
    
    

    