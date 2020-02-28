# References: https://code-maven.com/create-images-with-python-pil-pillow

import datetime
import time
import threading
import subprocess
import os
import shutil

import globalProcesses as gp
from getTweets import userTweets

shutil.copy('keys', 'keys.py')
from keys import *
      
def threads(userTweets):
    gp.twitterQueue.put(userTweets)
    worker = threading.Thread(target=userTweets.getTweetDataAndCreateVideo())
    worker.setDaemon(True)
    worker.start()
    return worker   
       
def userTasks():
    userInput = [""]
    print("Hello, welcome to Lizzy's Twitter Video API!")
    print("Directions: when you are done inputting Twitter Handles, type q")
    while True:
        userInput = input("Please Input @twitterhandle, NumberOfTweets, folderName to create in current directory: \n (Like this example: @elonmusk, 10, muskVideo): ").split(', ')
        if len(userInput) == 3:
            if userInput[0][0] != "@":
                print("Invalid Twitter Handle Structure. Try Again. \n \n")
            elif userInput[1].isnumeric() == False:
                print("Invalid, input a positive integer for number of tweets.")
            else:
                print("Your Input: "+ str(userInput))
                gp.twitterHandles.append(userInput[0])
                gp.numberOfTweetsArray.append(int(userInput[1]))
                gp.directoryNameArray.append(userInput[2])
        elif len(userInput) == 0:
            gp.twitterHandles = ["@elonmusk", "@elizabeth"]
            gp.numberOfTweetsArray = [5, 5]
            gp.directoryNameArray = ["photos4", "photos5"]   
            break  
        elif userInput[0] == "q":
            break
        elif len(userInput) != 3:
            print("Your Input: "+ str(userInput))
            print("Incorrect, input exactly three arguments.\n \n \n")  

def main():
    
    gp.init()
    userTasks()

    for i in range(len(gp.twitterHandles)):
        gp.twitterCompletedTasks[gp.twitterHandles[i]] = "Not Completed"

    for i in range(0, len(gp.twitterHandles)):
        userTweetsObj = userTweets(consumer_key, consumer_secret, access_token, access_token_secret, gp.twitterHandles[i], gp.numberOfTweetsArray[i], gp.directoryNameArray[i])
        threads(userTweetsObj)

main()
