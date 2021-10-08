from instagramy import InstagramUser
from instascrape import Profile
from selenium.webdriver import Chrome
import pandas as pd

users = pd.read_csv("Social_Media_Study_Handles.csv")
print(users.shape, users.dtypes)

chrome_driver_path = "/Users/chena23/Desktop/InstragramScraper/chromedriver"

driver = Chrome(chrome_driver_path)
headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
    "cookie": "sessionid=7320119797%3Ai4FA7JQKcRyMNJ%3A15"
}

test_profile = Profile('albert239825')
posts = test_profile.get_posts(webdrver=driver, login_first=True)


# test_profile.scrape()

# test_profile_dict = test_profile.to_dict()

# print(test_profile_dict)


# From InstaScrape GitHub
# RECOMMENDED: Pause between each scrape with a randomized time.sleep! Depending on use case, this can be everywhere from a couple seconds to a full minute (the longer, the better). Just do anything to trick Instagram into thinking you're a standard user browsing the site.


# This code uses the package instagramy - Decided to switch from this package as there was a 12 post limitation. Decided to Swtich to the insta-scrape package instead
# session_id = "7320119797%3Ai4FA7JQKcRyMNJ%3A15"
# # Connecting the profile
# user = InstagramUser('albert239825', sessionid=session_id)


# # printing the basic details like
# # followers, following, bio
# print(user.is_verified)
# print(user.number_of_followers)
# print(user.number_of_posts)
# posts = user.posts
# for post in posts:
#     print(post.likes)
