
# Lizzy's HW4:
given a twitter handle, display tweets in a video using FFMPEG



## How to Run:

1. pip install -r requirements.txt
2. python3 getVideo.py

please note that my program assumes you have a file named keys that contains consumer_key,
consumer_secret, access_token, access_token_secret.

you will be prompted to type in twitter handle, number of tweets you want and lastly the directory you want to be created.
        
        example: @elonmusk,5,helloMusk


3. to test, run pytest test_app.py
- please note that even though in the actions, pytest fails, running it locally works.

## Tasks:
    - get twitter API working so that given a twitter handle, it returns plain text tweets
    - implement a queue and threading system
    - put tweet text into an image
    - convert images into video, more like slide show.
