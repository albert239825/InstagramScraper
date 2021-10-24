from instascrape import Profile, scrape_posts, Post
from selenium.webdriver import Chrome
from datetime import datetime
import pandas as pd
import numpy as np
import pickle
from openpyxl.workbook.child import INVALID_TITLE_REGEX
from openpyxl import workbook
import re
from utils import check_valid_username, write_to_excel, get_top_post, create_post_df
from pathlib import Path

cwd = Path.cwd()

# mac
#chrome_driver_path = cwd / 'chromedriver'

# windows
chrome_driver_path = cwd / 'chromedriver.exe'
driver = Chrome(chrome_driver_path)

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
    "cookie": "sessionid=7320119797%3ASNZXyzR0VduyTA%3A0"
}
users = pd.read_csv("Social_Media_Study_Handles.csv")
users = users.reindex(
    columns=[*users.columns, 'follower_count', 'number_of_posts'])

# Specifying datatype for each columns
users['School'] = users['School'].astype(object)
users['IG Username'] = users['IG Username'].astype(object)
users['follower_count'] = users['follower_count'].astype('Int64')
users['number_of_posts'] = users['number_of_posts'].astype('Int64')

# users = users.reindex(columns=[*users.columns, 'follower_count', 'number_of_posts', 'top_post_likes',
# 'top_post_date_posted', 'top_post_url', 'first_post_likes', 'first_post_date_posted', 'first_post_url'])
# This code is no longer userful since we are storing each account's posts in its own dataframe
# users['top_post_likes'] = users['top_post_likes'].astype('Int64')
# users['top_post_date_posted'] = users['top_post_date_posted'].astype('datetime64[ns]')
# users['top_post_url'] = users['top_post_url'].astype(object)
# users['first_post_likes'] = users['first_post_likes'].astype('Int64')
# users['first_post_date_posted'] = users['first_post_date_posted'].astype('datetime64[ns]')
# users['first_post_url'] = users['first_post_url'].astype(object)
# test purposes
# users = users.head(5).append(users.iloc[89])

# List of dataframes representing the posts of each user
users_df = []

for i in range(0, len(users)):
    if (not pd.isnull(users.iloc[i]['IG Username'])):
        # Scrape the profile
        print(users.iloc[i]['IG Username'])
        profile = Profile(users.iloc[i]['IG Username'])
        profile.scrape(headers=headers)

        # Adding profile datapoints to dataframe
        users.at[i, 'follower_count'] = profile.followers
        users.at[i, 'number_of_posts'] = profile.posts

        # Scraping Posts

        # Do we need a webdriver to scrape profile information?
        posts = profile.get_posts(webdriver=driver, login_first=True, login_pause=30)
        print(len(posts))
        scraped_posts, unscraped = scrape_posts(
            posts, webdriver=driver, silent=False, headers=headers, pause=5)

        # Appending dataframe from account to each
        users_df.append(create_post_df(scraped_posts))

    # if no username, we're just going to add an empty dataframe
    else:
        users_df.append(create_post_df([]))

        # old code from just getting top and first posts
        # top_post = get_top_post(scraped_posts)

        # #Post are scraped from most recent to oldest, therefore, the earliest post will be the last one scraped in theory
        # first_post = scraped_posts[-1]

        # users.at[i, 'top_post_likes'] = top_post.likes
        # users.at[i, 'top_post_date_posted'] = datetime.fromtimestamp(top_post.timestamp)
        # users.at[i, 'top_post_url'] = "instagram.com/p/{}".format(top_post.shortcode)
        # users.at[i, 'first_post_likes'] = first_post.likes
        # users.at[i, 'first_post_date_posted'] = datetime.fromtimestamp(first_post.timestamp)
        # users.at[i, 'first_post_url'] = "instagram.com/p/{}".format(first_post.shortcode)

write_to_excel(users_df, users)
