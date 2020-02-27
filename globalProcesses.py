import queue

def init():
    global twitterQueue 
    global twitterCompletedTasks
    
    twitterQueue = queue.Queue(maxsize=40)
    twitterCompletedTasks = []