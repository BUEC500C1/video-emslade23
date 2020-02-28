# test python application
from getTweets import userTweets
import globalProcesses
import os
import shutil
import threading


flag = False
 

if os.path.isfile(os.getcwd() + "/keys") == True:
    flag = True
    shutil.copy('keys', 'keys.py')
    from keys import *

def testCreateVideoGivenTwitterHandleAndKeys():
    globalProcesses.init()
    twitterHandle = "@elonmusk"
    tweetNumber = 5
    globalProcesses.twitterCompletedTasks[twitterHandle] = "Not Completed"

    if flag:
        directory = "musky"
        userTweetsObj = userTweets(consumer_key, consumer_secret, access_token, access_token_secret, twitterHandle, tweetNumber, directory)
        userTweetsObj.getTweetData()
        userTweetsObj.makeDirectory()

        assert len(userTweetsObj.textOfTweets) > 0
        assert len(userTweetsObj.imagesOfTweets) > 0

        userTweetsObj.createImagesofTweets()
        assert globalProcesses.twitterCompletedTasks[twitterHandle] == "50% Complete"

        userTweetsObj.convertImagestoVideo()
        assert os.path.isfile(os.getcwd() + '/' + userTweetsObj.directory + '/test2.mp4') == True

    else:
        directory = "apiExampleVideo"
        userTweetsObj = userTweets(0, 0, 0, 0, twitterHandle, tweetNumber, directory)
        userTweetsObj.convertImagestoVideo()
        assert os.path.isfile(os.getcwd() + '/' + userTweetsObj.directory + '/test2.mp4') == True

def testFilesExist():
    if flag:
        assert os.path.exists(os.getcwd() + '/' + "musky") == True
        assert os.path.isfile(os.getcwd() + '/musky/frame0.png') == True
    else:
        assert os.path.isfile(os.getcwd() + '/apiExampleVideo/frame0.png') == True


def testDirectoryCreateAndDelete():
    userTweetsObj2 = userTweets(0, 0, 0, 0, "@elizabeth", 4, "hello")
    userTweetsObj2.makeDirectory()
    assert os.path.exists(os.getcwd() + '/' + "hello") == True
    userTweetsObj2.deletePhotosFolder()
    assert os.path.exists(os.getcwd() + '/' + "hello") == False