# test python application

from getTweets import getTweetText
from getTweets import insertNewLines
from getTweets import createImagesOfTweets


def testTweetText():
    assert getTweetText('@elonmusk', 1) == ['@flcnhvy @sydney_ev Probably']