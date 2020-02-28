import queue

def init():
    global twitterQueue 
    global twitterCompletedTasks
    global twitterHandles
    global numberOfTweetsArray
    global directoryNameArray
    
    twitterQueue = queue.Queue(maxsize=40)
    twitterCompletedTasks = {}
    twitterHandles = []
    numberOfTweetsArray = []
    directoryNameArray = []