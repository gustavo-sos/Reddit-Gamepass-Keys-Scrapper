# Reddit-Gamepass-Keys-Scrapper
Utilizing the Reddit API, this webscrapper parses posts in r/XboxGamePass, looking for keys to redeem, and writes it into a .txt file.

But you may ask, what if the key has already been redeemed?
You have to be quick, but I'll help you with these conditionals that the scrapper has:
- It only parses posts that are 10min old or newer;
- It will send a Windows notification with sound when a new key is found;
- It will only write keys that are not previously present in the keys.txt file.

And with that, if you leave this running in the background, chances are that you will be the first to know when a new, unredeemed, Gamepass key is available.
