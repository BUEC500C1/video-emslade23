import queue

def init():
    global twitterQueue 
    
    twitterQueue = queue.Queue(maxsize=40)