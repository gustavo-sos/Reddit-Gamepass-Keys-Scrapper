import os
import praw
import time
from datetime import datetime
import re
import praw.exceptions
from winotify import Notification, audio

def create_notification_item():
    temp_item = Notification(app_id="Xbox Gamepass Keys from Reddit",
                            title="New Key Fetched!",
                            msg=f"You have new keys available",
                            duration="short")
            
    temp_item.add_actions(label="Show Me", launch="file:///- The absolute path to the folder where this file is goes here - \\keys.txt") # This lib, unfortunately, only accepts abolute paths :c
    temp_item.set_audio(audio.Default, loop=False)
    return temp_item

def get_unix_from_10_min_ago():
    current_time = datetime.now()
    unix_now = time.mktime(current_time.timetuple())
    unix_10_min_ago = unix_now - 600 # This is the part that, effectively, measures the time between the post date and now, in seconds. 
                                     # Default is 600, change the value for testing purposes, 60 = 1 minute, 600 = 10 minutes, 3600 = 1 hour
    return unix_10_min_ago

def scrape_reddit():
    
    unix_10_min_ago = get_unix_from_10_min_ago()
    regexp = re.compile(r"[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}") # Here you can customize the RegExp, I recommend using "regex101.com" if you're not familiar with manually writing those
    key_list = []

    try:
        reddit = praw.Reddit("Your bot goes here.", user_agent="Your user agent goes here.") # You should use your own client_id and secret here
    except praw.exceptions.PRAWException as err:
        print(f"Reddit initialization failed: {err}")
        return
    except Exception as err:
        print(f"Reddit initialization failed: {err}") # Just for good measure, this will probably never get triggered
        return
    
    try:
        with open("keys.txt", "r+") as f:
            saved_keys = {line.strip() for line in f}
    except FileNotFoundError:
        with open("keys.txt", "x") as f:
            saved_keys = set()
    except Exception as err:
        print(err) # Again, just for good measure, as this will probably never get triggered
        return
    
    custom_subreddit = "XboxGamePass" # You can change the Subreddit here. It is not case sensitive.
    for submission in reddit.subreddit(custom_subreddit).new(limit=None):
            
        if submission.created_utc < unix_10_min_ago:
            print("Posts from now on are older than 10 minutes.\nNow it will write the keys and check for duplicates.")
            break
            
        post_content = submission.selftext

        if (regexp.search(post_content)):
            key_list.append(regexp.findall(post_content))
        
    key_list_set = set(map(tuple, key_list))
    write_check = 0

    with open("keys.txt", "a") as f:
        for item in key_list_set:            
            if item[0] not in saved_keys:
                f.write(f"{item[0]}\n")
                write_check = 1
            else:
                print(f"The fetched key {item[0]} already is in your file.")

        popup = create_notification_item()

        if write_check == 1:
            popup.show()

os.chdir("The absolute path to the folder where this file is goes here.")
scrape_reddit()

# If you want it to run in the background, use the code below and comment the function call above
# It runs every 9 minutes for the slight chance that something is posted on the very second that the 10th minute flips

# "Supposedly" you should manually delete the file when you feel like it

# while True:
#     scrape_reddit()
#     time.sleep(540)