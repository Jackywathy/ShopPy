import datetime
currentLog = None
dolog = True
def SetLog(name):
    global currentLog
    currentLog = open(name, 'a+')

def LOG(*args,loc="main.py:",delimiter=","):
    if dolog:
        print('['+str(datetime.datetime.now())+']',loc, delimiter.join(map(str,args)), file=currentLog)
        currentLog.flush()

def LogExit():
    currentLog.close()

def RemoveImage(info):
    if info is None:
        return info
    ret = []
    for i in info:
        if len(str(i)) < 100:
            ret.append(i)
    return ret