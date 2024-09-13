import praw
import time
from datetime import datetime
import re
import praw.exceptions
from winotify import Notification, audio

def get_unix_from_10_min_ago():
    current_time = datetime.now()
    unix_now = time.mktime(current_time.timetuple())
    unix_10_min_ago = unix_now - 600 # This is the part that effectively measures the time between the post date and now, in seconds. Change the value for testing purposes
    return unix_10_min_ago

def scrape_reddit():
    
    unix_10_min_ago = get_unix_from_10_min_ago()
    regexp = re.compile(r"[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}")
    key_list = []

    try:
        reddit = praw.Reddit("bot1", user_agent="windows:teste-keys:v0.1 by /u/dathed-bot") # You should use your own client_id and secret here
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

    for submission in reddit.subreddit("XboxGamePass").new(limit=None):
            
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

        popup = Notification(app_id="Xbox Gamepass Keys from Reddit",
                            title="New Key Fetched!",
                            msg=f"You have new keys available",
                            duration="short")
            
        popup.add_actions(label="Show Me", launch="file:///C:\\THE_PATH_TO_YOUR_TXT_FILE") # This lib, unfortunately, only accepts abolute paths :c
        popup.set_audio(audio.Default, loop=False)

        if write_check == 1:
            popup.show()

scrape_reddit()

# If you want it to run in the background, use the code below and comment the function call above
# It runs every 9 minutes for the slight chance that something is posted on the very second that the 10th minute flips

# "Supposedly" you should manually delete the file when you feel like it

# while True:
#     scrape_reddit()
#     time.sleep(540)